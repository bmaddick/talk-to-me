#!/bin/bash
set -e

echo "Preparing PortAudio library..."

# Get PortAudio path
PORTAUDIO_PREFIX=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PREFIX/lib/libportaudio.2.dylib"

# Create build directory
BUILD_DIR="build"
mkdir -p "$BUILD_DIR"

# Copy library to build directory
echo "Copying PortAudio library..."
cp "$PORTAUDIO_LIB" "$BUILD_DIR/libportaudio.2.dylib"

# Fix library install name
echo "Fixing library install names..."
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib" \
  "$BUILD_DIR/libportaudio.2.dylib"

# Make executable
chmod +x "$BUILD_DIR/libportaudio.2.dylib"

echo "Verifying library..."
ls -l "$BUILD_DIR/libportaudio.2.dylib"
otool -L "$BUILD_DIR/libportaudio.2.dylib"

echo "Library preparation completed successfully"
