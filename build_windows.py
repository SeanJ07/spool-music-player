#!/usr/bin/env python3
"""
Windows-specific build and shortcut creation for Spool Music Player.
Creates the Windows .exe and desktop shortcut.
"""

import os
import subprocess
import sys
from pathlib import Path

def build_windows_executable():
    """Build Windows-specific executable with console support."""
    
    print("🪟 Building Windows executable for Spool...")
    
    cmd = [
        "pyinstaller",
        "--name", "Spool",
        "--onefile",
        "--console",  # Show console for debugging (can switch to --windowed for production)
        "--add-data", f"src{os.pathsep}src",  # Include source files
        "--icon", "assets/spool-icon.png",
        "--distpath", "dist/windows",
        "src/spool/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Windows build completed successfully!")
        print("📁 Executable created: dist/windows/Spool.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")
        return False

def create_windows_shortcut():
    """Create a Windows desktop shortcut for Spool."""
    print("🔗 Creating Windows desktop shortcut...")
    
    try:
        # Create a simple shortcut using Windows shell
        import winshell
        from win32com.client import Dispatch
        
        # Get desktop path
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "Spool.lnk")
        
        # Path to the executable
        if sys.platform == "win32":
            exe_path = os.path.join(os.getcwd(), "dist", "windows", "Spool.exe")
        else:
            exe_path = os.path.join(os.getcwd(), "dist", "linux", "Spool")
        
        if not os.path.exists(exe_path):
            print(f"❌ Executable not found: {exe_path}")
            return False
        
        # Create shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        
        # Use the same icon
        if os.path.exists("assets/spool-icon.png"):
            shortcut.IconLocation = exe_path
        
        shortcut.Description = "Spool Music Player - iPod-inspired music player"
        shortcut.save()
        
        print(f"✅ Desktop shortcut created: {shortcut_path}")
        return True
        
    except ImportError as e:
        print(f"⚠️ Windows libraries not available: {e}")
        print("💡 To create shortcuts manually:")
        print("   1. Right-click on your desktop")
        print("   2. Select 'New' > 'Shortcut'")
        print("   3. Browse to: dist/windows/Spool.exe")
        print("   4. Name it 'Spool'")
        return False
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")
        return False

def create_simple_launcher():
    """Create a simple .bat launcher for Windows if shortcut creation fails."""
    
    bat_content = """@echo off
title Spool Music Player
echo Starting Spool Music Player...
echo.
cd /d "%~dp0"
dist\\windows\\Spool.exe
if errorlevel 1 (
    echo.
    echo Spool encountered an error. Press any key to exit...
    pause > nul
)
"""
    
    launcher_path = "dist/windows/Start Spool.bat"
    with open(launcher_path, 'w') as f:
        f.write(bat_content)
    
    print(f"📝 Created launcher: {launcher_path}")
    print("💡 Double-click this .bat file to start Spool")

if __name__ == "__main__":
    print("🎵 Spool Music Player - Windows Build")
    print("=" * 50)
    
    # Check if source exists
    if not os.path.exists("src/spool/main.py"):
        print("❌ Source code not found")
        sys.exit(1)
    
    # Build the executable
    if build_windows_executable():
        # Try to create shortcut
        shortcut_created = create_windows_shortcut()
        
        if not shortcut_created:
            # Create a .bat launcher as fallback
            create_simple_launcher()
        
        print("\n🎉 Windows build complete!")
        print("📁 Executable: dist/windows/Spool.exe")
        print("🏠 Start from: Desktop shortcut or dist/windows/Start Spool.bat")
        print("\n📋 Distribution ready:")
        print("   - Copy dist/windows/ to any Windows machine")
        print("   - The .exe contains all dependencies")
        print("   - No Python installation required")
        
    else:
        print("\n❌ Build failed")
        sys.exit(1)