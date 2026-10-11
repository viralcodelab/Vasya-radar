import asyncio
import logging
from userbot import LeadUserbot
from bot import LeadBot
from config.config import LOG_FILE

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


async def main():
    """Основная функция запуска бота"""
    try:
        logger.info("=" * 50)
        logger.info("Запуск Лид-Радар бота")
        logger.info("=" * 50)

        # Создание общей очереди для передачи сообщений
        message_queue = asyncio.Queue()

        # Инициализация userbot
        userbot = LeadUserbot()
        userbot.message_queue = message_queue

        # Инициализация основного бота
        main_bot = LeadBot(message_queue, userbot)

        # Запуск обоих ботов параллельно
        await asyncio.gather(
            userbot.run(),
            main_bot.start()
        )

    except KeyboardInterrupt:
        logger.info("Остановка бота по команде пользователя")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
    finally:
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Программа завершена")
