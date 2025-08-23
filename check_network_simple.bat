@echo off
title ESP32 Network Check
echo ========================================
echo ESP32 Mini Program Network Check
echo ========================================
echo.

echo Checking network configuration...
echo.

echo 1. Local IP Address:
echo ----------------------------------------
ipconfig | findstr "IPv4"
echo.

echo 2. Port 5000 Status:
echo ----------------------------------------
netstat -an | findstr ":5000"
if %errorlevel% == 0 (
    echo [SUCCESS] Port 5000 is listening
) else (
    echo [ERROR] Port 5000 is not listening
    echo Please start backend service: python main.py
)
echo.

echo 3. Mini Program Configuration:
echo ----------------------------------------
echo Please modify miniprogram/app.js:
echo.
echo serverConfig: {
echo   baseUrl: 'http://10.1.95.252:5000/api',
echo   timeout: 10000
echo }
echo.

echo 4. Network Test:
echo ----------------------------------------
echo Test from other devices:
echo ping 10.1.95.252
echo telnet 10.1.95.252 5000
echo.

echo 5. Troubleshooting:
echo ----------------------------------------
echo Problem: Cannot connect to server
echo Solution: Ensure phone and PC are on same WiFi
echo.
echo Problem: Connection timeout
echo Solution: Check firewall settings for port 5000
echo.
echo Problem: Data not updating
echo Solution: Check if backend service is running
echo.

echo ========================================
echo Configuration check completed!
echo ========================================
echo.
echo Please configure the mini program according to the above information
echo If you have problems, check network connection and firewall settings
echo.
echo Press any key to exit...
pause >nul
