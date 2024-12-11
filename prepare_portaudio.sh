#!/bin/bash
set -e

echo "Preparing PortAudio framework..."

# Get PortAudio path
PORTAUDIO_PREFIX=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PREFIX/lib/libportaudio.2.dylib"

# Create framework structure
FRAMEWORK_NAME="libportaudio.2.dylib.framework"
FRAMEWORK_DIR="build/$FRAMEWORK_NAME"

# Clean up any existing framework
rm -rf "$FRAMEWORK_DIR"
mkdir -p "$FRAMEWORK_DIR"

# Copy library directly to framework
echo "Copying PortAudio library..."
cp "$PORTAUDIO_LIB" "$FRAMEWORK_DIR/libportaudio.2.dylib"

# Fix library install name
echo "Fixing library install names..."
install_name_tool -id "@executable_path/../Frameworks/$FRAMEWORK_NAME/libportaudio.2.dylib" \
  "$FRAMEWORK_DIR/libportaudio.2.dylib"

# Make executable
chmod +x "$FRAMEWORK_DIR/libportaudio.2.dylib"

echo "Verifying framework structure..."
ls -l "$FRAMEWORK_DIR"
otool -L "$FRAMEWORK_DIR/libportaudio.2.dylib"

echo "Framework preparation completed successfully"
