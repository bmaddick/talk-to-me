#!/bin/bash
set -e

# Ensure the DMG creation tools are installed
if ! command -v create-dmg &> /dev/null; then
    brew install create-dmg
fi

# Build the app bundle first
./build_mac_app.sh

# Create a temporary directory for DMG creation
TEMP_DIR=$(mktemp -d)
DMG_DIR="$TEMP_DIR/TalkToMe"
mkdir -p "$DMG_DIR"

# Copy the .app bundle
cp -r "dist/TalkToMe.app" "$DMG_DIR/"

# Create symlink to Applications folder
ln -s /Applications "$DMG_DIR/Applications"

# Set custom DMG appearance
create-dmg \
  --volname "TalkToMe Installer" \
  --volicon "src/assets/AppIcon.icns" \
  --background "src/assets/background.png" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "TalkToMe.app" 200 190 \
  --hide-extension "TalkToMe.app" \
  --app-drop-link 600 185 \
  --format UDZO \
  --window-size 800 400 \
  --text-size 12 \
  --icon-size 100 \
  --eula "LICENSE" \
  --no-internet-enable \
  "dist/TalkToMe.dmg" \
  "$DMG_DIR"

# Cleanup
rm -rf "$TEMP_DIR"

echo "Created TalkToMe.dmg with standard Mac installer interface"
