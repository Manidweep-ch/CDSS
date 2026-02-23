from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.database.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("chat_sessions.id"))

    role = Column(String)  # "user" or "assistant"
    message = Column(Text)

    timestamp = Column(DateTime, default=datetime.utcnow)
