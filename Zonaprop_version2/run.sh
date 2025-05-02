#!/bin/bash

# Move to the directory where the script is located
cd "$(dirname "$0")"

# Run the Python file
python3 run.py

# Wait for user input (optional, similar to 'pause')
read -p "Press [Enter] key to exit..."
