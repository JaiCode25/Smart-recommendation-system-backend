"""User Interest Profile Model."""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class UserInterest(Base):
    """Computed interest score for a user-tag pair (Direct vs Graph Expanded)."""
    __tablename__ = "user_interests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, default=0.0, nullable=False)
    is_direct = Column(Boolean, default=True, nullable=False)
    source_tag_id = Column(Integer, ForeignKey("tags.id", ondelete="SET NULL"), nullable=True)
    hop_distance = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="interests")
    tag = relationship("Tag", foreign_keys=[tag_id], back_populates="user_interests")
    source_tag = relationship("Tag", foreign_keys=[source_tag_id])

    __table_args__ = (
        UniqueConstraint("user_id", "tag_id", "is_direct", name="uq_user_tag_interest"),
    )
