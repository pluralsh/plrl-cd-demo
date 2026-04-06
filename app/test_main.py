from fastapi.testclient import TestClient
import os
import time

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_returns_ok_by_default():
    """Test that /ping returns 200 OK when PING_FAIL_INJECT is not set"""
    # Ensure PING_FAIL_INJECT is not set
    os.environ.pop('PING_FAIL_INJECT', None)

    # Test multiple times to ensure it's consistently successful
    for _ in range(5):
        response = client.get("/ping")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "uptime_seconds" in data
        assert "version" in data
        assert "environment" in data
        time.sleep(0.5)

def test_ping_with_failure_injection():
    """Test that /ping can inject failures when PING_FAIL_INJECT=true"""
    # Set PING_FAIL_INJECT to enable failure injection
    os.environ['PING_FAIL_INJECT'] = 'true'

    # Try multiple times to catch the failure (happens when time % 3 == 0)
    failures = 0
    successes = 0
    for _ in range(10):
        try:
            response = client.get("/ping")
            if response.status_code == 200:
                successes += 1
            else:
                failures += 1
        except Exception:
            failures += 1
        time.sleep(0.4)

    # Clean up
    os.environ.pop('PING_FAIL_INJECT', None)

    # We should have seen at least one failure and one success
    assert failures > 0, "Expected at least one failure with PING_FAIL_INJECT=true"
    assert successes > 0, "Expected at least one success with PING_FAIL_INJECT=true"
