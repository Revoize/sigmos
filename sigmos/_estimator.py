"""Singleton estimator wrapper for SigMOS."""

from pathlib import Path

from ._sigmos import SigMOS, Version

# Get the models directory where the ONNX model is located
_MODEL_DIR = Path(__file__).parent / "models"

# Initialize SigMOS estimator (singleton pattern)
_sigmos_estimator = None


def _get_estimator() -> SigMOS:
    """Get or create the SigMOS estimator instance."""
    global _sigmos_estimator
    if _sigmos_estimator is None:
        _sigmos_estimator = SigMOS(model_dir=str(_MODEL_DIR), model_version=Version.V1)
    return _sigmos_estimator
