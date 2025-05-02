#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

# Upgrade pip to the latest version
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install necessary libraries
echo "Installing required libraries..."
python3 -m pip install DrissionPage pandas

echo "All libraries installed successfully."
