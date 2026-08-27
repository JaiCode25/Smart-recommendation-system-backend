"""Pydantic Schemas for Interactions."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class InteractionCreate(BaseModel):
    user_id: int
    item_id: int
    interaction_type: str = Field(..., description="view, click, like, dislike, save, skip, search")
    weight: Optional[float] = None


class InteractionResponse(BaseModel):
    id: int
    user_id: int
    item_id: int
    item_title: Optional[str] = None
    item_source: Optional[str] = None
    interaction_type: str
    weight: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class InteractionFilterParams(BaseModel):
    user_id: Optional[int] = None
    interaction_type: Optional[str] = None
    source: Optional[str] = None
    limit: int = 50
    offset: int = 0
