"""
Setup script for building the TalkToMe application.
"""
import os
from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns']),
]

# Simplified package configuration
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['rubicon'],  # Minimal required packages
    'includes': [
        'pyaudio',
        'numpy.core.multiarray',
        'whisper'
    ],
    'excludes': ['matplotlib', 'tkinter', 'wx'],
    'frameworks': [],  # Will be populated if PortAudio is found
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

# Add PortAudio framework if available
portaudio_path = os.path.join(os.getcwd(), 'PortAudio.framework')
if os.path.exists(portaudio_path):
    OPTIONS['frameworks'].append(portaudio_path)

setup(
    name='TalkToMe',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
