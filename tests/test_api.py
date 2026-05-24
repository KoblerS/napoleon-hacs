"""Tests for the Napoleon Ayla API client."""
import pytest

from custom_components.napoleon.api import NapoleonAylaApi, AuthenticationError
from custom_components.napoleon.const import REGIONS


def test_api_initialization():
    """Test API client initializes with correct region config."""
    api = NapoleonAylaApi("test@example.com", "password123", "EU")
    assert api._email == "test@example.com"
    assert api._region_config == REGIONS["EU"]
    assert api.access_token is None
    assert api.refresh_token is None


def test_api_set_tokens():
    """Test setting tokens on the API client."""
    api = NapoleonAylaApi("test@example.com", "password123")
    api.set_tokens("access123", "refresh456")
    assert api.access_token == "access123"
    assert api.refresh_token == "refresh456"


def test_api_default_region():
    """Test API client defaults to EU region."""
    api = NapoleonAylaApi("test@example.com", "password123")
    assert api._region_config == REGIONS["EU"]
