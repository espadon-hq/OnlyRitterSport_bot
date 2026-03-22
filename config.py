import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_TELEGRAM_ID = int(os.getenv("MY_TELEGRAM_ID", "0"))

TIMEZONE = "Europe/Kyiv"
DB_PATH = "data/health.db"
PHOTOS_DIR = "data/photos"

SUPPLEMENTS = [
    {"name": "Креатин",          "dose": "5г",        "times": ["08:00"]},
    {"name": "Глютамін",         "dose": "5г",        "times": ["08:00", "21:00"]},
    {"name": "Аргінін+Цитрулін", "dose": "1 капс",     "times": ["08:00"]},
    {"name": "Протеїн",          "dose": "1 порція",  "times": ["08:00", "21:00"]},
    {"name": "Ашваганда",        "dose": "1 капс",     "times": ["21:00"]},
    {"name": "Вітамін D3+K2",    "dose": "1 капс",    "times": ["08:00"]},
    {"name": "Вітамін C",        "dose": "1 капс",     "times": ["08:00", "13:00"]},
    {"name": "Магній",           "dose": "1 капс",     "times": ["21:00"]},
    {"name": "Цинк піколінат",   "dose": "1 капс",      "times": ["21:00"]},
    {"name": "Омега-3",          "dose": "2 капс",    "times": ["08:00"]},
    {"name": "Tribulus",         "dose": "1 капс",    "times": ["08:00"]},
]