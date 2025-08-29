@echo off
chcp 65001 >nul
title ESP32IOT 系统启动脚本

echo ========================================
echo        ESP32IOT 系统启动脚本
echo ========================================
echo.

echo 正在检查系统环境...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [信息] Python环境检查通过

REM 检查pip是否可用
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] pip不可用，请检查Python安装
    pause
    exit /b 1
)

echo [信息] pip环境检查通过

echo.
echo 正在安装/更新依赖包...
echo.

REM 安装必要的Python包
pip install paho-mqtt --upgrade
pip install pyserial --upgrade
pip install requests --upgrade

echo.
echo 依赖包安装完成
echo.

echo 请选择要启动的服务:
echo.
echo 1. 启动MQTT测试工具 (测试ESP32通信)
echo 2. 启动MQTT服务器 (需要先安装Mosquitto)
echo 3. 查看ESP32项目文件
echo 4. 退出
echo.

:menu
set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" goto start_mqtt_tester
if "%choice%"=="2" goto start_mqtt_server
if "%choice%"=="3" goto show_files
if "%choice%"=="4" goto exit
echo 无效选择，请重新输入
goto menu

:start_mqtt_tester
echo.
echo 正在启动MQTT测试工具...
echo 注意: 请确保ESP32已连接到网络并运行
echo.

REM 检查ESP32IOT.ino是否存在
if not exist "ESP32IOT.ino" (
    echo [错误] 未找到ESP32IOT.ino文件
    echo 请确保在正确的目录中运行此脚本
    pause
    goto menu
)

echo [信息] 找到ESP32项目文件
echo.
echo 请输入MQTT服务器地址 (默认: localhost):
set /p mqtt_broker="MQTT服务器: "
if "%mqtt_broker%"=="" set mqtt_broker=localhost

echo.
echo 正在启动MQTT测试工具...
echo 连接到服务器: %mqtt_broker%
echo.

python mqtt_test.py --broker %mqtt_broker%
pause
goto menu

:start_mqtt_server
echo.
echo 正在检查MQTT服务器...
echo.

REM 检查Mosquitto是否安装
mosquitto --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Mosquitto MQTT服务器
    echo 请先安装Mosquitto:
    echo Windows: https://mosquitto.org/download/
    echo 或使用: winget install mosquitto
    echo.
    echo 安装完成后重新运行此脚本
    pause
    goto menu
)

echo [信息] 找到Mosquitto MQTT服务器
echo.
echo 正在启动MQTT服务器...
echo 服务器将在后台运行，端口: 1883
echo.

REM 启动Mosquitto服务器
start /min mosquitto -c mosquitto.conf

echo MQTT服务器已启动
echo 可以使用MQTT客户端连接到 localhost:1883
echo.
pause
goto menu

:show_files
echo.
echo ESP32IOT 项目文件列表:
echo ========================================
dir /b
echo ========================================
echo.
echo 主要文件说明:
echo - ESP32IOT.ino: ESP32主程序 (Arduino代码)
echo - config.h: 配置文件
echo - platformio.ini: PlatformIO项目配置
echo - mqtt_test.py: MQTT测试工具
echo - README.md: 项目说明文档
echo.
pause
goto menu

:exit
echo.
echo 感谢使用ESP32IOT系统!
echo.
pause
exit /b 0

