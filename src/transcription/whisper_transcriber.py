"""Speech recognition module using OpenAI's Whisper."""
import whisper
from typing import Optional
import numpy as np

class WhisperTranscriber:
    def __init__(self, model_name: str = "base"):
        """Initialize Whisper model for transcription."""
        self.model = whisper.load_model(model_name)

    def transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """
        Transcribe audio data to text.

        Args:
            audio_data: Audio data as numpy array

        Returns:
            Transcribed text if successful, None otherwise
        """
        try:
            result = self.model.transcribe(audio_data)
            return result["text"].strip()
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
