from fastapi.testclient import TestClient
import os
from unittest import mock

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_default_returns_200():
    """Test that /ping returns 200 OK by default (PING_FAIL_ENABLED=false)."""
    # By default PING_FAIL_ENABLED is false, so /ping should always return 200
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json()["pong"] is True
    assert response.json()["status"] == "ok"


def test_ping_stable_when_disabled():
    """Test that /ping is stable (multiple calls all return 200) when failures disabled."""
    # Make multiple requests to ensure stability
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200


def test_ping_with_failure_enabled():
    """Test that /ping can fail when PING_FAIL_ENABLED=true and rate is 100%."""
    # We need to reload the module with new env vars to test failure mode
    # Using mock.patch to simulate the failure condition
    # Use raise_server_exceptions=False to catch 500 errors
    test_client = TestClient(app, raise_server_exceptions=False)
    with mock.patch("app.main.PING_FAIL_ENABLED", True):
        with mock.patch("app.main.PING_FAIL_RATE", 100):
            with mock.patch("app.main.random.randint", return_value=50):  # 50 <= 100, so should fail
                response = test_client.get("/ping")
                assert response.status_code == 500


def test_ping_no_failure_when_rate_zero():
    """Test that /ping returns 200 when PING_FAIL_ENABLED=true but rate is 0%."""
    with mock.patch("app.main.PING_FAIL_ENABLED", True):
        with mock.patch("app.main.PING_FAIL_RATE", 0):
            # Even with failures "enabled", rate of 0 means no failures
            for _ in range(5):
                response = client.get("/ping")
                assert response.status_code == 200
