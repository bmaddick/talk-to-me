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

# Configure logging with file output
log_file = os.path.expanduser('~/Library/Logs/TalkToMe/app.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TalkToMeApp(rumps.App):
    def __init__(self):
        # Ensure icon path is absolute
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'AppIcon.png')
        logger.debug(f"Using icon path: {icon_path}")

        super().__init__("TalkToMe", icon=icon_path, quit_button=None)
        self.recording = False
        self.recorder = None
        self.transcriber = None
        self.input_simulator = None
        self.menu = ["Start Recording", "Stop Recording", "Check Permissions", None, "Quit"]

        # Verify app visibility on startup
        self.verify_visibility()
        # Initial permission check on startup
        self.check_permissions(None)

    def verify_visibility(self):
        """Verify the app is visible in the menu bar."""
        logger.debug("Verifying menu bar visibility...")
        try:
            # Force menu bar update
            self.menu.update()
            # Check if app is visible
            result = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get every process whose name contains "TalkToMe"'],
                capture_output=True,
                text=True
            )
            if "TalkToMe" not in result.stdout:
                logger.warning("App not visible in menu bar, attempting to refresh...")
                # Try to force app to front
                subprocess.run(['osascript', '-e', 'tell application "TalkToMe" to activate'])
                time.sleep(1)  # Give system time to update
                self.menu.update()
        except Exception as e:
            logger.error(f"Error verifying visibility: {e}")
            # Try to recover visibility
            self.menu = self.menu  # Force menu rebuild

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
            permissions_granted = True

            # Check microphone permission
            mic_check = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get microphone access of current application'],
                capture_output=True,
                text=True
            )
            if mic_check.returncode != 0:
                permissions_granted = False
                logger.info("Requesting microphone permission...")
                subprocess.run(['tccutil', 'reset', 'Microphone'], check=True)
                subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to display dialog "TalkToMe needs microphone access. Please click OK, then allow access in System Settings. After granting permission, please restart the app." buttons {"Open Settings", "Cancel"} default button "Open Settings"'
                ], check=True)
                subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone'])

            # Check accessibility permission
            acc_check = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get UI elements enabled'],
                capture_output=True,
                text=True
            )
            if acc_check.returncode != 0:
                permissions_granted = False
                logger.info("Requesting accessibility permission...")
                subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to display dialog "TalkToMe needs accessibility access. Please click OK, then allow access in System Settings. After granting permission, please restart the app." buttons {"Open Settings", "Cancel"} default button "Open Settings"'
                ], check=True)
                subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'])

            # If permissions were just granted, suggest restart
            if not permissions_granted:
                rumps.notification("TalkToMe", "Restart Required", "Please restart the app after granting permissions")
                logger.info("Permissions changed - restart recommended")
            else:
                # Verify visibility after confirming permissions
                self.verify_visibility()
                rumps.notification("TalkToMe", "Permissions Check", "All permissions are properly configured")

        except Exception as e:
            logger.error(f"Error checking permissions: {e}")
            rumps.notification("TalkToMe Error", "Permission Check Failed", str(e))

    @rumps.clicked("Quit")
    def quit_app(self, _):
        """Properly clean up and quit the app."""
        logger.info("Quitting application...")
        if self.recording:
            self.stop_recording(None)
        rumps.quit_application()

def main():
    logger.info("Starting TalkToMe menu bar app...")
    try:
        app = TalkToMeApp()
        # Initial permission check
        app.check_permissions(None)
        app.run()
    except Exception as e:
        logger.error(f"Failed to start app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
