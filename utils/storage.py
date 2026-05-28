import os
from datetime import datetime
from aiogram import Bot
from aiogram.types import Message
from config import MEDIA_ROOT   # ← Добавили эту строку

async def save_file(bot: Bot, message: Message, file_type: str):
    folder = os.path.join(MEDIA_ROOT, file_type)
    os.makedirs(folder, exist_ok=True)
    
    if file_type == "photo":
        file_obj = message.photo[-1]
        ext = "jpg"
    elif file_type == "document":
        file_obj = message.document
        ext = file_obj.file_name.split('.')[-1] if file_obj.file_name else "bin"
    elif file_type == "video":
        file_obj = message.video
        ext = "mp4"
    elif file_type == "voice":
        file_obj = message.voice
        ext = "ogg"
    elif file_type == "audio":
        file_obj = message.audio
        ext = "mp3"
    else:
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    username = message.from_user.username or f"user{message.from_user.id}"
    filename = f"{timestamp}_{username}_{file_obj.file_unique_id}.{ext}"
    
    path = os.path.join(folder, filename)
    
    await bot.download(file_obj, destination=path)
    return path