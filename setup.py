"""
Setup script for building the TalkToMe application.
"""
import os
import sys
from setuptools import setup

# Check for PortAudio library
lib_dir = os.path.join(os.getcwd(), 'lib')
portaudio_lib = os.path.join(lib_dir, 'libportaudio.2.dylib')
if not os.path.exists(portaudio_lib):
    print("Error: PortAudio library not found in lib directory")
    sys.exit(1)

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns']),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'includes': ['pyaudio', 'numpy.core.multiarray', 'whisper'],
    'packages': [],  # Minimize package inclusions
    'excludes': ['matplotlib', 'tkinter', 'wx', 'PIL'],
    'frameworks': [portaudio_lib],  # Use frameworks instead of resources
    'plist': {
        'CFBundleName': 'TalkToMe',
        'CFBundleDisplayName': 'TalkToMe',
        'CFBundleIdentifier': 'com.bmaddick.talktome',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.15.0',
        'NSMicrophoneUsageDescription': 'TalkToMe needs microphone access to convert speech to text.',
        'NSRequiresAquaSystemAppearance': False,
    }
}

setup(
    name='TalkToMe',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
