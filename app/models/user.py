"""User Model."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User entity in the recommendation system."""

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    username = Column(
        String(64),
        unique=True,
        index=True,
        nullable=False
    )

    email = Column(
        String(128),
        unique=True,
        index=True,
        nullable=True
    )

    password_hash = Column(
        String(256),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    interactions = relationship(
        "Interaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    interests = relationship(
        "UserInterest",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    recommendations = relationship(
        "RecommendationRecord",
        back_populates="user",
        cascade="all, delete-orphan"
    )