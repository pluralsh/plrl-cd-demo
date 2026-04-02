from fastapi.testclient import TestClient
from unittest.mock import patch
import os

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_healthz():
    """Test liveness probe endpoint always returns 200."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readyz():
    """Test readiness probe endpoint always returns 200."""
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_ping_default_no_chaos():
    """Test /ping returns 200 when CHAOS_MODE is disabled (default)."""
    # When CHAOS_MODE=false (default), ping should always succeed
    with patch('app.main.CHAOS_MODE', False):
        for _ in range(10):  # Run multiple times to ensure consistency
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}


def test_ping_chaos_mode_enabled():
    """Test /ping behavior when CHAOS_MODE is enabled."""
    with patch('app.main.CHAOS_MODE', True):
        with patch('app.main.random.random', return_value=0.1):  # Force failure path
            response = client.get("/ping")
            assert response.status_code == 500

        with patch('app.main.random.random', return_value=0.5):  # Force success path
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}
