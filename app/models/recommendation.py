"""Recommendation Record Model."""
from datetime import datetime
import json
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class RecommendationRecord(Base):
    """Historical generated recommendations and explainability payloads."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    rank = Column(Integer, default=1, nullable=False)
    raw_explanation = Column(Text, default="{}", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="recommendations")
    item = relationship("Item", back_populates="recommendations")

    @property
    def explanation_dict(self):
        try:
            return json.loads(self.raw_explanation or "{}")
        except Exception:
            return {}

    @explanation_dict.setter
    def explanation_dict(self, val):
        self.raw_explanation = json.dumps(val or {})
