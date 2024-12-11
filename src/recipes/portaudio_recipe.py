import os
import subprocess
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

    # Create a framework-style bundle for PortAudio
    framework_path = os.path.join(os.getcwd(), 'Frameworks')
    os.makedirs(framework_path, exist_ok=True)
    framework_lib = os.path.join(framework_path, 'libportaudio.2.dylib')

    # Copy and configure the library
    if not os.path.exists(framework_lib):
        subprocess.run(['cp', portaudio_lib, framework_lib], check=True)
        subprocess.run(['chmod', '+x', framework_lib], check=True)
        subprocess.run(['install_name_tool', '-id', '@rpath/libportaudio.2.dylib', framework_lib], check=True)

    return dict(
        frameworks=[framework_lib],
        resources=[framework_lib]
    )
