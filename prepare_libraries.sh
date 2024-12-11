#!/bin/bash
set -e

echo "Starting library preparation..."

# Get PortAudio path
PORTAUDIO_PREFIX=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PREFIX/lib/libportaudio.2.dylib"

# Create directories
mkdir -p build/lib
mkdir -p dist/TalkToMe.app/Contents/Frameworks

# Copy library to build directory
echo "Copying PortAudio library..."
cp "$PORTAUDIO_LIB" build/lib/
chmod +x build/lib/libportaudio.2.dylib

# Fix library install name
echo "Fixing library install names..."
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib" build/lib/libportaudio.2.dylib

# Create symlink in the expected framework location
echo "Creating framework structure..."
mkdir -p build/libportaudio.2.dylib.framework/Versions/A
cp build/lib/libportaudio.2.dylib build/libportaudio.2.dylib.framework/Versions/A/
cd build/libportaudio.2.dylib.framework
ln -sf Versions/A/libportaudio.2.dylib .
cd Versions
ln -sf A Current

echo "Verifying library setup..."
otool -L ../libportaudio.2.dylib

echo "Library preparation completed successfully"
