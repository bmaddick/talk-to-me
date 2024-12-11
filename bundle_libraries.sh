#!/bin/bash
set -e

echo "Starting library bundling process..."

# Get PortAudio path from Homebrew
PORTAUDIO_PATH=$(brew --prefix portaudio)
echo "PortAudio path: $PORTAUDIO_PATH"

# Create frameworks directory
mkdir -p build/frameworks
echo "Created frameworks directory"

# Copy PortAudio library
cp "$PORTAUDIO_PATH/lib/libportaudio.2.dylib" build/frameworks/
echo "Copied PortAudio library to build/frameworks"

# Fix library install name and rpath
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib" build/frameworks/libportaudio.2.dylib
echo "Fixed library install name"

# Make executable
chmod +x build/frameworks/libportaudio.2.dylib
echo "Made library executable"

# Verify library exists and check its dependencies
ls -l build/frameworks/libportaudio.2.dylib
otool -L build/frameworks/libportaudio.2.dylib

echo "Library bundling completed successfully"
