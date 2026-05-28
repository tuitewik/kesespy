import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "./media")
DATABASE_URL = "sqlite+aiosqlite:///bot.db"