@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title ESP32后台系统
echo ========================================
echo ESP32数据采集和控制系统
echo ========================================
echo "功能: 北向采集AD1数据，南向控制IO1开关"
echo "协议: MQTT + JSON"
echo "注意: ESP32模拟器功能已禁用"
echo ========================================
echo.

echo 正在检查系统环境...
echo.

echo 1. 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Python未安装或未添加到PATH
    echo 请先运行 install_dependencies.bat 安装依赖
    echo.
    pause
    exit /b 1
)
echo [成功] Python环境正常
echo.

echo 2. 检查MQTT代理...
echo 正在检查Mosquitto安装状态...
timeout /t 3 /nobreak >nul 2>&1

REM 使用更快的检查方法
if exist "C:\Program Files\mosquitto\mosquitto.exe" (
    echo [成功] MQTT代理已安装 (Program Files)
    set MOSQUITTO_PATH="C:\Program Files\mosquitto\mosquitto.exe"
) else if exist "C:\Program Files (x86)\mosquitto\mosquitto.exe" (
    echo [成功] MQTT代理已安装 (Program Files x86)
    set MOSQUITTO_PATH="C:\Program Files (x86)\mosquitto\mosquitto.exe"
) else (
    echo [警告] Mosquitto MQTT代理未安装
    echo 请先运行 install_mqtt.bat 安装MQTT代理
    echo.
    echo 是否继续启动系统？(y/n)
    set /p choice=
    if /i "!choice!" neq "y" (
        echo 系统启动已取消
        pause
        exit /b 1
    )
    echo 跳过MQTT检查，继续启动系统...
    goto :skip_mqtt
)

echo [成功] MQTT代理已安装
echo 正在启动MQTT服务...
net start mosquitto >nul 2>&1
if %errorlevel% == 0 (
    echo [成功] MQTT服务已启动
) else (
    echo [警告] MQTT服务启动失败，错误代码: %errorlevel%
    if %errorlevel% == 2 (
        echo [错误] 系统找不到指定的文件 - Mosquitto服务未安装
        echo.
        echo 解决方案：
        echo 1. 重新安装Mosquitto，确保选择"Service"选项
        echo 2. 或者手动安装服务：
echo    - 以管理员身份打开命令提示符
echo    - 运行: sc create mosquitto binPath= "C:\Program Files\mosquitto\mosquitto.exe -v" start= auto
echo    - 然后运行: net start mosquitto
        echo.
        echo 3. 检查服务是否已安装：
        echo    - 按 Win+R，输入 services.msc
        echo    - 查找是否有 "mosquitto" 服务
    ) else if %errorlevel% == 5 (
        echo [错误] 权限不足，请以管理员身份运行此脚本
        echo 右键点击脚本 -> "以管理员身份运行"
    ) else if %errorlevel% == 1060 (
        echo [信息] 服务未配置为自动启动，正在尝试手动启动...
        sc start mosquitto >nul 2>&1
        if !errorlevel! == 0 (
            echo [成功] MQTT服务手动启动成功
        ) else (
            echo [错误] MQTT服务启动失败
        )
    ) else (
        echo [信息] 可能服务已在运行，正在检查状态...
        sc query mosquitto >nul 2>&1
        if %errorlevel! == 0 (
            sc query mosquitto | find "RUNNING" >nul 2>&1
            if %errorlevel! == 0 (
                echo [成功] MQTT服务已在运行
            ) else (
                echo [信息] MQTT服务已安装但未运行，正在尝试启动...
                sc start mosquitto >nul 2>&1
                if !errorlevel! == 0 (
                    echo [成功] MQTT服务启动成功
                ) else (
                    echo [错误] MQTT服务启动失败
                )
            )
        ) else (
            echo [错误] MQTT服务未安装，请重新安装Mosquitto
        )
    )
)

:skip_mqtt
echo.

echo 3. 检查Python依赖...
python -c "import paho.mqtt.client, flask, flask_cors, schedule" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Python依赖包未安装
    echo 请先运行 install_dependencies.bat 安装依赖
    echo.
    pause
    exit /b 1
)
echo [成功] Python依赖包已安装
echo.

echo 4. 检查配置文件...
if not exist "config.ini" (
    echo [错误] 配置文件 config.ini 不存在
    echo.
    pause
    exit /b 1
)
echo [成功] 配置文件存在
echo.

echo 所有检查完成，正在启动系统...
echo.
echo 系统启动后，Web界面地址: http://localhost:5000
echo 按 Ctrl+C 停止系统
echo.

echo 正在启动ESP32后台系统...
python main.py

echo.
echo 系统已停止
pause
