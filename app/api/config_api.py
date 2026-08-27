"""System Dynamic Configuration API Router."""
from fastapi import APIRouter, HTTPException
from app.schemas.config import ConfigUpdate
from app.config import settings

router = APIRouter(prefix="/config", tags=["Configuration"])


@router.get("")
def get_configuration():
    """Get current mathematical scoring weights and graph parameters."""
    return {
        "tag_similarity_weight": settings.TAG_SIMILARITY_WEIGHT,
        "graph_expansion_weight": settings.GRAPH_EXPANSION_WEIGHT,
        "direct_interest_weight": settings.DIRECT_INTEREST_WEIGHT,
        "popularity_weight": settings.POPULARITY_WEIGHT,
        "dislike_penalty_weight": settings.DISLIKE_PENALTY_WEIGHT,
        "graph_damping_factor": settings.GRAPH_DAMPING_FACTOR,
        "max_graph_hops": settings.MAX_GRAPH_HOPS,
        "time_decay_half_life_days": settings.TIME_DECAY_HALF_LIFE_DAYS,
        "interaction_weights": {
            "like": settings.WEIGHT_LIKE,
            "save": settings.WEIGHT_SAVE,
            "click": settings.WEIGHT_CLICK,
            "view": settings.WEIGHT_VIEW,
            "search": settings.WEIGHT_SEARCH,
            "skip": settings.WEIGHT_SKIP,
            "dislike": settings.WEIGHT_DISLIKE
        }
    }


@router.post("")
def update_configuration(update: ConfigUpdate):
    """Update mathematical scoring weights dynamically at runtime."""
    if update.tag_similarity_weight is not None:
        settings.TAG_SIMILARITY_WEIGHT = update.tag_similarity_weight
    if update.graph_expansion_weight is not None:
        settings.GRAPH_EXPANSION_WEIGHT = update.graph_expansion_weight
    if update.direct_interest_weight is not None:
        settings.DIRECT_INTEREST_WEIGHT = update.direct_interest_weight
    if update.popularity_weight is not None:
        settings.POPULARITY_WEIGHT = update.popularity_weight
    if update.dislike_penalty_weight is not None:
        settings.DISLIKE_PENALTY_WEIGHT = update.dislike_penalty_weight
    if update.graph_damping_factor is not None:
        settings.GRAPH_DAMPING_FACTOR = update.graph_damping_factor

    return {
        "status": "success",
        "message": "Scoring parameters updated successfully.",
        "config": get_configuration()
    }
