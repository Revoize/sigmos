"""Shared test fixtures."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def mono_fixture():
    """Path to the mono audio fixture file."""
    return FIXTURES_DIR / "karol_1_long_noisy.wav"


@pytest.fixture(scope="session")
def stereo_fixture():
    """Path to the stereo audio fixture file."""
    return FIXTURES_DIR / "karol_1_long_noisy_stereo.wav"
