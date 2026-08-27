"""Tag and Tag Relationship Endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagResponse, TagDetailResponse, TagNeighborItem
from app.graph.tag_graph import tag_graph_engine

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("", response_model=List[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    """Retrieve all tags along with their graph degree and weighted connectivity."""
    tags = db.query(Tag).all()
    results = []
    for t in tags:
        deg = tag_graph_engine.get_degree(t.name)
        w_deg = tag_graph_engine.get_weighted_degree(t.name)
        results.append(
            TagResponse(
                id=t.id,
                name=t.name,
                category=t.category,
                created_at=t.created_at,
                degree=deg,
                weighted_degree=round(w_deg, 2)
            )
        )
    return sorted(results, key=lambda x: x.degree, reverse=True)


@router.get("/{tag_name}", response_model=TagDetailResponse)
def get_tag_detail(tag_name: str, db: Session = Depends(get_db)):
    """Get detailed graph metrics and 1-hop neighbor relations for a tag."""
    norm_tag = tag_name.lower().strip()
    tag_obj = db.query(Tag).filter(Tag.name == norm_tag).first()
    if not tag_obj:
        raise HTTPException(status_code=404, detail=f"Tag '{norm_tag}' not found.")

    deg = tag_graph_engine.get_degree(norm_tag)
    w_deg = tag_graph_engine.get_weighted_degree(norm_tag)
    cents = tag_graph_engine.get_degree_centrality()
    cent_val = cents.get(norm_tag, 0.0)
    raw_neighbors = tag_graph_engine.get_neighbors(norm_tag)

    neighbors = [
        TagNeighborItem(
            tag=n["tag"],
            weight=round(n["weight"], 2),
            relationship_type=n["relationship_type"],
            co_occurrence_count=n["co_occurrence_count"]
        )
        for n in raw_neighbors
    ]

    return TagDetailResponse(
        tag=norm_tag,
        category=tag_obj.category,
        degree=deg,
        weighted_degree=round(w_deg, 2),
        centrality=round(cent_val, 3),
        neighbors=neighbors
    )
