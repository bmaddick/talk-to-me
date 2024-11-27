#!/bin/bash

# Exit on error
set -e

# Clean previous builds
rm -rf build dist

# Ensure assets directory exists
mkdir -p src/assets

# Set environment variables for library paths
export DYLD_LIBRARY_PATH="/usr/local/lib:/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export LIBRARY_PATH="/usr/local/lib:/opt/homebrew/lib:$LIBRARY_PATH"
export CFLAGS="-I/usr/local/include -I/opt/homebrew/include"
export LDFLAGS="-L/usr/local/lib -L/opt/homebrew/lib"

# Build Mac app with py2app
python3 setup.py py2app --use-pep517

# Verify the app bundle was created
if [ ! -d "dist/TalkToMe.app" ]; then
    echo "Error: Failed to create app bundle"
    exit 1
fi

echo "Mac application bundle created in dist/TalkToMe.app"
