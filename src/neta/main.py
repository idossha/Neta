"""
Main entry point for Neta transcription application
"""

import argparse
import os
import sys
import subprocess
import tempfile
import numpy as np
from faster_whisper import WhisperModel
from .transcriber import RealTimeTranscriber
from .session import TranscriptionSession


def transcribe_video(input_path, output_path, model_size="base", compute_type="int8"):
    """Transcribe audio from a video file"""

    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            "Error: ffmpeg not found. Please install ffmpeg to use video transcription."
        )
        print("Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)")
        sys.exit(1)

    print(f"Loading model: {model_size}...")
    model = WhisperModel(model_size, device="cpu", compute_type=compute_type)

    print(f"Extracting audio from video: {input_path}...")

    # Create a temporary file for the extracted audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio_path = temp_audio.name

    try:
        # Extract audio using ffmpeg (convert to 16kHz mono WAV)
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_path,
                "-vn",  # No video
                "-acodec",
                "pcm_s16le",  # PCM 16-bit
                "-ar",
                "16000",  # 16kHz sample rate
                "-ac",
                "1",  # Mono
                "-y",  # Overwrite output file
                temp_audio_path,
            ],
            capture_output=True,
            check=True,
        )

        print("Transcribing audio...")

        # Transcribe the audio file
        segments, info = model.transcribe(
            temp_audio_path,
            language="en",
            vad_filter=True,
            vad_parameters=dict(threshold=0.5, min_speech_duration_ms=250),
        )

        # Collect all transcription segments
        transcriptions = []
        for segment in segments:
            if segment.text.strip():
                # Format with timestamps
                start_time = format_timestamp(segment.start)
                end_time = format_timestamp(segment.end)
                transcriptions.append(
                    f"[{start_time} -> {end_time}] {segment.text.strip()}"
                )

        # Write to output file
        with open(output_path, "w") as f:
            f.write(f"Neta Video Transcription\n")
            f.write(f"Source: {input_path}\n")
            f.write(f"Model: {model_size}\n")
            f.write("=" * 50 + "\n\n")
            for line in transcriptions:
                f.write(line + "\n")

        print(f"\nTranscription completed!")
        print(f"Output saved to: {output_path}")
        print(f"Total segments: {len(transcriptions)}")

    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


def format_timestamp(seconds):
    """Format seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Neta - Real-time voice transcription and video transcription",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Real-time mode:
    neta
    neta --model small --compute-type float16

  Video transcription mode:
    neta -i video.mp4 -o transcription.txt
    neta -i recording.mov -o output.txt --model small
        """,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input video file (.mp4, .mov, etc.) for transcription",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output text file for transcription (required with -i)",
    )
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="Whisper model size (default: base)",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        choices=["int8", "float16", "float32"],
        help="Compute type for optimization (default: int8)",
    )

    args = parser.parse_args()

    # Video transcription mode
    if args.input:
        if not args.output:
            parser.error("--output (-o) is required when --input (-i) is specified")
        transcribe_video(args.input, args.output, args.model, args.compute_type)
        return

    # Real-time transcription mode
    # Start new session for saving transcriptions
    session = TranscriptionSession()
    session.start_session()

    def transcription_callback(text):
        print(text)
        session.add_transcription(text)

    # Create and start transcriber
    transcriber = RealTimeTranscriber(
        args.model, args.compute_type, callback=transcription_callback
    )
    transcriber.start_transcription()

    print(f"\nRecording started. Session file: {session.session_file}")
    print("Press Ctrl+C or Enter to stop recording...")

    try:
        input()  # Wait for user input
    except KeyboardInterrupt:
        print("\nStopping recording...")
    finally:
        transcriber.stop_transcription()
        session.end_session()
        print(f"Session saved to: {session.session_file}")


if __name__ == "__main__":
    main()
