from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


class TestMain(TestCase):
    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    @patch("time.time", return_value=3)
    def test_ping_returns_pong_when_epoch_is_divisible_by_three(self, _time):
        response = client.get("/ping")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"pong": True})
