@echo off
chcp 65001 >nul
title System Test
echo ========================================
echo ESP32 System Test
echo ========================================
echo.

echo Running basic system tests...
echo.

echo 1. Testing Python environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    goto :end
) else (
    echo [SUCCESS] Python found
)

echo.
echo 2. Testing required files...
if exist "main.py" (
    echo [SUCCESS] main.py found
) else (
    echo [ERROR] main.py missing
)

if exist "config.ini" (
    echo [SUCCESS] config.ini found
) else (
    echo [ERROR] config.ini missing
)

if exist "database.py" (
    echo [SUCCESS] database.py found
) else (
    echo [ERROR] database.py missing
)

echo.
echo 3. Testing Python imports...
python -c "import flask, paho.mqtt.client, schedule" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Some Python packages missing
    echo Run install_dependencies.bat first
) else (
    echo [SUCCESS] All Python packages available
)

:end
echo.
echo ========================================
echo Test completed
echo ========================================
echo.
echo Press any key to close...
pause >nul
