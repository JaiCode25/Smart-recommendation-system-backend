"""Unit tests for content collectors."""
from app.collectors.youtube_collector import YouTubeCollector
from app.collectors.instagram_collector import InstagramCollector
from app.collectors.shopping_collector import ShoppingCollector
from app.collectors.demo_collector import DemoCollector
from app.collectors.factory import collector_registry


def test_youtube_collector_fallback():
    col = YouTubeCollector()
    items = col.collect(limit=3)
    assert len(items) > 0
    assert items[0].source == "youtube"
    assert len(items[0].tags) > 0


def test_instagram_collector_fallback():
    col = InstagramCollector()
    items = col.collect(limit=2)
    assert len(items) > 0
    assert items[0].source == "instagram"


def test_shopping_collector():
    col = ShoppingCollector()
    items = col.collect(limit=2)
    assert len(items) > 0
    assert items[0].source == "shopping"
    assert items[0].price is not None


def test_collector_registry():
    sources = collector_registry.list_sources()
    assert "youtube" in sources
    assert "instagram" in sources
    assert "shopping" in sources
    assert "demo" in sources
