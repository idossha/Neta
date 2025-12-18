"""
Configuration settings for Neta
"""

class Config:
    # Audio settings
    SAMPLE_RATE = 16000
    CHANNELS = 1
    CHUNK_DURATION = 3  # seconds
    OVERLAP_DURATION = 0.5  # seconds

    # Model settings
    DEFAULT_MODEL = "base"
    COMPUTE_TYPE = "int8"

    # UI settings
    WINDOW_TITLE = "Neta - Real-time Transcription"
    WINDOW_SIZE = "400x300"

    # Session settings
    SESSIONS_DIR = "sessions"
