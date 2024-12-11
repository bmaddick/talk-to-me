import sys
import os
import subprocess
from setuptools import setup

sys.setrecursionlimit(5000)

def get_portaudio_lib():
    try:
        result = subprocess.run(['brew', '--prefix', 'portaudio'],
                              capture_output=True, text=True, check=True)
        return os.path.join(result.stdout.strip(), 'lib', 'libportaudio.2.dylib')
    except:
        return None

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

portaudio_lib = get_portaudio_lib()
if not portaudio_lib or not os.path.exists(portaudio_lib):
    raise ValueError(f"PortAudio library not found at expected location: {portaudio_lib}")

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch'],
    'includes': ['numpy', 'whisper', 'pyautogui', 'pyaudio._portaudio'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'strip': True,
    'frameworks': [portaudio_lib],
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
