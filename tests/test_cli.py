"""Tests for SIGMOS CLI."""

import json
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf
from typer.testing import CliRunner

from sigmos.cli import app


def test_cli_simple_output(tmp_path):
    """Test CLI with simple output format."""
    # Create a simple test audio file
    sample_rate = 48000
    duration = 0.5
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)

    test_file = tmp_path / "test.wav"
    sf.write(str(test_file), audio, sample_rate)

    runner = CliRunner()
    result = runner.invoke(app, [str(test_file)])

    assert result.exit_code == 0
    # Should output just a float
    output = result.stdout.strip()
    try:
        score = float(output)
        assert 1 <= score <= 5
    except ValueError:
        pytest.fail(f"Expected float output, got: {output}")


def test_cli_json_output(tmp_path):
    """Test CLI with JSON output format."""
    # Create a simple test audio file
    sample_rate = 48000
    duration = 0.5
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)

    test_file = tmp_path / "test.wav"
    sf.write(str(test_file), audio, sample_rate)

    runner = CliRunner()
    result = runner.invoke(app, [str(test_file), "--json"])

    assert result.exit_code == 0
    output = result.stdout.strip()
    data = json.loads(output)

    assert "file" in data
    assert "channel" in data
    assert "sample_rate" in data
    assert "duration_seconds" in data
    assert "scores" in data
    assert "MOS_OVRL" in data["scores"]


def test_cli_verbose_output(tmp_path):
    """Test CLI with verbose output format."""
    # Create a simple test audio file
    sample_rate = 48000
    duration = 0.5
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)

    test_file = tmp_path / "test.wav"
    sf.write(str(test_file), audio, sample_rate)

    runner = CliRunner()
    result = runner.invoke(app, [str(test_file), "--verbose"])

    assert result.exit_code == 0
    output = result.stdout
    assert "SIGMOS Scores" in output
    assert "MOS_OVRL" in output
    assert "MOS_SIG" in output


def test_cli_real_audio_file():
    """Test CLI with the real audio file."""
    audio_file = Path(__file__).parent / "fixtures" / "karol_1_long_noisy.wav"

    if not audio_file.exists():
        pytest.fail(f"Test audio file not found: {audio_file}")

    runner = CliRunner()
    result = runner.invoke(app, [str(audio_file)])

    assert result.exit_code == 0
    output = result.stdout.strip()
    try:
        score = float(output)
        assert 1 <= score <= 5
        # Should be < 2.5 for noisy audio
        assert score < 2.5, f"Expected score < 2.5 for noisy audio, got {score}"
    except ValueError:
        pytest.fail(f"Expected float output, got: {output}")


def test_cli_channel_selection(tmp_path):
    """Test CLI channel selection."""
    # Create a stereo test audio file
    sample_rate = 48000
    duration = 0.5
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    channel0 = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    channel1 = np.cos(2 * np.pi * frequency * t).astype(np.float32)
    stereo_audio = np.column_stack([channel0, channel1])

    test_file = tmp_path / "test_stereo.wav"
    sf.write(str(test_file), stereo_audio, sample_rate)

    runner = CliRunner()

    # Test channel 0
    result0 = runner.invoke(app, [str(test_file), "--channel", "0"])
    assert result0.exit_code == 0

    # Test channel 1
    result1 = runner.invoke(app, [str(test_file), "--channel", "1"])
    assert result1.exit_code == 0

    # Test invalid channel
    result_invalid = runner.invoke(app, [str(test_file), "--channel", "2"])
    assert result_invalid.exit_code != 0


def test_cli_file_not_found():
    """Test CLI with non-existent file."""
    runner = CliRunner()
    result = runner.invoke(app, ["/nonexistent/file.wav"])

    assert result.exit_code != 0
    # Error message goes to stderr, not stdout
    assert "not found" in result.stderr.lower() or "Error" in result.stderr
