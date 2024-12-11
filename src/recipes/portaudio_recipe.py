import os
import subprocess
import shutil
from typing import Dict, Any

def check(cmd, mf):
    """Custom py2app recipe for handling PortAudio library."""
    m = mf.findNode('pyaudio')
    if m is None:
        return None

    def get_lib_path():
        # Try environment variable first
        if 'PORTAUDIO_LIB' in os.environ:
            lib_path = os.environ['PORTAUDIO_LIB']
            if os.path.exists(lib_path):
                print(f"Found PortAudio from environment: {lib_path}")
                return lib_path

        # Try Homebrew
        try:
            brew_prefix = subprocess.check_output(['brew', '--prefix', 'portaudio']).decode().strip()
            lib_path = os.path.join(brew_prefix, 'lib', 'libportaudio.2.dylib')
            if os.path.exists(lib_path):
                print(f"Found PortAudio from Homebrew: {lib_path}")
                return lib_path
        except:
            pass

        # Check common locations
        common_paths = [
            '/usr/local/lib/libportaudio.2.dylib',
            '/opt/homebrew/lib/libportaudio.2.dylib',
            '/usr/lib/libportaudio.2.dylib'
        ]
        for path in common_paths:
            if os.path.exists(path):
                print(f"Found PortAudio at: {path}")
                return path
        return None

    portaudio_lib = get_lib_path()
    if not portaudio_lib:
        print("Warning: PortAudio library not found")
        return None

    print(f"Using PortAudio library: {portaudio_lib}")

    # Create framework structure that py2app expects
    framework_name = 'libportaudio.2.dylib'
    framework_dir = os.path.join(os.getcwd(), 'build', 'frameworks')
    framework_path = os.path.join(framework_dir, framework_name)
    os.makedirs(framework_dir, exist_ok=True)

    # Copy library directly to frameworks directory
    if not os.path.exists(framework_path):
        shutil.copy2(portaudio_lib, framework_path)
        os.chmod(framework_path, 0o755)
        subprocess.run([
            'install_name_tool', '-id',
            '@executable_path/../Frameworks/libportaudio.2.dylib',
            framework_path
        ], check=True)

    print(f"Framework library created at: {framework_path}")
    subprocess.run(['otool', '-L', framework_path], check=True)

    # Return the library path for py2app to handle
    return dict(
        frameworks=[framework_path]
    )
