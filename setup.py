import sys
import os
import subprocess
from setuptools import setup

sys.setrecursionlimit(5000)

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

def get_portaudio_lib():
    """Get PortAudio library path with fallbacks."""
    try:
        # Try to get from environment first
        if 'PORTAUDIO_LIB' in os.environ:
            lib_path = os.environ['PORTAUDIO_LIB']
            if os.path.exists(lib_path):
                return lib_path

        # Try Homebrew
        brew_prefix = subprocess.check_output(['brew', '--prefix', 'portaudio']).decode().strip()
        lib_path = os.path.join(brew_prefix, 'lib', 'libportaudio.2.dylib')
        if os.path.exists(lib_path):
            return lib_path
    except:
        pass

    # Check common locations
    common_paths = [
        '/usr/local/lib/libportaudio.2.dylib',
        '/opt/homebrew/lib/libportaudio.2.dylib',
        '/usr/lib/libportaudio.2.dylib'
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path

    return None

PORTAUDIO_LIB = get_portaudio_lib()
if not PORTAUDIO_LIB:
    print("Warning: PortAudio library not found. Build may fail.")
else:
    print(f"Found PortAudio library at: {PORTAUDIO_LIB}")

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch'],
    'includes': ['numpy', 'whisper', 'pyautogui'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'frameworks': [PORTAUDIO_LIB] if PORTAUDIO_LIB else [],
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
