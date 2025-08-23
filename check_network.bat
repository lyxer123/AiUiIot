@echo off
chcp 65001 >nul
title ESP32小程序网络配置检查
echo ========================================
echo ESP32小程序网络配置检查工具
echo ========================================
echo.

echo 正在检查网络配置...
echo.

REM 获取本机IP地址
echo 1. 本机IP地址信息:
echo ----------------------------------------
ipconfig | findstr "IPv4"
echo.

REM 检查5000端口是否被监听
echo 2. 检查5000端口状态:
echo ----------------------------------------
netstat -an | findstr ":5000"
if %errorlevel% == 0 (
    echo [成功] 端口5000正在监听
) else (
    echo [错误] 端口5000未监听，请先启动后端服务
    echo 运行命令: python main.py
)
echo.

REM 检查防火墙设置
echo 3. 检查Windows防火墙设置:
echo ----------------------------------------
netsh advfirewall firewall show rule name="ESP32 Backend" >nul 2>&1
if %errorlevel% == 0 (
    echo [信息] 发现ESP32后端防火墙规则
) else (
    echo [提示] 建议添加防火墙规则允许5000端口
    echo 运行命令: netsh advfirewall firewall add rule name="ESP32 Backend" dir=in action=allow protocol=TCP localport=5000
)
echo.

REM 显示网络配置建议
echo 4. 小程序网络配置建议:
echo ----------------------------------------
echo 在 miniprogram/app.js 中修改以下配置:
echo.
echo serverConfig: {
echo   baseUrl: 'http://YOUR_IP:5000/api',
echo   timeout: 10000
echo }
echo.
echo 将 YOUR_IP 替换为上面显示的IPv4地址
echo.

REM 检查网络连通性
echo 5. 网络连通性测试:
echo ----------------------------------------
echo 请在其他设备上测试以下命令:
echo ping YOUR_IP
echo telnet YOUR_IP 5000
echo.

echo 6. 常见问题解决:
echo ----------------------------------------
echo 问题1: 小程序无法连接服务器
echo 解决: 确保手机和电脑在同一WiFi网络
echo.
echo 问题2: 连接超时
echo 解决: 检查防火墙设置，允许5000端口
echo.
echo 问题3: 数据不更新
echo 解决: 检查后端服务是否正常运行
echo.

echo ========================================
echo 配置检查完成！
echo ========================================
echo.
echo 请根据以上信息配置小程序
echo 如有问题，请检查网络连接和防火墙设置
echo.
echo 按任意键退出...
pause >nul
