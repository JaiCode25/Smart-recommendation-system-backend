"""Pydantic Schemas for Tags and Relations."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str
    category: str = "general"


class TagResponse(TagBase):
    id: int
    created_at: datetime
    degree: Optional[int] = 0
    weighted_degree: Optional[float] = 0.0

    model_config = ConfigDict(from_attributes=True)


class TagRelationshipBase(BaseModel):
    source_tag: str
    target_tag: str
    weight: float = 1.0
    relationship_type: str = "co_occurrence"


class TagRelationshipResponse(TagRelationshipBase):
    id: int
    co_occurrence_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagNeighborItem(BaseModel):
    tag: str
    weight: float
    relationship_type: str
    co_occurrence_count: int


class TagDetailResponse(BaseModel):
    tag: str
    category: str
    degree: int
    weighted_degree: float
    centrality: float
    neighbors: List[TagNeighborItem]
