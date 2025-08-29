@echo off
chcp 65001 >nul
title ESP32IOT 编译测试 - 修复版本

echo ========================================
echo    ESP32IOT 编译测试 - 修复版本
echo ========================================
echo.

echo 正在检查项目配置...
echo.

REM 检查必要文件
if not exist "src\main.cpp" (
    echo [错误] 未找到 src\main.cpp
    pause
    exit /b 1
)

if not exist "platformio.ini" (
    echo [错误] 未找到 platformio.ini
    pause
    exit /b 1
)

if not exist "config.h" (
    echo [错误] 未找到 config.h
    pause
    exit /b 1
)

echo [信息] 项目文件检查通过
echo.

echo 正在检查PlatformIO环境...
echo.

REM 检查PlatformIO
pio --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到PlatformIO
    echo 请先安装: pip install platformio
    pause
    exit /b 1
)

echo [信息] PlatformIO环境检查通过
echo.

echo 正在清理之前的编译文件...
echo.

REM 清理编译文件
pio run --target clean

echo [信息] 清理完成
echo.

echo 正在尝试编译项目...
echo.

REM 尝试编译
pio run

if errorlevel 1 (
    echo.
    echo [错误] 编译仍然失败！
    echo.
    echo 请检查错误信息，可能的原因:
    echo 1. 依赖库版本不兼容
    echo 2. ESP32开发板配置错误
    echo 3. 代码中还有其他语法错误
    echo.
    echo 建议:
    echo 1. 查看详细错误信息
    echo 2. 使用简化版本测试: main_simple.cpp
    echo 3. 检查TROUBLESHOOTING.md
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo [成功] 编译成功！问题已修复！
    echo.
    echo 下一步操作:
    echo 1. 连接ESP32开发板
    echo 2. 运行: pio run --target upload
    echo 3. 监控输出: pio device monitor
    echo.
    echo 如果上传成功，您应该看到:
    echo - ESP32IOT系统启动信息
    echo - WiFi连接状态
    echo - MQTT连接状态
    echo - LED状态指示
    echo.
)

pause
