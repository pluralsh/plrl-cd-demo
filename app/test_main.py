from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_endpoint():
    """Test that /ping endpoint returns 200 and expected payload"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}
