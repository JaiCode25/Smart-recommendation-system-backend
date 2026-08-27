"""Shopping and E-Commerce Products Collector."""
import logging
from typing import List, Optional
from app.collectors.base import BaseCollector
from app.schemas.item import CollectedItem

logger = logging.getLogger(__name__)


class ShoppingCollector(BaseCollector):
    """Shopping & Products Collector supporting e-commerce catalog items."""

    def __init__(self):
        super().__init__(source_name="shopping")

    def is_available(self) -> bool:
        return True

    def collect(self, query: Optional[str] = None, limit: int = 10) -> List[CollectedItem]:
        catalog = [
            {
                "id": "shop-crick-pro-bat",
                "title": "Custom Edition Grade 1 English Willow Cricket Bat",
                "desc": "Engineered for elite power hitting, sweet spot balance, and aerodynamic pick-up.",
                "url": "https://shop.cricketgear.example/products/grade-1-bat",
                "thumb": "https://images.unsplash.com/photo-1589801258579-18e091f4ca26?w=600&auto=format&fit=crop&q=80",
                "cat": "shopping",
                "brand": "MRF / SG Cricket",
                "price": 319.99,
                "tags": ["cricket", "batting", "equipment", "shopping", "sports"]
            },
            {
                "id": "shop-tech-monitor",
                "title": "34-Inch UltraWide 144Hz IPS Programmer & Gaming Display",
                "desc": "Ultra-sharp 4K color accurate display with USB-C 90W charging and ergonomic stand.",
                "url": "https://shop.techdisplays.example/products/ultrawide-34",
                "thumb": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80",
                "cat": "shopping",
                "brand": "LG / Dell UltraSharp",
                "price": 499.99,
                "tags": ["technology", "gadgets", "programming", "shopping"]
            },
            {
                "id": "shop-fit-strap",
                "title": "Precision Heart Rate Monitor Chest Strap with Bluetooth & ANT+",
                "desc": "ECG-accurate live biometric data streaming for sprint interval training and sports telemetry.",
                "url": "https://shop.fitbiometrics.example/products/hr-chest-strap",
                "thumb": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80",
                "cat": "shopping",
                "brand": "Polar / Garmin",
                "price": 89.99,
                "tags": ["fitness", "training", "gadgets", "health", "shopping"]
            }
        ]

        return [
            self.standardize_item(
                item_id=c["id"],
                title=c["title"],
                description=c["desc"],
                url=c["url"],
                thumbnail=c["thumb"],
                category=c["cat"],
                creator_or_brand=c["brand"],
                price=c["price"],
                tags=c["tags"]
            )
            for c in catalog[:limit]
        ]
