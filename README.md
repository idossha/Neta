# Neta - Real-Time Voice Transcription

A lightweight, command-line Python application for real-time voice transcription using Faster Whisper.

## Features

- 🎙️ **Real-time transcription** using Faster Whisper
- 💾 **Automatic session saving** to timestamped .txt files
- ⚡ **Optimized performance** with voice activity detection
- 🏗️ **Modular design** for easy customization
- 📝 **Clean CLI interface** with live feedback

## Installation

```bash
# Install from source
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage (base model)
python -m neta

# Different model size
python -m neta --model tiny     # Fastest, least accurate
python -m neta --model small    # Good balance
python -m neta --model base     # Default, recommended

# Different compute type
python -m neta --compute-type float16  # Higher quality, slower
```

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
- Microphone access
- PortAudio (usually included with sounddevice)

## Controls

- **Start**: Run the command
- **Stop**: Press `Ctrl+C` or `Enter`
- **View results**: Check the generated session file
