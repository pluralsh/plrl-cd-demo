import os
from unittest import mock

import pytest
from fastapi.testclient import TestClient

# Import app only once - don't reload to avoid prometheus port conflicts
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint returns expected structure."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Commit" in data
    assert "From" in data


def test_hello():
    """Test the /hello endpoint."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"hello": "world!"}


def test_world():
    """Test the /world endpoint."""
    response = client.get("/world")
    assert response.status_code == 200
    assert response.json() == {"world": "hello!"}


def test_ping_returns_200_by_default():
    """Test that /ping returns 200 when fault injection is disabled (default).
    
    Default behavior (FAULT_INJECT_PING=false or unset) should always return 200.
    """
    # Since default env vars disable fault injection, /ping should always succeed
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_returns_pong_multiple_times():
    """Test that /ping consistently returns 200 with default settings."""
    # Call multiple times to verify consistent behavior
    for _ in range(5):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}


def test_ping_fault_injection_with_mocked_config():
    """Test fault injection by mocking the config variables directly."""
    import app.main as main_module
    
    # Save original values
    original_fault_inject = main_module.FAULT_INJECT_PING
    original_rate = main_module.FAULT_INJECT_RATE
    
    try:
        # Enable fault injection with 100% rate
        main_module.FAULT_INJECT_PING = True
        main_module.FAULT_INJECT_RATE = 1.0
        
        # Mock random to always trigger failure
        with mock.patch('app.main.random.random', return_value=0.5):
            response = client.get("/ping")
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "fault injection" in data["detail"].lower()
    finally:
        # Restore original values
        main_module.FAULT_INJECT_PING = original_fault_inject
        main_module.FAULT_INJECT_RATE = original_rate


def test_ping_fault_injection_respects_rate():
    """Test that fault injection respects the configured rate."""
    import app.main as main_module
    
    # Save original values
    original_fault_inject = main_module.FAULT_INJECT_PING
    original_rate = main_module.FAULT_INJECT_RATE
    
    try:
        # Enable fault injection with 50% rate
        main_module.FAULT_INJECT_PING = True
        main_module.FAULT_INJECT_RATE = 0.5
        
        # Mock random to return value below rate - should fail
        with mock.patch('app.main.random.random', return_value=0.3):
            response = client.get("/ping")
            assert response.status_code == 500
        
        # Mock random to return value above rate - should succeed
        with mock.patch('app.main.random.random', return_value=0.7):
            response = client.get("/ping")
            assert response.status_code == 200
    finally:
        # Restore original values
        main_module.FAULT_INJECT_PING = original_fault_inject
        main_module.FAULT_INJECT_RATE = original_rate


def test_ping_no_failure_when_rate_is_zero():
    """Test that setting rate to 0 means no failures even when enabled."""
    import app.main as main_module
    
    # Save original values
    original_fault_inject = main_module.FAULT_INJECT_PING
    original_rate = main_module.FAULT_INJECT_RATE
    
    try:
        # Enable fault injection but set rate to 0
        main_module.FAULT_INJECT_PING = True
        main_module.FAULT_INJECT_RATE = 0.0
        
        # Should always succeed since rate is 0
        for _ in range(5):
            response = client.get("/ping")
            assert response.status_code == 200
    finally:
        # Restore original values
        main_module.FAULT_INJECT_PING = original_fault_inject
        main_module.FAULT_INJECT_RATE = original_rate


def test_ping_no_failure_when_disabled():
    """Test that disabling fault injection prevents failures regardless of rate."""
    import app.main as main_module
    
    # Save original values
    original_fault_inject = main_module.FAULT_INJECT_PING
    original_rate = main_module.FAULT_INJECT_RATE
    
    try:
        # Disable fault injection but set high rate
        main_module.FAULT_INJECT_PING = False
        main_module.FAULT_INJECT_RATE = 1.0
        
        # Should always succeed since injection is disabled
        for _ in range(5):
            response = client.get("/ping")
            assert response.status_code == 200
    finally:
        # Restore original values
        main_module.FAULT_INJECT_PING = original_fault_inject
        main_module.FAULT_INJECT_RATE = original_rate
