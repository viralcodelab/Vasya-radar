import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# Userbot configuration
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Keywords configuration
POSITIVE_KEYWORDS = [
    "веб-дизайн", "дизайнер", "дизайн сайта", "верстка", "верстальщик",
    "web-developer", "разработка сайта", "ui/ux", "ui ux", "лендинг",
    "figma", "tilda", "frontend", "фронтенд", "ищу дизайнера",
    "нужен сайт", "заказ", "webflow", "html", "css", "react",
    "wordpress", "вордпресс", "сайт под ключ", "нужен разработчик",
    "ищу верстальщика", "нужна верстка", "разработать сайт"
]

NEGATIVE_KEYWORDS = [
    "резюме", "ищу работу", "обучение", "курс", "подпишись",
    "крипта", "криптовалюта", "стажировка без оплаты", "бесплатно",
    "без оплаты", "за опыт", "портфолио нужно", "подписывайся"
]

# Files
CHANNELS_FILE = "config/channels.json"
SESSION_FILE = "userbot_session"
LOG_FILE = "logs/bot.log"
