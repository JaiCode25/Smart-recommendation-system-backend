"""Data Collection API Router."""
from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.collectors.factory import collector_registry
from app.services.item_service import ItemService

router = APIRouter(prefix="/collect", tags=["Data Collection"])


class CollectRequest(BaseModel):
    source: Optional[str] = "demo"  # youtube, instagram, shopping, demo, or all
    query: Optional[str] = None
    limit: int = 15


@router.post("")
def trigger_collection(req: CollectRequest, db: Session = Depends(get_db)):
    """
    Trigger content collection from a specific source or all sources.
    Standardizes collected data, extracts/normalizes tags, updates the graph, and stores items in DB.
    """
    total_added = 0
    sources_collected = []
    
    if req.source == "all" or not req.source:
        all_results = collector_registry.collect_all(limit_per_source=req.limit)
        for src, items in all_results.items():
            for item in items:
                ItemService.save_collected_item(db, item)
                total_added += 1
            sources_collected.append({"source": src, "items_count": len(items)})
    else:
        try:
            items = collector_registry.collect_from_source(req.source, query=req.query, limit=req.limit)
            for item in items:
                ItemService.save_collected_item(db, item)
                total_added += 1
            sources_collected.append({"source": req.source, "items_count": len(items)})
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "success",
        "items_added": total_added,
        "sources": sources_collected,
        "message": f"Successfully collected {total_added} items and updated tag graph."
    }
