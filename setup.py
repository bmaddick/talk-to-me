import sys
import os
import site
import subprocess
from setuptools import setup

sys.setrecursionlimit(5000)

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

# Get PortAudio path from environment or find it
def find_portaudio():
    # First check environment variable
    portaudio_path = os.getenv('PORTAUDIO_PATH')
    if portaudio_path:
        lib_path = os.path.join(portaudio_path, 'lib', 'libportaudio.2.dylib')
        if os.path.exists(lib_path):
            return lib_path

    # Check if we have a local copy in lib/
    local_lib = os.path.join('lib', 'libportaudio.2.dylib')
    if os.path.exists(local_lib):
        return os.path.abspath(local_lib)

    # Try to find it using system paths
    try:
        brew_prefix = subprocess.check_output(['brew', '--prefix', 'portaudio']).decode().strip()
        lib_path = os.path.join(brew_prefix, 'lib', 'libportaudio.2.dylib')
        if os.path.exists(lib_path):
            return lib_path
    except:
        pass

    # Check common locations
    common_paths = [
        '/usr/local/lib/libportaudio.2.dylib',
        '/opt/local/lib/libportaudio.2.dylib',
        '/usr/lib/libportaudio.2.dylib'
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path

    raise ValueError("Could not find PortAudio library")

PORTAUDIO_LIB = find_portaudio()
print(f"Using PortAudio library at: {PORTAUDIO_LIB}")

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch'],
    'includes': ['numpy', 'whisper', 'pyautogui'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'binary_includes': [PORTAUDIO_LIB],  # Include PortAudio binary
    'frameworks': [PORTAUDIO_LIB],  # Also include as framework
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
