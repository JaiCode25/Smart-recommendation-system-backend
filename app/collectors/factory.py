"""Collector Factory and Aggregator Registry."""
import logging
from typing import Dict, List, Optional
from app.collectors.base import BaseCollector
from app.collectors.youtube_collector import YouTubeCollector
from app.collectors.instagram_collector import InstagramCollector
from app.collectors.shopping_collector import ShoppingCollector
from app.collectors.demo_collector import DemoCollector
from app.schemas.item import CollectedItem

logger = logging.getLogger(__name__)


class CollectorRegistry:
    """Registry managing all content collectors."""

    def __init__(self):
        self._collectors: Dict[str, BaseCollector] = {
            "youtube": YouTubeCollector(),
            "instagram": InstagramCollector(),
            "shopping": ShoppingCollector(),
            "demo": DemoCollector()
        }

    def register(self, name: str, collector: BaseCollector):
        self._collectors[name.lower()] = collector

    def get_collector(self, name: str) -> Optional[BaseCollector]:
        return self._collectors.get(name.lower())

    def list_sources(self) -> List[str]:
        return list(self._collectors.keys())

    def collect_from_source(self, source: str, query: Optional[str] = None, limit: int = 20) -> List[CollectedItem]:
        collector = self.get_collector(source)
        if not collector:
            raise ValueError(f"Collector source '{source}' is not supported. Supported: {self.list_sources()}")
        return collector.collect(query=query, limit=limit)

    def collect_all(self, limit_per_source: int = 15) -> Dict[str, List[CollectedItem]]:
        results = {}
        for name, collector in self._collectors.items():
            try:
                items = collector.collect(limit=limit_per_source)
                results[name] = items
            except Exception as e:
                logger.error(f"Collection failed for source '{name}': {e}")
                results[name] = []
        return results


collector_registry = CollectorRegistry()
