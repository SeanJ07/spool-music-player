@echo off
title Spool Music Player
echo Starting Spool Music Player...
echo.
cd /d "%~dp0"
if exist "dist\windows\Spool.exe" (
    "dist\windows\Spool.exe"
) else (
    echo ERROR: Spool.exe not found!
    echo Please run the build script first.
    pause
)
