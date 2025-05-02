@echo off

python "run.py"
if %errorlevel% neq 0 (
    echo The script encountered an error.
    pause
    exit /b
)

pause