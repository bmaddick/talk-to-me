"""
Setup script for building the TalkToMe application.
"""
import os
import sys
from setuptools import setup

def get_dylib_path():
    """Get the path to the PortAudio dylib."""
    lib_path = os.path.abspath('lib/libportaudio.2.dylib')
    if not os.path.exists(lib_path):
        raise ValueError(f"PortAudio library not found at {lib_path}")
    return lib_path

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns']),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['pyaudio'],
    'includes': ['numpy', 'torch', 'whisper', 'rubicon.objc'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'frameworks': [get_dylib_path()],
    'strip': True,
    'optimize': 2,
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
