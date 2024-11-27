#!/bin/bash

# Ensure the DMG creation tools are installed
brew install create-dmg

# Build the app bundle first
./build_mac_app.sh

# Create a temporary directory for DMG creation
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/TalkToMe"

# Copy the .app bundle
cp -r "dist/TalkToMe.app" "$TEMP_DIR/TalkToMe/"

# Create the DMG with Applications folder shortcut and background
create-dmg \
  --volname "TalkToMe" \
  --volicon "src/assets/AppIcon.icns" \
  --background "src/assets/background.png" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "TalkToMe.app" 200 190 \
  --app-drop-link 600 185 \
  --no-internet-enable \
  "dist/TalkToMe.dmg" \
  "$TEMP_DIR/TalkToMe/"

# Cleanup
rm -rf "$TEMP_DIR"

echo "Created TalkToMe.dmg with drag-and-drop installation interface"
