from fastapi.testclient import TestClient
from unittest.mock import patch
import os
import pytest

from .main import app

client = TestClient(app)
client_no_raise = TestClient(app, raise_server_exceptions=False)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_default_success():
    """Test that /ping returns 200 by default (demo failures disabled)"""
    # Ensure ENABLE_DEMO_FAILURES is not set or is false
    with patch.dict(os.environ, {}, clear=False):
        if 'ENABLE_DEMO_FAILURES' in os.environ:
            del os.environ['ENABLE_DEMO_FAILURES']
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

def test_ping_with_failures_disabled_explicit():
    """Test that /ping returns 200 when ENABLE_DEMO_FAILURES=false"""
    with patch.dict(os.environ, {'ENABLE_DEMO_FAILURES': 'false'}):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

def test_ping_with_failures_enabled_success():
    """Test that /ping can return 200 when failures are enabled but timing doesn't trigger"""
    with patch.dict(os.environ, {'ENABLE_DEMO_FAILURES': 'true'}):
        # Mock time to return a value that won't trigger failure (not divisible by 3)
        with patch('app.main.time.time', return_value=1.0):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

def test_ping_with_failures_enabled_error():
    """Test that /ping returns 500 when failures are enabled and timing triggers"""
    with patch.dict(os.environ, {'ENABLE_DEMO_FAILURES': 'true'}):
        # Mock time to return a value that will trigger failure (divisible by 3)
        with patch('app.main.time.time', return_value=3.0):
            response = client_no_raise.get("/ping")
            assert response.status_code == 500
