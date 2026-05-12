from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_endpoint_success():
    """Test that /ping returns 200 and correct response structure"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}

def test_ping_endpoint_idempotency():
    """Test that multiple calls to /ping are consistent"""
    responses = [client.get("/ping") for _ in range(10)]
    assert all(r.status_code == 200 for r in responses)
    assert all(r.json() == {"pong": True} for r in responses)

def test_ping_not_affected_by_timestamp():
    """Regression test: ensure /ping doesn't fail based on timestamp modulo 3"""
    import time
    from unittest.mock import patch

    # Test at various timestamp modulos to ensure no time-based failures
    for offset in range(3):
        with patch('time.time', return_value=1000000000 + offset):
            response = client.get("/ping")
            assert response.status_code == 200, \
                f"Failed at timestamp % 3 == {offset}"
            assert response.json() == {"pong": True}
