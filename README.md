# Neta - Real-Time Voice Transcription

A lightweight, command-line Python application for real-time voice transcription using Faster Whisper.

## Features

- Real-time transcription using Faster Whisper
- Video file transcription from .mp4, .mov, and other formats
- Automatic session saving to timestamped .txt files
- Optimized performance with voice activity detection
- Modular design for easy customization
- Clean CLI interface with live feedback

## Installation

```bash
# Install dependencies and package using uv
uv sync
uv pip install -e .
```

## Running

After installation, run with:

```bash
# Option 1: Use uv run (no activation needed)
uv run neta

# Option 2: Activate the virtual environment first
source .venv/bin/activate
neta
```

### Real-time Transcription

```bash
# Basic usage (base model)
neta

# Different model size
neta --model tiny     # Fastest, least accurate
neta --model small    # Good balance
neta --model base     # Default, recommended

# Different compute type
neta --compute-type float16  # Higher quality, slower
neta --compute-type int8      # Faster, less accurate (default)
```

### Video File Transcription

```bash
# After installing: neta -i video.mp4 -o transcription.txt
# Or with uv run: uv run neta -i video.mp4 -o transcription.txt

# With different model
neta -i recording.mov -o output.txt --model small

# Full example
neta -i presentation.mp4 -o transcript.txt --model base --compute-type int8
```

Supported video formats: .mp4, .mov, .avi, .mkv, and any format supported by ffmpeg.

## How it works

1. **Starts recording** from your microphone
2. **Processes audio** in real-time chunks with overlap
3. **Transcribes speech** using Faster Whisper
4. **Displays results** live in terminal
5. **Saves session** to timestamped file

## Sessions Directory

Transcriptions are automatically saved to `sessions/` directory:

```
sessions/
├── session_20241217_143052.txt
├── session_20241217_150305.txt
└── ...
```

Each session file contains:
- Session start timestamp
- All transcriptions with timestamps
- Session end timestamp

## File Structure

```
src/neta/
├── __init__.py      # Package initialization
├── transcriber.py   # Core transcription logic
├── session.py       # Session management and file saving
├── config.py        # Configuration settings
└── main.py         # CLI application entry point
```

## Configuration

Edit `src/neta/config.py` to customize:
- Audio settings (sample rate, chunk size)
- Model parameters
- Session file location (`SESSIONS_DIR`)

## Requirements

- Python 3.8+
- Microphone access (for real-time mode)
- PortAudio (usually included with sounddevice)
- ffmpeg (for video transcription mode)
  - macOS: `brew install ffmpeg`
  - Linux: `apt install ffmpeg` or `yum install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Controls

- **Start**: Run the command
- **Stop**: Press `Ctrl+C` or `Enter`
- **View results**: Check the generated session file

## Programmatic Usage

You can also use Neta as a Python library:

```python
from neta import RealTimeTranscriber

# Create transcriber with optional callback
def on_transcription(text):
    print(f"Transcribed: {text}")

transcriber = RealTimeTranscriber(
    model_size="base",      # tiny, small, base, etc.
    compute_type="int8",    # float16, int8, etc.
    callback=on_transcription
)

# Start/stop transcription
transcriber.start_transcription()
# ... transcription runs ...
transcriber.stop_transcription()
```

Available methods:
- `start_transcription()` - Start recording and transcribing
- `pause_transcription()` - Pause transcription (keeps recording)
- `resume_transcription()` - Resume from pause
- `stop_transcription()` - Stop and cleanup
