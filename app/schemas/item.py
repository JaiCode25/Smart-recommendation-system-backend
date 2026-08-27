"""Pydantic Schemas for Items."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    item_id: str
    source: str
    title: str
    description: str = ""
    url: str
    thumbnail: str = ""
    category: str = "general"
    creator_or_brand: str = ""
    price: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemFilterParams(BaseModel):
    source: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    query: Optional[str] = None
    limit: int = 50
    offset: int = 0


class CollectedItem(ItemBase):
    pass
