#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python if not present
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    brew install python@3.12
fi

# Install PortAudio
echo "Installing PortAudio..."
brew install portaudio

# Install pip if not present
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install py2app for Mac app bundling
pip3 install py2app

# Install project dependencies
pip3 install -r requirements.txt

echo "Installation complete! Now creating Mac application bundle..."
