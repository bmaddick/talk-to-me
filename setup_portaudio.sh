#!/bin/bash
set -e

# Create frameworks directory if it doesn't exist
mkdir -p build/frameworks

# Copy PortAudio library from Homebrew
cp /opt/homebrew/opt/portaudio/lib/libportaudio.2.dylib build/frameworks/

# Fix library install name and rpath
install_name_tool -id @executable_path/../Frameworks/libportaudio.2.dylib build/frameworks/libportaudio.2.dylib

# Make the script executable
chmod +x build/frameworks/libportaudio.2.dylib

echo "PortAudio library has been copied and configured."
