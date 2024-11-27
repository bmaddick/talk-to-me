#!/bin/bash

# Run installer
./install.sh

# Build Mac app
python3 setup.py py2app

echo "Mac application bundle created in dist/TalkToMe.app"
echo "You can now drag TalkToMe.app to your Applications folder"
