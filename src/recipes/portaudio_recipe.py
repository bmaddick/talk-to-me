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

    # Create a proper framework bundle structure
    framework_dir = os.path.join(os.getcwd(), 'build', 'frameworks')
    framework_name = 'libportaudio.2.dylib.framework'
    framework_path = os.path.join(framework_dir, framework_name)
    versions_dir = os.path.join(framework_path, 'Versions', 'A')
    lib_path = os.path.join(versions_dir, 'libportaudio.2.dylib')

    # Create the framework directory structure
    os.makedirs(versions_dir, exist_ok=True)

    # Copy the library to the framework
    if not os.path.exists(lib_path):
        subprocess.run(['cp', portaudio_lib, lib_path], check=True)
        subprocess.run(['chmod', '+x', lib_path], check=True)

        # Create symlinks
        os.symlink('A', os.path.join(framework_path, 'Versions', 'Current'))
        os.symlink(
            os.path.join('Versions', 'Current', 'libportaudio.2.dylib'),
            os.path.join(framework_path, 'libportaudio.2.dylib')
        )

        # Update install names
        subprocess.run([
            'install_name_tool', '-id',
            '@executable_path/../Frameworks/libportaudio.2.dylib.framework/Versions/A/libportaudio.2.dylib',
            lib_path
        ], check=True)

    return dict(
        frameworks=[framework_path],
        resources=[framework_path]
    )
