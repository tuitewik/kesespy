from aiogram import Router, Bot
from aiogram.types import Message
from utils.storage import save_file
from database import async_session, MessageLog
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message()
async def save_all(message: Message, bot: Bot):
    if not message.from_user:
        return

    session = async_session()
    file_path = None
    file_type = "text"
    content = message.text or message.caption

    try:
        # Определяем тип
        if message.photo:
            file_type = "photo"
            file_path = await save_file(bot, message, "photo")
        elif message.document:
            file_type = "document"
            file_path = await save_file(bot, message, "document")
        elif message.video:
            file_type = "video"
            file_path = await save_file(bot, message, "video")
        elif message.voice:
            file_type = "voice"
            file_path = await save_file(bot, message, "voice")
        elif message.audio:
            file_type = "audio"
            file_path = await save_file(bot, message, "audio")
        # Можно добавить больше типов позже

        # Сохраняем в базу
        log = MessageLog(
            message_id=message.message_id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            date=message.date,
            message_type=file_type,
            file_unique_id=getattr(getattr(message, file_type, None), 'file_unique_id', None) if file_type != "text" else None,
            file_name=message.document.file_name if message.document else None,
            text=content
        )
        session.add(log)
        await session.commit()

        logger.info(f"✅ Сохранено: {file_type} от @{message.from_user.username or message.from_user.id}")

    except Exception as e:
        logger.error(f"Ошибка сохранения: {e}")
    finally:
        await session.close()