"""SQLAlchemy Database Models Package."""
from app.models.user import User
from app.models.item import Item, ItemTag
from app.models.tag import Tag, TagRelationship
from app.models.interaction import Interaction
from app.models.interest import UserInterest
from app.models.recommendation import RecommendationRecord
from app.models.config_model import SystemConfig

__all__ = [
    "User",
    "Item",
    "ItemTag",
    "Tag",
    "TagRelationship",
    "Interaction",
    "UserInterest",
    "RecommendationRecord",
    "SystemConfig",
]
