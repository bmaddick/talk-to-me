#!/bin/bash
set -e

echo "Starting library bundling process..."

# Get PortAudio path from Homebrew
PORTAUDIO_PATH=$(brew --prefix portaudio)
echo "PortAudio path: $PORTAUDIO_PATH"

# Create lib directory structure
mkdir -p lib
echo "Created lib directory"

# Copy PortAudio library
cp "$PORTAUDIO_PATH/lib/libportaudio.2.dylib" lib/
echo "Copied PortAudio library to lib/"

# Fix library install name and rpath
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib" lib/libportaudio.2.dylib
echo "Fixed library install name"

# Make executable
chmod +x lib/libportaudio.2.dylib
echo "Made library executable"

# Verify library exists and check its dependencies
ls -l lib/libportaudio.2.dylib
otool -L lib/libportaudio.2.dylib

echo "Library bundling completed successfully"
