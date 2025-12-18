"""
Main entry point for Neta transcription application
"""

import argparse
from .transcriber import RealTimeTranscriber
from .session import TranscriptionSession


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Neta - Real-time voice transcription")
    parser.add_argument("--model", default="base",
                       choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--compute-type", default="int8",
                       choices=["int8", "float16", "float32"],
                       help="Compute type for optimization (default: int8)")

    args = parser.parse_args()

    # Start new session for saving transcriptions
    session = TranscriptionSession()
    session.start_session()

    def transcription_callback(text):
        print(text)
        session.add_transcription(text)

    # Create and start transcriber
    transcriber = RealTimeTranscriber(args.model, args.compute_type, callback=transcription_callback)
    transcriber.start_transcription()

    print(f"\n🎙️  Recording started. Session file: {session.session_file}")
    print("💡 Press Ctrl+C or Enter to stop recording...")

    try:
        input()  # Wait for user input
    except KeyboardInterrupt:
        print("\n⏹️  Stopping recording...")
    finally:
        transcriber.stop_transcription()
        session.end_session()
        print(f"✅ Session saved to: {session.session_file}")


if __name__ == "__main__":
    main()
