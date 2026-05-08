import pytest
from requests.exceptions import Timeout

from safecatch.safecatch import safecatch_handler


# Mock API function that always times out
def simulated_api_call():
    raise Timeout("Request timed out")


# Fallback response
FALLBACK_RESPONSE = {"status": "fallback", "data": {}}


# Decorated function using safecatch
@safecatch_handler(Timeout, FALLBACK_RESPONSE)
def fetch_user_data():
    return simulated_api_call()


def test_fetch_user_data_timeout_returns_fallback():
    """
    Ensure that a Timeout exception is caught
    and the fallback response is returned.
    """

    result = fetch_user_data()

    assert result == FALLBACK_RESPONSE
    assert result["status"] == "fallback"
    assert result["data"] == {}


def test_fetch_user_data_success(monkeypatch):
    """
    Ensure normal successful responses are returned unchanged.
    """

    expected_response = {"status": "success", "data": {"id": 1, "name": "Alice"}}

    # Mock successful API call
    def successful_api_call():
        return expected_response

    # Replace the timeout function with a successful one
    monkeypatch.setattr("test_safecatch_external_handler.simulated_api_call", successful_api_call)

    result = fetch_user_data()

    assert result == expected_response
    assert result["status"] == "success"
    assert result["data"]["name"] == "Alice"


def test_non_timeout_exception_propagates(monkeypatch):
    """
    Ensure unexpected exceptions are NOT suppressed.
    """

    def failing_api_call():
        raise ValueError("Unexpected parsing failure")

    monkeypatch.setattr("test_safecatch_external_handler.simulated_api_call", failing_api_call)

    with pytest.raises(ValueError, match="Unexpected parsing failure"):
        fetch_user_data()
