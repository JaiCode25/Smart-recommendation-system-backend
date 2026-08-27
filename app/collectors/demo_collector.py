"""Demo Collector Loading Verified Multi-Domain Items from Local JSON."""
import json
import os
import logging
from typing import List, Optional
from app.collectors.base import BaseCollector
from app.schemas.item import CollectedItem

logger = logging.getLogger(__name__)


def find_demo_file(filename: str) -> Optional[str]:
    """Find demo file across possible working directory offsets."""
    candidates = [
        os.path.join("data", "demo", filename),
        os.path.join("..", "data", "demo", filename),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "data", "demo", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return None


class DemoCollector(BaseCollector):
    """Collector loading benchmark test dataset from data/demo/items.json."""

    def __init__(self):
        super().__init__(source_name="demo")

    def is_available(self) -> bool:
        return find_demo_file("items.json") is not None

    def collect(self, query: Optional[str] = None, limit: int = 50) -> List[CollectedItem]:
        filepath = find_demo_file("items.json")
        if not filepath or not os.path.exists(filepath):
            logger.warning("items.json not found.")
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw_items = json.load(f)
            
            results = []
            for r in raw_items:
                results.append(
                    self.standardize_item(
                        item_id=r["item_id"],
                        title=r["title"],
                        description=r["description"],
                        url=r["url"],
                        thumbnail=r["thumbnail"],
                        category=r["category"],
                        creator_or_brand=r["creator_or_brand"],
                        price=r.get("price"),
                        tags=r.get("tags", []),
                        metadata=r.get("metadata", {})
                    )
                )
            return results[:limit]
        except Exception as e:
            logger.error(f"Error loading demo items from {filepath}: {e}")
            return []
