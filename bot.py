import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from config.config import BOT_TOKEN, ADMIN_ID, LOG_FILE

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

            channel_list = "\n".join([f"• @{ch}" for ch in channels])
            await message.answer(
                f"📋 <b>Отслеживаемые каналы ({len(channels)}):</b>\n\n{channel_list}",
                parse_mode="HTML"
            )

        @self.dp.message(Command("add_channel"))
        async def cmd_add_channel(message: Message):
            if message.from_user.id != ADMIN_ID:
                await message.answer("⛔ У вас нет доступа к этой команде.")
                return

            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                await message.answer("❌ Использование: /add_channel @channel_username")
                return

            channel_username = args[1].strip()
            success = await self.userbot.add_channel(channel_username)

            if success:
                await message.answer(f"✅ Канал {channel_username} добавлен в мониторинг!")
            else:
                await message.answer(
                    f"❌ Не удалось добавить канал {channel_username}. "
                    "Проверьте правильность имени или канал уже добавлен."
                )

        @self.dp.message(Command("remove_channel"))
        async def cmd_remove_channel(message: Message):
            if message.from_user.id != ADMIN_ID:
                await message.answer("⛔ У вас нет доступа к этой команде.")
                return

            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                await message.answer("❌ Использование: /remove_channel @channel_username")
                return

            channel_username = args[1].strip()
            success = await self.userbot.remove_channel(channel_username)

            if success:
                await message.answer(f"✅ Канал {channel_username} удален из мониторинга.")
            else:
                await message.answer(f"❌ Канал {channel_username} не найден в списке.")

    async def send_lead_notification(self, lead_data: dict):
        """Отправка уведомления о новом лиде"""
        try:
            message_text = (
                f"🎯 <b>Новый лид: {lead_data['category']}</b>\n\n"
                f"📝 <b>Текст:</b>\n{lead_data['text']}\n\n"
                f"🔗 <b>Ссылка:</b> {lead_data['message_link']}\n"
                f"👤 <b>Автор:</b> {lead_data['author_link']}\n"
                f"📢 <b>Канал:</b> {lead_data['channel']}"
            )

            await self.bot.send_message(
                chat_id=ADMIN_ID,
                text=message_text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            logger.info(f"Уведомление о лиде отправлено: {lead_data['category']}")

        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления: {e}", exc_info=True)

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
