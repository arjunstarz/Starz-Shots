@echo off
echo Starz Shots File Copier - Portable Build Script
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

echo Python found. Starting build process...
echo.

REM Run the build script
python build_portable.py

echo.
echo Build process completed.
pause
