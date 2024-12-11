#!/bin/bash
set -e

# Create framework structure
FRAMEWORK_DIR="PortAudio.framework"
mkdir -p "$FRAMEWORK_DIR/Versions/A/Resources"
cd "$FRAMEWORK_DIR/Versions"
ln -sf A Current
cd A

# Get PortAudio library path
PORTAUDIO_PATH=$(brew --prefix portaudio)
PORTAUDIO_LIB="$PORTAUDIO_PATH/lib/libportaudio.2.dylib"

if [ ! -f "$PORTAUDIO_LIB" ]; then
    echo "Error: PortAudio library not found at $PORTAUDIO_LIB"
    exit 1
fi

# Copy library and create symlinks
cp "$PORTAUDIO_LIB" .
mv libportaudio.2.dylib PortAudio
cd ..
cd ..
ln -sf Versions/Current/PortAudio PortAudio
ln -sf Versions/Current/Resources Resources

# Create Info.plist
cat > Resources/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>English</string>
    <key>CFBundleExecutable</key>
    <string>PortAudio</string>
    <key>CFBundleIdentifier</key>
    <string>org.portaudio</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>PortAudio</string>
    <key>CFBundlePackageType</key>
    <string>FMWK</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleVersion</key>
    <string>2.0</string>
</dict>
</plist>
EOF

# Fix library install name
install_name_tool -id "@rpath/$FRAMEWORK_DIR/PortAudio" Versions/Current/PortAudio

echo "PortAudio framework created successfully"
