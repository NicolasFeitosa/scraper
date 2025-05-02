@echo off
REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

REM Upgrade pip to the latest version
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install necessary libraries
echo Installing required libraries...
python -m pip install DrissionPage pandas


echo All libraries installed successfully.
pause
