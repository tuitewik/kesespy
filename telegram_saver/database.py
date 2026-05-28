from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from config import DATABASE_URL   # ← Добавили эту строку

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class MessageLog(Base):
    __tablename__ = "message_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int]
    chat_id: Mapped[int]
    user_id: Mapped[int]
    username: Mapped[str | None]
    date: Mapped[datetime]
    message_type: Mapped[str]
    file_unique_id: Mapped[str | None]
    file_name: Mapped[str | None]
    text: Mapped[str | None]