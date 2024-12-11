"""
Setup script for building the TalkToMe application.
"""
import os
from setuptools import setup

def find_portaudio():
    """Find the PortAudio library."""
    portaudio_path = os.path.join('lib', 'libportaudio.2.dylib')
    if os.path.exists(portaudio_path):
        print(f"Found PortAudio at: {portaudio_path}")
        return portaudio_path
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
    'packages': [
        'numpy',
        'whisper',
        'pyaudio',
        'tiktoken',
        'torch',
        'rubicon_objc',
        'Foundation',
        'AppKit'
    ],
    'includes': [
        'numpy',
        'whisper',
        'pyautogui',
        'rubicon_objc',
        'Foundation',
        'AppKit'
    ],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'strip': True,
    'site_packages': True,
    'plist': {
        'CFBundleName': 'TalkToMe',
        'CFBundleDisplayName': 'TalkToMe',
        'CFBundleGetInfoString': "Voice to text for any application",
        'CFBundleIdentifier': "com.bmaddick.talktome",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'LSMinimumSystemVersion': '10.13.0',
        'NSMicrophoneUsageDescription': 'TalkToMe needs microphone access to convert your speech to text.',
        'NSAppleEventsUsageDescription': 'TalkToMe needs accessibility access to type text in any application.',
        'LSUIElement': True,
        'LSBackgroundOnly': False,
        'NSHighResolutionCapable': True,
        'CFBundleIconFile': 'AppIcon',
        'CFBundleDocumentTypes': [],
        'CFBundlePackageType': 'APPL',
        'NSRequiresAquaSystemAppearance': True,
        'LSApplicationCategoryType': 'public.app-category.productivity',
    }
}

setup(
    app=APP,
    name='TalkToMe',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'pyaudio',
        'numpy',
        'openai-whisper',
        'pyautogui',
        'rubicon-objc>=0.4.7',
        'py2app>=0.28.6'
    ],
    version='1.0.0',
    description='Voice to text for any application',
    author='Brandon Maddick',
    author_email='',
)
