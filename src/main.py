"""Main application entry point with Mac permission handling."""
import time
import os
import sys
import logging
import rumps
from audio.recorder import AudioRecorder
from transcription.whisper_transcriber import WhisperTranscriber
from input_simulation.text_input import TextInputSimulator
import subprocess
import platform

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TalkToMeApp(rumps.App):
    def __init__(self):
        super().__init__("TalkToMe", icon='assets/AppIcon.png')
        self.recording = False
        self.recorder = None
        self.transcriber = None
        self.input_simulator = None
        self.menu = ["Start Recording", "Stop Recording", "Check Permissions"]

    @rumps.clicked("Start Recording")
    def start_recording(self, _):
        if not self.recording:
            logger.info("Starting recording...")
            try:
                if not self.recorder:
                    self.recorder = AudioRecorder()
                    self.transcriber = WhisperTranscriber(model_name="base")
                    self.input_simulator = TextInputSimulator()

                self.recording = True
                rumps.notification("TalkToMe", "Recording Started", "Speak to convert to text")

                # Start in a separate thread
                rumps.Timer(self.process_audio, 0.1).start()
            except Exception as e:
                logger.error(f"Failed to start recording: {e}")
                rumps.notification("TalkToMe Error", "Failed to Start", str(e))

    @rumps.clicked("Stop Recording")
    def stop_recording(self, _):
        if self.recording:
            logger.info("Stopping recording...")
            self.recording = False
            if self.recorder:
                self.recorder.stop_stream()
            rumps.notification("TalkToMe", "Recording Stopped", "")

    def process_audio(self, _):
        if self.recording:
            try:
                for audio_chunk in self.recorder.start_stream():
                    if not self.recording:
                        break
                    text = self.transcriber.transcribe_audio(audio_chunk)
                    if text:
                        self.input_simulator.type_text(text)
                        self.input_simulator.press_key('enter')
            except Exception as e:
                logger.error(f"Error processing audio: {e}")
                self.recording = False
                rumps.notification("TalkToMe Error", "Recording Error", str(e))

    @rumps.clicked("Check Permissions")
    def check_permissions(self, _):
        logger.info("Checking permissions...")
        if platform.system() != 'Darwin':
            return True

        try:
            # Check microphone permission
            mic_check = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get microphone access of current application'],
                capture_output=True
            )
            if mic_check.returncode != 0:
                logger.info("Requesting microphone permission...")
                subprocess.run(['tccutil', 'reset', 'Microphone'])
                subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to display dialog "TalkToMe needs microphone access. Please click OK, then allow access in the next prompt."'
                ])

            # Check accessibility permission
            acc_check = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get UI elements enabled'],
                capture_output=True
            )
            if acc_check.returncode != 0:
                logger.info("Requesting accessibility permission...")
                subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to display dialog "TalkToMe needs accessibility access. Please click OK, then allow access in System Settings."'
                ])
                subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'])

            rumps.notification("TalkToMe", "Permissions Check", "Please grant any requested permissions")
        except Exception as e:
            logger.error(f"Error checking permissions: {e}")
            rumps.notification("TalkToMe Error", "Permission Check Failed", str(e))

def main():
    logger.info("Starting TalkToMe menu bar app...")
    TalkToMeApp().run()

if __name__ == "__main__":
    main()
