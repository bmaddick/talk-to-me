#!/bin/bash

# Exit on error
set -e

# Clean previous builds
rm -rf build dist

# Ensure assets directory exists
mkdir -p src/assets

# Build Mac app with py2app
python3 setup.py py2app

# Verify the app bundle was created
if [ ! -d "dist/TalkToMe.app" ]; then
    echo "Error: Failed to create app bundle"
    exit 1
fi

echo "Mac application bundle created in dist/TalkToMe.app"
