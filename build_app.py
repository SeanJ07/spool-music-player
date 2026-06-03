"""PyInstaller build script for Spool Music Player

Creates standalone executables for Windows and Linux with proper icon and metadata.
"""

import os
import subprocess
import sys
from pathlib import Path

# Build configuration
APP_NAME = "Spool"
VERSION = "1.0.0"
DESCRIPTION = "Spool - iPod-inspired music player with vinyl visualization"

# Paths (adjust if needed)
project_root = Path(__file__).parent
src_dir = project_root / "src"
main_script = src_dir / "spool" / "main.py"
icon_path = project_root / "assets" / "spool-icon.png"

def build_executable(platform="auto"):
    """Build the Spool executable for the specified platform."""
    
    # Determine PyInstaller flags based on platform
    if platform == "auto":
        if sys.platform == "win32":
            platform = "windows"
        elif sys.platform == "darwin":
            platform = "macos"
        else:
            platform = "linux"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--onefile",  # Create single executable
        "--windowed",  # Hide console window for GUI app
        "--version-file", "version_info.txt",
        "--add-data", f"{src_dir}{os.pathsep}src",  # Include source files
    ]
    
    # Add icon if available
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    # Platform-specific options
    if platform == "windows":
        cmd.extend([
            "--console",  # Keep console for debugging (remove for production)
            "--distpath", "dist/windows",
        ])
    elif platform == "linux":
        cmd.extend([
            "--distpath", "dist/linux",
        ])
    elif platform == "macos":
        cmd.extend([
            "--distpath", "dist/macos",
        ])
    
    # Add main script
    cmd.append(str(main_script))
    
    print(f"🚀 Building {APP_NAME} for {platform}...")
    print(f"📁 Command: {' '.join(cmd)}")
    
    # Execute build
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        print("📦 Output:")
        print(result.stdout)
        if result.stderr:
            print("⚠️  Warnings:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with exit code {e.returncode}")
        print("📄 Error output:")
        print(e.stdout)
        print("📄 Error details:")
        print(e.stderr)
        return False
    
    return True

def create_window_shortcut():
    """Create a Windows desktop shortcut for the executable."""
    if sys.platform != "win32":
        print("❌ Shortcut creation only available on Windows")
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Spool.lnk")
        target = os.path.join(os.getcwd(), "dist", "windows", "Spool.exe")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.setDescription("Spool Music Player")
        shortcut.save()
        
        print("✅ Desktop shortcut created successfully!")
        
    except ImportError:
        print("⚠️  Windows shortcut creation requires pywin32 package")
        print("💡 Install with: pip install pywin32")
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")

if __name__ == "__main__":
    print("🎵 Spool Music Player - Build Script")
    print("=" * 50)
    
    # Check if main script exists
    if not main_script.exists():
        print(f"❌ Main script not found: {main_script}")
        sys.exit(1)
    
    # Build executable
    success = build_executable()
    
    if success:
        print("\n🎉 Build completed! ")
        print("📁 Check the 'dist' directory for your executable:")
        print("   - dist/windows/Spool.exe (Windows)")
        print("   - dist/linux/Spool (Linux)")
        print("   - dist/macos/Spool (macOS)")
        
        # Create Windows shortcut if on Windows
        if sys.platform == "win32":
            create_window_shortcut()
            
        print("\n📋 Next steps:")
        print("1. Distribute the executable or installer")
        print("2. For Windows, the .exe includes all dependencies")
        print("3. Double-click the executable to run Spool!")
        
    else:
        print("\n❌ Build failed. Check the error messages above.")
        sys.exit(1)