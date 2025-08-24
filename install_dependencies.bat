@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Python Dependencies Installation
echo ========================================
echo ESP32 Backend System - Python Dependencies
echo ========================================
echo.

echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ first
    echo Download: https://www.python.org/downloads/
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo [SUCCESS] Python environment check passed
python --version
echo.

echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] pip not found, trying to install...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install pip
        echo Please install pip manually
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
)

echo [SUCCESS] pip is available
echo.

echo Installing Python dependencies...
echo.

echo Installing paho-mqtt...
pip install paho-mqtt==1.6.1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install paho-mqtt
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Installing Flask...
pip install flask==2.3.3
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Flask
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Installing Flask-CORS...
pip install flask-cors==4.0.0
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Flask-CORS
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Installing schedule...
pip install schedule==1.2.0
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install schedule
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo.
echo [SUCCESS] All dependencies installed!
echo.

echo Verifying installation...
python -c "import paho.mqtt.client; import flask; import flask_cors; import schedule; print('All modules imported successfully!')"

if %errorlevel% == 0 (
    echo.
    echo [SUCCESS] Dependencies verification passed!
    echo.
    echo You can now run start_system.bat to start the ESP32 backend
) else (
    echo.
    echo [ERROR] Dependencies verification failed
    echo Please check the error messages above
    echo.
    echo Common solutions:
    echo 1. Try running as Administrator
    echo 2. Check internet connection
    echo 3. Update pip: python -m pip install --upgrade pip
)

echo.
echo ========================================
echo Installation process completed
echo ========================================
echo.
echo Press any key to close this window...
pause >nul