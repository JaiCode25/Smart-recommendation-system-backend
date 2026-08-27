"""System Analytics and Metrics API Router."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.config import SystemStatsResponse
from app.services.stats_service import StatsService

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("", response_model=SystemStatsResponse)
def get_system_statistics(db: Session = Depends(get_db)):
    """Aggregated counts and distributions for the dashboard."""
    return StatsService.get_system_stats(db)
