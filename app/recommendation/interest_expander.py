"""Graph-Based Interest Expansion Engine."""
from typing import Dict, Any
from app.graph.tag_graph import tag_graph_engine
from app.graph.traversal import expand_interests_multi_hop
from app.config import settings


class InterestExpander:
    """
    Expands direct user interests using Discrete Mathematics NetworkX Tag Graph.
    Uses multi-hop propagation with damping factor to discover related interests.
    """

    @staticmethod
    def expand(
        direct_interests: Dict[str, float],
        max_hops: int = 2,
        damping_factor: float = 0.70
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculates expanded interests from direct interest scores across graph relationships.
        """
        if not direct_interests:
            return {}

        return expand_interests_multi_hop(
            graph_engine=tag_graph_engine,
            direct_interests=direct_interests,
            max_hops=max_hops or settings.MAX_GRAPH_HOPS,
            damping_factor=damping_factor or settings.GRAPH_DAMPING_FACTOR
        )
