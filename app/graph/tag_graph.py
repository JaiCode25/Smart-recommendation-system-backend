"""NetworkX Discrete Tag Graph Engine."""
import networkx as nx
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.tag import Tag, TagRelationship


class TagGraphEngine:
    """
    Discrete Mathematics Tag Graph G = (V, E, W) using NetworkX.
    Nodes = Tags (Vertices)
    Edges = Relationships (Weighted Edges)
    """

    def __init__(self):
        self.graph: nx.Graph = nx.Graph()

    def build_from_db(self, db: Session):
        """Reconstruct the in-memory NetworkX graph from database records."""
        self.graph.clear()
        
        tags = db.query(Tag).all()
        for t in tags:
            self.graph.add_node(
                t.name,
                id=t.id,
                category=t.category,
                name=t.name
            )

        relations = db.query(TagRelationship).all()
        for rel in relations:
            if rel.source_tag and rel.target_tag:
                self.graph.add_edge(
                    rel.source_tag.name,
                    rel.target_tag.name,
                    id=rel.id,
                    weight=rel.weight,
                    co_occurrence=rel.co_occurrence_count,
                    rel_type=rel.relationship_type
                )

    def add_node(self, tag_name: str, category: str = "general", tag_id: Optional[int] = None):
        """Add a tag vertex to the graph."""
        if not self.graph.has_node(tag_name):
            self.graph.add_node(tag_name, category=category, id=tag_id, name=tag_name)

    def add_edge(self, tag1: str, tag2: str, weight: float = 1.0, rel_type: str = "co_occurrence", co_occurrence: int = 1):
        """Add or update an edge between two tags."""
        if not self.graph.has_node(tag1):
            self.add_node(tag1)
        if not self.graph.has_node(tag2):
            self.add_node(tag2)
        
        self.graph.add_edge(
            tag1,
            tag2,
            weight=weight,
            rel_type=rel_type,
            co_occurrence=co_occurrence
        )

    def get_neighbors(self, tag_name: str) -> List[Dict[str, Any]]:
        """Get 1-hop neighbors of a tag with edge weights."""
        if not self.graph.has_node(tag_name):
            return []
        neighbors = []
        for n in self.graph.neighbors(tag_name):
            edge_data = self.graph.get_edge_data(tag_name, n) or {}
            neighbors.append({
                "tag": n,
                "weight": edge_data.get("weight", 1.0),
                "relationship_type": edge_data.get("rel_type", "co_occurrence"),
                "co_occurrence_count": edge_data.get("co_occurrence", 1)
            })
        # Sort by weight descending
        return sorted(neighbors, key=lambda x: x["weight"], reverse=True)

    def get_degree(self, tag_name: str) -> int:
        """Return the vertex degree (number of incident edges)."""
        if self.graph.has_node(tag_name):
            return int(self.graph.degree(tag_name))
        return 0

    def get_weighted_degree(self, tag_name: str) -> float:
        """Return sum of weights of incident edges."""
        if not self.graph.has_node(tag_name):
            return 0.0
        return sum(
            self.graph[tag_name][nbr].get("weight", 1.0)
            for nbr in self.graph.neighbors(tag_name)
        )

    def get_degree_centrality(self) -> Dict[str, float]:
        """Compute degree centrality for all nodes."""
        if len(self.graph) == 0:
            return {}
        return nx.degree_centrality(self.graph)

    def get_topology(self) -> Dict[str, Any]:
        """Return complete graph topology formatted for UI visualization (Vis.js / Force-Graph)."""
        centralities = self.get_degree_centrality()
        nodes = []
        for node in self.graph.nodes:
            data = self.graph.nodes[node]
            deg = self.get_degree(node)
            w_deg = self.get_weighted_degree(node)
            cent = centralities.get(node, 0.0)
            nodes.append({
                "id": node,
                "label": node,
                "category": data.get("category", "general"),
                "degree": deg,
                "weighted_degree": round(w_deg, 2),
                "centrality": round(cent, 3),
                "group": data.get("category", "general"),
                "size": max(12.0, min(35.0, 12.0 + deg * 2.5))
            })

        edges = []
        edge_id = 1
        for u, v, data in self.graph.edges(data=True):
            edges.append({
                "id": f"e-{edge_id}",
                "source": u,
                "target": v,
                "weight": round(data.get("weight", 1.0), 2),
                "relationship_type": data.get("rel_type", "co_occurrence"),
                "title": f"{u} ↔ {v} (weight: {round(data.get('weight', 1.0), 2)})"
            })
            edge_id += 1

        density = nx.density(self.graph) if len(self.graph) > 1 else 0.0
        avg_deg = sum(dict(self.graph.degree()).values()) / len(self.graph) if len(self.graph) > 0 else 0.0

        return {
            "nodes_count": len(nodes),
            "edges_count": len(edges),
            "nodes": nodes,
            "edges": edges,
            "density": round(density, 4),
            "average_degree": round(avg_deg, 2)
        }


# Global singleton instance
tag_graph_engine = TagGraphEngine()
