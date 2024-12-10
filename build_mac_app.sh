#!/bin/bash

# Exit on error
set -e

# Clean previous builds
rm -rf build dist

# Ensure assets directory exists
mkdir -p src/assets

# Install PortAudio using Homebrew
echo "Installing PortAudio..."
brew install portaudio

# Install dependencies with PEP 517
python3 -m pip install --use-pep517 -r requirements.txt
python3 -m pip install --use-pep517 py2app

# Set environment variables for library paths
export DYLD_LIBRARY_PATH="$(brew --prefix)/lib:/usr/local/lib:$DYLD_LIBRARY_PATH"
export LIBRARY_PATH="$(brew --prefix)/lib:/usr/local/lib:$LIBRARY_PATH"
export CFLAGS="-I$(brew --prefix)/include -I/usr/local/include"
export LDFLAGS="-L$(brew --prefix)/lib -L/usr/local/lib"
export PKG_CONFIG_PATH="$(brew --prefix)/lib/pkgconfig:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"

# Create temporary frameworks directory
mkdir -p build/frameworks

# Find and copy PortAudio framework
echo "Locating PortAudio library..."
PORTAUDIO_PATH=$(brew --prefix portaudio)/lib/libportaudio.2.dylib

if [ ! -f "$PORTAUDIO_PATH" ]; then
    echo "Error: PortAudio library not found at $PORTAUDIO_PATH"
    echo "Checking alternative locations..."

    # Fallback locations
    PORTAUDIO_PATHS=(
        "/usr/local/lib/libportaudio.2.dylib"
        "/opt/homebrew/lib/libportaudio.2.dylib"
        "/opt/homebrew/Cellar/portaudio/19.7.0/lib/libportaudio.2.dylib"
    )

    for path in "${PORTAUDIO_PATHS[@]}"; do
        if [ -f "$path" ]; then
            echo "Found PortAudio at: $path"
            PORTAUDIO_PATH=$path
            break
        fi
    done
fi

if [ ! -f "$PORTAUDIO_PATH" ]; then
    echo "Error: Could not find libportaudio.2.dylib in any location"
    echo "Current environment:"
    echo "DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH"
    echo "LIBRARY_PATH=$LIBRARY_PATH"
    echo "PKG_CONFIG_PATH=$PKG_CONFIG_PATH"
    exit 1
fi

echo "Copying PortAudio from $PORTAUDIO_PATH to build/frameworks/"
cp "$PORTAUDIO_PATH" build/frameworks/

# Update DYLD_LIBRARY_PATH to include our temporary frameworks
export DYLD_LIBRARY_PATH="$(pwd)/build/frameworks:$DYLD_LIBRARY_PATH"

# Build Mac app with py2app
echo "Building Mac app..."
python3 setup.py py2app

# Copy frameworks to final location
mkdir -p dist/TalkToMe.app/Contents/Frameworks/
cp build/frameworks/* dist/TalkToMe.app/Contents/Frameworks/

# Verify the app bundle was created
if [ ! -d "dist/TalkToMe.app" ]; then
    echo "Error: Failed to create app bundle"
    exit 1
fi

echo "Mac application bundle created in dist/TalkToMe.app"
