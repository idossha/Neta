"""
Real-time transcription functionality using Faster Whisper
"""

import numpy as np
import sounddevice as sd
import queue
import threading
import time

from faster_whisper import WhisperModel
from .config import Config


class RealTimeTranscriber:
    """Handles real-time audio transcription using Faster Whisper"""

    def __init__(self, model_size=Config.DEFAULT_MODEL, compute_type=Config.COMPUTE_TYPE,
                 callback=None):
        self.model = WhisperModel(model_size, device="cpu", compute_type=compute_type)

        # Audio settings
        self.sample_rate = Config.SAMPLE_RATE
        self.chunk_samples = self.sample_rate * Config.CHUNK_DURATION
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.is_paused = False
        self.stream = None
        self.callback = callback

    def audio_callback(self, indata, frames, time_info, status):
        """Audio stream callback"""
        if not self.is_paused:
            self.audio_queue.put(indata.copy())

    def start_transcription(self):
        """Start the transcription process"""
        self.is_running = True
        self.is_paused = False

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=Config.CHANNELS,
            callback=self.audio_callback,
            blocksize=self.sample_rate // 10
        )
        self.stream.start()

        threading.Thread(target=self._transcription_worker, daemon=True).start()

    def pause_transcription(self):
        """Pause transcription"""
        self.is_paused = True

    def resume_transcription(self):
        """Resume transcription"""
        self.is_paused = False

    def stop_transcription(self):
        """Stop transcription and cleanup"""
        self.is_running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def _transcription_worker(self):
        """Background worker for transcription"""
        audio_buffer = []
        overlap_samples = int(self.sample_rate * Config.OVERLAP_DURATION)

        while self.is_running:
            try:
                if not self.is_paused:
                    audio_data = self.audio_queue.get(timeout=0.1)
                    audio_buffer.extend(audio_data.flatten())

                    if len(audio_buffer) >= self.chunk_samples:
                        chunk = np.array(audio_buffer[:self.chunk_samples], dtype=np.float32)
                        audio_buffer = audio_buffer[self.chunk_samples - overlap_samples:]
                        self._transcribe_chunk(chunk)

            except queue.Empty:
                continue

    def _transcribe_chunk(self, audio_chunk):
        """Transcribe a chunk of audio"""
        audio_chunk = audio_chunk / max(np.max(np.abs(audio_chunk)), 1e-8)

        segments, _ = self.model.transcribe(
            audio_chunk,
            language="en",
            vad_filter=True,
            vad_parameters=dict(threshold=0.5, min_speech_duration_ms=250),
            without_timestamps=True
        )

        for segment in segments:
            if segment.text.strip():
                text = segment.text.strip()
                timestamp = time.strftime('%H:%M:%S')
                if self.callback:
                    self.callback(f"[{timestamp}] {text}")
                else:
                    print(f"[{timestamp}] {text}")
