@echo off
chcp 65001 >nul
title ESP32 System Startup
echo ========================================
echo ESP32 Backend System Startup
echo ========================================
echo.

echo Starting ESP32 backend system...
echo.

echo System will be available at: http://localhost:5000
echo Press Ctrl+C to stop the system
echo.

REM Start the Python backend
python main.py

echo.
echo ========================================
echo System has stopped
echo ========================================
echo.
echo Exit code: %errorlevel%
echo.
echo Press any key to close this window...
pause >nul
