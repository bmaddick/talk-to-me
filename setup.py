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
    """Get PortAudio library path with comprehensive fallback strategy."""
    # Try environment variable first
    if 'PORTAUDIO_LIB' in os.environ:
        lib_path = os.environ['PORTAUDIO_LIB']
        if os.path.exists(lib_path):
            print(f"Found PortAudio from environment: {lib_path}")
            return lib_path

    # Try Homebrew with explicit error handling
    try:
        brew_prefix = subprocess.check_output(['brew', '--prefix', 'portaudio']).decode().strip()
        lib_path = os.path.join(brew_prefix, 'lib', 'libportaudio.2.dylib')
        if os.path.exists(lib_path):
            print(f"Found PortAudio from Homebrew: {lib_path}")
            return lib_path
    except subprocess.CalledProcessError as e:
        print(f"Homebrew check failed: {e}")
    except Exception as e:
        print(f"Error checking Homebrew: {e}")

    # Check common locations with detailed logging
    common_paths = [
        '/usr/local/lib/libportaudio.2.dylib',
        '/opt/homebrew/lib/libportaudio.2.dylib',
        '/usr/lib/libportaudio.2.dylib',
        os.path.expanduser('~/Frameworks/libportaudio.2.dylib')
    ]
    for path in common_paths:
        if os.path.exists(path):
            print(f"Found PortAudio at common location: {path}")
            return path
        else:
            print(f"Checked location (not found): {path}")

    print("ERROR: PortAudio library not found in any expected location")
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
    'resources': ['src/assets', 'src/recipes'],
    'dylib_excludes': ['libportaudio.2.dylib'],  # Exclude from automatic detection
    'frameworks': [portaudio_path],  # Add explicitly
    'strip': True,
    'recipes': ['src/recipes'],
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
