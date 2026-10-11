import logging
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import User
import json
import os
from config.config import API_ID, API_HASH, PHONE_NUMBER, SESSION_FILE, CHANNELS_FILE, LOG_FILE
from filter import LeadFilter

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


class LeadUserbot:
    """Userbot для мониторинга каналов и поиска лидов"""

    def __init__(self):
        self.client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        self.filter = LeadFilter()
        self.channels = self.load_channels()
        self.message_queue = asyncio.Queue()

    def load_channels(self) -> list:
        """Загрузка списка каналов из конфигурационного файла"""
        try:
            with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
                channels = json.load(f)
                logger.info(f"Загружено {len(channels)} каналов для мониторинга")
                return channels
        except FileNotFoundError:
            logger.warning(f"Файл {CHANNELS_FILE} не найден. Создаю пустой список.")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return []

    def save_channels(self):
        """Сохранение списка каналов в файл"""
        try:
            with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.channels, f, indent=2, ensure_ascii=False)
            logger.info("Список каналов сохранен")
        except Exception as e:
            logger.error(f"Ошибка при сохранении списка каналов: {e}")

    async def start(self):
        """Запуск userbot"""
        await self.client.start(phone=PHONE_NUMBER)
        logger.info("Userbot запущен")

        # Подписка на новые сообщения
        @self.client.on(events.NewMessage())
        async def handler(event):
            try:
                # Получение информации о чате
                chat = await event.get_chat()
                chat_username = getattr(chat, 'username', None)

                # Проверка, что сообщение из отслеживаемого канала
                if not chat_username or chat_username not in self.channels:
                    return

                message_text = event.message.message
                if not message_text:
                    return

                # Фильтрация сообщения
                if self.filter.is_relevant(message_text):
                    category = self.filter.get_category(message_text)

                    # Получение ссылки на сообщение
                    message_link = f"https://t.me/{chat_username}/{event.message.id}"

                    # Получение информации об авторе
                    sender = await event.get_sender()
                    author_link = None
                    author_name = "Неизвестно"

                    if isinstance(sender, User):
                        author_name = sender.first_name or "Неизвестно"
                        if sender.username:
                            author_link = f"@{sender.username}"
                        else:
                            author_link = f"[ID: {sender.id}]"

                    # Формирование данных лида
                    lead_data = {
                        'category': category,
                        'text': message_text[:300] + ('...' if len(message_text) > 300 else ''),
                        'message_link': message_link,
                        'author_name': author_name,
                        'author_link': author_link,
                        'channel': f"@{chat_username}"
                    }

                    # Добавление в очередь для отправки через основной бот
                    await self.message_queue.put(lead_data)
                    logger.info(f"Найден лид в @{chat_username}: {category}")

            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения: {e}", exc_info=True)

        logger.info(f"Начинаю мониторинг {len(self.channels)} каналов...")
        logger.info(f"Каналы: {', '.join(['@' + ch for ch in self.channels])}")

    async def add_channel(self, channel_username: str) -> bool:
        """Добавление канала в список мониторинга"""
        channel_username = channel_username.replace('@', '').strip()

        if channel_username in self.channels:
            logger.warning(f"Канал @{channel_username} уже в списке")
            return False

        try:
            # Проверка существования канала
            await self.client.get_entity(channel_username)
            self.channels.append(channel_username)
            self.save_channels()
            logger.info(f"Канал @{channel_username} добавлен")
            return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении канала @{channel_username}: {e}")
            return False

    async def remove_channel(self, channel_username: str) -> bool:
        """Удаление канала из списка мониторинга"""
        channel_username = channel_username.replace('@', '').strip()

        if channel_username not in self.channels:
            logger.warning(f"Канал @{channel_username} не найден в списке")
            return False

        self.channels.remove(channel_username)
        self.save_channels()
        logger.info(f"Канал @{channel_username} удален")
        return True

    async def run(self):
        """Основной цикл работы userbot"""
        await self.start()
        await self.client.run_until_disconnected()
