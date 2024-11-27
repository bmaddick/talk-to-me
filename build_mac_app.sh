#!/bin/bash

# Run installer
./install.sh

# Clean previous builds
rm -rf build dist

# Create icns file from iconset
iconutil -c icns AppIcon.iconset

# Build Mac app
python3 setup.py py2app

echo "Mac application bundle created in dist/TalkToMe.app"
echo "You can now drag TalkToMe.app to your Applications folder"
