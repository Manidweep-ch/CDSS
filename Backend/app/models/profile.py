from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    profile_name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
