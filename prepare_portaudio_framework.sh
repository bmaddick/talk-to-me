#!/bin/bash
set -e

# Create framework structure
FRAMEWORK_DIR="PortAudio.framework"
mkdir -p "$FRAMEWORK_DIR/Versions/A"
cd "$FRAMEWORK_DIR/Versions"
ln -sf A Current
cd A

# Get PortAudio library path
PORTAUDIO_PATH=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PATH/lib/libportaudio.2.dylib"

if [ ! -f "$PORTAUDIO_LIB" ]; then
    echo "Error: PortAudio library not found at $PORTAUDIO_LIB"
    exit 1
fi

# Copy library and create symlinks
cp "$PORTAUDIO_LIB" .
mv libportaudio.2.dylib PortAudio
cd ..
cd ..
ln -sf Versions/Current/PortAudio PortAudio

# Fix library install name
install_name_tool -id "@rpath/$FRAMEWORK_DIR/PortAudio" Versions/Current/PortAudio

echo "PortAudio framework created successfully"
ls -R
