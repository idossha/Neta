"""
Transcription session management and file saving
"""

import os
from datetime import datetime
from .config import Config


class TranscriptionSession:
    """Manages a transcription session and saves to file"""

    def __init__(self):
        self.transcriptions = []
        self.is_active = False
        self.session_file = None

        # Create sessions directory if it doesn't exist
        os.makedirs(Config.SESSIONS_DIR, exist_ok=True)

    def start_session(self):
        """Start a new transcription session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = os.path.join(Config.SESSIONS_DIR, f"session_{timestamp}.txt")
        self.transcriptions = []
        self.is_active = True

        # Write session header
        with open(self.session_file, 'w') as f:
            f.write(f"Neta Transcription Session\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

    def add_transcription(self, text):
        """Add a transcription line to the session"""
        if self.is_active:
            self.transcriptions.append(text)

            # Append to file immediately
            with open(self.session_file, 'a') as f:
                f.write(text + "\n")

    def pause_session(self):
        """Pause the current session"""
        if self.is_active:
            self.add_transcription(f"\n[PAUSED: {datetime.now().strftime('%H:%M:%S')}]\n")

    def resume_session(self):
        """Resume the current session"""
        if self.is_active:
            self.add_transcription(f"\n[RESUMED: {datetime.now().strftime('%H:%M:%S')}]\n")

    def end_session(self):
        """End the current session"""
        if self.is_active:
            self.add_transcription(f"\n[ENDED: {datetime.now().strftime('%H:%M:%S')}]\n")
            self.is_active = False

    def get_session_info(self):
        """Get information about the current session"""
        if self.session_file:
            return {
                'file': self.session_file,
                'line_count': len(self.transcriptions),
                'active': self.is_active
            }
        return None
