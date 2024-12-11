#!/bin/bash
set -e

# Install PortAudio using brew
brew install portaudio

# Get PortAudio paths
PORTAUDIO_PREFIX=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PREFIX/lib/libportaudio.2.dylib"

# Create lib directory
mkdir -p lib

# Copy PortAudio library
cp -v "$PORTAUDIO_LIB" lib/
chmod 755 lib/libportaudio.2.dylib

# Fix library install name
install_name_tool -id "@rpath/libportaudio.2.dylib" lib/libportaudio.2.dylib

# Debug output
echo "Library details:"
otool -L lib/libportaudio.2.dylib

# Create rpath directory structure
mkdir -p dist/TalkToMe.app/Contents/Frameworks || true

# Export environment variables
echo "export DYLD_LIBRARY_PATH=$PWD/lib:$DYLD_LIBRARY_PATH" > env.sh
echo "export LIBRARY_PATH=$PWD/lib:$LIBRARY_PATH" >> env.sh
echo "export CFLAGS=-I$PORTAUDIO_PREFIX/include" >> env.sh
echo "export LDFLAGS=-L$PWD/lib" >> env.sh
