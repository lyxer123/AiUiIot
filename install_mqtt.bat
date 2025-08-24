@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title MQTT Broker Installation
echo ========================================
echo ESP32 Backend System - MQTT Broker Setup
echo ========================================
echo.

echo Checking if Mosquitto MQTT broker is already installed...
echo Checking Mosquitto installation status...
timeout /t 2 /nobreak >nul 2>&1

REM Use faster check method
if exist "C:\Program Files\mosquitto\mosquitto.exe" (
    set MOSQUITTO_PATH="C:\Program Files\mosquitto\mosquitto.exe"
    echo [INFO] Found Mosquitto in Program Files
) else if exist "C:\Program Files (x86)\mosquitto\mosquitto.exe" (
    set MOSQUITTO_PATH="C:\Program Files (x86)\mosquitto\mosquitto.exe"
    echo [INFO] Found Mosquitto in Program Files (x86)
) else (
    goto :not_installed
)

echo.
echo Mosquitto is installed. Version information:
!MOSQUITTO_PATH! -h
echo.

echo Starting Mosquitto service...
net start mosquitto >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Mosquitto service started successfully
) else (
    echo [WARNING] Failed to start Mosquitto service, error code: %errorlevel%
    if %errorlevel% == 2 (
        echo [ERROR] System cannot find specified file - Mosquitto service not installed
        echo.
        echo Solutions:
        echo 1. Reinstall Mosquitto, make sure to select "Service" option
        echo 2. Or manually install the service:
        echo    - Open Command Prompt as Administrator
        echo    - Run: sc create mosquitto binPath= "C:\Program Files\mosquitto\mosquitto.exe -v" start= auto
        echo    - Then run: net start mosquitto
        echo.
        echo 3. Check if service is installed:
        echo    - Press Win+R, type services.msc
        echo    - Look for "mosquitto" service
    ) else if %errorlevel% == 5 (
        echo [ERROR] Access denied, please run this script as Administrator
        echo Right-click script -> "Run as Administrator"
        echo.
        echo Or manually start the service:
        echo 1. Press Win+R, type services.msc
        echo 2. Find "mosquitto" service
        echo 3. Right-click and select "Start"
    ) else if %errorlevel% == 1060 (
        echo [INFO] Service not configured for auto-start, trying manual start...
        sc start mosquitto >nul 2>&1
        if !errorlevel! == 0 (
            echo [SUCCESS] MQTT service manually started successfully
        ) else (
            echo [ERROR] Failed to start MQTT service manually
        )
    ) else (
        echo [INFO] Service might already be running, checking status...
        sc query mosquitto >nul 2>&1
        if !errorlevel! == 0 (
            sc query mosquitto | find "RUNNING" >nul 2>&1
            if !errorlevel! == 0 (
                echo [SUCCESS] MQTT service is already running
            ) else (
                echo [INFO] MQTT service is installed but not running, trying to start...
                sc start mosquitto >nul 2>&1
                if !errorlevel! == 0 (
                    echo [SUCCESS] MQTT service started successfully
                ) else (
                    echo [ERROR] Failed to start MQTT service
                )
            )
        ) else (
            echo [ERROR] MQTT service not installed, please reinstall Mosquitto
        )
    )
)
goto :end

:not_installed

echo.
echo Mosquitto is not installed. Downloading installation package...
echo.

echo Please follow these steps to manually install Mosquitto:
echo 1. Visit https://mosquitto.org/download/
echo 2. Download Windows version installation package
echo 3. Run the installer, select "Service" option
echo 4. After installation, Mosquitto will run automatically as Windows service
echo.

echo Or use Chocolatey package manager:
echo choco install mosquitto
echo.

echo After installation, please run this script again
echo.

:end

echo.
echo ========================================
echo MQTT setup process completed
echo ========================================
echo.
echo Next steps:
echo 1. If Mosquitto is running, you can start the ESP32 backend
echo 2. If there were errors, please fix them and run this script again
echo 3. Run start_system.bat to start the ESP32 backend
echo.
echo Press any key to close this window...
pause >nul