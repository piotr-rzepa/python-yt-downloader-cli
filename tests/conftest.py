"""Pytest testing setup and configuration file."""


def pytest_configure(config):
    """Adds configuration for differentiating between e2e and unit tests."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
    config.addinivalue_line("markers", "unit: mark as unit test.")
