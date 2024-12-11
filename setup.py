import sys
sys.setrecursionlimit(5000)  # Increase recursion limit for py2app

from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])]
OPTIONS = {
    'argv_emulation': False,  # Disable argv emulation for better Mac integration
    'iconfile': 'src/assets/AppIcon.icns',
    'packages': [
        'numpy', 'whisper', 'pyaudio', 'openai_whisper', 'tiktoken', 'torch',
        'regex', 'tqdm', 'more_itertools', 'requests', 'typing_extensions'
    ],
    'includes': [
        'numpy', 'whisper', 'pyaudio', 'pyautogui', 'openai_whisper',
        'tiktoken', 'torch', 'regex', 'tqdm'
    ],
    'excludes': ['matplotlib', 'tkinter', 'PyQt5', 'wx', 'test', 'sphinx', 'sqlalchemy', 'pandas', 'pygame'],
    'frameworks': [
        '@executable_path/../Frameworks/libportaudio.2.dylib',  # Use relative path for final bundle
        '/System/Library/Frameworks/CoreAudio.framework',
        '/System/Library/Frameworks/AudioToolbox.framework',
        '/System/Library/Frameworks/AVFoundation.framework',
        '/System/Library/Frameworks/ApplicationServices.framework'
    ],
    'resources': ['src/assets'],
    'dylib_excludes': ['libgfortran.3.dylib', 'libquadmath.0.dylib', 'libgcc_s.1.dylib'],
    'strip': True,  # Strip debug symbols to reduce size
    'plist': {
        'CFBundleName': 'TalkToMe',
        'CFBundleDisplayName': 'TalkToMe',
        'CFBundleGetInfoString': "Voice to text for any application",
        'CFBundleIdentifier': "com.bmaddick.talktome",
        'CFBundleVersion': "0.1.9",
        'CFBundleShortVersionString': "0.1.9",
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
