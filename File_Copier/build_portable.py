#!/usr/bin/env python3
"""
Build script to create a portable executable from the File Copier GUI application.

This script uses PyInstaller to create a standalone executable that can be run
on any Windows machine without requiring Python to be installed.
"""

import subprocess
import sys
import os
from pathlib import Path


def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyInstaller: {e}")
            return False


def build_executable():
    """Build the portable executable."""
    print("Building portable executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # Hide console window (GUI app)
        "--name=StarzShotsFileCopier",  # Name of the executable
        "--icon=NONE",                 # No icon (you can add one later)
        "--add-data=sample_reference.txt;.",  # Include sample reference file
        "file_copier.py"               # Main script
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL!")
        print("="*50)
        print("Your portable executable is located at:")
        print("  dist/StarzShotsFileCopier.exe")
        print("\nYou can copy this file to any Windows computer and run it")
        print("without needing Python installed.")
        print("\nThe sample reference file is included in the executable.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found in PATH. Please ensure it's properly installed.")
        return False


def main():
    """Main build function."""
    print("Starz Shots File Copier - Portable Build Script")
    print("="*48)
    
    # Check if main script exists
    if not Path("file_copier.py").exists():
        print("Error: file_copier.py not found in current directory.")
        return
    
    # Install PyInstaller if needed
    if not install_pyinstaller():
        print("Cannot proceed without PyInstaller.")
        return
    
    # Build the executable
    if build_executable():
        print("\nBuild completed successfully!")
        
        # Clean up build files (optional)
        cleanup = input("\nDo you want to clean up build files? (y/n): ").strip().lower()
        if cleanup == 'y':
            import shutil
            try:
                if Path("build").exists():
                    shutil.rmtree("build")
                if Path("StarzShotsFileCopier.spec").exists():
                    Path("StarzShotsFileCopier.spec").unlink()
                print("Build files cleaned up.")
            except Exception as e:
                print(f"Warning: Could not clean up build files: {e}")
    else:
        print("Build failed.")


if __name__ == "__main__":
    main()
