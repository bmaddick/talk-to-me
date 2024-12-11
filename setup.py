import sys
import os
import subprocess
import shutil
from setuptools import setup

sys.setrecursionlimit(5000)

# Get PortAudio library path and copy to a known location
try:
    portaudio_lib = subprocess.check_output(['brew', '--prefix', 'portaudio']).decode().strip()
    source_lib = os.path.join(portaudio_lib, 'lib', 'libportaudio.2.dylib')
    lib_dir = os.path.join(os.getcwd(), 'lib')
    os.makedirs(lib_dir, exist_ok=True)
    dest_lib = os.path.join(lib_dir, 'libportaudio.2.dylib')
    if os.path.exists(source_lib):
        shutil.copy2(source_lib, dest_lib)
        os.chmod(dest_lib, 0o755)
    portaudio_lib = dest_lib
except Exception as e:
    print(f"Warning: Error copying PortAudio library: {e}")
    portaudio_lib = '/usr/local/lib/libportaudio.2.dylib'

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png']),
    ('lib', [portaudio_lib])
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': ['numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch'],
    'includes': ['numpy', 'whisper', 'pyautogui'],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test'],
    'resources': ['src/assets'],
    'strip': True,
    'frameworks': [],
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
