"""Discrete Graph Traversal and Interest Expansion Algorithms."""
import networkx as nx
from typing import Dict, List, Any, Optional, Set
from app.graph.tag_graph import TagGraphEngine


def expand_interests_multi_hop(
    graph_engine: TagGraphEngine,
    direct_interests: Dict[str, float],
    max_hops: int = 2,
    damping_factor: float = 0.70
) -> Dict[str, Dict[str, Any]]:
    """
    Propagate user interest scores through graph relations across multiple hops:
    Score(expanded_tag) = sum_{direct_tag} Score(direct_tag) * Edge_Weight(path) * (damping_factor ^ hop_distance)
    
    Returns:
    Dict[expanded_tag_name, {
        "score": float,
        "source_tag": str,
        "hop_distance": int,
        "path": List[str],
        "edge_weight": float
    }]
    """
    g = graph_engine.graph
    expanded: Dict[str, Dict[str, Any]] = {}
    direct_tag_set = set(direct_interests.keys())

    for direct_tag, score in direct_interests.items():
        if not g.has_node(direct_tag):
            continue

        # Hop 1 traversal
        for neighbor in g.neighbors(direct_tag):
            if neighbor in direct_tag_set:
                continue  # Keep direct interests pure
            
            edge_w = g[direct_tag][neighbor].get("weight", 1.0)
            propagated_score = score * edge_w * (damping_factor ** 1)

            if neighbor not in expanded or propagated_score > expanded[neighbor]["score"]:
                expanded[neighbor] = {
                    "score": round(propagated_score, 2),
                    "source_tag": direct_tag,
                    "hop_distance": 1,
                    "path": [direct_tag, neighbor],
                    "edge_weight": edge_w
                }

            # Hop 2 traversal
            if max_hops >= 2:
                for hop2_nbr in g.neighbors(neighbor):
                    if hop2_nbr in direct_tag_set or hop2_nbr == direct_tag:
                        continue
                    
                    edge2_w = g[neighbor][hop2_nbr].get("weight", 1.0)
                    hop2_score = score * edge_w * edge2_w * (damping_factor ** 2)

                    if hop2_nbr not in expanded or hop2_score > expanded[hop2_nbr]["score"]:
                        expanded[hop2_nbr] = {
                            "score": round(hop2_score, 2),
                            "source_tag": direct_tag,
                            "hop_distance": 2,
                            "path": [direct_tag, neighbor, hop2_nbr],
                            "edge_weight": round(edge_w * edge2_w, 2)
                        }

    return expanded


def find_shortest_path_explanation(
    graph_engine: TagGraphEngine,
    source_tag: str,
    target_tag: str
) -> Optional[Dict[str, Any]]:
    """Find shortest path between two tags and return connection weight."""
    g = graph_engine.graph
    if not g.has_node(source_tag) or not g.has_node(target_tag):
        return None
    try:
        path = nx.shortest_path(g, source=source_tag, target=target_tag)
        if len(path) <= 1:
            return None
        
        edges = []
        total_weight = 1.0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            w = g[u][v].get("weight", 1.0)
            total_weight *= w
            edges.append({"from": u, "to": v, "weight": w})
            
        return {
            "path": path,
            "hops": len(path) - 1,
            "path_weight": round(total_weight, 3),
            "edges": edges
        }
    except nx.NetworkXNoPath:
        return None
