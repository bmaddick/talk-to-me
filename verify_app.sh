#!/bin/bash

# Script to verify TalkToMe app status and help with troubleshooting

echo "=== TalkToMe App Status Check ==="
echo "Checking app processes..."
ps aux | grep -i "TalkToMe" | grep -v grep
if [ $? -eq 0 ]; then
    echo "✓ App is running"
else
    echo "✗ App is not running"
fi

echo -e "\nChecking menu bar status..."
osascript -e 'tell application "System Events" to get every process whose name contains "TalkToMe"'
if [ $? -eq 0 ]; then
    echo "✓ Menu bar app is visible"
else
    echo "✗ Menu bar app is not visible"
fi

echo -e "\nChecking permissions..."
echo "Microphone permission:"
osascript -e 'tell application "System Events" to get microphone access of current application'
if [ $? -eq 0 ]; then
    echo "✓ Microphone permission granted"
else
    echo "✗ Microphone permission not granted"
fi

echo -e "\nAccessibility permission:"
osascript -e 'tell application "System Events" to get UI elements enabled'
if [ $? -eq 0 ]; then
    echo "✓ Accessibility permission granted"
else
    echo "✗ Accessibility permission not granted"
fi

echo -e "\nChecking app bundle..."
if [ -d "/Applications/TalkToMe.app" ]; then
    echo "✓ App is installed in Applications folder"
    echo "App contents:"
    ls -la "/Applications/TalkToMe.app/Contents/MacOS"
else
    echo "✗ App not found in Applications folder"
fi

echo -e "\nTo fix visibility issues:"
echo "1. Make sure the app is installed in the Applications folder"
echo "2. Grant required permissions when prompted"
echo "3. If the menu bar icon is still not visible, try:"
echo "   - Running 'killall TalkToMe' and then relaunch the app"
echo "   - Check Console.app for any error messages"
echo "   - Run debug_app.py for detailed diagnostics"
