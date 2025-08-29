@echo off
chcp 65001 >nul
echo ========================================
echo ESP32后台系统重启脚本 (应用MQTT修复)
echo ========================================
echo.

echo [INFO] 正在停止当前系统...
echo [INFO] 请按 Ctrl+C 停止当前运行的ESP32后台系统
echo [INFO] 等待5秒后自动重启...
timeout /t 5 /nobreak >nul

echo.
echo [INFO] 正在启动修复后的系统...
echo [INFO] 使用启动脚本: start_system_smart.bat
echo.

call start_system_smart.bat

echo.
echo [INFO] 系统重启完成
echo [INFO] 请刷新Web界面检查MQTT状态
echo [INFO] 按任意键退出...
pause >nul



