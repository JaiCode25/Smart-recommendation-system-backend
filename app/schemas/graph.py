"""Pydantic Schemas for Graph Topology."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str
    category: str = "general"
    degree: int = 0
    weighted_degree: float = 0.0
    centrality: float = 0.0
    group: Optional[str] = None
    size: float = 15.0


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    weight: float = 1.0
    relationship_type: str = "co_occurrence"
    title: Optional[str] = None


class GraphResponse(BaseModel):
    nodes_count: int
    edges_count: int
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    density: float
    average_degree: float
