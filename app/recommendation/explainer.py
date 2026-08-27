"""Explainable Recommendation Rationale Generator."""
from typing import List, Dict, Any, Set
from app.schemas.recommendation import ExplainabilityDetail
from app.graph.tag_graph import tag_graph_engine
from app.graph.traversal import find_shortest_path_explanation


class RecommendationExplainer:
    """
    Generates transparent, mathematically grounded rationales for why an item was recommended.
    """

    @staticmethod
    def explain(
        item_title: str,
        item_tags: List[str],
        direct_interests: Dict[str, float],
        expanded_interests: Dict[str, Dict[str, Any]],
        jaccard_sim: float,
        score_breakdown: Dict[str, float],
        recent_interactions: List[str]
    ) -> ExplainabilityDetail:
        direct_matched: List[str] = [t for t in item_tags if t in direct_interests]
        expanded_matched: List[str] = [t for t in item_tags if t in expanded_interests]

        graph_paths = []
        for direct_tag in direct_matched or list(direct_interests.keys())[:2]:
            for item_t in item_tags:
                if direct_tag != item_t:
                    path_info = find_shortest_path_explanation(tag_graph_engine, direct_tag, item_t)
                    if path_info and path_info["hops"] <= 2:
                        graph_paths.append(path_info)

        reasons = []
        if direct_matched:
            top_tags = ", ".join(f"'{t}'" for t in direct_matched[:3])
            reasons.append(f"Direct match with your interests in {top_tags}")
        if expanded_matched:
            exp_top = ", ".join(f"'{t}'" for t in expanded_matched[:2])
            reasons.append(f"Discovered through graph relationships connecting to {exp_top}")
        if jaccard_sim > 0.15:
            reasons.append(f"High tag overlap ({int(jaccard_sim * 100)}% Jaccard similarity)")

        if not reasons:
            reasons.append("Recommended based on domain popularity & quality rating")

        summary = " • ".join(reasons)

        return ExplainabilityDetail(
            summary=summary,
            direct_matching_tags=direct_matched,
            expanded_matching_tags=expanded_matched,
            graph_paths=graph_paths[:3],
            jaccard_similarity=round(jaccard_sim, 3),
            score_breakdown={k: round(v, 2) for k, v in score_breakdown.items()},
            interaction_influences=recent_interactions[:3]
        )
