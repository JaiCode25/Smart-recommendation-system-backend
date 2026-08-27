"""Recommendation Generation & Explanations API Router."""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recommendation import (
    RecommendationListResponse,
    RecommendationGenerateRequest,
    RecommendationItemResponse
)
from app.recommendation.engine import RecommendationEngine

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=RecommendationListResponse)
def get_user_recommendations(
    user_id: int = Query(1, description="Target User ID"),
    limit: int = Query(12, ge=1, le=50),
    source_filter: Optional[str] = Query(None, description="Filter recommendations by source"),
    category_filter: Optional[str] = Query(None, description="Filter recommendations by category"),
    include_consumed: bool = Query(False, description="Include already interacted items"),
    db: Session = Depends(get_db)
):
    """Get top explainable recommendations for a user."""
    engine = RecommendationEngine(db)
    recs = engine.generate_recommendations(
        user_id=user_id,
        limit=limit,
        include_consumed=include_consumed,
        source_filter=source_filter,
        category_filter=category_filter
    )
    return RecommendationListResponse(
        user_id=user_id,
        recommendations_count=len(recs),
        generated_at=datetime.utcnow(),
        recommendations=recs
    )


@router.post("/generate", response_model=RecommendationListResponse)
def generate_recommendations_post(
    req: RecommendationGenerateRequest,
    db: Session = Depends(get_db)
):
    """Trigger fresh recommendation computation with customizable filters."""
    engine = RecommendationEngine(db)
    recs = engine.generate_recommendations(
        user_id=req.user_id,
        limit=req.limit,
        include_consumed=req.include_consumed,
        source_filter=req.source_filter,
        category_filter=req.category_filter
    )
    return RecommendationListResponse(
        user_id=req.user_id,
        recommendations_count=len(recs),
        generated_at=datetime.utcnow(),
        recommendations=recs
    )
