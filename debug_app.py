"""Debug script to help diagnose app launch and permission issues."""
import os
import sys
import logging
import subprocess
import platform

# Configure debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_app_process():
    """Check if the app process is running."""
    try:
        result = subprocess.run(['pgrep', '-f', 'TalkToMe'], capture_output=True, text=True)
        if result.stdout:
            logger.info(f"App processes found: {result.stdout}")
        else:
            logger.warning("No app processes found")
    except Exception as e:
        logger.error(f"Error checking process: {e}")

def check_menu_extras():
    """Check menu extras status on macOS."""
    if platform.system() != 'Darwin':
        return

    try:
        result = subprocess.run([
            'osascript',
            '-e',
            'tell application "System Events" to get every process whose name contains "TalkToMe"'
        ], capture_output=True, text=True)
        logger.info(f"Menu extras check result: {result.stdout}")
    except Exception as e:
        logger.error(f"Error checking menu extras: {e}")

def check_permissions():
    """Check current permission status."""
    if platform.system() != 'Darwin':
        return

    try:
        # Check microphone
        mic_result = subprocess.run([
            'osascript',
            '-e',
            'tell application "System Events" to get microphone access of current application'
        ], capture_output=True, text=True)
        logger.info(f"Microphone permission status: {mic_result.stdout}")

        # Check accessibility
        acc_result = subprocess.run([
            'osascript',
            '-e',
            'tell application "System Events" to get UI elements enabled'
        ], capture_output=True, text=True)
        logger.info(f"Accessibility permission status: {acc_result.stdout}")
    except Exception as e:
        logger.error(f"Error checking permissions: {e}")

def main():
    """Run all debug checks."""
    logger.info("Starting debug checks...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Working directory: {os.getcwd()}")

    check_app_process()
    check_menu_extras()
    check_permissions()

    logger.info("Debug checks completed")

if __name__ == "__main__":
    main()
