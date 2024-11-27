# Talk To Me

A Mac application that converts voice input to text and types it into any active text field.

## Features
- Voice-to-text conversion using OpenAI's Whisper
- Support for whispering and quiet speech
- System-wide text input in any application
- Real-time audio processing

## Requirements
- macOS
- Python 3.8 or higher
- Microphone access

## Installation

1. Install system dependencies:
```bash
brew install portaudio
brew install ffmpeg
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage
(Documentation to be added)

## Development
This project uses:
- OpenAI Whisper for speech recognition
- PyAudio for microphone input
- PyAutoGUI for system-wide text input
- PyObjC for Mac-specific functionality
