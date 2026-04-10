# Revoize SIGMOS

Python package for speech signal quality evaluation using the SIGMOS metric.

SIGMOS is a metric that estimates speech quality dimensions defined in the ITU-T P.804 standard. It is trained on subjectively annotated data collected according to the P.804 methodology to mimic human perception of speech quality.

This package is based on the [Microsoft SIG-Challenge repository](https://github.com/microsoft/SIG-Challenge) and includes the original SIGMOS implementation and ONNX model.

## Installation

1. Make sure you have `git-lfs` installed and initialized.
2. install the package with

```sh
uv tool install --editable .
```

That should automatically update the tool if there are any changes to this repository.

## Usage

### Command Line Interface

Calculate SIGMOS scores from an audio file:

```bash
sigmos <audio_file> [options]
```

**Options:**

- `--channel`, `-c`: Channel to analyze (default: 0)
- `--json`, `-j`: Output JSON format
- `--verbose`, `-v`: Show detailed information

**Examples:**

```bash
# Simple output (overall score only)
sigmos audio.wav

# Analyze specific channel
sigmos audio.wav --channel 1

# JSON output with all scores
sigmos audio.wav --json

# Verbose human-readable output
sigmos audio.wav --verbose
```

**Output Formats:**

- **Default**: Overall score as float (for script compatibility)
- **JSON** (`--json`): Full JSON with all scores and metadata
- **Verbose** (`--verbose`): Human-readable formatted output with all scores

### Python API

```python
from sigmos import calculate_sigmos
import numpy as np
import soundfile as sf

# Load audio file
audio, sample_rate = sf.read("audio.wav")

# Calculate SIGMOS scores
scores = calculate_sigmos(audio, sample_rate=sample_rate)

# Access individual scores
print(f"Overall quality: {scores['MOS_OVRL']:.3f}")
print(f"Signal quality: {scores['MOS_SIG']:.3f}")
print(f"Color/tonal: {scores['MOS_COL']:.3f}")
print(f"Discontinuity: {scores['MOS_DISC']:.3f}")
print(f"Loudness: {scores['MOS_LOUD']:.3f}")
print(f"Noise: {scores['MOS_NOISE']:.3f}")
print(f"Reverberation: {scores['MOS_REVERB']:.3f}")
```

**Function Signature:**

```python
def calculate_sigmos(
    audio: np.ndarray,
    sample_rate: int = 48000
) -> dict
```

**Parameters:**

- `audio`: Audio signal as 1D numpy array
- `sample_rate`: Sample rate in Hz (defaults to 48000). Audio will be resampled to 48kHz if different.

**Returns:**
Dictionary with SIGMOS scores:

- `MOS_OVRL`: Overall MOS score (main metric, typically 1-5)
- `MOS_SIG`: Signal quality
- `MOS_COL`: Color/tonal quality
- `MOS_DISC`: Discontinuity
- `MOS_LOUD`: Loudness
- `MOS_NOISE`: Noise level
- `MOS_REVERB`: Reverberation

**Note:** SIGMOS scores typically range from 1-5, where higher is better.

## Supported Audio Formats

The CLI supports all audio formats supported by `soundfile`, including:

- WAV
- FLAC
- OGG
- And other formats supported by libsndfile

## Troubleshooting

### Issues loading the onnx file

If you encounter an error like

```
Error: Failed to calculate SIGMOS scores: [ONNXRuntimeError] : 7 : INVALID_PROTOBUF : Load model from .../sigmos/models/model-sigmos_1697718653_41d092e8-epo-200.onnx failed: Protobuf parsing failed.
```

it likely means you don't have git-lfs installed. Install git-lfs and do

```sh
git lfs pull
```

to fix.

### Reinstalling the package

If you installed the package without the `--editable` flag and you want to update it, you need to run

```sh
uv tool install --editable --reinstall .
```

(also works without the `--editable` flag).

uv is particularly sticky when it comes to local tool installs. Just running `uv tool install .` or `uv tool install --force .` will likely result in reusing the wheel that was built in the past, i.e. not actually updating the package. Using `--reinstall` will rebuild the wheel.

## Attribution

This implementation is based on code from Microsoft's SIG-Challenge repository:

- **Repository**: https://github.com/microsoft/SIG-Challenge
- **License**: MIT
- **Original Work**: Microsoft Corporation
- **Challenge**: ICASSP 2024 Speech Signal Improvement Challenge

The following components were adapted from the Microsoft SIG-Challenge repository:

- Core SIGMOS implementation
- ONNX model weights

Attribution headers are preserved in the source files copied over from the original repository.

## License

This package is distributed under the MIT License.
