#!/usr/bin/env python3
"""
64-bit Windows build script for Spool Music Player
Creates a proper x64 executable using native Windows Python
"""

import subprocess
import os
import sys
from pathlib import Path

def build_windows_x64():
    """Build proper 64-bit Windows executable using native Windows Python."""
    
    print("🪟 Building 64-bit Windows Spool Application")
    print("=" * 60)
    
    # Path to Windows Python
    windows_python = "/mnt/c/Users/seanj/AppData/Local/Programs/Python/Python312/python.exe"
    
    if not os.path.exists(windows_python):
        print(f"❌ Windows Python not found at: {windows_python}")
        print("💡 Please ensure Python is installed at the standard location")
        return False
    
    # Install dependencies with Windows Python
    print("📦 Installing dependencies with Windows Python...")
    deps_cmd = [
        windows_python, "-m", "pip", "install", 
        "PySide6", "mutagen", "pyinstaller", "--upgrade"
    ]
    
    try:
        print(f"Running: {' '.join(deps_cmd)}")
        result = subprocess.run(deps_cmd, check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    for dir_name in ["dist/windows-x64", "build/windows-x64"]:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
    
    # Build the executable with correct syntax
    print("🚀 Building 64-bit executable...")
    
    pyinstaller_cmd = [
        windows_python, "-m", "PyInstaller",
        "--name", "Spool",
        "--onefile",
        "--windowed",  # No console window for GUI app
        "--clean",
        "--noconfirm",
        "--distpath", "dist/windows-x64",
        "--workpath", "build/windows-x64",
        "--add-data", "src:src",  # Correct syntax: source:destination
        "--exclude-module", "matplotlib",
        "--exclude-module", "tkinter", 
        "--exclude-module", "numpy",
        "--hidden-import", "PySide6.QtMultimedia",
        "--hidden-import", "PySide6.QtMultimediaWidgets",
        "--icon", "assets/spool-icon.png",
        "src/spool/main.py"
    ]
    
    try:
        print(f"Building with command: {' '.join(pyinstaller_cmd)}")
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True,
                              cwd=os.getcwd())
        
        print("✅ 64-bit build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with exit code {e.returncode}")
        print("Error output:")
        print(e.stderr)
        return False

def create_x64_launcher():
    """Create a batch launcher for the 64-bit executable."""
    
    bat_content = """@echo off
title Spool Music Player (64-bit)
echo 🎵 Starting Spool Music Player (64-bit)...
echo.
cd /d "%~dp0"
if exist "dist\\windows-x64\\Spool.exe" (
    echo 🎯 Launching 64-bit application...
    "dist\\windows-x64\\Spool.exe"
) else (
    echo ❌ ERROR: Spool.exe not found in dist/windows-x64/
    echo Please run the build script first.
    pause
)
"""
    
    launcher_path = "Start Spool 64-bit.bat"
    with open(launcher_path, 'w') as f:
        f.write(bat_content)
    
    print(f"🚀 Created: {launcher_path}")

def verify_build():
    """Verify the build and show file information."""
    
    exe_path = Path("dist/windows-x64/Spool.exe")
    if not exe_path.exists():
        print("❌ Spool.exe not found!")
        return False
    
    # Get file size
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    
    print("\n✅ Build verification:")
    print(f"📁 Location: {exe_path}")
    print(f"💾 Size: {size_mb:.1f} MB")
    print(f"🏗️  Architecture: x64 (64-bit)")
    print(f"🪟 Platform: Windows")
    
    return True

if __name__ == "__main__":
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    success = build_windows_x64()
    
    if success:
        create_x64_launcher()
        if verify_build():
            print("\n🎉 Your 64-bit Spool application is ready!")
            print("\n🎯 To launch:")
            print("   Double-click: Start Spool 64-bit.bat")
            print("   Or run directly: dist/windows-x64/Spool.exe")
            print("\n📦 Distribution ready:")
            print("   Copy 'dist/windows-x64/' folder to any Windows PC")
            print("   Users just double-click Spool.exe - no installation needed!")
        else:
            print("\n❌ Build verification failed")
    else:
        print("\n❌ Build failed")