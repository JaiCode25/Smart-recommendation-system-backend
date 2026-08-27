"""Integration tests for FastAPI REST API endpoints."""
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, SessionLocal, engine, Base
from app.utils.seed import seed_database_if_empty


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    init_db()
    db = SessionLocal()
    seed_database_if_empty(db)
    db.close()


def test_health_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "service" in data


def test_items_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/items?limit=5")
        assert resp.status_code == 200
        items = resp.json()
        assert isinstance(items, list)
        assert len(items) > 0


def test_tags_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/tags")
        assert resp.status_code == 200
        tags = resp.json()
        assert isinstance(tags, list)
        assert len(tags) > 0


def test_graph_topology_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/graph")
        assert resp.status_code == 200
        topo = resp.json()
        assert "nodes" in topo
        assert "edges" in topo
        assert "density" in topo
        assert topo["nodes_count"] > 0


def test_users_and_interests_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/users/1/profile")
        assert resp.status_code == 200
        profile = resp.json()
        assert profile["user_id"] == 1
        assert "direct_interests" in profile
        assert "expanded_interests" in profile


def test_recommendations_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/recommendations?user_id=1&limit=5&include_consumed=true")
        assert resp.status_code == 200
        recs = resp.json()
        assert recs["user_id"] == 1
        assert "recommendations" in recs
        assert len(recs["recommendations"]) > 0


def test_interaction_creation():
    with TestClient(app) as client:
        resp = client.get("/api/items?limit=1")
        items = resp.json()
        assert len(items) > 0
        first_item_id = items[0]["id"]

        payload = {
            "user_id": 1,
            "item_id": first_item_id,
            "interaction_type": "like"
        }
        resp = client.post("/api/interactions", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["interaction_type"] == "like"
        assert data["user_id"] == 1


def test_statistics_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/statistics")
        assert resp.status_code == 200
        stats = resp.json()
        assert stats["total_items"] > 0
        assert stats["total_tags"] > 0
