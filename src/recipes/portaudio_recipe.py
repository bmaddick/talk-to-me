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

        return None

    portaudio_lib = get_lib_path()
    if not portaudio_lib:
        print("Warning: PortAudio library not found")
        return None

    print(f"Using PortAudio library: {portaudio_lib}")

    # Create simple library directory structure
    lib_dir = os.path.join(os.getcwd(), 'lib')
    lib_path = os.path.join(lib_dir, 'libportaudio.2.dylib')
    os.makedirs(lib_dir, exist_ok=True)

    # Copy library to lib directory
    if not os.path.exists(lib_path):
        shutil.copy2(portaudio_lib, lib_path)
        os.chmod(lib_path, 0o755)
        subprocess.run([
            'install_name_tool', '-id',
            '@executable_path/../lib/libportaudio.2.dylib',
            lib_path
        ], check=True)

    print(f"Library created at: {lib_path}")
    subprocess.run(['otool', '-L', lib_path], check=True)

    # Return the library path for py2app to handle
    return dict(
        dylibs=[lib_path]
    )
