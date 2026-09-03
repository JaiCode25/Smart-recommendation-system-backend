"""Smart Recommendation System - FastAPI Main Application Entrypoint."""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.config import settings
from app.database import init_db, SessionLocal
from app.utils.seed import seed_database_if_empty

from app.api.health import router as health_router
from app.api.items import router as items_router
from app.api.tags import router as tags_router
from app.api.graph import router as graph_router
from app.api.users import router as users_router
from app.api.interactions import router as interactions_router
from app.api.recommendations import router as recommendations_router
from app.api.collect import router as collect_router
from app.api.statistics import router as statistics_router
from app.api.config_api import router as config_router
from app.api.auth import router as auth_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan hook to initialize database and seed sample data on startup."""

    logger.info(
        "Initializing Smart Recommendation System database..."
    )

    init_db()

    db = SessionLocal()

    try:
        seed_database_if_empty(db)
    finally:
        db.close()

    logger.info(
        "Application initialized and ready to serve requests."
    )

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    # Smart Recommendation System API

    Academic Discrete Mathematics + Software Engineering Project.
    """,
    lifespan=lifespan
)


# ---------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# REST API Routers
# ---------------------------------------------------------

app.include_router(
    health_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    items_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    tags_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    graph_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    users_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    interactions_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    recommendations_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    collect_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    statistics_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    config_router,
    prefix=settings.API_PREFIX
)

# Authentication routes
# Gives us:
# POST /api/auth/register
# POST /api/auth/login

app.include_router(
    auth_router,
    prefix=settings.API_PREFIX
)


# ---------------------------------------------------------
# Frontend Directory Resolution
# ---------------------------------------------------------

def get_frontend_index():
    """Find the frontend index.html file."""

    candidates = [
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "frontend",
                "dist",
                "index.html"
            )
        ),

        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "frontend",
                "public",
                "index.html"
            )
        ),

        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "frontend",
                "index.html"
            )
        ),

        os.path.abspath(
            os.path.join(
                "frontend",
                "dist",
                "index.html"
            )
        ),

        os.path.abspath(
            os.path.join(
                "frontend",
                "public",
                "index.html"
            )
        ),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return None


# ---------------------------------------------------------
# Root Route
# ---------------------------------------------------------

@app.get("/", include_in_schema=False)
async def serve_root():
    """Serve frontend or return API health message."""

    index_file = get_frontend_index()

    if index_file:
        return FileResponse(index_file)

    return JSONResponse(
        {
            "status": "healthy",
            "message": "Smart Recommendation System API is active."
        }
    )


# ---------------------------------------------------------
# Frontend SPA Route
# ---------------------------------------------------------

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str):
    """Serve the frontend single-page application."""

    # Do not intercept API/documentation routes
    if (
        full_path.startswith("api")
        or full_path.startswith("docs")
        or full_path.startswith("redoc")
        or full_path.startswith("openapi.json")
    ):
        return JSONResponse(
            {"detail": "Not Found"},
            status_code=404
        )

    index_file = get_frontend_index()

    if index_file:
        return FileResponse(index_file)

    return JSONResponse(
        {"detail": "Frontend index not found"},
        status_code=404
    )