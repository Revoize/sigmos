"""
Revoize SIGMOS - Audio quality evaluation using SIGMOS metric.

This package provides both CLI and Python API for calculating SIGMOS scores,
which estimate P.804 audio quality dimensions based on subjectively annotated
data from ITU-T P.804 to mimic human perception of audio quality.

This implementation is based on code from Microsoft's SIG-Challenge repository:
https://github.com/microsoft/SIG-Challenge
"""

import numpy as np

from ._estimator import _get_estimator

__all__ = ["calculate_sigmos"]


def calculate_sigmos(audio: np.ndarray, sample_rate: int = 48000) -> dict:
    """
    Calculate SIGMOS score for audio.

    Args:
        audio: Audio signal (1D numpy array)
        sample_rate: Sample rate in Hz (defaults to 48000).
            Audio will be resampled to 48kHz if different.

    Returns:
        Dictionary with SIGMOS scores including:
        - MOS_OVRL: Overall MOS score (main metric)
        - MOS_SIG: Signal quality
        - MOS_COL: Color/tonal quality
        - MOS_DISC: Discontinuity
        - MOS_LOUD: Loudness
        - MOS_NOISE: Noise level
        - MOS_REVERB: Reverberation

    Raises:
        ValueError: If audio is invalid or processing fails
        ImportError: If required dependencies are missing

    """
    if len(audio) == 0:
        raise ValueError("Audio array is empty")
    estimator = _get_estimator()
    return estimator.run(audio, sr=sample_rate)
