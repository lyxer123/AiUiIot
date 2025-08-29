@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title ESP32 Backend System (Improved)
echo ========================================
echo ESP32 Data Collection and Control System
echo ========================================
echo "Function: Northbound AD1 data collection, Southbound IO1 switch control"
echo "Protocol: MQTT + JSON"
echo "ESP32 Simulator enabled - Periodic simulated AD values"
echo ========================================
echo.

echo Checking system environment...
echo.

echo 1. Checking Python environment...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not installed or not in PATH
    echo Please run install_dependencies_fixed.bat first
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [SUCCESS] Python environment OK
py --version
echo.

echo 2. Checking Python dependencies...
py -c "import paho.mqtt.client, flask, flask_cors, schedule" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python dependencies not installed
    echo Please run install_dependencies_fixed.bat first
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [SUCCESS] Python dependencies installed
echo.

echo 3. Checking configuration file...
if not exist "config.ini" (
    echo [ERROR] Configuration file config.ini not found
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [SUCCESS] Configuration file exists
echo.

echo 4. Checking main.py syntax...
py -m py_compile main.py >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] main.py has syntax errors
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [SUCCESS] main.py syntax check passed
echo.

echo All checks completed, starting system...
echo.
echo [INFO] System is starting up...
echo [INFO] You may see some MQTT connection warnings (this is normal if MQTT broker is not running)
echo [INFO] Web interface will be available at: http://localhost:5000
echo [INFO] Press Ctrl+C to stop system
echo.
echo Starting ESP32 backend system...
echo.

REM Start Python program and capture exit code
py main.py
set PYTHON_EXIT_CODE=%errorlevel%

echo.
echo ========================================
if %PYTHON_EXIT_CODE% == 0 (
    echo [INFO] System exited normally
) else if %PYTHON_EXIT_CODE% == 1 (
    echo [ERROR] System exited abnormally (error code: %PYTHON_EXIT_CODE%)
    echo Possible causes:
    echo - Port 5000 is occupied
    echo - Configuration file error
    echo - Python dependency issues
    echo - Insufficient permissions
) else if %PYTHON_EXIT_CODE% == 2 (
    echo [ERROR] System startup failed (error code: %PYTHON_EXIT_CODE%)
    echo Possible causes:
    echo - Database file corrupted
    echo - Network configuration error
    echo - MQTT connection failed
) else (
    echo [INFO] System exited (exit code: %PYTHON_EXIT_CODE%)
)
echo ========================================
echo.

echo System stopped
echo.
echo To restart, run this script again
echo To view detailed error info, check log files in logs/ directory
echo.
echo Press any key to close window...
pause >nul



