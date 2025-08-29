@echo off
rem 设置控制台代码页为UTF-8
chcp 65001 >nul
title MQTT连接修复工具

echo ========================================
echo MQTT连接问题修复工具
echo ========================================
echo.

echo 当前MQTT连接问题分析:
echo 1. Mosquitto服务正在运行
echo 2. 服务绑定在localhost:1883
echo 3. 配置文件使用10.1.95.252:1883
echo 4. 网络接口不匹配导致连接失败
echo.

echo 解决方案选择:
echo 1. 修改配置文件使用localhost (推荐)
echo 2. 配置Mosquitto绑定到所有网络接口
echo 3. 测试当前连接
echo.

set /p choice="请选择解决方案 (1-3): "

if "%choice%"=="1" goto fix_config
if "%choice%"=="2" goto fix_mosquitto
if "%choice%"=="3" goto test_connection
goto invalid_choice

:fix_config
echo.
echo 正在修复配置文件...
echo 将MQTT broker地址改为localhost...
echo.

rem 备份原配置文件
copy config.ini config.ini.backup
echo [INFO] 原配置文件已备份为 config.ini.backup

rem 修改配置文件
powershell -Command "(Get-Content config.ini) -replace 'broker = 10.1.95.252', 'broker = localhost' | Set-Content config.ini"
echo [SUCCESS] 配置文件已修复
echo.
echo 现在可以重新启动系统测试MQTT连接
goto end

:fix_mosquitto
echo.
echo 正在配置Mosquitto绑定到所有网络接口...
echo 这需要管理员权限...
echo.

rem 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 需要管理员权限来修改Mosquitto配置
    echo 请右键点击此脚本，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo [INFO] 正在修改Mosquitto配置...
echo listener 1883 0.0.0.0 >> "C:\Program Files\mosquitto\mosquitto.conf"
echo [SUCCESS] Mosquitto配置已修改
echo.
echo 需要重启Mosquitto服务使配置生效
set /p restart="是否现在重启服务? (y/n): "
if /i "%restart%"=="y" (
    echo 正在重启Mosquitto服务...
    net stop mosquitto
    timeout /t 2 /nobreak >nul
    net start mosquitto
    echo [SUCCESS] Mosquitto服务已重启
)
goto end

:test_connection
echo.
echo 正在测试MQTT连接...
echo.

echo 测试localhost:1883连接...
python -c "
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('[SUCCESS] MQTT连接到localhost:1883成功')
    else:
        print(f'[ERROR] MQTT连接失败，错误码: {rc}')
    client.disconnect()

def on_disconnect(client, userdata, rc):
    print('连接已断开')

client = mqtt.Client('test_client')
client.on_connect = on_connect
client.on_disconnect = on_disconnect

try:
    client.connect('localhost', 1883, 60)
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
except Exception as e:
    print(f'[ERROR] 连接异常: {e}')
"

echo.
echo 测试10.1.95.252:1883连接...
python -c "
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('[SUCCESS] MQTT连接到10.1.95.252:1883成功')
    else:
        print(f'[ERROR] MQTT连接失败，错误码: {rc}')
    client.disconnect()

def on_disconnect(client, userdata, rc):
    print('连接已断开')

client = mqtt.Client('test_client2')
client.on_connect = on_connect
client.on_disconnect = on_disconnect

try:
    client.connect('10.1.95.252', 1883, 60)
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
except Exception as e:
    print(f'[ERROR] 连接异常: {e}')
"
goto end

:invalid_choice
echo [ERROR] 无效选择，请输入1-3
goto end

:end
echo.
echo ========================================
echo 修复完成
echo ========================================
echo.
echo 建议:
echo 1. 如果选择方案1，直接重启系统即可
echo 2. 如果选择方案2，确保重启Mosquitto服务
echo 3. 运行测试确认连接正常
echo.
echo Press any key to close...
pause >nul