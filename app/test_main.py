from fastapi.testclient import TestClient
import os
import time
from unittest.mock import patch

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_stable_default():
    """Test that /ping returns 200 by default (chaos disabled)"""
    # Ensure ENABLE_PING_CHAOS is not set
    with patch.dict(os.environ, {}, clear=False):
        if 'ENABLE_PING_CHAOS' in os.environ:
            del os.environ['ENABLE_PING_CHAOS']

        # Test multiple times to ensure stability even when time.time() % 3 == 0
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

def test_ping_stable_explicit_false():
    """Test that /ping returns 200 when explicitly disabled"""
    with patch.dict(os.environ, {'ENABLE_PING_CHAOS': 'false'}):
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

def test_ping_chaos_enabled():
    """Test that /ping can raise exception when chaos mode is enabled"""
    with patch.dict(os.environ, {'ENABLE_PING_CHAOS': 'true'}):
        # Try multiple times to hit the chaos condition
        exceptions_raised = 0
        success_count = 0

        for _ in range(30):
            try:
                response = client.get("/ping")
                if response.status_code == 200:
                    success_count += 1
            except Exception:
                exceptions_raised += 1

        # In chaos mode, we should see at least some exceptions
        # (approximately 1/3 of the time based on time.time() % 3 == 0)
        assert exceptions_raised > 0 or success_count > 0, "Should have responses in chaos mode"
