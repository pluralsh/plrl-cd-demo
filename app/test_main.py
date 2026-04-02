import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app, get_chaos_enabled

client = TestClient(app)
# Client that doesn't raise on server errors - for testing 500 responses
client_no_raise = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


class TestChaosEnabled(unittest.TestCase):
    """Tests for get_chaos_enabled function."""

    def test_chaos_disabled_by_default(self):
        """When CHAOS_ENABLED is not set, chaos should be disabled."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove CHAOS_ENABLED if it exists
            os.environ.pop('CHAOS_ENABLED', None)
            assert get_chaos_enabled() is False

    def test_chaos_enabled_true(self):
        """When CHAOS_ENABLED=true, chaos should be enabled."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'true'}):
            assert get_chaos_enabled() is True

    def test_chaos_enabled_false(self):
        """When CHAOS_ENABLED=false, chaos should be disabled."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'false'}):
            assert get_chaos_enabled() is False

    def test_chaos_enabled_1(self):
        """When CHAOS_ENABLED=1, chaos should be enabled."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': '1'}):
            assert get_chaos_enabled() is True

    def test_chaos_enabled_0(self):
        """When CHAOS_ENABLED=0, chaos should be disabled."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': '0'}):
            assert get_chaos_enabled() is False

    def test_chaos_enabled_yes(self):
        """When CHAOS_ENABLED=yes, chaos should be enabled."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'yes'}):
            assert get_chaos_enabled() is True

    def test_chaos_enabled_case_insensitive(self):
        """CHAOS_ENABLED should be case-insensitive."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'TRUE'}):
            assert get_chaos_enabled() is True
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'True'}):
            assert get_chaos_enabled() is True
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'FALSE'}):
            assert get_chaos_enabled() is False

    def test_chaos_enabled_whitespace(self):
        """CHAOS_ENABLED should handle whitespace."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': '  true  '}):
            assert get_chaos_enabled() is True


class TestPingEndpoint(unittest.TestCase):
    """Tests for /ping endpoint."""

    def test_ping_returns_200_when_chaos_disabled(self):
        """When CHAOS_ENABLED is false, /ping should always return 200."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'false'}):
            # Multiple requests should all succeed
            for _ in range(10):
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"pong": True}

    def test_ping_returns_200_when_chaos_unset(self):
        """When CHAOS_ENABLED is not set, /ping should always return 200."""
        env_backup = os.environ.get('CHAOS_ENABLED')
        try:
            os.environ.pop('CHAOS_ENABLED', None)
            # Multiple requests should all succeed
            for _ in range(10):
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"pong": True}
        finally:
            if env_backup is not None:
                os.environ['CHAOS_ENABLED'] = env_backup

    def test_ping_can_fail_when_chaos_enabled(self):
        """When CHAOS_ENABLED is true, /ping can return 500 based on time modulo."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'true'}):
            # Mock time to force failure (time % 3 == 0)
            with patch('app.main.time') as mock_time:
                mock_time.time.return_value = 3  # 3 % 3 == 0, should fail
                response = client_no_raise.get("/ping")
                assert response.status_code == 500

    def test_ping_succeeds_when_chaos_enabled_but_time_not_divisible(self):
        """When CHAOS_ENABLED is true but time % 3 != 0, /ping returns 200."""
        with patch.dict(os.environ, {'CHAOS_ENABLED': 'true'}):
            # Mock time to avoid failure (time % 3 != 0)
            with patch('app.main.time') as mock_time:
                mock_time.time.return_value = 4  # 4 % 3 == 1, should succeed
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"pong": True}
