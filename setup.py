import sys
import os
import subprocess
from setuptools import setup

sys.setrecursionlimit(5000)

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

def get_portaudio_path():
    """Get PortAudio library path."""
    # Check environment variable first
    if 'PORTAUDIO_LIB' in os.environ:
        return os.environ['PORTAUDIO_LIB']

    # Try Homebrew
    try:
        brew_prefix = subprocess.check_output(['brew', '--prefix', 'portaudio']).decode().strip()
        return os.path.join(brew_prefix, 'lib', 'libportaudio.2.dylib')
    except:
        pass

    # Check common locations
    common_paths = [
        '/usr/local/lib/libportaudio.2.dylib',
        '/opt/homebrew/lib/libportaudio.2.dylib',
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None

portaudio_path = get_portaudio_path()
if not portaudio_path:
    print("Error: PortAudio library not found. Please install PortAudio using 'brew install portaudio'")
    sys.exit(1)

print(f"Using PortAudio from: {portaudio_path}")

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch'],
    'includes': ['numpy', 'whisper', 'pyautogui'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'frameworks': [portaudio_path],
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
