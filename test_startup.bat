@echo off
chcp 65001 >nul
title ESP32 System Startup Test
echo ========================================
echo ESP32 System Startup Test
echo ========================================
echo.

echo Testing Python environment...
py --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not working
    pause
    exit /b 1
)

echo.
echo Testing Python dependencies...
py -c "import paho.mqtt.client, flask, flask_cors, schedule; print('All dependencies OK')"
if %errorlevel% neq 0 (
    echo [ERROR] Dependencies not working
    pause
    exit /b 1
)

echo.
echo Testing main.py syntax...
py -m py_compile main.py
if %errorlevel% neq 0 (
    echo [ERROR] main.py has syntax errors
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All tests passed!
echo System should be able to start normally
echo.
echo Press any key to close...
pause >nul



