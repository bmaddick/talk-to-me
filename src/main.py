"""Main application entry point."""
import time
from audio.recorder import AudioRecorder
from transcription.whisper_transcriber import WhisperTranscriber
from input_simulation.text_input import TextInputSimulator

def main():
    # Initialize components
    recorder = AudioRecorder()
    transcriber = WhisperTranscriber(model_name="base")
    input_simulator = TextInputSimulator()

    print("Starting Talk To Me...")
    print("Press Ctrl+C to stop")

    try:
        # Start audio stream
        for audio_chunk in recorder.start_stream():
            # Transcribe audio
            text = transcriber.transcribe_audio(audio_chunk)

            # If we got text, simulate typing it
            if text:
                input_simulator.type_text(text)
                input_simulator.press_key('enter')

    except KeyboardInterrupt:
        print("\nStopping Talk To Me...")
    finally:
        recorder.stop_stream()

if __name__ == "__main__":
    main()
