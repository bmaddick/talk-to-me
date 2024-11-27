"""Main application entry point with Mac permission handling."""
import time
import os
import sys
from audio.recorder import AudioRecorder
from transcription.whisper_transcriber import WhisperTranscriber
from input_simulation.text_input import TextInputSimulator
import subprocess
import platform

def check_permissions():
    """Check and request necessary Mac permissions."""
    if platform.system() != 'Darwin':
        return True

    # Check microphone permission
    mic_check = subprocess.run(['osascript', '-e', 'tell application "System Events" to get microphone access of current application'], capture_output=True)
    if mic_check.returncode != 0:
        print("Please grant microphone access when prompted...")
        subprocess.run(['tccutil', 'reset', 'Microphone'])
        subprocess.run(['osascript', '-e', 'tell application "System Events" to display dialog "TalkToMe needs microphone access to convert your speech to text. Please click OK, then allow access in the next prompt."'])

    # Check accessibility permission
    acc_check = subprocess.run(['osascript', '-e', 'tell application "System Events" to get UI elements enabled'], capture_output=True)
    if acc_check.returncode != 0:
        print("Please grant accessibility access when prompted...")
        subprocess.run(['osascript', '-e', 'tell application "System Events" to display dialog "TalkToMe needs accessibility access to type text in your applications. Please click OK, then allow access in System Settings."'])
        subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'])

def main():
    print("Starting Talk To Me...")
    print("Checking permissions...")
    check_permissions()

    # Initialize components
    recorder = AudioRecorder()
    transcriber = WhisperTranscriber(model_name="base")
    input_simulator = TextInputSimulator()

    print("Ready to convert speech to text!")
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
