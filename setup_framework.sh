#!/bin/bash
set -e

# Get PortAudio path from Homebrew
PORTAUDIO_PREFIX=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PREFIX/lib/libportaudio.2.dylib"

# Create framework structure
FRAMEWORK_DIR="build/libportaudio.2.dylib.framework"
mkdir -p "$FRAMEWORK_DIR/Versions/A"

# Copy library to framework
cp "$PORTAUDIO_LIB" "$FRAMEWORK_DIR/Versions/A/"

# Create symbolic links
cd "$FRAMEWORK_DIR"
ln -sf Versions/A/libportaudio.2.dylib libportaudio.2.dylib
cd Versions
ln -sf A Current

# Fix install names
install_name_tool -id "@executable_path/../Frameworks/libportaudio.2.dylib.framework/Versions/A/libportaudio.2.dylib" \
  "A/libportaudio.2.dylib"

# Make executable
chmod +x "A/libportaudio.2.dylib"

echo "Framework structure created at $FRAMEWORK_DIR"
ls -lR "$FRAMEWORK_DIR"
otool -L "$FRAMEWORK_DIR/Versions/A/libportaudio.2.dylib"
