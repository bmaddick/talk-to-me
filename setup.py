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

# Framework configuration
PORTAUDIO_FRAMEWORK = 'PortAudio.framework'

# Minimal package configuration to avoid recursion
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'includes': [
        'numpy.core.multiarray',  # Explicit numpy import
        'torch.nn',  # Minimal torch import
        'whisper',
        'rubicon.objc',
        'pyaudio'
    ],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'strip': True,
    'optimize': 2,
    'frameworks': [PORTAUDIO_FRAMEWORK] if os.path.exists(PORTAUDIO_FRAMEWORK) else [],
    'plist': {
        'CFBundleName': 'TalkToMe',
        'CFBundleDisplayName': 'TalkToMe',
        'CFBundleIdentifier': 'com.bmaddick.talktome',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.12.0',
        'NSMicrophoneUsageDescription': 'TalkToMe needs microphone access to convert speech to text.',
        'NSAppleEventsUsageDescription': 'TalkToMe needs to control other applications to input text.',
        'LSUIElement': True,
    }
}

setup(
    name='TalkToMe',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
