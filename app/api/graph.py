"""NetworkX Tag Graph Topology API Router."""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.graph import GraphResponse
from app.schemas.tag import TagNeighborItem
from app.graph.tag_graph import tag_graph_engine

router = APIRouter(prefix="/graph", tags=["Graph"])


@router.get("", response_model=GraphResponse)
def get_graph_topology():
    """Get complete graph topology nodes and weighted edges for Vis.js visualization."""
    return tag_graph_engine.get_topology()


@router.get("/neighbors/{tag_name}", response_model=List[TagNeighborItem])
def get_tag_neighbors(tag_name: str):
    """Get 1-hop connected neighbors and edge weights for a specific tag."""
    norm_tag = tag_name.lower().strip()
    neighbors = tag_graph_engine.get_neighbors(norm_tag)
    if not neighbors and not tag_graph_engine.graph.has_node(norm_tag):
        raise HTTPException(status_code=404, detail=f"Tag '{norm_tag}' does not exist in graph.")
    return [
        TagNeighborItem(
            tag=n["tag"],
            weight=round(n["weight"], 2),
            relationship_type=n["relationship_type"],
            co_occurrence_count=n["co_occurrence_count"]
        )
        for n in neighbors
    ]
