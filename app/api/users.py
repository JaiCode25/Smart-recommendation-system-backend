"""User Profile & Interests API Router."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, InterestProfileResponse, TagInterestScore
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """List all registered users."""
    return db.query(User).all()


@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    """Retrieve user by ID."""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
    return user


@router.get("/{id}/interests", response_model=List[TagInterestScore])
def get_user_direct_interests(id: int, db: Session = Depends(get_db)):
    """Retrieve user's direct interest scores derived directly from their interactions."""
    profile = UserService.get_user_interest_profile(db, user_id=id)
    return profile.direct_interests


@router.get("/{id}/expanded-interests", response_model=List[TagInterestScore])
def get_user_expanded_interests(id: int, db: Session = Depends(get_db)):
    """Retrieve user's expanded interests discovered via Discrete Math Graph Propagation."""
    profile = UserService.get_user_interest_profile(db, user_id=id)
    return profile.expanded_interests


@router.get("/{id}/profile", response_model=InterestProfileResponse)
def get_user_full_profile(id: int, db: Session = Depends(get_db)):
    """Retrieve complete user interest profile (both Direct and Graph Expanded)."""
    return UserService.get_user_interest_profile(db, user_id=id)
