"""System Aggregation and Analytics Metrics Service."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.item import Item
from app.models.user import User
from app.models.tag import Tag, TagRelationship
from app.models.interaction import Interaction
from app.models.recommendation import RecommendationRecord
from app.graph.tag_graph import tag_graph_engine
from app.schemas.config import SystemStatsResponse
from app.config import settings


class StatsService:
    @staticmethod
    def get_system_stats(db: Session) -> SystemStatsResponse:
        total_items = db.query(Item).count()
        total_users = db.query(User).count()
        total_tags = db.query(Tag).count()
        total_interactions = db.query(Interaction).count()
        total_recommendations = db.query(RecommendationRecord).count()

        # Sources breakdown
        sources_raw = db.query(Item.source, func.count(Item.id)).group_by(Item.source).all()
        sources_breakdown = {src: count for src, count in sources_raw}

        # Categories breakdown
        cats_raw = db.query(Item.category, func.count(Item.id)).group_by(Item.category).all()
        cats_breakdown = {cat: count for cat, count in cats_raw}

        topo = tag_graph_engine.get_topology()

        return SystemStatsResponse(
            total_items=total_items,
            total_users=total_users,
            total_tags=total_tags,
            total_graph_nodes=topo["nodes_count"],
            total_graph_edges=topo["edges_count"],
            total_interactions=total_interactions,
            total_recommendations=total_recommendations,
            sources_breakdown=sources_breakdown,
            categories_breakdown=cats_breakdown,
            demo_mode=settings.DEMO_MODE
        )
