"""Pytest configuration and shared fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def test_data_dir():
    """Return the test data directory path."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_pdf(test_data_dir):
    """Return path to a sample PDF for testing."""
    # This would point to a test PDF file
    return test_data_dir / "sample_form.pdf"


@pytest.fixture
def sample_user_data():
    """Return sample user data dictionary."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "address": "123 Test St",
        "city": "Test City",
        "postal_code": "12345",
    }
