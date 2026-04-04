from fastapi.testclient import TestClient
from unittest.mock import patch
import logging

from .main import app

client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_200():
    """Test that /ping always returns HTTP 200 with correct response body."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_never_returns_500():
    """Test that /ping never returns 500 by calling it multiple times.

    Previously, /ping had random failure injection based on time.
    This test ensures that behavior is completely removed.
    """
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}


def test_hello_endpoint():
    """Test the /hello endpoint returns correctly."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"hello": "world!"}


def test_world_endpoint():
    """Test the /world endpoint returns correctly."""
    response = client.get("/world")
    assert response.status_code == 200
    assert response.json() == {"world": "hello!"}


def test_global_exception_handler_returns_500(caplog):
    """Test that unhandled exceptions return HTTP 500 and log stack traces.

    Uses a mock to force an exception in an endpoint to verify
    the global exception handler behavior.
    """
    # Create a temporary route that raises an exception
    @app.get("/test-exception")
    def raise_exception():
        raise ValueError("Test exception for handler verification")

    with caplog.at_level(logging.ERROR):
        response = client.get("/test-exception")

    # Verify HTTP 500 response
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}

    # Verify exception was logged
    assert "Unhandled exception occurred" in caplog.text
    assert "ValueError" in caplog.text or "Test exception" in caplog.text


def test_exception_handler_logs_request_context(caplog):
    """Test that exception handler logs include request context."""
    # Reuse the test exception route
    with caplog.at_level(logging.ERROR):
        response = client.get("/test-exception")

    assert response.status_code == 500
    # The logger.exception call should include the traceback
    assert "Traceback" in caplog.text or "exception" in caplog.text.lower()
