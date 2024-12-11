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
    framework_name = 'libportaudio.2.dylib.framework'
    framework_dir = os.path.join(os.getcwd(), 'build', 'frameworks')
    framework_path = os.path.join(framework_dir, framework_name)
    versions_dir = os.path.join(framework_path, 'Versions', 'A')
    lib_path = os.path.join(versions_dir, 'libportaudio.2.dylib')

    # Ensure clean framework directory
    if os.path.exists(framework_path):
        shutil.rmtree(framework_path)

    # Create framework directory structure
    os.makedirs(versions_dir, exist_ok=True)

    # Copy and configure library
    shutil.copy2(portaudio_lib, lib_path)
    os.chmod(lib_path, 0o755)

    # Create framework symlinks
    current_dir = os.getcwd()
    try:
        # Create Versions/Current symlink
        os.chdir(os.path.join(framework_path, 'Versions'))
        if os.path.exists('Current'):
            os.remove('Current')
        os.symlink('A', 'Current')

        # Create framework-level symlink
        os.chdir(framework_path)
        if os.path.exists('libportaudio.2.dylib'):
            os.remove('libportaudio.2.dylib')
        os.symlink('Versions/Current/libportaudio.2.dylib', 'libportaudio.2.dylib')
    finally:
        os.chdir(current_dir)

    # Update install name
    subprocess.run([
        'install_name_tool', '-id',
        '@executable_path/../Frameworks/libportaudio.2.dylib.framework/Versions/A/libportaudio.2.dylib',
        lib_path
    ], check=True)

    print(f"Framework structure created at: {framework_path}")
    subprocess.run(['ls', '-R', framework_path], check=True)
    subprocess.run(['otool', '-L', lib_path], check=True)

    return dict(
        frameworks=[framework_path]
    )
