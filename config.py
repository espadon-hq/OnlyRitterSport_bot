import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_TELEGRAM_ID = int(os.getenv("MY_TELEGRAM_ID", "0"))

TIMEZONE = "Europe/Kyiv"
DB_PATH = "data/health.db"
PHOTOS_DIR = "data/photos"