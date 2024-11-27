"""Audio recording module using PyAudio."""
import pyaudio
import wave
import numpy as np
from typing import Generator, Optional

class AudioRecorder:
    def __init__(self,
                 rate: int = 16000,
                 chunk_size: int = 1024,
                 channels: int = 1,
                 format_type: int = pyaudio.paFloat32):
        self.rate = rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.format = format_type
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None

    def start_stream(self) -> Generator[np.ndarray, None, None]:
        """Start recording audio in chunks."""
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        try:
            while True:
                data = np.frombuffer(
                    self.stream.read(self.chunk_size),
                    dtype=np.float32
                )
                yield data
        except KeyboardInterrupt:
            self.stop_stream()

    def stop_stream(self):
        """Stop and clean up the audio stream."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.stream = None

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_stream()
        self.audio.terminate()
