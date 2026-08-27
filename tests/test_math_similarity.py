"""Unit tests for Discrete Mathematics similarity metrics."""
from app.graph.similarity import (
    jaccard_similarity,
    weighted_jaccard_similarity,
    cosine_similarity,
    dice_coefficient,
    overlap_coefficient
)


def test_jaccard_similarity_exact_matches():
    set_a = {"cricket", "batting", "sports"}
    set_b = {"cricket", "batting", "sports"}
    assert jaccard_similarity(set_a, set_b) == 1.0


def test_jaccard_similarity_disjoint():
    set_a = {"cricket", "batting"}
    set_b = {"python", "fastapi"}
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_partial_overlap():
    # Intersection = {cricket, sports} (size 2), Union = {cricket, batting, sports, virat-kohli} (size 4)
    # Jaccard = 2 / 4 = 0.5
    set_a = {"cricket", "batting", "sports"}
    set_b = {"cricket", "virat-kohli", "sports"}
    assert jaccard_similarity(set_a, set_b) == 0.5


def test_weighted_jaccard_similarity():
    w_a = {"cricket": 8.0, "batting": 6.0}
    w_b = {"cricket": 4.0, "batting": 6.0, "bowling": 2.0}
    # min sum: min(8,4) + min(6,6) + min(0,2) = 4 + 6 + 0 = 10
    # max sum: max(8,4) + max(6,6) + max(0,2) = 8 + 6 + 2 = 16
    # weighted jaccard = 10 / 16 = 0.625
    assert round(weighted_jaccard_similarity(w_a, w_b), 3) == 0.625


def test_cosine_similarity():
    v1 = {"a": 3.0, "b": 4.0}  # norm = 5
    v2 = {"a": 3.0, "b": 4.0}  # norm = 5
    assert round(cosine_similarity(v1, v2), 4) == 1.0

    v3 = {"c": 5.0}
    assert cosine_similarity(v1, v3) == 0.0


def test_dice_and_overlap_coefficients():
    s1 = {"a", "b", "c"}
    s2 = {"b", "c", "d", "e"}
    # intersection = 2, total len = 7 => Dice = 4 / 7
    assert round(dice_coefficient(s1, s2), 3) == round(4.0 / 7.0, 3)
    # intersection = 2, min len = 3 => Overlap = 2 / 3
    assert round(overlap_coefficient(s1, s2), 3) == round(2.0 / 3.0, 3)
