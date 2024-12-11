"""
Setup script for building the TalkToMe application.
"""
import os
import sys
from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns']),
]

# Ensure lib directory exists
lib_dir = os.path.join(os.getcwd(), 'lib')
if not os.path.exists(lib_dir):
    print("Error: lib directory not found. Please run prepare_library.sh first.")
    sys.exit(1)

# Check for PortAudio library
portaudio_lib = os.path.join(lib_dir, 'libportaudio.2.dylib')
if not os.path.exists(portaudio_lib):
    print("Error: PortAudio library not found. Please run prepare_library.sh first.")
    sys.exit(1)

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['rubicon'],
    'includes': [
        'pyaudio',
        'numpy.core.multiarray',
        'whisper'
    ],
    'excludes': ['matplotlib', 'tkinter', 'wx'],
    'frameworks': [portaudio_lib],
    'dylib_excludes': ['libportaudio.2.dylib'],  # Exclude system-wide PortAudio
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
