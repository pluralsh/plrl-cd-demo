from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ping_is_stable_and_returns_pong():
    responses = [client.get('/ping') for _ in range(5)]

    for response in responses:
        assert response.status_code == 200
        assert response.json() == {"pong": True}
