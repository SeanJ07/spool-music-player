@echo off
title Spool Music Player (64-bit)
echo 🎵 Starting Spool Music Player (64-bit)...
echo.
cd /d "%~dp0"
if exist "dist\windows-x64\Spool.exe" (
    echo 🎯 Launching 64-bit application...
    "dist\windows-x64\Spool.exe"
) else (
    echo ❌ ERROR: Spool.exe not found in dist/windows-x64/
    echo Please run the build script first.
    pause
)