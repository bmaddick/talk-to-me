#!/bin/bash

# Exit on error
set -e

# Clean previous builds
rm -rf build dist

# Install dependencies
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller

# Install PortAudio
brew install portaudio

# Build app using PyInstaller
pyinstaller TalkToMe.spec

# Create DMG
mkdir -p dmg
cp -r "dist/TalkToMe.app" dmg/
ln -s /Applications dmg/
hdiutil create -volname "TalkToMe" -srcfolder dmg -ov -format UDZO TalkToMe.dmg

echo "Mac application bundle and DMG created successfully"
