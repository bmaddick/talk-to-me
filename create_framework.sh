#!/bin/bash
set -e

echo "Creating PortAudio framework structure..."

# Get PortAudio path
PORTAUDIO_PREFIX=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PREFIX/lib/libportaudio.2.dylib"

# Create framework structure
FRAMEWORK_DIR="build/libportaudio.2.dylib.framework"
mkdir -p "$FRAMEWORK_DIR"

# Copy library directly to framework
echo "Copying PortAudio library..."
cp "$PORTAUDIO_LIB" "$FRAMEWORK_DIR/libportaudio.2.dylib"

# Fix library install name
echo "Fixing library install names..."
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib.framework/libportaudio.2.dylib" \
  "$FRAMEWORK_DIR/libportaudio.2.dylib"

# Make executable
chmod +x "$FRAMEWORK_DIR/libportaudio.2.dylib"

echo "Verifying framework structure..."
ls -lR "$FRAMEWORK_DIR"
otool -L "$FRAMEWORK_DIR/libportaudio.2.dylib"

echo "Framework creation completed successfully"
