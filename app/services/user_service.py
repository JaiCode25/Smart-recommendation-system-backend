"""User Profile and Interest Service."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.interest import UserInterest
from app.models.tag import Tag
from app.schemas.user import UserResponse, UserCreate, InterestProfileResponse, TagInterestScore
from app.recommendation.profile_builder import UserProfileBuilder
from app.recommendation.interest_expander import InterestExpander


class UserService:
    @staticmethod
    def get_or_create_user(db: Session, username: str = "demo_user", email: Optional[str] = None) -> User:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username, email=email or f"{username}@example.com")
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def get_user_interest_profile(db: Session, user_id: int) -> InterestProfileResponse:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = UserService.get_or_create_user(db, username="demo_user")
            user_id = user.id

        direct_dict, _ = UserProfileBuilder.calculate_direct_interests(db, user_id=user_id)
        expanded_dict = InterestExpander.expand(direct_interests=direct_dict)

        now = datetime.utcnow()
        direct_scores: List[TagInterestScore] = [
            TagInterestScore(
                tag=t,
                score=score,
                is_direct=True,
                hop_distance=0,
                last_updated=now
            )
            for t, score in sorted(direct_dict.items(), key=lambda x: x[1], reverse=True)
        ]

        expanded_scores: List[TagInterestScore] = [
            TagInterestScore(
                tag=t,
                score=data["score"],
                is_direct=False,
                source_tag=data.get("source_tag"),
                hop_distance=data.get("hop_distance", 1),
                last_updated=now
            )
            for t, data in sorted(expanded_dict.items(), key=lambda x: x[1]["score"], reverse=True)
        ]

        return InterestProfileResponse(
            user_id=user_id,
            username=user.username,
            direct_interests=direct_scores,
            expanded_interests=expanded_scores,
            total_interests_count=len(direct_scores) + len(expanded_scores),
            last_updated=now
        )
