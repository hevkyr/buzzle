"""
buzzle/tests/test_api.py
Integration tests for the FastAPI endpoints.
Uses httpx's ASGI transport — no running server required.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from main import app

client = TestClient(app)


class TestRootEndpoint:
    def test_root_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200

    def test_root_has_service_key(self):
        r = client.get("/")
        assert r.json()["service"] == "buzzle"


class TestPhraseEndpoint:
    def test_single_phrase(self):
        r = client.get("/phrase")
        assert r.status_code == 200
        data = r.json()
        assert "phrase" in data
        assert "score" in data
        assert "category" in data
        assert "generated_at" in data

    def test_multiple_phrases(self):
        r = client.get("/phrase?count=5")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) == 5

    def test_count_max_clamped(self):
        r = client.get("/phrase?count=999")
        assert r.status_code == 422  # FastAPI validates ge/le constraints

    def test_count_min_clamped(self):
        r = client.get("/phrase?count=0")
        assert r.status_code == 422

    def test_seed_reproducibility(self):
        r1 = client.get("/phrase?seed=1337")
        r2 = client.get("/phrase?seed=1337")
        assert r1.json()["phrase"] == r2.json()["phrase"]

    def test_score_in_range(self):
        for _ in range(5):
            r = client.get("/phrase")
            score = r.json()["score"]
            assert 1 <= score <= 100


class TestRatedEndpoint:
    def test_rated_phrase(self):
        r = client.get("/phrase/rated")
        assert r.status_code == 200
        data = r.json()
        assert "score" in data


class TestCustomPhraseEndpoint:
    def test_custom_noun(self):
        r = client.post("/phrase/custom", json={"noun": "hamster"})
        assert r.status_code == 200
        assert "hamster" in r.json()["phrase"].lower()

    def test_all_custom_fields(self):
        r = client.post("/phrase/custom", json={
            "noun": "ferret",
            "verb": "deploys",
            "adjective": "lazy",
            "seed": 0,
        })
        assert r.status_code == 200
        data = r.json()
        assert "phrase" in data

    def test_empty_body_ok(self):
        r = client.post("/phrase/custom", json={})
        assert r.status_code == 200


class TestStatsEndpoint:
    def test_stats_structure(self):
        # Generate a few to populate stats
        client.get("/phrase?count=3")
        r = client.get("/stats")
        assert r.status_code == 200
        data = r.json()
        assert "total_phrases_generated" in data
        assert "uptime_seconds" in data
        assert "most_used_noun" in data

    def test_stats_total_increases(self):
        r1 = client.get("/stats")
        before = r1.json()["total_phrases_generated"]
        client.get("/phrase?count=5")
        r2 = client.get("/stats")
        after = r2.json()["total_phrases_generated"]
        assert after == before + 5


class TestHealthEndpoint:
    def test_health_ok(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
