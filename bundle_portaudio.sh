#!/bin/bash
set -e

# Get PortAudio path from Homebrew
PORTAUDIO_PATH=$(brew --prefix portaudio)

# Create frameworks directory
mkdir -p build/frameworks

# Copy PortAudio library
cp "$PORTAUDIO_PATH/lib/libportaudio.2.dylib" build/frameworks/

# Fix library install name and rpath
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib" build/frameworks/libportaudio.2.dylib

# Make executable
chmod +x build/frameworks/libportaudio.2.dylib

echo "PortAudio library has been bundled successfully"
