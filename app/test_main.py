from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping():
    """Test that /ping endpoint returns success consistently.

    This test verifies the fix for HTTP 500 errors caused by the
    time-based exception that was removed from the /ping endpoint.
    """
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}
