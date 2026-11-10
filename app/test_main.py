from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_successful_at_mocked_time_values(monkeypatch):
    # Multiples of three previously raised a 500 response.
    for timestamp in (0, 1, 2, 3, 6, 9):
        monkeypatch.setattr("time.time", lambda: timestamp)

        response = client.get("/ping")

        assert response.status_code == 200
        assert response.json() == {"pong": True}
