@echo off
chcp 65001 >nul
title ESP32IOT 编译测试

echo ========================================
echo        ESP32IOT 编译测试
echo ========================================
echo.

echo 正在检查PlatformIO环境...
echo.

REM 检查PlatformIO是否安装
pio --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到PlatformIO
    echo 请先安装PlatformIO Core:
    echo pip install platformio
    pause
    exit /b 1
)

echo [信息] PlatformIO环境检查通过
echo.

echo 正在检查项目配置...
echo.

REM 检查platformio.ini是否存在
if not exist "platformio.ini" (
    echo [错误] 未找到platformio.ini文件
    pause
    exit /b 1
)

echo [信息] 找到platformio.ini配置文件
echo.

echo 正在检查依赖库...
echo.

REM 安装依赖库
echo 安装ArduinoJson库...
pio lib install "bblanchon/ArduinoJson@^6.21.3"

echo 安装PubSubClient库...
pio lib install "knolleary/PubSubClient@^2.8"

echo.
echo 依赖库安装完成
echo.

echo 正在尝试编译项目...
echo.

REM 尝试编译
pio run

if errorlevel 1 (
    echo.
    echo [错误] 编译失败！
    echo.
    echo 可能的原因:
    echo 1. 依赖库版本不兼容
    echo 2. ESP32开发板配置错误
    echo 3. 代码语法错误
    echo.
    echo 建议尝试:
    echo 1. 使用简化版本: main_simple.cpp
    echo 2. 检查platformio.ini配置
    echo 3. 查看详细错误信息
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo [成功] 编译成功！
    echo.
    echo 下一步操作:
    echo 1. 连接ESP32开发板
    echo 2. 运行: pio run --target upload
    echo 3. 监控输出: pio device monitor
    echo.
)

pause

