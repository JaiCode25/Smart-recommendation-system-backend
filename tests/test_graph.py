"""Unit tests for NetworkX Tag Graph Engine."""
from app.graph.tag_graph import TagGraphEngine


def test_tag_graph_construction_and_degrees():
    engine = TagGraphEngine()
    engine.add_node("cricket", category="sports")
    engine.add_node("batting", category="sports")
    engine.add_node("sports", category="sports")
    engine.add_node("python", category="programming")

    engine.add_edge("cricket", "batting", weight=0.9)
    engine.add_edge("cricket", "sports", weight=0.95)

    assert engine.get_degree("cricket") == 2
    assert engine.get_degree("batting") == 1
    assert engine.get_degree("python") == 0
    assert round(engine.get_weighted_degree("cricket"), 2) == 1.85


def test_tag_graph_neighbors():
    engine = TagGraphEngine()
    engine.add_edge("cricket", "virat-kohli", weight=0.92)
    engine.add_edge("cricket", "bowling", weight=0.85)

    nbrs = engine.get_neighbors("cricket")
    assert len(nbrs) == 2
    assert nbrs[0]["tag"] == "virat-kohli"  # sorted by weight
    assert nbrs[0]["weight"] == 0.92


def test_tag_graph_topology():
    engine = TagGraphEngine()
    engine.add_edge("fastapi", "python", weight=0.88)
    engine.add_edge("python", "programming", weight=0.95)

    topo = engine.get_topology()
    assert topo["nodes_count"] == 3
    assert topo["edges_count"] == 2
    assert topo["density"] > 0
