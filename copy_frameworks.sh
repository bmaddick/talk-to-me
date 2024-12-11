#!/bin/bash
set -e

# Create frameworks directory
mkdir -p build/frameworks

# Copy PortAudio library from Homebrew
PORTAUDIO_LIB=$(brew --prefix portaudio)/lib/libportaudio.2.dylib
if [ -f "$PORTAUDIO_LIB" ]; then
    cp "$PORTAUDIO_LIB" build/frameworks/
    echo "Copied PortAudio library to build/frameworks/"
else
    echo "Error: PortAudio library not found at $PORTAUDIO_LIB"
    exit 1
fi
