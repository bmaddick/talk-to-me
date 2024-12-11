"""
Setup script for building the TalkToMe application.
"""
import os
from setuptools import setup

def find_portaudio():
    """Find the PortAudio library."""
    framework_path = os.path.join('lib', 'libportaudio.2.dylib.framework')
    if os.path.exists(framework_path):
        dylib_path = os.path.join(framework_path, 'libportaudio.2.dylib')
        if os.path.exists(dylib_path):
            print(f"Found PortAudio at: {dylib_path}")
            return dylib_path
        version_path = os.path.join(framework_path, 'Versions', 'A', 'libportaudio.2.dylib')
        if os.path.exists(version_path):
            print(f"Found PortAudio at: {version_path}")
            return version_path
    raise ValueError("PortAudio library not found")

PORTAUDIO_LIB = find_portaudio()

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
    'resources': ['src/assets'],
    'strip': True,
    'optimize': 2,
    'frameworks': [PORTAUDIO_LIB],
    'dylib_excludes': [],
    'site_packages': True,
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
