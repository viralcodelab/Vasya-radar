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
    "создать сайт", "сайт под ключ", "разработка сайта", "дизайн сайта",
    "дизайн лендинга", "ui/ux дизайн", "ui/ux", "ui ux", "дизайн и верстка",
    "веб-дизайнер", "tilda", "webflow", "wordpress", "figma", "верстка сайта",
    "лендинг под ключ", "фронтенд", "верстальщик", "нужен сайт", "нужна верстка",
    "разработать сайт", "интернет-магазин", "дизайн интерфейса"
]

NEGATIVE_KEYWORDS = [
    "логотип", "баннер", "картинка", "полиграфия", "презентация", "аватарка",
    "обложка", "обработка фото", "coreldraw", "резюме", "ищу работу", "курсы",
    "обучение", "крипта", "криптовалюта", "стажировка без оплаты"
]

# OpenAI-compatible Chat Completions API. Для другого совместимого сервиса
# задайте AI_BASE_URL и AI_MODEL в .env.
AI_API_KEY = os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "30"))

# Files
CHANNELS_FILE = "config/channels.json"
SESSION_FILE = "userbot_session"
LOG_FILE = "logs/bot.log"
