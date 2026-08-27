"""Items Management API Router."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.item import Item, ItemTag
from app.models.tag import Tag
from app.schemas.item import ItemResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=List[ItemResponse])
def get_items(
    source: Optional[str] = Query(None, description="Filter by source: youtube, instagram, shopping, demo"),
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by specific tag"),
    query: Optional[str] = Query(None, description="Keyword search across title and description"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retrieve items with flexible filtering, search, and pagination."""
    items, _ = ItemService.get_items(
        db, source=source, category=category, tag=tag, query=query, limit=limit, offset=offset
    )
    return items


@router.get("/{id}", response_model=ItemResponse)
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    """Retrieve detailed item by database ID."""
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found.")

    item_tag_objs = (
        db.query(Tag.name)
        .join(ItemTag, ItemTag.tag_id == Tag.id)
        .filter(ItemTag.item_id == item.id)
        .all()
    )
    tags = [t[0] for t in item_tag_objs]

    return ItemResponse(
        id=item.id,
        item_id=item.item_id,
        source=item.source,
        title=item.title,
        description=item.description,
        url=item.url,
        thumbnail=item.thumbnail,
        category=item.category,
        creator_or_brand=item.creator_or_brand,
        price=item.price,
        tags=tags,
        metadata=item.metadata_dict,
        created_at=item.created_at
    )
