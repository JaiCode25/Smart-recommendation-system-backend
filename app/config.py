"""Application Configuration and Settings Module."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Global system configuration loaded from environment or defaults."""
    PROJECT_NAME: str = "Smart Recommendation System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./smart_recommendation.db"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # External API Keys (Leave blank for Demo Mode)
    YOUTUBE_API_KEY: str = ""
    INSTAGRAM_ACCESS_TOKEN: str = ""
    
    # Mode
    DEMO_MODE: bool = True
    
    # Recommendation Scoring Weights (Default Discrete Math Weights)
    TAG_SIMILARITY_WEIGHT: float = 0.35
    GRAPH_EXPANSION_WEIGHT: float = 0.30
    DIRECT_INTEREST_WEIGHT: float = 0.20
    POPULARITY_WEIGHT: float = 0.15
    DISLIKE_PENALTY_WEIGHT: float = 0.50
    
    # Interaction Scoring Values
    WEIGHT_LIKE: float = 5.0
    WEIGHT_SAVE: float = 4.0
    WEIGHT_CLICK: float = 2.0
    WEIGHT_VIEW: float = 1.0
    WEIGHT_SEARCH: float = 1.5
    WEIGHT_SKIP: float = -1.0
    WEIGHT_DISLIKE: float = -5.0
    
    # Graph & Interest Expansion Parameters
    GRAPH_DAMPING_FACTOR: float = 0.70
    MAX_GRAPH_HOPS: int = 2
    TIME_DECAY_HALF_LIFE_DAYS: float = 14.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
