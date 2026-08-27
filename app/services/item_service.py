"""Item Management Service."""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.item import Item, ItemTag
from app.models.tag import Tag
from app.schemas.item import ItemCreate, ItemResponse, CollectedItem
from app.tagging.normalizer import normalize_tag_list
from app.graph.tag_graph import tag_graph_engine


class ItemService:
    @staticmethod
    def get_items(
        db: Session,
        source: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[ItemResponse], int]:
        q = db.query(Item)
        if source:
            q = q.filter(Item.source == source.lower())
        if category:
            q = q.filter(Item.category == category.lower())
        if tag:
            q = q.join(ItemTag, ItemTag.item_id == Item.id).join(Tag, Tag.id == ItemTag.tag_id).filter(Tag.name == tag.lower())
        if query:
            search_str = f"%{query}%"
            q = q.filter((Item.title.ilike(search_str)) | (Item.description.ilike(search_str)))

        total = q.count()
        items = q.order_by(Item.created_at.desc()).offset(offset).limit(limit).all()

        responses = []
        for itm in items:
            item_tag_objs = (
                db.query(Tag.name)
                .join(ItemTag, ItemTag.tag_id == Tag.id)
                .filter(ItemTag.item_id == itm.id)
                .all()
            )
            tag_names = [t[0] for t in item_tag_objs]
            responses.append(
                ItemResponse(
                    id=itm.id,
                    item_id=itm.item_id,
                    source=itm.source,
                    title=itm.title,
                    description=itm.description,
                    url=itm.url,
                    thumbnail=itm.thumbnail,
                    category=itm.category,
                    creator_or_brand=itm.creator_or_brand,
                    price=itm.price,
                    tags=tag_names,
                    metadata=itm.metadata_dict,
                    created_at=itm.created_at
                )
            )
        return responses, total

    @staticmethod
    def save_collected_item(db: Session, collected: CollectedItem) -> Item:
        existing = db.query(Item).filter(Item.item_id == collected.item_id).first()
        if existing:
            existing.title = collected.title
            existing.description = collected.description
            existing.url = collected.url
            existing.thumbnail = collected.thumbnail
            existing.category = collected.category
            existing.creator_or_brand = collected.creator_or_brand
            existing.price = collected.price
            existing.metadata_dict = collected.metadata
            item = existing
        else:
            item = Item(
                item_id=collected.item_id,
                source=collected.source,
                title=collected.title,
                description=collected.description,
                url=collected.url,
                thumbnail=collected.thumbnail,
                category=collected.category,
                creator_or_brand=collected.creator_or_brand,
                price=collected.price,
                raw_metadata="{}"
            )
            item.metadata_dict = collected.metadata
            db.add(item)
            db.flush()

        # Link Tags
        norm_tags = normalize_tag_list(collected.tags)
        # Clear existing associations if updating
        if existing:
            db.query(ItemTag).filter(ItemTag.item_id == item.id).delete()

        for tag_str in norm_tags:
            tag_obj = db.query(Tag).filter(Tag.name == tag_str).first()
            if not tag_obj:
                tag_obj = Tag(name=tag_str, category=collected.category)
                db.add(tag_obj)
                db.flush()
                tag_graph_engine.add_node(tag_str, category=collected.category, tag_id=tag_obj.id)
            
            item_tag = ItemTag(
                item_id=item.id,
                tag_id=tag_obj.id,
                confidence=1.0,
                is_primary=1 if tag_str == collected.category else 0
            )
            db.add(item_tag)

        # Update pairwise co-occurrence edges in DB and graph
        from app.models.tag import TagRelationship
        for i in range(len(norm_tags)):
            for j in range(i + 1, len(norm_tags)):
                t1_name, t2_name = norm_tags[i], norm_tags[j]
                t1 = db.query(Tag).filter(Tag.name == t1_name).first()
                t2 = db.query(Tag).filter(Tag.name == t2_name).first()
                if t1 and t2:
                    # Canonical order to avoid double edges
                    s_id, tgt_id = (t1.id, t2.id) if t1.id < t2.id else (t2.id, t1.id)
                    rel = db.query(TagRelationship).filter(
                        TagRelationship.source_tag_id == s_id,
                        TagRelationship.target_tag_id == tgt_id
                    ).first()
                    if rel:
                        rel.co_occurrence_count += 1
                        rel.weight = min(1.0, 0.5 + (rel.co_occurrence_count * 0.05))
                    else:
                        rel = TagRelationship(
                            source_tag_id=s_id,
                            target_tag_id=tgt_id,
                            weight=0.6,
                            co_occurrence_count=1,
                            relationship_type="co_occurrence"
                        )
                        db.add(rel)
                    tag_graph_engine.add_edge(
                        t1_name, t2_name,
                        weight=rel.weight,
                        rel_type="co_occurrence",
                        co_occurrence=rel.co_occurrence_count
                    )

        db.commit()
        db.refresh(item)
        return item
