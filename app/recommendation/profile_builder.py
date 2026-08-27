"""Dynamic User Interest Profile Builder with Exponential Time Decay."""
import math
from datetime import datetime
from typing import Dict, Tuple
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.item import ItemTag
from app.models.tag import Tag
from app.config import settings


class UserProfileBuilder:
    """
    Computes direct user interest scores from interaction history.
    Interaction weights: like=+5, save=+4, click=+2, view=+1, search=+1.5, skip=-1, dislike=-5
    Time decay: e^(-lambda * delta_days)
    """

    @staticmethod
    def get_interaction_weight(interaction_type: str) -> float:
        mapping = {
            "like": settings.WEIGHT_LIKE,
            "save": settings.WEIGHT_SAVE,
            "click": settings.WEIGHT_CLICK,
            "view": settings.WEIGHT_VIEW,
            "search": settings.WEIGHT_SEARCH,
            "skip": settings.WEIGHT_SKIP,
            "dislike": settings.WEIGHT_DISLIKE
        }
        return mapping.get(interaction_type.lower(), 1.0)

    @classmethod
    def calculate_direct_interests(
        cls,
        db: Session,
        user_id: int,
        half_life_days: float = 14.0
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Calculate direct positive interest scores and negative penalty scores for a user.
        """
        interactions = (
            db.query(Interaction)
            .filter(Interaction.user_id == user_id)
            .order_by(Interaction.timestamp.desc())
            .all()
        )

        if not interactions:
            return {}, {}

        lambda_decay = math.log(2) / max(1.0, half_life_days)
        now = datetime.utcnow()

        raw_tag_scores: Dict[str, float] = {}
        negative_tag_scores: Dict[str, float] = {}

        for inter in interactions:
            delta_days = max(0.0, (now - inter.timestamp).total_seconds() / 86400.0)
            decay = math.exp(-lambda_decay * delta_days)
            
            weight = inter.weight if inter.weight is not None else cls.get_interaction_weight(inter.interaction_type)
            effective_weight = weight * decay

            item_tags = (
                db.query(Tag.name)
                .join(ItemTag, ItemTag.tag_id == Tag.id)
                .filter(ItemTag.item_id == inter.item_id)
                .all()
            )

            for (tag_name,) in item_tags:
                if effective_weight > 0:
                    raw_tag_scores[tag_name] = raw_tag_scores.get(tag_name, 0.0) + effective_weight
                else:
                    negative_tag_scores[tag_name] = negative_tag_scores.get(tag_name, 0.0) + abs(effective_weight)

        if raw_tag_scores:
            max_score = max(raw_tag_scores.values())
            normalized_positive = {
                tag: round((score / max_score) * 10.0, 2)
                for tag, score in raw_tag_scores.items()
                if score > 0.05
            }
        else:
            normalized_positive = {}

        return normalized_positive, negative_tag_scores
