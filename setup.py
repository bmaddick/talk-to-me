import sys
import os
import shutil
from setuptools import setup
from setuptools.command.build_py import build_py
sys.setrecursionlimit(5000)  # Increase recursion limit for py2app

class CustomBuildPy(build_py):
    def run(self):
        # Run the standard build
        build_py.run(self)

        # Copy PortAudio library to the build directory
        portaudio_lib = os.path.join(os.getenv('PORTAUDIO_PATH', '/opt/homebrew/opt/portaudio'), 'lib', 'libportaudio.2.dylib')
        if not os.path.exists(portaudio_lib):
            raise ValueError(f"PortAudio library not found at {portaudio_lib}")

        # Create Frameworks directory in build
        frameworks_dir = os.path.join('build', 'TalkToMe.app', 'Contents', 'Frameworks')
        os.makedirs(frameworks_dir, exist_ok=True)

        # Copy library and fix its install name
        dest_lib = os.path.join(frameworks_dir, 'libportaudio.2.dylib')
        shutil.copy2(portaudio_lib, dest_lib)
        os.chmod(dest_lib, 0o755)
        os.system(f'install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib" "{dest_lib}"')
        print(f"Copied PortAudio library to: {dest_lib}")

APP = ['src/main.py']
DATA_FILES = [
    ('assets', ['src/assets/AppIcon.icns', 'src/assets/background.png'])
]

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
    cmdclass={'build_py': CustomBuildPy},
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
