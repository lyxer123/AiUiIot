@echo off
chcp 65001 >nul
echo ========================================
echo ESP32后台系统 - 动态IP配置启动脚本
echo ========================================
echo.

echo 正在检测本机IP地址...
python -c "import socket; print('本机IP地址:', socket.gethostbyname(socket.gethostname()))"

echo.
echo 正在更新IP配置...
python ip_config.py

echo.
echo 正在启动ESP32后台系统...
python main.py

pause



