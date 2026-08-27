"""Tag and TagRelationship Models for the Discrete Graph Structure."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Tag(Base):
    """Tag entity representing a vertex in the Discrete Math Tag Graph."""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), unique=True, index=True, nullable=False)
    category = Column(String(64), default="general", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    item_associations = relationship("ItemTag", back_populates="tag", cascade="all, delete-orphan")
    user_interests = relationship("UserInterest", back_populates="tag", foreign_keys="UserInterest.tag_id", cascade="all, delete-orphan")


class TagRelationship(Base):
    """Weighted edge between two tag vertices in the NetworkX graph."""
    __tablename__ = "tag_relationships"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False, index=True)
    target_tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False, index=True)
    weight = Column(Float, default=1.0, nullable=False)
    co_occurrence_count = Column(Integer, default=1, nullable=False)
    relationship_type = Column(String(32), default="co_occurrence", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    source_tag = relationship("Tag", foreign_keys=[source_tag_id])
    target_tag = relationship("Tag", foreign_keys=[target_tag_id])

    __table_args__ = (
        UniqueConstraint("source_tag_id", "target_tag_id", name="uq_tag_pair"),
    )
