"""Database Initial Seeding with Realistic Demo Dataset."""
import json
import os
import logging
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.item import Item
from app.models.tag import Tag, TagRelationship
from app.models.interaction import Interaction
from app.graph.tag_graph import tag_graph_engine
from app.services.item_service import ItemService
from app.collectors.demo_collector import DemoCollector, find_demo_file

logger = logging.getLogger(__name__)


def seed_database_if_empty(db: Session):
    """Seed the database with sample users, multi-source items, semantic relations and demo user interactions."""
    item_count = db.query(Item).count()
    if item_count > 0:
        tag_graph_engine.build_from_db(db)
        logger.info(f"Database already populated ({item_count} items). Loaded {len(tag_graph_engine.graph)} graph nodes.")
        return

    logger.info("Initializing database seed data...")

    # 1. Create Default Demo User
    demo_user = db.query(User).filter(User.id == 1).first()
    if not demo_user:
        demo_user = User(
            id=1,
            username="alex_dev",
            email="alex.dev@example.com"
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

    # 2. Ingest Sample Demo Items
    collector = DemoCollector()
    items = collector.collect(limit=100)
    for itm in items:
        ItemService.save_collected_item(db, itm)

    # 3. Ingest Semantic Tag Relations
    relations_path = find_demo_file("tag_relations.json")
    if relations_path and os.path.exists(relations_path):
        try:
            with open(relations_path, "r", encoding="utf-8") as f:
                rels = json.load(f)
            for r in rels:
                t1 = db.query(Tag).filter(Tag.name == r["source"]).first()
                t2 = db.query(Tag).filter(Tag.name == r["target"]).first()
                if not t1:
                    t1 = Tag(name=r["source"], category="general")
                    db.add(t1)
                    db.flush()
                if not t2:
                    t2 = Tag(name=r["target"], category="general")
                    db.add(t2)
                    db.flush()

                s_id, tgt_id = (t1.id, t2.id) if t1.id < t2.id else (t2.id, t1.id)
                existing_rel = db.query(TagRelationship).filter(
                    TagRelationship.source_tag_id == s_id,
                    TagRelationship.target_tag_id == tgt_id
                ).first()

                if not existing_rel:
                    new_rel = TagRelationship(
                        source_tag_id=s_id,
                        target_tag_id=tgt_id,
                        weight=r.get("weight", 0.8),
                        co_occurrence_count=3,
                        relationship_type=r.get("type", "semantic")
                    )
                    db.add(new_rel)
            db.commit()
        except Exception as e:
            logger.error(f"Error seeding tag relationships: {e}")

    # 4. Ingest Initial Realistic User Interactions for Demo User
    item_vk1 = db.query(Item).filter(Item.item_id == "yt-crick-001").first()
    item_vk2 = db.query(Item).filter(Item.item_id == "insta-crick-003").first()
    item_py1 = db.query(Item).filter(Item.item_id == "yt-prog-001").first()
    item_api = db.query(Item).filter(Item.item_id == "yt-ai-003").first()
    item_math = db.query(Item).filter(Item.item_id == "insta-tech-004").first()
    item_bat = db.query(Item).filter(Item.item_id == "shop-crick-004").first()

    interactions_to_add = [
        (item_vk1, "like", 5.0),
        (item_vk2, "like", 5.0),
        (item_py1, "like", 5.0),
        (item_bat, "save", 4.0),
        (item_api, "click", 2.0),
        (item_math, "view", 1.0)
    ]

    for item_obj, inter_type, w in interactions_to_add:
        if item_obj:
            db.add(
                Interaction(
                    user_id=demo_user.id,
                    item_id=item_obj.id,
                    interaction_type=inter_type,
                    weight=w
                )
            )

    db.commit()

    # 5. Build NetworkX In-Memory Tag Graph
    tag_graph_engine.build_from_db(db)
    logger.info(f"Seeding completed successfully! Loaded {len(tag_graph_engine.graph)} nodes and {tag_graph_engine.graph.number_of_edges()} edges.")
