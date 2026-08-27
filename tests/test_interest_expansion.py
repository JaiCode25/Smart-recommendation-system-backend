"""Unit tests for graph interest expansion."""
from app.graph.tag_graph import tag_graph_engine
from app.recommendation.interest_expander import InterestExpander


def test_interest_expansion_propagation():
    tag_graph_engine.graph.clear()
    tag_graph_engine.add_edge("cricket", "batting", weight=0.90)
    tag_graph_engine.add_edge("batting", "technique", weight=0.80)

    direct_interests = {"cricket": 10.0}
    expanded = InterestExpander.expand(direct_interests, max_hops=2, damping_factor=0.7)

    # 1-hop: batting = 10.0 * 0.90 * 0.7 = 6.30
    assert "batting" in expanded
    assert expanded["batting"]["hop_distance"] == 1
    assert expanded["batting"]["score"] == 6.30

    # 2-hop: technique = 10.0 * 0.90 * 0.80 * (0.7^2) = 10.0 * 0.72 * 0.49 = 3.53
    assert "technique" in expanded
    assert expanded["technique"]["hop_distance"] == 2
    assert expanded["technique"]["score"] == 3.53
