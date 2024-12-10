#!/bin/bash

# Exit on error
set -e

# Clean previous builds
rm -rf build dist

# Ensure assets directory exists
mkdir -p src/assets

# Install dependencies with PEP 517
python3 -m pip install --use-pep517 -r requirements.txt
python3 -m pip install --use-pep517 py2app

# Set environment variables for library paths
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:/usr/local/lib:$DYLD_LIBRARY_PATH"
export LIBRARY_PATH="/opt/homebrew/lib:/usr/local/lib:$LIBRARY_PATH"
export CFLAGS="-I/opt/homebrew/include -I/usr/local/include"
export LDFLAGS="-L/opt/homebrew/lib -L/usr/local/lib"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"

# Create temporary frameworks directory
mkdir -p build/frameworks

# Copy PortAudio framework to temporary location
if [ -f "/opt/homebrew/lib/libportaudio.2.dylib" ]; then
    cp /opt/homebrew/lib/libportaudio.2.dylib build/frameworks/
elif [ -f "/usr/local/lib/libportaudio.2.dylib" ]; then
    cp /usr/local/lib/libportaudio.2.dylib build/frameworks/
else
    echo "Error: Could not find libportaudio.2.dylib"
    exit 1
fi

# Update DYLD_LIBRARY_PATH to include our temporary frameworks
export DYLD_LIBRARY_PATH="$(pwd)/build/frameworks:$DYLD_LIBRARY_PATH"

# Build Mac app with py2app
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
