"""Tests for SIGMOS calculation."""

from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from sigmos import calculate_sigmos


def test_calculate_sigmos_basic():
    """Test calculate_sigmos with a simple NumPy array."""
    # Generate a simple sine wave at 48kHz
    sample_rate = 48000
    duration = 1.0  # 1 second
    frequency = 440  # A4 note
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)

    scores = calculate_sigmos(audio, sample_rate=sample_rate)

    # Validate structure
    assert isinstance(scores, dict)
    assert "MOS_OVRL" in scores
    assert "MOS_SIG" in scores
    assert "MOS_COL" in scores
    assert "MOS_DISC" in scores
    assert "MOS_LOUD" in scores
    assert "MOS_NOISE" in scores
    assert "MOS_REVERB" in scores

    # Validate all scores are floats
    for key, value in scores.items():
        assert isinstance(value, float), f"{key} should be float, got {type(value)}"
        # Scores range from 1-5
        assert 0 <= value <= 5, f"{key} should be in reasonable range, got {value}"


def test_calculate_sigmos_resampling():
    """Test that sample rate resampling works."""
    # Generate audio at 44.1kHz
    sample_rate = 44100
    duration = 1.0
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)

    # Should resample to 48kHz internally
    scores = calculate_sigmos(audio, sample_rate=sample_rate)

    assert isinstance(scores, dict)
    assert "MOS_OVRL" in scores
    assert isinstance(scores["MOS_OVRL"], float)


def test_calculate_sigmos_empty_audio():
    """Test that empty audio raises an error."""
    audio = np.array([])

    with pytest.raises((ValueError, IndexError)):
        calculate_sigmos(audio, sample_rate=48000)


def test_calculate_sigmos_integration_real_audio():
    """Integration test with real audio file."""
    audio_file = Path(__file__).parent / "fixtures" / "karol_1_long_noisy.wav"

    if not audio_file.exists():
        pytest.fail(f"Test audio file not found: {audio_file}")

    # Load the audio file
    audio_data, sample_rate = sf.read(str(audio_file))

    # Handle mono or stereo
    if audio_data.ndim == 2:
        audio = audio_data[:, 0]  # Use first channel
    else:
        audio = audio_data

    # Calculate SIGMOS scores
    scores = calculate_sigmos(audio, sample_rate=sample_rate)

    # Validate result structure
    assert isinstance(scores, dict)
    expected_keys = [
        "MOS_OVRL",
        "MOS_SIG",
        "MOS_COL",
        "MOS_DISC",
        "MOS_LOUD",
        "MOS_NOISE",
        "MOS_REVERB",
    ]
    for key in expected_keys:
        assert key in scores, f"Missing key: {key}"

    # Validate all scores are floats in reasonable range
    for key, value in scores.items():
        assert isinstance(value, float), f"{key} should be float, got {type(value)}"
        assert 0 <= value <= 5, f"{key} should be in reasonable range, got {value}"

    # Check expected score for noisy audio file (based on test-quality.sh expectations)
    # Noisy audio should have lower overall score
    assert scores["MOS_OVRL"] < 2.5, (
        f"Expected MOS_OVRL < 2.5 for noisy audio, got {scores['MOS_OVRL']}"
    )

    # Output all scores for validation (but don't check thresholds)
    print(f"\nSIGMOS scores for {audio_file.name}:")
    print(f"  MOS_OVRL: {scores['MOS_OVRL']:.3f}")
    print(f"  MOS_SIG: {scores['MOS_SIG']:.3f}")
    print(f"  MOS_COL: {scores['MOS_COL']:.3f}")
    print(f"  MOS_DISC: {scores['MOS_DISC']:.3f}")
    print(f"  MOS_LOUD: {scores['MOS_LOUD']:.3f}")
    print(f"  MOS_NOISE: {scores['MOS_NOISE']:.3f}")
    print(f"  MOS_REVERB: {scores['MOS_REVERB']:.3f}")
