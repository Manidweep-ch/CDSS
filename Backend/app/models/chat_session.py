from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    session_type = Column(String)  # "panel" or "global"
    panel_name = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
