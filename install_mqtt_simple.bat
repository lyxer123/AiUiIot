@echo off
chcp 65001 >nul
title MQTT Setup
echo ========================================
echo MQTT Broker Setup
echo ========================================
echo.

echo Checking Mosquitto installation...
echo.

if exist "C:\Program Files\mosquitto\mosquitto.exe" (
    echo [SUCCESS] Mosquitto found in Program Files
    echo Starting service...
    net start mosquitto
    if %errorlevel% == 0 (
        echo [SUCCESS] Service started
    ) else (
        echo [ERROR] Failed to start service
        echo Try running as Administrator
    )
) else if exist "C:\Program Files (x86)\mosquitto\mosquitto.exe" (
    echo [SUCCESS] Mosquitto found in Program Files (x86)
    echo Starting service...
    net start mosquitto
    if %errorlevel% == 0 (
        echo [SUCCESS] Service started
    ) else (
        echo [ERROR] Failed to start service
        echo Try running as Administrator
    )
) else (
    echo [ERROR] Mosquitto not found
    echo Please install from: https://mosquitto.org/download/
    echo Make sure to select "Service" option during installation
)

echo.
echo ========================================
echo Setup completed
echo ========================================
echo.
echo Press any key to close...
pause >nul
