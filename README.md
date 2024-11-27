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

2. Clone the repository:
```bash
git clone https://github.com/bmaddick/talk-to-me.git
cd talk-to-me
```

3. Install Python dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Run the application:
```bash
python src/main.py
```

3. Click into any text field where you want to type
4. Start speaking (including whispers!)
5. Press Ctrl+C to stop the application

## Development
This project uses:
- OpenAI Whisper for speech recognition (optimized for quiet speech)
- PyAudio for microphone input
- PyAutoGUI for system-wide text input
- PyObjC for Mac-specific functionality

## How It Works
1. The application continuously captures audio from your microphone
2. Audio chunks are processed in real-time using OpenAI's Whisper model
3. Recognized text is automatically typed into the currently focused text field
4. Whisper's base model is optimized for various speech volumes, including whispers

## Troubleshooting
If you encounter permission issues:
1. Ensure microphone access is granted in System Preferences > Security & Privacy > Privacy > Microphone
2. Allow accessibility access for terminal/IDE in System Preferences > Security & Privacy > Privacy > Accessibility
