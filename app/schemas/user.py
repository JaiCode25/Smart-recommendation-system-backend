"""Pydantic Schemas for Users and Interest Profiles."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagInterestScore(BaseModel):
    tag: str
    score: float
    is_direct: bool
    source_tag: Optional[str] = None
    hop_distance: int = 0
    last_updated: datetime


class InterestProfileResponse(BaseModel):
    user_id: int
    username: str
    direct_interests: List[TagInterestScore]
    expanded_interests: List[TagInterestScore]
    total_interests_count: int
    last_updated: datetime
