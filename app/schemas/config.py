"""Pydantic Schemas for System Stats and Dynamic Parameters."""
from typing import Dict, Any, Optional
from pydantic import BaseModel


class ConfigUpdate(BaseModel):
    tag_similarity_weight: Optional[float] = None
    graph_expansion_weight: Optional[float] = None
    direct_interest_weight: Optional[float] = None
    popularity_weight: Optional[float] = None
    dislike_penalty_weight: Optional[float] = None
    graph_damping_factor: Optional[float] = None


class SystemStatsResponse(BaseModel):
    total_items: int
    total_users: int
    total_tags: int
    total_graph_nodes: int
    total_graph_edges: int
    total_interactions: int
    total_recommendations: int
    sources_breakdown: Dict[str, int]
    categories_breakdown: Dict[str, int]
    demo_mode: bool
