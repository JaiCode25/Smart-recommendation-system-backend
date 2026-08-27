"""User Interaction Logging and Profile Sync Service."""
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.item import Item
from app.models.user import User
from app.schemas.interaction import InteractionCreate, InteractionResponse
from app.recommendation.profile_builder import UserProfileBuilder


class InteractionService:
    @staticmethod
    def record_interaction(db: Session, payload: InteractionCreate) -> InteractionResponse:
        # Resolve user
        user = db.query(User).filter(User.id == payload.user_id).first()
        if not user:
            user = db.query(User).first()
            if not user:
                user = User(username="demo_user", email="demo@example.com")
                db.add(user)
                db.commit()
                db.refresh(user)

        # Resolve item
        item = db.query(Item).filter(Item.id == payload.item_id).first()
        if not item:
            raise ValueError(f"Item with ID {payload.item_id} not found.")

        weight = payload.weight if payload.weight is not None else UserProfileBuilder.get_interaction_weight(payload.interaction_type)

        inter = Interaction(
            user_id=user.id,
            item_id=item.id,
            interaction_type=payload.interaction_type.lower(),
            weight=weight
        )
        db.add(inter)
        db.commit()
        db.refresh(inter)

        return InteractionResponse(
            id=inter.id,
            user_id=inter.user_id,
            item_id=inter.item_id,
            item_title=item.title,
            item_source=item.source,
            interaction_type=inter.interaction_type,
            weight=inter.weight,
            timestamp=inter.timestamp
        )

    @staticmethod
    def get_interactions(
        db: Session,
        user_id: int = 1,
        interaction_type: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[InteractionResponse], int]:
        q = db.query(Interaction).filter(Interaction.user_id == user_id)
        if interaction_type:
            q = q.filter(Interaction.interaction_type == interaction_type.lower())

        total = q.count()
        records = q.order_by(Interaction.timestamp.desc()).offset(offset).limit(limit).all()

        responses = []
        for r in records:
            itm = db.query(Item).filter(Item.id == r.item_id).first()
            responses.append(
                InteractionResponse(
                    id=r.id,
                    user_id=r.user_id,
                    item_id=r.item_id,
                    item_title=itm.title if itm else "Unknown Item",
                    item_source=itm.source if itm else "unknown",
                    interaction_type=r.interaction_type,
                    weight=r.weight,
                    timestamp=r.timestamp
                )
            )
        return responses, total
