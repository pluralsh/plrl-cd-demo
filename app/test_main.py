from fastapi.testclient import TestClient
import os
import pytest

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_no_failure_by_default():
    """Test that /ping succeeds when PING_FAILURE_MODULO is not set or is 0"""
    # Ensure env var is not set
    os.environ.pop('PING_FAILURE_MODULO', None)

    # Test multiple requests - none should fail
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

def test_ping_with_zero_modulo():
    """Test that /ping succeeds when PING_FAILURE_MODULO is explicitly 0"""
    os.environ['PING_FAILURE_MODULO'] = '0'

    try:
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}
    finally:
        os.environ.pop('PING_FAILURE_MODULO', None)

def test_ping_with_invalid_modulo():
    """Test that /ping succeeds when PING_FAILURE_MODULO is invalid"""
    test_values = ['invalid', '', '-1', '0.5']

    for test_val in test_values:
        os.environ['PING_FAILURE_MODULO'] = test_val
        try:
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}
        finally:
            os.environ.pop('PING_FAILURE_MODULO', None)

def test_ping_with_modulo_failures():
    """Test that /ping fails deterministically when PING_FAILURE_MODULO > 0"""
    # This test verifies the modulo logic works as expected
    # Note: The counter is global and persists across tests, and FastAPI's test client
    # raises exceptions directly rather than converting them to 500 responses

    # Save the current value
    original_value = os.environ.get('PING_FAILURE_MODULO')

    try:
        # Set the environment variable to fail every 7th request
        os.environ['PING_FAILURE_MODULO'] = '7'

        # Get the current counter from the module
        from . import main
        initial_counter = main._ping_request_counter

        # Make requests and verify behavior
        # We'll test enough requests to ensure we hit at least one failure
        num_requests = 15
        actual_failures = 0
        actual_successes = 0

        for i in range(num_requests):
            expected_counter = initial_counter + i + 1

            try:
                response = client.get("/ping")
                # If we get here, request succeeded
                assert response.status_code == 200
                actual_successes += 1
                # Verify this counter value should not be divisible by 7
                assert expected_counter % 7 != 0, f"Counter {expected_counter} should have failed but succeeded"
            except Exception as e:
                # Request raised an exception (intentional failure in test client)
                # Verify this counter value should be divisible by 7
                assert expected_counter % 7 == 0, f"Counter {expected_counter} should have succeeded but failed with: {e}"
                assert "intentional test failure" in str(e), f"Unexpected exception: {e}"
                actual_failures += 1

        # Ensure we actually tested at least one failure
        assert actual_failures > 0, f"Test should have triggered at least one failure (got {actual_failures} failures, {actual_successes} successes)"
        # And at least one success
        assert actual_successes > 0, f"Test should have had at least one success (got {actual_failures} failures, {actual_successes} successes)"
    finally:
        # Restore original value
        if original_value is None:
            os.environ.pop('PING_FAILURE_MODULO', None)
        else:
            os.environ['PING_FAILURE_MODULO'] = original_value
