"""Multi-Factor Hybrid Recommendation Engine."""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.item import Item, ItemTag
from app.models.tag import Tag
from app.models.interaction import Interaction
from app.schemas.recommendation import RecommendationItemResponse
from app.schemas.item import ItemResponse
from app.recommendation.profile_builder import UserProfileBuilder
from app.recommendation.interest_expander import InterestExpander
from app.recommendation.explainer import RecommendationExplainer
from app.graph.similarity import jaccard_similarity
from app.config import settings

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Discrete Mathematics + Software Engineering Hybrid Scoring Engine.
    """

    def __init__(self, db: Session):
        self.db = db

    def generate_recommendations(
        self,
        user_id: int = 1,
        limit: int = 12,
        include_consumed: bool = False,
        source_filter: Optional[str] = None,
        category_filter: Optional[str] = None
    ) -> List[RecommendationItemResponse]:
        # 1. Compute Direct Interests & Negative Penalties
        direct_interests, negative_penalties = UserProfileBuilder.calculate_direct_interests(
            self.db, user_id=user_id, half_life_days=settings.TIME_DECAY_HALF_LIFE_DAYS
        )

        # 2. Compute Graph Expanded Interests
        expanded_interests = InterestExpander.expand(
            direct_interests=direct_interests,
            max_hops=settings.MAX_GRAPH_HOPS,
            damping_factor=settings.GRAPH_DAMPING_FACTOR
        )

        # 3. Interacted items to optionally filter
        interacted_item_ids = {
            r[0] for r in self.db.query(Interaction.item_id).filter(Interaction.user_id == user_id).all()
        }

        # 4. Fetch candidate items
        query = self.db.query(Item)
        if source_filter:
            query = query.filter(Item.source == source_filter.lower())
        if category_filter:
            query = query.filter(Item.category == category_filter.lower())
        if not include_consumed and interacted_item_ids:
            query = query.filter(~Item.id.in_(interacted_item_ids))

        items = query.all()
        if not items:
            items = self.db.query(Item).all()

        user_all_tags = set(direct_interests.keys()) | set(expanded_interests.keys())

        # 5. Score items
        scored_results = []
        for item in items:
            item_tag_objs = (
                self.db.query(Tag.name)
                .join(ItemTag, ItemTag.tag_id == Tag.id)
                .filter(ItemTag.item_id == item.id)
                .all()
            )
            item_tags = [t[0] for t in item_tag_objs]

            direct_score = sum(direct_interests.get(t, 0.0) for t in item_tags)
            graph_score = sum(expanded_interests[t]["score"] for t in item_tags if t in expanded_interests)
            jaccard_val = jaccard_similarity(user_all_tags, item_tags) if user_all_tags else 0.0

            meta = item.metadata_dict
            raw_views = meta.get("views", meta.get("likes", 10000))
            pop_score = min(10.0, float(raw_views) / 200000.0)

            penalty = sum(negative_penalties.get(t, 0.0) for t in item_tags)

            w_dir = settings.DIRECT_INTEREST_WEIGHT * 10.0
            w_graph = settings.GRAPH_EXPANSION_WEIGHT * 10.0
            w_jacc = settings.TAG_SIMILARITY_WEIGHT * 20.0
            w_pop = settings.POPULARITY_WEIGHT * 2.0
            w_pen = settings.DISLIKE_PENALTY_WEIGHT

            total_raw_score = (
                (direct_score * w_dir) +
                (graph_score * w_graph) +
                (jaccard_val * w_jacc) +
                (pop_score * w_pop) -
                (penalty * w_pen)
            )

            final_score = max(0.0, min(100.0, total_raw_score))

            score_breakdown = {
                "direct_interest_contribution": direct_score * w_dir,
                "graph_expansion_contribution": graph_score * w_graph,
                "jaccard_similarity_contribution": jaccard_val * w_jacc,
                "popularity_contribution": pop_score * w_pop,
                "negative_penalty": penalty * w_pen
            }

            explanation = RecommendationExplainer.explain(
                item_title=item.title,
                item_tags=item_tags,
                direct_interests=direct_interests,
                expanded_interests=expanded_interests,
                jaccard_sim=jaccard_val,
                score_breakdown=score_breakdown,
                recent_interactions=[f"Liked tag: {t}" for t in list(direct_interests.keys())[:2]]
            )

            item_response = ItemResponse(
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
                tags=item_tags,
                metadata=item.metadata_dict,
                created_at=item.created_at
            )

            scored_results.append({
                "item": item_response,
                "score": round(final_score, 2),
                "confidence_percentage": round(min(99.0, max(15.0, final_score)), 1),
                "explanation": explanation
            })

        scored_results.sort(key=lambda x: x["score"], reverse=True)

        recommendations = []
        for rank_idx, res in enumerate(scored_results[:limit], start=1):
            recommendations.append(
                RecommendationItemResponse(
                    item=res["item"],
                    score=res["score"],
                    rank=rank_idx,
                    confidence_percentage=res["confidence_percentage"],
                    explanation=res["explanation"]
                )
            )

        return recommendations
