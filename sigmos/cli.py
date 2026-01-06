"""CLI interface for SIGMOS audio quality evaluation."""

import json
import sys
from pathlib import Path

import soundfile as sf
import typer

from . import calculate_sigmos

app = typer.Typer(help="Calculate SIGMOS score for audio quality assessment.")


def calculate_sigmos_from_file(audio_file_path: str, channel: int = 0) -> dict:
    """
    Calculate SIGMOS score for a channel in an audio file.

    Args:
        audio_file_path: Path to the audio file
        channel: Channel to analyze (default 0)

    Returns:
        Dictionary containing SIGMOS scores and metadata

    Raises:
        ValueError: If audio file cannot be loaded or is invalid

    """
    # Load the audio file
    try:
        audio_data, sample_rate = sf.read(audio_file_path)
    except Exception as e:
        raise ValueError(f"Failed to load audio file: {e}") from e

    if len(audio_data) == 0:
        raise ValueError("Audio file is empty")

    # Handle mono (1D) or multi-channel (2D) audio
    if audio_data.ndim == 1:
        # Mono audio
        if channel != 0:
            raise ValueError(
                f"Channel {channel} requested but file is mono "
                "(only channel 0 available)"
            )
        selected_channel = audio_data
        num_channels = 1
    elif audio_data.ndim == 2:
        # Multi-channel audio
        num_channels = audio_data.shape[1]
        if channel < 0 or channel >= num_channels:
            raise ValueError(
                f"Channel {channel} out of range. File has {num_channels} "
                f"channel(s) (0-{num_channels - 1})"
            )
        selected_channel = audio_data[:, channel]
    else:
        raise ValueError(
            f"Unsupported audio format: expected 1D or 2D array, got {audio_data.ndim}D"
        )

    # Calculate SIGMOS scores
    try:
        scores = calculate_sigmos(selected_channel, sample_rate=sample_rate)
    except Exception as e:
        raise ValueError(f"Failed to calculate SIGMOS scores: {e}") from e

    return {
        "file": audio_file_path,
        "channel": channel,
        "scores": scores,
        "overall_score": scores["MOS_OVRL"],
        "sample_rate": sample_rate,
        "duration_seconds": len(selected_channel) / sample_rate,
    }


@app.command()
def main(
    file: Path = typer.Argument(..., help="Audio file to analyze"),
    channel: int = typer.Option(
        0, "-c", "--channel", help="Channel to analyze (default: 0)"
    ),
    json_output: bool = typer.Option(False, "-j", "--json", help="Output JSON format"),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Show detailed information"
    ),
):
    """Calculate SIGMOS score for audio quality assessment."""
    try:
        if not file.exists():
            typer.echo(f"Error: File not found: {file}", err=True)
            sys.exit(1)

        results = calculate_sigmos_from_file(str(file), channel=channel)

        if json_output:
            # JSON output with all scores + metadata
            output = {
                "file": results["file"],
                "channel": results["channel"],
                "sample_rate": results["sample_rate"],
                "duration_seconds": round(results["duration_seconds"], 2),
                "scores": results["scores"],
            }
            typer.echo(json.dumps(output, indent=2))
        elif verbose:
            # Verbose human-readable output
            typer.echo(f"File: {results['file']}")
            typer.echo(f"Channel: {results['channel']}")
            typer.echo(f"Sample rate: {results['sample_rate']} Hz")
            typer.echo(f"Duration: {results['duration_seconds']:.2f} seconds")
            typer.echo()
            typer.echo(f"=== Channel {results['channel']} SIGMOS Scores ===")
            scores = results["scores"]
            typer.echo(f"  Overall (MOS_OVRL): {scores['MOS_OVRL']:.3f}")
            typer.echo(f"  Signal Quality (MOS_SIG): {scores['MOS_SIG']:.3f}")
            typer.echo(f"  Color/Tonal (MOS_COL): {scores['MOS_COL']:.3f}")
            typer.echo(f"  Discontinuity (MOS_DISC): {scores['MOS_DISC']:.3f}")
            typer.echo(f"  Loudness (MOS_LOUD): {scores['MOS_LOUD']:.3f}")
            typer.echo(f"  Noise (MOS_NOISE): {scores['MOS_NOISE']:.3f}")
            typer.echo(f"  Reverberation (MOS_REVERB): {scores['MOS_REVERB']:.3f}")
            typer.echo()
        else:
            # Simple output format: just the overall score (for script compatibility)
            typer.echo(f"{results['overall_score']:.3f}")

    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
