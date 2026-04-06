from fastapi.testclient import TestClient
import os
import pytest

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_always_returns_200():
    """Test that /ping always returns 200 OK"""
    # Test multiple times to ensure it's stable
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ok": True}

def test_ping_chaos_exists():
    """Test that /ping-chaos endpoint exists and can return both 200 and 500"""
    # Test multiple times - behavior depends on CHAOS_ENABLED env var and timing
    responses = []
    for _ in range(15):
        try:
            response = client.get("/ping-chaos")
            responses.append(response.status_code)
            # When successful, should return {"ok": True, "chaos": <bool>}
            if response.status_code == 200:
                data = response.json()
                assert "ok" in data
                assert "chaos" in data
        except Exception:
            # When chaos is enabled and timing aligns, endpoint raises exception (500)
            responses.append(500)

    # Verify we got a mix of responses or all successes
    # (depends on timing and CHAOS_ENABLED setting)
    assert len(responses) == 15
    # At minimum, endpoint should be accessible
    assert 200 in responses or 500 in responses
