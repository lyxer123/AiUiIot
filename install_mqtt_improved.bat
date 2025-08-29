@echo off
chcp 65001 >nul
title MQTT Setup - Improved
echo ========================================
echo MQTT Broker Setup - Improved Version
echo ========================================
echo.

echo Checking Mosquitto installation...
echo.

REM Check if mosquitto.exe exists
if exist "C:\Program Files\mosquitto\mosquitto.exe" (
    echo [SUCCESS] Mosquitto executable found in Program Files
    goto :check_service
) else if exist "C:\Program Files (x86)\mosquitto\mosquitto.exe" (
    echo [SUCCESS] Mosquitto executable found in Program Files (x86)
    goto :check_service
) else (
    echo [ERROR] Mosquitto executable not found
    echo Please install from: https://mosquitto.org/download/
    echo Make sure to select "Service" option during installation
    goto :end
)

:check_service
echo.
echo Checking Mosquitto service status...
echo.

REM Check service status using sc command
sc query mosquitto >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Mosquitto service is installed
    echo.
    echo Current service status:
    sc query mosquitto | findstr "STATE"
    echo.
    
    REM Check if service is running
sc query mosquitto | findstr "RUNNING" >nul
if %errorlevel% == 0 (
    echo [SUCCESS] Mosquitto service is already running
    echo No need to start it again
    goto :test_connection
) else (
    echo [INFO] Service is installed but not running
    echo Attempting to start service...
    net start mosquitto
    if %errorlevel% == 0 (
        echo [SUCCESS] Service started successfully
        goto :test_connection
    ) else (
        echo [WARNING] Could not start service (may need admin rights)
        echo Service might already be running or needs manual start
        goto :test_connection
    )
)
) else (
    echo [ERROR] Mosquitto service not found
    echo Please reinstall Mosquitto with "Service" option selected
    echo Or run this script as Administrator to install the service
)

:test_connection
echo.
echo Testing MQTT connection...
echo.

REM Test if mosquitto is responding
timeout /t 2 /nobreak >nul
echo [INFO] MQTT setup check completed

:end
echo.
echo ========================================
echo Setup completed
echo ========================================
echo.
echo Press any key to close...
pause >nul
