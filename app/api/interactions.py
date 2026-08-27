"""User Interaction Logging API Router."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.interaction import InteractionCreate, InteractionResponse
from app.services.interaction_service import InteractionService

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.post("", response_model=InteractionResponse)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    """
    Record a user interaction event (view, click, like, dislike, save, skip, search)
    and dynamically update the user's interest profile.
    """
    try:
        return InteractionService.record_interaction(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[InteractionResponse])
def list_interactions(
    user_id: int = Query(1, description="User ID"),
    interaction_type: Optional[str] = Query(None, description="Filter: like, dislike, view, save, click"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Audit log of all user interactions with timestamps and interaction weights."""
    records, _ = InteractionService.get_interactions(
        db, user_id=user_id, interaction_type=interaction_type, limit=limit, offset=offset
    )
    return records
