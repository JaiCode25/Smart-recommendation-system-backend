"""Base Collector Interface and Data Standard."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.schemas.item import CollectedItem
from app.tagging.normalizer import normalize_tag_list
from app.tagging.extractor import extract_tags_from_text


class BaseCollector(ABC):
    """Abstract Base Class for Multi-Source Content Collectors."""

    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    def is_available(self) -> bool:
        """Check if external credentials/API keys are configured for live collection."""
        pass

    @abstractmethod
    def collect(self, query: Optional[str] = None, limit: int = 10) -> List[CollectedItem]:
        """Collect items from source. If unavailable or credentials missing, return realistic demo data."""
        pass

    def standardize_item(
        self,
        item_id: str,
        title: str,
        description: str,
        url: str,
        thumbnail: str,
        category: str,
        creator_or_brand: str,
        price: Optional[float] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CollectedItem:
        """Create and normalize a standard CollectedItem."""
        if not tags:
            derived_tags = extract_tags_from_text(title, description, category)
        else:
            derived_tags = normalize_tag_list(tags)

        return CollectedItem(
            item_id=item_id,
            source=self.source_name,
            title=title.strip(),
            description=description.strip(),
            url=url.strip(),
            thumbnail=thumbnail.strip(),
            category=category.lower().strip(),
            creator_or_brand=creator_or_brand.strip(),
            price=price,
            tags=derived_tags,
            metadata=metadata or {}
        )
