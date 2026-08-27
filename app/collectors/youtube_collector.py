"""YouTube Video Collector with Live API + Realistic Fallback Dataset."""
import logging
from typing import List, Optional
from app.collectors.base import BaseCollector
from app.schemas.item import CollectedItem
from app.config import settings

logger = logging.getLogger(__name__)


class YouTubeCollector(BaseCollector):
    """YouTube Collector using YouTube Data API v3 with automatic graceful fallback."""

    def __init__(self):
        super().__init__(source_name="youtube")
        self.api_key = settings.YOUTUBE_API_KEY

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def collect(self, query: Optional[str] = None, limit: int = 10) -> List[CollectedItem]:
        if self.is_available():
            try:
                from googleapiclient.discovery import build
                youtube = build("youtube", "v3", developerKey=self.api_key)
                search_query = query or "cricket highlights programming machine learning"
                req = youtube.search().list(
                    q=search_query,
                    part="snippet",
                    maxResults=limit,
                    type="video"
                )
                res = req.execute()
                items = []
                for entry in res.get("items", []):
                    snippet = entry["snippet"]
                    video_id = entry["id"]["videoId"]
                    raw_tags = snippet.get("tags", [])
                    item = self.standardize_item(
                        item_id=f"yt-{video_id}",
                        title=snippet["title"],
                        description=snippet["description"],
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        thumbnail=snippet["thumbnails"].get("high", {}).get("url", ""),
                        category="video",
                        creator_or_brand=snippet["channelTitle"],
                        price=None,
                        tags=raw_tags,
                        metadata={"published_at": snippet["publishedAt"]}
                    )
                    items.append(item)
                if items:
                    return items
            except Exception as e:
                logger.warning(f"YouTube Live API failed ({e}). Falling back to realistic demo dataset.")

        return self._get_fallback_data(query, limit)

    def _get_fallback_data(self, query: Optional[str] = None, limit: int = 10) -> List[CollectedItem]:
        raw_pool = [
            {
                "id": "yt-crick-live-01",
                "title": "Virat Kohli Iconic 82* vs Pakistan: The Masterclass Chase Breakdown",
                "desc": "Tactical analysis of pacing, strike rotation, and clutch hitting in high-pressure ICC matches.",
                "url": "https://www.youtube.com/watch?v=demo_vk_82",
                "thumb": "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=600&auto=format&fit=crop&q=80",
                "cat": "sports",
                "creator": "Cricket Insights HD",
                "tags": ["cricket", "virat-kohli", "batting", "sports", "world-cup", "india"]
            },
            {
                "id": "yt-py-live-02",
                "title": "FastAPI Masterclass: High-Throughput REST APIs & NetworkX RecSys",
                "desc": "Learn how to build real-time recommendation engines with FastAPI, Pydantic, and SQLite.",
                "url": "https://www.youtube.com/watch?v=demo_fastapi_recsys",
                "thumb": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600&auto=format&fit=crop&q=80",
                "cat": "programming",
                "creator": "Code Architect",
                "tags": ["python", "fastapi", "programming", "technology", "backend", "api"]
            },
            {
                "id": "yt-ds-live-03",
                "title": "Discrete Mathematics in Machine Learning & Recommendation Systems",
                "desc": "Graph theory, set intersections, Jaccard matrices, and PageRank algorithms explained simply.",
                "url": "https://www.youtube.com/watch?v=demo_math_ml",
                "thumb": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&auto=format&fit=crop&q=80",
                "cat": "ai",
                "creator": "Math & CS University",
                "tags": ["discrete-mathematics", "graph-theory", "algorithms", "machine-learning", "ai"]
            },
            {
                "id": "yt-fit-live-04",
                "title": "Cricket Fast Bowling Strength & Mobility Workout for Speed",
                "desc": "Rotational power, shoulder health, and sprint mechanics for elite cricket bowlers.",
                "url": "https://www.youtube.com/watch?v=demo_bowling_fitness",
                "thumb": "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?w=600&auto=format&fit=crop&q=80",
                "cat": "fitness",
                "creator": "Pro Athlete Lab",
                "tags": ["fitness", "cricket", "bowling", "sports", "training"]
            }
        ]
        
        results = []
        for r in raw_pool[:limit]:
            results.append(
                self.standardize_item(
                    item_id=r["id"],
                    title=r["title"],
                    description=r["desc"],
                    url=r["url"],
                    thumbnail=r["thumb"],
                    category=r["cat"],
                    creator_or_brand=r["creator"],
                    tags=r["tags"]
                )
            )
        return results
