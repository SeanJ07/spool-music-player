@echo off
echo 🪟 Building 64-bit Spool Windows Executable
echo =====================================

REM Check if we have the right Python
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo 💡 Please install Python from python.org
    pause
    exit /b 1
)

REM Install required packages if needed
echo 📦 Installing PyInstaller and dependencies...
python -m pip install --upgrade pip
python -m pip install PySide6 mutagen pyinstaller

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build the 64-bit executable
echo 🚀 Building 64-bit executable...
python -m PyInstaller ^
    --name "Spool" ^
    --onefile ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --distpath "dist\windows-x64" ^
    --workpath "build\windows-x64" ^
    --add-data "src\src" ^
    --exclude-module "matplotlib" ^
    --exclude-module "tkinter" ^
    --exclude-module "numpy" ^
    --hidden-import "PySide6.QtMultimedia" ^
    --hidden-import "PySide6.QtMultimediaWidgets" ^
    --icon "assets\spool-icon.png" ^
    "src\spool\main.py"

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

REM Create batch launcher
echo 📝 Creating launcher...
(
echo @echo off
echo title Spool Music Player
echo echo Starting Spool Music Player...
echo cd /d "%%~dp0"
echo if exist "dist\windows-x64\Spool.exe" (
echo     "dist\windows-x64\Spool.exe"
echo ^) else (
echo     echo ERROR: Spool.exe not found!
echo     pause
echo ^)
) > "Start Spool 64-bit.bat"

REM Check file size and architecture
echo ✅ Build completed!
echo.
echo 📂 Your Spool Application:
echo    🎯 Executable: dist\windows-x64\Spool.exe

if exist "dist\windows-x64\Spool.exe" (
    for %%F in ("dist\windows-x64\Spool.exe") do (
        set /a size=%%~zF / 1048576
        echo    📦 Size: %%size%% MB ^(64-bit^)
    )
)

echo    🚀 Launcher: Start Spool 64-bit.bat
echo.
echo 🎯 To run Spool:
echo    1. Double-click "Start Spool 64-bit.bat"
echo    2. It will launch your 64-bit Spool application!
echo.
echo ✅ Your 64-bit Spool is ready for Windows!
pause