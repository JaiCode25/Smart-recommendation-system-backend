"""Tag Normalization Module."""
import re
from typing import List, Set

STOP_WORDS = {
    "a", "an", "the", "in", "on", "at", "for", "to", "of", "and", "or", "with",
    "by", "from", "up", "about", "into", "over", "after", "is", "are", "was",
    "were", "be", "this", "that", "it", "how", "what", "top", "best", "vs", "new"
}


def normalize_tag(tag: str) -> str:
    """
    Normalize a raw tag string:
    - Lowercase
    - Replace spaces and underscores with hyphens
    - Strip non-alphanumeric characters (except hyphens)
    - Collapse consecutive hyphens
    - Strip leading/trailing hyphens
    """
    if not tag:
        return ""
    tag = tag.strip().lower()
    tag = re.sub(r"[_\s]+", "-", tag)
    tag = re.sub(r"[^a-z0-9\-]", "", tag)
    tag = re.sub(r"-+", "-", tag)
    tag = tag.strip("-")
    return tag


def normalize_tag_list(tags: List[str]) -> List[str]:
    """Normalize a list of tags, filter out stop words, and eliminate duplicates preserving order."""
    seen: Set[str] = set()
    normalized: List[str] = []
    for raw in tags:
        norm = normalize_tag(raw)
        if norm and len(norm) > 1 and norm not in STOP_WORDS and norm not in seen:
            seen.add(norm)
            normalized.append(norm)
    return normalized
