import sys
sys.setrecursionlimit(5000)  # Increase recursion limit for py2app

from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])]
OPTIONS = {
    'argv_emulation': False,  # Disable argv emulation for better Mac integration
    'iconfile': 'src/assets/AppIcon.icns',
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
