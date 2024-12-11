import sys
import os
import shutil
sys.setrecursionlimit(5000)  # Increase recursion limit for py2app

from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

# Framework configuration
FRAMEWORK_NAME = 'libportaudio.2.dylib.framework'
FRAMEWORK_DIR = os.path.join(os.getcwd(), FRAMEWORK_NAME)
PORTAUDIO_PATH = os.getenv('PORTAUDIO_PATH', '/opt/homebrew/opt/portaudio')
PORTAUDIO_LIB = os.path.join(PORTAUDIO_PATH, 'lib', 'libportaudio.2.dylib')

# Create framework structure
if os.path.exists(PORTAUDIO_LIB):
    # Create framework directory structure
    os.makedirs(os.path.join(FRAMEWORK_DIR, 'Versions', 'A'), exist_ok=True)
    framework_lib = os.path.join(FRAMEWORK_DIR, 'Versions', 'A', 'libportaudio.2.dylib')

    # Copy library and create symlinks
    shutil.copy2(PORTAUDIO_LIB, framework_lib)
    os.chmod(framework_lib, 0o755)

    # Create symbolic links
    if not os.path.exists(os.path.join(FRAMEWORK_DIR, 'Versions', 'Current')):
        os.symlink('A', os.path.join(FRAMEWORK_DIR, 'Versions', 'Current'))
    if not os.path.exists(os.path.join(FRAMEWORK_DIR, 'libportaudio.2.dylib')):
        os.symlink('Versions/Current/libportaudio.2.dylib', os.path.join(FRAMEWORK_DIR, 'libportaudio.2.dylib'))

    print(f"Created framework at: {FRAMEWORK_DIR}")
else:
    print(f"Warning: PortAudio not found at {PORTAUDIO_LIB}")

OPTIONS = {
    'argv_emulation': False,  # Disable argv emulation for better Mac integration
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
    'frameworks': [FRAMEWORK_NAME],
    'resources': ['src/assets'],
    'dylib_excludes': ['libgfortran.3.dylib', 'libquadmath.0.dylib', 'libgcc_s.1.dylib'],
    'strip': True,  # Strip debug symbols to reduce size
    'plist': {
        'CFBundleName': 'TalkToMe',
        'CFBundleDisplayName': 'TalkToMe',
        'CFBundleGetInfoString': "Voice to text for any application",
        'CFBundleIdentifier': "com.bmaddick.talktome",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'LSMinimumSystemVersion': '10.13.0',  # Minimum macOS version
        'NSMicrophoneUsageDescription': 'TalkToMe needs microphone access to convert your speech to text.',
        'NSAppleEventsUsageDescription': 'TalkToMe needs accessibility access to type text in any application.',
        'LSUIElement': True,  # Makes it a background application
        'LSBackgroundOnly': False,
        'NSHighResolutionCapable': True,
        'CFBundleIconFile': 'AppIcon',
        'CFBundleDocumentTypes': [],  # Ensures proper app bundle handling
        'CFBundlePackageType': 'APPL',  # Explicitly mark as application
        'NSRequiresAquaSystemAppearance': True,  # Ensure proper Mac app appearance
        'LSApplicationCategoryType': 'public.app-category.productivity',  # Set app category
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
