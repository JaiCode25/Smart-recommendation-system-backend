"""Pydantic Schemas for Recommendation Generation and Explainability."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.schemas.item import ItemResponse


class ExplainabilityDetail(BaseModel):
    summary: str
    direct_matching_tags: List[str]
    expanded_matching_tags: List[str]
    graph_paths: List[Dict[str, Any]]
    jaccard_similarity: float
    score_breakdown: Dict[str, float]
    interaction_influences: List[str]


class RecommendationItemResponse(BaseModel):
    item: ItemResponse
    score: float
    rank: int
    confidence_percentage: float
    explanation: ExplainabilityDetail


class RecommendationListResponse(BaseModel):
    user_id: int
    recommendations_count: int
    generated_at: datetime
    recommendations: List[RecommendationItemResponse]


class RecommendationGenerateRequest(BaseModel):
    user_id: int = 1
    limit: int = 12
    include_consumed: bool = False
    source_filter: Optional[str] = None
    category_filter: Optional[str] = None
