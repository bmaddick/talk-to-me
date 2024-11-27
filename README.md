# Talk To Me

A Mac application that converts voice input to text and types it into any active text field.

## Features
- Voice-to-text conversion using OpenAI's Whisper
- Support for whispering and quiet speech
- System-wide text input in any application
- Real-time audio processing

## Requirements
- macOS 10.13 or later
- Microphone
- Internet connection (for initial installation)

## Installation
### Easy Install (Recommended)
1. Download TalkToMe.app from the latest release
2. Drag TalkToMe.app to your Applications folder
3. Double-click to launch
4. Grant permissions when prompted:
   - Microphone access (required for voice input)
   - Accessibility access (required for typing)

The app will automatically guide you through permission setup on first launch.

### Advanced Installation (For Developers)
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
1. Launch TalkToMe from your Applications folder
2. Click into any text field where you want to type
3. Start speaking (including whispers!)
4. Press Cmd+Q to quit the application

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
The app will automatically request necessary permissions on first launch. If you need to manually adjust permissions:

1. Microphone Access:
   - Open System Settings > Privacy & Security > Microphone
   - Enable TalkToMe

2. Accessibility Access:
   - Open System Settings > Privacy & Security > Accessibility
   - Enable TalkToMe

3. If the app doesn't launch:
   - Right-click TalkToMe.app and select "Open"
   - Click "Open" in the security dialog
