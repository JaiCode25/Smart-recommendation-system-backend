"""Instagram Content Collector with Live Graph API + Realistic Fallback Dataset."""
import logging
import httpx
from typing import List, Optional
from app.collectors.base import BaseCollector
from app.schemas.item import CollectedItem
from app.config import settings

logger = logging.getLogger(__name__)


class InstagramCollector(BaseCollector):
    """Instagram Content Collector via Graph API with fallback dataset."""

    def __init__(self):
        super().__init__(source_name="instagram")
        self.access_token = settings.INSTAGRAM_ACCESS_TOKEN

    def is_available(self) -> bool:
        return bool(self.access_token and len(self.access_token.strip()) > 5)

    def collect(self, query: Optional[str] = None, limit: int = 10) -> List[CollectedItem]:
        if self.is_available():
            try:
                url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,permalink,timestamp&access_token={self.access_token}&limit={limit}"
                resp = httpx.get(url, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    items = []
                    for entry in data.get("data", []):
                        caption = entry.get("caption", "")
                        item = self.standardize_item(
                            item_id=f"insta-{entry['id']}",
                            title=caption[:80] + ("..." if len(caption) > 80 else "") or "Instagram Post",
                            description=caption,
                            url=entry.get("permalink", "https://instagram.com"),
                            thumbnail=entry.get("media_url", "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=600"),
                            category="social",
                            creator_or_brand="@creator",
                            price=None,
                            metadata={"timestamp": entry.get("timestamp")}
                        )
                        items.append(item)
                    if items:
                        return items
            except Exception as e:
                logger.warning(f"Instagram Live API request failed ({e}). Using realistic fallback.")

        return self._get_fallback_data(query, limit)

    def _get_fallback_data(self, query: Optional[str] = None, limit: int = 10) -> List[CollectedItem]:
        raw_posts = [
            {
                "id": "insta-vk-01",
                "title": "Gym Grind: Core Stability & Explosive Jump Training with Virat Kohli",
                "desc": "Consistency in preparation builds consistency on the 22 yards. Hard work never takes a day off.",
                "url": "https://www.instagram.com/p/demo_vk_gym",
                "thumb": "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?w=600&auto=format&fit=crop&q=80",
                "cat": "sports",
                "creator": "@virat.kohli",
                "tags": ["virat-kohli", "fitness", "cricket", "training", "sports"]
            },
            {
                "id": "insta-dev-02",
                "title": "React 19 Hooks & Visualizing Discrete Math Networks",
                "desc": "How modern frontends transform complex graph structures into intuitive visual dashboards.",
                "url": "https://www.instagram.com/p/demo_react_graph",
                "thumb": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600&auto=format&fit=crop&q=80",
                "cat": "frontend",
                "creator": "@frontend.visuals",
                "tags": ["react", "javascript", "web-development", "frontend", "graph-theory"]
            },
            {
                "id": "insta-cook-03",
                "title": "Anti-Inflammatory High Energy Athlete Bowl for Muscle Recovery",
                "desc": "Healthy fats, lean proteins, and micro-nutrients formulated for peak performance.",
                "url": "https://www.instagram.com/p/demo_athlete_bowl",
                "thumb": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&auto=format&fit=crop&q=80",
                "cat": "fitness",
                "creator": "@nutrition.pro",
                "tags": ["nutrition", "health", "fitness", "cooking"]
            }
        ]
        return [
            self.standardize_item(
                item_id=p["id"],
                title=p["title"],
                description=p["desc"],
                url=p["url"],
                thumbnail=p["thumb"],
                category=p["cat"],
                creator_or_brand=p["creator"],
                tags=p["tags"]
            )
            for p in raw_posts[:limit]
        ]
