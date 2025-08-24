@echo off
chcp 65001 >nul
title ESP32 Network Check
echo ========================================
echo ESP32 Network Configuration Check Tool
echo ========================================
echo.

echo Checking network configuration...
echo.

REM Get local IP address
echo 1. Local IP Address Information:
echo ----------------------------------------
ipconfig | findstr "IPv4"
echo.

REM Check if port 5000 is listening
echo 2. Check Port 5000 Status:
echo ----------------------------------------
netstat -an | findstr ":5000"
if %errorlevel% == 0 (
    echo [SUCCESS] Port 5000 is listening
) else (
    echo [ERROR] Port 5000 is not listening, please start backend service first
    echo Run command: python main.py
)
echo.

REM Check firewall settings
echo 3. Check Windows Firewall Settings:
echo ----------------------------------------
netsh advfirewall firewall show rule name="ESP32 Backend" >nul 2>&1
if %errorlevel% == 0 (
    echo [INFO] Found ESP32 backend firewall rule
) else (
    echo [TIP] Recommend adding firewall rule to allow port 5000
    echo Run command: netsh advfirewall firewall add rule name="ESP32 Backend" dir=in action=allow protocol=TCP localport=5000
)
echo.

REM Show network configuration suggestions
echo 4. Mini Program Network Configuration:
echo ----------------------------------------
echo In miniprogram/app.js, modify the following configuration:
echo.
echo serverConfig: {
echo   baseUrl: 'http://YOUR_IP:5000/api',
echo   timeout: 10000
echo }
echo.
echo Replace YOUR_IP with the IPv4 address shown above
echo.

REM Check network connectivity
echo 5. Network Connectivity Test:
echo ----------------------------------------
echo Please test the following commands on other devices:
echo ping YOUR_IP
echo telnet YOUR_IP 5000
echo.

echo 6. Common Issues and Solutions:
echo ----------------------------------------
echo Issue 1: Mini program cannot connect to server
echo Solution: Ensure phone and computer are on the same WiFi network
echo.
echo Issue 2: Connection timeout
echo Solution: Check firewall settings, allow port 5000
echo.
echo Issue 3: Data not updating
echo Solution: Check if backend service is running normally
echo.

echo ========================================
echo Configuration check completed!
echo ========================================
echo.
echo Please configure the mini program according to the above information
echo If there are issues, check network connection and firewall settings
echo.
echo Press any key to exit...
pause >nul
