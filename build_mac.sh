#!/bin/bash

# NBCRI CSV Cleaner - Mac Build Script

echo "--- NBCRI CSV Cleaner Mac Builder ---"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 from https://www.python.org/downloads/macos/"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install pandas openpyxl FreeSimpleGUI pyinstaller Pillow

# Build Application
echo "Building Mac Application..."
# --windowed creates a .app bundle instead of a console executable
pyinstaller --clean --noconsole --onefile --windowed --name "NBCRI CSV Cleaner" gui.py

echo "--- Build Complete ---"
echo "You can find your Mac App in the 'dist' folder:"
echo "$(pwd)/dist/NBCRI CSV Cleaner.app"
