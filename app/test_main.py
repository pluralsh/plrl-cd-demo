from fastapi.testclient import TestClient
import os
from unittest.mock import patch

from .main import app, is_chaos_mode_enabled, should_trigger_chaos_error

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


class TestIsChaosModeEnabled:
    """Test the is_chaos_mode_enabled helper function."""

    def test_chaos_mode_disabled_by_default(self):
        """When CHAOS_MODE is not set, should return False."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove CHAOS_MODE if it exists
            os.environ.pop('CHAOS_MODE', None)
            assert is_chaos_mode_enabled() is False

    def test_chaos_mode_enabled_with_true(self):
        """When CHAOS_MODE=true, should return True."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'true'}):
            assert is_chaos_mode_enabled() is True

    def test_chaos_mode_enabled_with_TRUE(self):
        """When CHAOS_MODE=TRUE (uppercase), should return True."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'TRUE'}):
            assert is_chaos_mode_enabled() is True

    def test_chaos_mode_enabled_with_1(self):
        """When CHAOS_MODE=1, should return True."""
        with patch.dict(os.environ, {'CHAOS_MODE': '1'}):
            assert is_chaos_mode_enabled() is True

    def test_chaos_mode_disabled_with_false(self):
        """When CHAOS_MODE=false, should return False."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'false'}):
            assert is_chaos_mode_enabled() is False

    def test_chaos_mode_disabled_with_0(self):
        """When CHAOS_MODE=0, should return False."""
        with patch.dict(os.environ, {'CHAOS_MODE': '0'}):
            assert is_chaos_mode_enabled() is False

    def test_chaos_mode_disabled_with_empty(self):
        """When CHAOS_MODE is empty string, should return False."""
        with patch.dict(os.environ, {'CHAOS_MODE': ''}):
            assert is_chaos_mode_enabled() is False


class TestShouldTriggerChaosError:
    """Test the should_trigger_chaos_error pure function."""

    def test_triggers_when_divisible_by_3(self):
        """Should return True when timestamp % 3 == 0."""
        assert should_trigger_chaos_error(0) is True
        assert should_trigger_chaos_error(3) is True
        assert should_trigger_chaos_error(6) is True
        assert should_trigger_chaos_error(9) is True

    def test_does_not_trigger_when_not_divisible_by_3(self):
        """Should return False when timestamp % 3 != 0."""
        assert should_trigger_chaos_error(1) is False
        assert should_trigger_chaos_error(2) is False
        assert should_trigger_chaos_error(4) is False
        assert should_trigger_chaos_error(5) is False


class TestPingEndpoint:
    """Test the /ping endpoint behavior."""

    def test_ping_returns_200_without_chaos_mode(self):
        """Without CHAOS_MODE, /ping should always return 200."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop('CHAOS_MODE', None)
            # Run multiple times to ensure consistency
            for _ in range(10):
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"pong": True}

    def test_ping_returns_200_with_chaos_mode_false(self):
        """With CHAOS_MODE=false, /ping should always return 200."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'false'}):
            for _ in range(10):
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"pong": True}

    def test_ping_with_chaos_mode_can_return_500(self):
        """With CHAOS_MODE=true, /ping can return 500 when time % 3 == 0."""
        # Use raise_server_exceptions=False to get HTTP 500 instead of raised exception
        chaos_client = TestClient(app, raise_server_exceptions=False)
        with patch.dict(os.environ, {'CHAOS_MODE': 'true'}):
            # Mock time.time to return a value divisible by 3
            with patch('app.main.time') as mock_time:
                mock_time.time.return_value = 6.0  # 6 % 3 == 0
                response = chaos_client.get("/ping")
                assert response.status_code == 500

    def test_ping_with_chaos_mode_returns_200_when_time_not_divisible_by_3(self):
        """With CHAOS_MODE=true, /ping returns 200 when time % 3 != 0."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'true'}):
            # Mock time.time to return a value not divisible by 3
            with patch('app.main.time') as mock_time:
                mock_time.time.return_value = 7.0  # 7 % 3 != 0
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"pong": True}
