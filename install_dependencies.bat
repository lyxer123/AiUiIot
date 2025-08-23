@echo off
chcp 65001 >nul
echo ========================================
echo ESP32后台系统 - Python依赖安装脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安装或未添加到PATH环境变量
    echo 请先安装Python 3.7+版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python环境检查通过
python --version
echo.

echo 正在检查pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip未安装，正在尝试安装...
    python -m ensurepip --upgrade
)

echo 正在安装Python依赖包...
echo.

echo 安装paho-mqtt...
pip install paho-mqtt==1.6.1

echo 安装Flask...
pip install flask==2.3.3

echo 安装Flask-CORS...
pip install flask-cors==4.0.0

echo 安装schedule...
pip install schedule==1.2.0

echo.
echo 所有依赖包安装完成！
echo.

echo 正在验证安装...
python -c "import paho.mqtt.client; import flask; import flask_cors; import schedule; print('所有模块导入成功！')"

if %errorlevel% == 0 (
    echo.
    echo 依赖安装验证成功！
) else (
    echo.
    echo 依赖安装验证失败，请检查错误信息
)

echo.
echo 按任意键退出...
pause >nul
