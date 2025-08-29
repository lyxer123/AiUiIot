@echo off
chcp 65001 >nul
title Python Dependencies Installation (Fixed)
echo ========================================
echo ESP32 Backend System - Python Dependencies
echo ========================================
echo.

echo Checking Python environment...
set PYTHON_CMD=py

%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found or py launcher not working
    echo Trying to find Python installation...
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo [SUCCESS] Python environment check passed
%PYTHON_CMD% --version
echo.

echo Checking pip...
%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] pip not found, trying to install...
    %PYTHON_CMD% -m ensurepip --upgrade
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
%PYTHON_CMD% -m pip install paho-mqtt==1.6.1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install paho-mqtt
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Installing Flask...
%PYTHON_CMD% -m pip install flask==2.3.3
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Flask
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Installing Flask-CORS...
%PYTHON_CMD% -m pip install flask-cors==4.0.0
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Flask-CORS
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Installing schedule...
%PYTHON_CMD% -m pip install schedule==1.2.0
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
%PYTHON_CMD% -c "import paho.mqtt.client; import flask; import flask_cors; import schedule; print('All modules imported successfully!')"

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
    echo 3. Update pip: %PYTHON_CMD% -m pip install --upgrade pip
)

echo.
echo ========================================
echo Installation process completed
echo ========================================
echo.
echo Press any key to close this window...
pause >nul
