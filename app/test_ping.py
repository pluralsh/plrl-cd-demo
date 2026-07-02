from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_ping_is_stable():
    for _ in range(5):
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.json() == {'pong': True}
