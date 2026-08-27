"""Discrete Mathematics Set-Theoretic and Vector Similarity Measures."""
import math
from typing import Set, Dict, Any, Iterable


def jaccard_similarity(set_a: Iterable[str], set_b: Iterable[str]) -> float:
    """
    Compute classical Jaccard similarity index between two sets:
    J(A, B) = |A ∩ B| / |A ∪ B|
    Range: [0.0, 1.0]
    """
    s_a = set(set_a)
    s_b = set(set_b)
    if not s_a or not s_b:
        return 0.0
    intersection = len(s_a & s_b)
    union = len(s_a | s_b)
    if union == 0:
        return 0.0
    return float(intersection) / float(union)


def weighted_jaccard_similarity(weights_a: Dict[str, float], weights_b: Dict[str, float]) -> float:
    """
    Compute Generalized/Weighted Jaccard similarity:
    J_w(A, B) = sum(min(w_a(x), w_b(x))) / sum(max(w_a(x), w_b(x)))
    """
    all_keys = set(weights_a.keys()) | set(weights_b.keys())
    if not all_keys:
        return 0.0
    min_sum = 0.0
    max_sum = 0.0
    for k in all_keys:
        wa = max(0.0, weights_a.get(k, 0.0))
        wb = max(0.0, weights_b.get(k, 0.0))
        min_sum += min(wa, wb)
        max_sum += max(wa, wb)
    if max_sum == 0.0:
        return 0.0
    return min_sum / max_sum


def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """
    Compute Cosine similarity between two sparse attribute vectors:
    cos(A, B) = (A · B) / (||A|| * ||B||)
    """
    common_keys = set(vec_a.keys()) & set(vec_b.keys())
    if not common_keys:
        return 0.0
    dot_product = sum(vec_a[k] * vec_b[k] for k in common_keys)
    norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return max(0.0, min(1.0, dot_product / (norm_a * norm_b)))


def dice_coefficient(set_a: Iterable[str], set_b: Iterable[str]) -> float:
    """
    Compute Sørensen–Dice coefficient:
    Dice(A, B) = 2 * |A ∩ B| / (|A| + |B|)
    """
    s_a = set(set_a)
    s_b = set(set_b)
    if not s_a or not s_b:
        return 0.0
    intersection = len(s_a & s_b)
    total = len(s_a) + len(s_b)
    if total == 0:
        return 0.0
    return (2.0 * intersection) / float(total)


def overlap_coefficient(set_a: Iterable[str], set_b: Iterable[str]) -> float:
    """
    Compute Overlap/Szymkiewicz–Simpson coefficient:
    Overlap(A, B) = |A ∩ B| / min(|A|, |B|)
    """
    s_a = set(set_a)
    s_b = set(set_b)
    if not s_a or not s_b:
        return 0.0
    intersection = len(s_a & s_b)
    min_len = min(len(s_a), len(s_b))
    if min_len == 0:
        return 0.0
    return float(intersection) / float(min_len)
