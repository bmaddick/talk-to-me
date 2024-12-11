import sys
import os
import subprocess
from setuptools import setup

sys.setrecursionlimit(5000)

def get_portaudio_path():
    try:
        result = subprocess.run(['brew', '--prefix', 'portaudio'],
                              capture_output=True, text=True, check=True)
        prefix = result.stdout.strip()
        lib_path = os.path.join(prefix, 'lib', 'libportaudio.2.dylib')
        if not os.path.exists(lib_path):
            raise ValueError(f"PortAudio library not found at {lib_path}")
        print(f"Found PortAudio at: {lib_path}")
        return lib_path
    except Exception as e:
        print(f"Error finding PortAudio: {e}")
        return None

PORTAUDIO_LIB = get_portaudio_path()
if not PORTAUDIO_LIB:
    raise ValueError("PortAudio not found. Install with 'brew install portaudio'")

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch'],
    'includes': ['numpy', 'whisper', 'pyautogui'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'frameworks': [PORTAUDIO_LIB],
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
    name='TalkToMe',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'pyaudio',
        'numpy',
        'openai-whisper',
        'pyautogui',
    ],
    version='1.0.0',
    description='Voice to text for any application',
    author='Brandon Maddick',
    author_email='',
)
