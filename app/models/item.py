"""Item and ItemTag Models."""
from datetime import datetime
import json
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Item(Base):
    """Collected content item across multiple sources."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(String(128), unique=True, index=True, nullable=False)
    source = Column(String(32), index=True, nullable=False)  # youtube, instagram, shopping, demo
    title = Column(String(256), nullable=False, index=True)
    description = Column(Text, default="", nullable=False)
    url = Column(String(512), nullable=False)
    thumbnail = Column(String(512), default="", nullable=False)
    category = Column(String(64), default="general", index=True, nullable=False)
    creator_or_brand = Column(String(128), default="", nullable=False)
    price = Column(Float, nullable=True)
    raw_metadata = Column(Text, default="{}", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tags = relationship("ItemTag", back_populates="item", cascade="all, delete-orphan")
    interactions = relationship("Interaction", back_populates="item", cascade="all, delete-orphan")
    recommendations = relationship("RecommendationRecord", back_populates="item", cascade="all, delete-orphan")

    @property
    def metadata_dict(self):
        try:
            return json.loads(self.raw_metadata or "{}")
        except Exception:
            return {}

    @metadata_dict.setter
    def metadata_dict(self, val):
        self.raw_metadata = json.dumps(val or {})


class ItemTag(Base):
    """Many-to-Many association between Items and Tags with confidence score."""
    __tablename__ = "item_tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False, index=True)
    confidence = Column(Float, default=1.0, nullable=False)
    is_primary = Column(Integer, default=0, nullable=False)  # 1 for primary category tag

    item = relationship("Item", back_populates="tags")
    tag = relationship("Tag", back_populates="item_associations")

    __table_args__ = (
        UniqueConstraint("item_id", "tag_id", name="uq_item_tag"),
    )
