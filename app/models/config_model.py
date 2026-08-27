"""System Configuration Model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class SystemConfig(Base):
    """Dynamic system parameters stored in DB."""
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(64), unique=True, index=True, nullable=False)
    value = Column(String(256), nullable=False)
    description = Column(String(256), default="", nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
