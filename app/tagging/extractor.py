"""Tag Extraction from Item Metadata and Text."""
import re
from typing import List, Set
from app.tagging.normalizer import normalize_tag_list, normalize_tag

DOMAIN_KEYWORDS = {
    "cricket": ["cricket", "sports"],
    "virat kohli": ["virat-kohli", "cricket", "batting"],
    "batting": ["batting", "cricket"],
    "bowling": ["bowling", "cricket"],
    "world cup": ["world-cup", "sports", "cricket"],
    "python": ["python", "programming", "technology"],
    "fastapi": ["fastapi", "python", "backend", "api"],
    "react": ["react", "javascript", "frontend", "web-development"],
    "javascript": ["javascript", "web-development", "frontend"],
    "discrete mathematics": ["discrete-mathematics", "graph-theory", "algorithms"],
    "graph theory": ["graph-theory", "algorithms", "discrete-mathematics"],
    "networkx": ["graph-theory", "python", "algorithms"],
    "machine learning": ["machine-learning", "ai", "data-science"],
    "artificial intelligence": ["ai", "machine-learning"],
    "fitness": ["fitness", "sports", "health", "training"],
    "nutrition": ["nutrition", "health", "food", "cooking"],
    "headphones": ["audio", "gadgets", "technology"],
    "keyboard": ["gadgets", "technology", "programming"]
}


def extract_tags_from_text(title: str, description: str = "", category: str = "general") -> List[str]:
    """
    Derive relevant semantic tags from item title, description and category.
    """
    tags: List[str] = []
    combined_text = f"{title} {description} {category}".lower()

    # 1. Match domain keywords
    for phrase, derived_tags in DOMAIN_KEYWORDS.items():
        if phrase in combined_text:
            tags.extend(derived_tags)

    # 2. Add category as tag
    if category and category != "general":
        tags.append(category)

    # 3. Extract meaningful tokens
    tokens = re.findall(r"[a-z0-9\-]{3,}", combined_text)
    tags.extend(tokens[:10])

    return normalize_tag_list(tags)
