import sys
import os
from setuptools import setup

sys.setrecursionlimit(5000)

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

# Get PortAudio path from environment or use default Homebrew location
PORTAUDIO_PATH = os.getenv('PORTAUDIO_PATH', '/opt/homebrew/opt/portaudio')
PORTAUDIO_LIB = os.path.join(PORTAUDIO_PATH, 'lib', 'libportaudio.2.dylib')

if not os.path.exists(PORTAUDIO_LIB):
    print(f"Warning: PortAudio library not found at {PORTAUDIO_LIB}")
    print("Searching in common locations...")
    common_paths = [
        '/usr/local/lib/libportaudio.2.dylib',
        '/opt/local/lib/libportaudio.2.dylib',
        '/usr/lib/libportaudio.2.dylib'
    ]
    for path in common_paths:
        if os.path.exists(path):
            PORTAUDIO_LIB = path
            break
    else:
        raise ValueError("Could not find PortAudio library in any common location")

print(f"Using PortAudio library at: {PORTAUDIO_LIB}")

OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': [
        'numpy', 'whisper', 'pyaudio', 'tiktoken', 'torch',
        'regex', 'tqdm', 'more_itertools', 'requests', 'typing_extensions'
    ],
    'includes': [
        'numpy', 'whisper', 'pyaudio', 'pyautogui',
        'tiktoken', 'torch', 'regex', 'tqdm'
    ],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test', 'sphinx', 'sqlalchemy', 'pandas', 'pygame'],
    'binary_includes': [PORTAUDIO_LIB],  # Directly include PortAudio binary
    'resources': ['src/assets'],
    'frameworks': [],  # Remove frameworks option
    'dylib_excludes': ['libgfortran.3.dylib', 'libquadmath.0.dylib', 'libgcc_s.1.dylib'],
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
