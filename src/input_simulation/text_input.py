"""System-wide text input simulation."""
import pyautogui
from typing import Optional

class TextInputSimulator:
    def __init__(self):
        """Initialize the text input simulator."""
        # Ensure PyAutoGUI fails safely
        pyautogui.FAILSAFE = True

    def type_text(self, text: str) -> bool:
        """
        Type the given text at the current cursor position.

        Args:
            text: Text to type

        Returns:
            True if successful, False otherwise
        """
        try:
            pyautogui.typewrite(text)
            return True
        except Exception as e:
            print(f"Text input error: {e}")
            return False

    def press_key(self, key: str) -> bool:
        """
        Press a specific key.

        Args:
            key: Key to press (e.g., 'enter', 'space')

        Returns:
            True if successful, False otherwise
        """
        try:
            pyautogui.press(key)
            return True
        except Exception as e:
            print(f"Key press error: {e}")
            return False
