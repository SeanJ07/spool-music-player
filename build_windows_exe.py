#!/usr/bin/env python3
"""
Windows Build Script for Spool Music Player
Creates proper Windows .exe executable using PyInstaller
"""

import os
import subprocess
import sys
from pathlib import Path

def build_windows_exe():
    """Build Windows executable with proper Windows-specific settings."""
    
    print("🪟 Building Windows .exe for Spool...")
    
    # PyInstaller command optimized for Windows
    cmd = [
        "python", "-m", "PyInstaller",
        "--name", "Spool",
        "--onefile",  # Single executable file
        "--windowed",  # Hide console (GUI app)
        "--clean",  # Clean previous builds
        "--noconfirm",  # Don't ask for confirmation
        "--distpath", "dist/windows",
        "--workpath", "build/windows",
        "--specpath", ".",
        "--add-data", f"src{os.pathsep}src",
        "--icon", "assets/spool-icon.png",
        "src/spool/main.py"
    ]
    
    try:
        print(f"🚀 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        print("✅ Windows build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def create_batch_launcher():
    """Create a .bat file to launch the Windows executable."""
    
    bat_content = """@echo off
title Spool Music Player
echo Starting Spool Music Player...
echo.
cd /d "%~dp0"
if exist "dist\\windows\\Spool.exe" (
    "dist\\windows\\Spool.exe"
) else (
    echo ERROR: Spool.exe not found!
    echo Please run the build script first.
    pause
)
"""
    
    launcher_path = "Start Spool.bat"
    with open(launcher_path, 'w') as f:
        f.write(bat_content)
    
    print(f"📝 Created launcher: {launcher_path}")

def create_shortcut_instructions():
    """Create a text file with shortcut creation instructions."""
    
    instructions = """
To create a desktop shortcut for Spool:

1. Right-click on your desktop
2. Select 'New' > 'Shortcut'
3. Click 'Browse' and navigate to:
   C:\\Users\\YourUsername\\Path\\To\\spool-music-player\\dist\\windows\\Spool.exe
4. Click 'Next'
5. Type 'Spool' as the name
6. Click 'Finish'
7. Double-click the shortcut to launch Spool!

Or simply double-click 'Start Spool.bat' in the project folder.
"""
    
    with open('SHORTCUT_INSTRUCTIONS.txt', 'w') as f:
        f.write(instructions)
    
    print("📋 Created shortcut instructions: SHORTCUT_INSTRUCTIONS.txt")

if __name__ == "__main__":
    print("🎵 Spool Music Player - Windows Executable Builder")
    print("=" * 60)
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("⚠️  This script is designed for Windows but can build for other platforms")
    
    # Build the executable
    if build_windows_exe():
        create_batch_launcher()
        create_shortcut_instructions()
        
        print("\n🎉 Build completed successfully!")
        print("\n📂 Your Spool application:")
        print("   🎯 Main executable: dist/windows/Spool.exe")
        print("   🚀 Quick launcher: Start Spool.bat")
        print("   📋 Help file: SHORTCUT_INSTRUCTIONS.txt")
        print("\n🖥️  To run Spool:")
        print("   1. Double-click 'Start Spool.bat' in this folder")
        print("   2. Or create a desktop shortcut using the instructions")
        
        # Check file size
        exe_path = Path("dist/windows/Spool.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 Executable size: {size_mb:.1f} MB (includes all dependencies)")
            print("✅ Ready to share with others - no Python installation required!")
        
    else:
        print("\n❌ Build failed. Check the error messages above.")
        print("\n💡 Make sure you have:")
        print("   ✅ PyInstaller installed: pip install pyinstaller")
        print("   ✅ Source code in src/spool/")
        print("   ✅ All requirements: PySide6, mutagen")