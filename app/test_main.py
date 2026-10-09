import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_ping_succeeds_when_clock_matches_former_error_interval(self):
        # A divisible-by-three timestamp previously made /ping raise a 500 error.
        with patch("app.main.time.time", return_value=1_728_000_000):
            response = self.client.get("/ping")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"pong": True})
