import sys
import os
import subprocess
from setuptools import setup

sys.setrecursionlimit(5000)

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

def find_portaudio():
    """Find PortAudio library with detailed logging."""
    # Try Homebrew first
    try:
        portaudio_path = subprocess.check_output(['brew', '--prefix', 'portaudio']).decode().strip()
        lib_path = os.path.join(portaudio_path, 'lib', 'libportaudio.2.dylib')
        if os.path.exists(lib_path):
            print(f"Found PortAudio via Homebrew at: {lib_path}")
            return lib_path
    except Exception as e:
        print(f"Homebrew detection failed: {e}")

    # Search common locations
    common_paths = [
        '/usr/local/lib/libportaudio.2.dylib',
        '/opt/local/lib/libportaudio.2.dylib',
        '/usr/lib/libportaudio.2.dylib',
        '/opt/homebrew/lib/libportaudio.2.dylib'
    ]

    for path in common_paths:
        if os.path.exists(path):
            print(f"Found PortAudio at: {path}")
            return path
        else:
            print(f"Checked path (not found): {path}")

    raise ValueError("Could not find PortAudio library in any standard location")

try:
    PORTAUDIO_LIB = find_portaudio()
    print(f"Using PortAudio library at: {PORTAUDIO_LIB}")
except Exception as e:
    print(f"Error finding PortAudio: {e}")
    sys.exit(1)

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch'],
    'includes': ['numpy', 'whisper', 'pyautogui'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'frameworks': [PORTAUDIO_LIB],
    'binary_includes': [PORTAUDIO_LIB],  # Add binary_includes for extra safety
    'strip': True,
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
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'pyaudio',
        'numpy',
        'openai-whisper',
        'pyautogui',
    ],
    name='TalkToMe',
    version='1.0.0',
    description='Voice to text for any application',
    author='Brandon Maddick',
    author_email='',
)
