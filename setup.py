"""
Setup script for building the TalkToMe application.
"""
import os
from setuptools import setup

def find_portaudio():
    """Find the PortAudio library."""
    possible_paths = [
        os.path.join('lib', 'libportaudio.2.dylib'),
        os.path.join('lib', 'libportaudio.2.dylib.framework', 'Versions', 'A', 'libportaudio.2.dylib')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found PortAudio at: {path}")
            return path
    raise ValueError("PortAudio library not found")

PORTAUDIO_LIB = find_portaudio()

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns']),
    ('lib', [PORTAUDIO_LIB]),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['pyaudio'],
    'includes': ['numpy', 'torch', 'whisper', 'rubicon.objc'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'strip': True,
    'optimize': 2,
    'frameworks': ['lib/libportaudio.2.dylib'],
    'dylib_excludes': [],
    'plist': {
        'CFBundleName': 'TalkToMe',
        'CFBundleDisplayName': 'TalkToMe',
        'CFBundleIdentifier': 'com.bmaddick.talktome',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.10.0',
        'NSMicrophoneUsageDescription': 'TalkToMe needs access to your microphone for voice input.',
        'NSAppleEventsUsageDescription': 'TalkToMe needs to control other applications to input text.',
        'LSApplicationCategoryType': 'public.app-category.productivity',
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
