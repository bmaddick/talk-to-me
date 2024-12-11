#!/bin/bash
set -e

echo "Starting frameworks preparation..."

# Get PortAudio path from Homebrew
PORTAUDIO_PATH=$(brew --prefix portaudio)
echo "PortAudio path: $PORTAUDIO_PATH"

# Create frameworks directory structure
mkdir -p Frameworks
echo "Created Frameworks directory"

# Copy PortAudio library with proper structure
cp "$PORTAUDIO_PATH/lib/libportaudio.2.dylib" Frameworks/
echo "Copied PortAudio library to Frameworks/"

# Fix library install name
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib" Frameworks/libportaudio.2.dylib
echo "Fixed library install name"

# Make executable
chmod +x Frameworks/libportaudio.2.dylib
echo "Made library executable"

# Verify library
ls -l Frameworks/libportaudio.2.dylib
otool -L Frameworks/libportaudio.2.dylib

echo "Framework preparation completed successfully"
