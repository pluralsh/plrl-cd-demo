from fastapi.testclient import TestClient
import os
from unittest.mock import patch

# Note: By default, demo mode is disabled (ENABLE_DEMO_FAILURES not set or "false")
from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_healthy_by_default():
    """Test that /ping is always healthy when demo mode is disabled (default)"""
    # With default config (demo mode disabled), ping should always succeed
    # Test multiple times to ensure it's always healthy regardless of time
    for _ in range(5):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

def test_ping_with_mocked_time():
    """Test that /ping works correctly with time-based conditions"""
    # Mock time to trigger potential failure condition (time % 3 == 0)
    # But since demo mode is disabled by default, it should still succeed
    with patch('app.main.time.time', return_value=3.0):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

    # Mock time to not trigger failure condition (time % 3 != 0)
    with patch('app.main.time.time', return_value=4.0):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
