from unittest.mock import patch

from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_at_previously_failing_epoch_second():
    with patch.object(main, "time", create=True) as mocked_time:
        mocked_time.time.return_value = 3
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
