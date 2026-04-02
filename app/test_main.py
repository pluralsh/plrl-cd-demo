from fastapi.testclient import TestClient
from unittest import mock
import os

from .main import app, _parse_bool_env

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


class TestParseBoolEnv:
    """Tests for the boolean environment variable parser."""

    def test_true_values(self):
        """Test that 'true', '1', 'yes' (case-insensitive) return True."""
        for val in ["true", "True", "TRUE", "1", "yes", "Yes", "YES"]:
            with mock.patch.dict(os.environ, {"TEST_VAR": val}):
                assert _parse_bool_env("TEST_VAR") is True

    def test_false_values(self):
        """Test that 'false', '0', 'no' (case-insensitive) return False."""
        for val in ["false", "False", "FALSE", "0", "no", "No", "NO"]:
            with mock.patch.dict(os.environ, {"TEST_VAR": val}):
                assert _parse_bool_env("TEST_VAR") is False

    def test_unset_returns_default(self):
        """Test that unset env var returns the default value."""
        with mock.patch.dict(os.environ, {}, clear=True):
            assert _parse_bool_env("NONEXISTENT_VAR", default=False) is False
            assert _parse_bool_env("NONEXISTENT_VAR", default=True) is True

    def test_invalid_returns_default(self):
        """Test that invalid values return the default."""
        with mock.patch.dict(os.environ, {"TEST_VAR": "invalid"}):
            assert _parse_bool_env("TEST_VAR", default=False) is False
            assert _parse_bool_env("TEST_VAR", default=True) is True


class TestPingEndpoint:
    """Tests for the /ping health check endpoint."""

    def test_ping_returns_200_when_chaos_mode_disabled(self):
        """When CHAOS_MODE is false/unset, /ping always returns 200."""
        with mock.patch.dict(os.environ, {"CHAOS_MODE": "false"}, clear=False):
            # Make multiple requests to ensure consistent behavior
            for _ in range(10):
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"status": "ok"}

    def test_ping_returns_200_when_chaos_mode_unset(self):
        """When CHAOS_MODE is unset, /ping defaults to healthy (200)."""
        env_copy = os.environ.copy()
        env_copy.pop("CHAOS_MODE", None)
        with mock.patch.dict(os.environ, env_copy, clear=True):
            for _ in range(10):
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"status": "ok"}

    def test_ping_can_return_500_when_chaos_mode_enabled(self):
        """When CHAOS_MODE is true, /ping can return 500 errors."""
        with mock.patch.dict(os.environ, {"CHAOS_MODE": "true"}, clear=False):
            # Mock time to ensure we hit the chaos condition (time % 3 == 0)
            with mock.patch("app.main.time") as mock_time:
                # Set time to a value divisible by 3 to trigger chaos
                mock_time.time.return_value = 3.0
                response = client.get("/ping")
                assert response.status_code == 500
                assert "chaos" in response.json().get("detail", "").lower()

    def test_ping_returns_200_in_chaos_mode_when_not_failing(self):
        """When CHAOS_MODE is true but not hitting chaos timing, returns 200."""
        with mock.patch.dict(os.environ, {"CHAOS_MODE": "true"}, clear=False):
            # Mock time to avoid the chaos condition (time % 3 != 0)
            with mock.patch("app.main.time") as mock_time:
                # Set time to a value NOT divisible by 3
                mock_time.time.return_value = 1.0
                response = client.get("/ping")
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "ok"
                assert data["chaos_mode"] is True
