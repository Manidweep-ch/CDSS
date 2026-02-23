from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, JSON, String
from datetime import datetime
from app.database.base import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    panels_run = Column(JSON, nullable=False)
    input_payload = Column(JSON, nullable=False)
    output_result = Column(JSON, nullable=False)

    override_flag = Column(Boolean, default=False)

    model_versions = Column(JSON)
    evaluation_version = Column(String)
