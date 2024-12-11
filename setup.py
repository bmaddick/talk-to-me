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

        # Create lib directory if it doesn't exist
        os.makedirs('lib', exist_ok=True)

        # Copy PortAudio to local lib directory
        local_lib_path = os.path.join('lib', 'libportaudio.2.dylib')
        subprocess.run(['cp', lib_path, local_lib_path], check=True)
        subprocess.run(['chmod', '644', local_lib_path], check=True)

        # Fix library install name
        subprocess.run(['install_name_tool', '-id', '@rpath/libportaudio.2.dylib', local_lib_path], check=True)
        print(f"Configured PortAudio at: {local_lib_path}")

        return local_lib_path
    except Exception as e:
        print(f"Error finding PortAudio: {e}")
        return None

PORTAUDIO_LIB = get_portaudio_path()
if not PORTAUDIO_LIB:
    raise ValueError("PortAudio not found. Install with 'brew install portaudio'")

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png']),
    ('lib', [PORTAUDIO_LIB])  # Bundle PortAudio in lib directory
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
    'dylib_excludes': ['libportaudio.2.dylib.framework'],
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
