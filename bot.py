import logging
import asyncio
import html
import uuid
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from config.config import BOT_TOKEN, ADMIN_ID, LOG_FILE
from ai_service import AIService

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LeadBot:
    """Основной бот для отправки уведомлений о лидах"""

    def __init__(self, message_queue: asyncio.Queue, userbot_instance):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.message_queue = message_queue
        self.userbot = userbot_instance
        self.ai = AIService()
        self.leads = {}
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка обработчиков команд"""

        @self.dp.message(Command("start"))
        async def cmd_start(message: Message):
            if message.from_user.id != ADMIN_ID:
                await message.answer("⛔ У вас нет доступа к этому боту.")
                return

            await message.answer(
                "🤖 <b>Лид-Радар запущен!</b>\n\n"
                "Я буду отправлять вам релевантные лиды из отслеживаемых каналов.\n\n"
                "<b>Доступные команды:</b>\n"
                "/channels - Список отслеживаемых каналов\n"
                "/add_channel @username - Добавить канал\n"
                "/remove_channel @username - Удалить канал\n"
                "/help - Помощь",
                parse_mode="HTML"
            )

        @self.dp.message(Command("help"))
        async def cmd_help(message: Message):
            if message.from_user.id != ADMIN_ID:
                return

            await message.answer(
                "📚 <b>Помощь по использованию бота</b>\n\n"
                "<b>Команды:</b>\n"
                "/start - Приветствие\n"
                "/channels - Показать список каналов\n"
                "/add_channel @channel - Добавить канал для мониторинга\n"
                "/remove_channel @channel - Удалить канал\n"
                "/help - Эта справка\n\n"
                "<b>Как работает бот:</b>\n"
                "Бот автоматически мониторит указанные Telegram-каналы и отправляет вам "
                "сообщения, содержащие ключевые слова по веб-дизайну, верстке и разработке сайтов.",
                parse_mode="HTML"
            )

        @self.dp.message(Command("channels"))
        async def cmd_channels(message: Message):
            if message.from_user.id != ADMIN_ID:
                return
            channels = self.userbot.channels
            if not channels:
                await message.answer("📭 Список каналов пуст.")
                return
            channel_list = "\n".join(f"• @{ch}" for ch in channels)
            await message.answer(
                f"📋 <b>Отслеживаемые каналы ({len(channels)}):</b>\n\n{channel_list}",
                parse_mode="HTML",
            )

        @self.dp.message(Command("add_channel"))
        async def cmd_add_channel(message: Message):
            if message.from_user.id != ADMIN_ID:
                await message.answer("⛔ У вас нет доступа к этой команде.")
                return
            args = (message.text or "").split(maxsplit=1)
            if len(args) < 2:
                await message.answer("❌ Использование: /add_channel @channel_username")
                return
            channel_username = args[1].strip()
            if await self.userbot.add_channel(channel_username):
                await message.answer(f"✅ Канал {channel_username} добавлен в мониторинг!")
            else:
                await message.answer(f"❌ Не удалось добавить канал {channel_username}.")

        @self.dp.message(Command("remove_channel"))
        async def cmd_remove_channel(message: Message):
            if message.from_user.id != ADMIN_ID:
                await message.answer("⛔ У вас нет доступа к этой команде.")
                return
            args = (message.text or "").split(maxsplit=1)
            if len(args) < 2:
                await message.answer("❌ Использование: /remove_channel @channel_username")
                return
            channel_username = args[1].strip()
            if await self.userbot.remove_channel(channel_username):
                await message.answer(f"✅ Канал {channel_username} удален из мониторинга.")
            else:
                await message.answer(f"❌ Канал {channel_username} не найден в списке.")

        @self.dp.callback_query(F.data.startswith("reply:"))
        async def callback_reply(callback: types.CallbackQuery):
            if callback.from_user.id != ADMIN_ID:
                await callback.answer("⛔ Нет доступа", show_alert=True)
                return
            lead = self.leads.get(callback.data.split(":", 1)[1])
            if not lead:
                await callback.answer("Карточка устарела. Дождитесь нового сообщения.", show_alert=True)
                return
            await callback.answer("Готовлю отклик…")
            try:
                reply = await self.ai.generate_reply(lead['text'])
                await callback.message.edit_text(
                    f"<b>Отклик:</b>\n<blockquote>{html.escape(reply)}</blockquote>",
                    parse_mode="HTML",
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
                        types.InlineKeyboardButton(text="↩️ К карточке", callback_data=f"back:{callback.data.split(':', 1)[1]}")
                    ]]),
                    disable_web_page_preview=True,
                )
            except Exception as exc:
                logger.error("Не удалось сгенерировать отклик: %s", exc, exc_info=True)
                await callback.message.answer("Не удалось получить отклик от AI. Проверьте настройки API и попробуйте позже.")

        @self.dp.callback_query(F.data.startswith("back:"))
        async def callback_back(callback: types.CallbackQuery):
            if callback.from_user.id != ADMIN_ID:
                await callback.answer("⛔ Нет доступа", show_alert=True)
                return
            token = callback.data.split(":", 1)[1]
            lead = self.leads.get(token)
            if not lead:
                await callback.answer("Карточка устарела.", show_alert=True)
                return
            await callback.message.edit_text(
                self.format_lead(lead), parse_mode="HTML",
                reply_markup=self.lead_keyboard(token, lead['message_link']),
                disable_web_page_preview=True,
            )
            await callback.answer()

    @staticmethod
    def lead_keyboard(token: str, message_link: str):
        return types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text="📩 ИИ отклик", callback_data=f"reply:{token}"),
            types.InlineKeyboardButton(text="🔗 К сообщению", url=message_link),
        ]])

    @staticmethod
    def format_lead(lead: dict) -> str:
        posted = lead.get('date')
        if posted:
            if posted.tzinfo is None:
                posted = posted.replace(tzinfo=datetime.now().astimezone().tzinfo)
            date_text = posted.astimezone().strftime("%d.%m.%Y %H:%M")
        else:
            date_text = "N/A"
        channel = html.escape(str(lead.get('channel', 'Неизвестно')))
        author = html.escape(str(lead.get('author_link') or '@неизвестно'))
        content = html.escape(str(lead.get('text', ''))[:3500])
        if len(str(lead.get('text', ''))) > 3500:
            content += "…"
        return (
            f"🔥 <b>ВЫГОДНОЕ ПРЕДЛОЖЕНИЕ | {html.escape(str(lead.get('id', 'N/A')))}</b> ⚡\n"
            "________________________________________\n"
            f"📍 <b>Группа:</b> {channel}\n"
            f"👤 <b>От кого:</b> {author}\n"
            f"🕒 <b>Время:</b> {date_text}\n"
            f"✉️ <b>Потенциальных откликов:</b> {html.escape(str(lead.get('potential_replies', 'N/A')))}\n\n"
            "<b>Содержание:</b>\n"
            f"<blockquote>{content}</blockquote>"
        )

    async def send_lead_notification(self, lead_data: dict):
        """Отправка уведомления о новом лиде"""
        try:
            # Строгая AI-проверка стоит перед отправкой: при ошибке API лид не проходит.
            if not await self.ai.is_qualified_lead(lead_data['text']):
                logger.info("Лид отклонен AI-проверкой: %s", lead_data.get('message_link'))
                return
            token = uuid.uuid4().hex[:12]
            self.leads[token] = lead_data
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
                types.InlineKeyboardButton(text="📩 ИИ отклик", callback_data=f"reply:{token}"),
                types.InlineKeyboardButton(text="🔗 К сообщению", url=lead_data['message_link']),
            ]])
            await self.bot.send_message(
                chat_id=ADMIN_ID,
                text=self.format_lead(lead_data),
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
            logger.info("Уведомление о проверенном лиде отправлено: %s", lead_data.get('message_link'))

        except Exception as e:
            logger.error("Ошибка при обработке/отправке лида: %s", e, exc_info=True)

    async def process_lead_queue(self):
        """Обработка очереди лидов"""
        while True:
            try:
                lead_data = await self.message_queue.get()
                await self.send_lead_notification(lead_data)
                # Небольшая задержка, чтобы избежать флуд-контроля
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Ошибка при обработке очереди лидов: {e}", exc_info=True)

    async def start(self):
        """Запуск бота"""
        logger.info("Основной бот запущен")

        # Запуск обработки очереди
        asyncio.create_task(self.process_lead_queue())

        # Запуск polling
        await self.dp.start_polling(self.bot)
