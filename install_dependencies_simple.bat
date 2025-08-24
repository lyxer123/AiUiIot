@echo off
chcp 65001 >nul
title Install Dependencies
echo ========================================
echo Installing Python Dependencies
echo ========================================
echo.

echo Installing required packages...
echo.

pip install paho-mqtt==1.6.1
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install schedule==1.2.0

echo.
echo ========================================
echo Installation completed
echo ========================================
echo.
echo Press any key to close...
pause >nul
