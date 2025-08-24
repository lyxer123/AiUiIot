@echo off
chcp 65001 >nul
title ESP32后台系统测试
echo ========================================
echo ESP32后台系统 - 功能测试脚本
echo ========================================
echo.

echo 正在启动测试模式...
echo.

echo 1. 测试数据库连接...
python -c "from database import DatabaseManager; db = DatabaseManager('test.db'); print('[成功] 数据库连接测试通过'); db.save_ad1_data(1234); db.save_io1_control(True); print('[成功] 数据库写入测试通过')" 2>nul
if %errorlevel% neq 0 (
    echo [错误] 数据库测试失败，请检查database.py文件
)

echo.
echo 2. 测试MQTT客户端...
python -c "from mqtt_client import MQTTClient; from database import DatabaseManager; db = DatabaseManager('test.db'); mqtt = MQTTClient('config.ini', db); print('[成功] MQTT客户端初始化测试通过')" 2>nul
if %errorlevel% neq 0 (
    echo [错误] MQTT客户端测试失败，请检查mqtt_client.py文件
)

echo.
echo 3. 测试ESP32模拟器...
python -c "from esp32_simulator import ESP32Simulator; sim = ESP32Simulator('config.ini'); print('[成功] ESP32模拟器初始化测试通过'); print('[信息] 模拟器状态:', sim.get_status())" 2>nul
if %errorlevel% neq 0 (
    echo [错误] ESP32模拟器测试失败，请检查esp32_simulator.py文件
)

echo.
echo 4. 测试Web服务器...
python -c "from web_server import WebServer; from database import DatabaseManager; from mqtt_client import MQTTClient; db = DatabaseManager('test.db'); mqtt = MQTTClient('config.ini', db); web = WebServer('config.ini', db, mqtt); print('[成功] Web服务器初始化测试通过')" 2>nul
if %errorlevel% neq 0 (
    echo [错误] Web服务器测试失败，请检查web_server.py文件
)

echo.
echo 5. 测试配置文件...
python -c "import configparser; config = configparser.ConfigParser(); config.read('config.ini'); print('[成功] 配置文件读取测试通过'); print('[信息] MQTT代理: ' + config.get('MQTT', 'broker') + ':' + config.get('MQTT', 'port')); print('[信息] Web服务器: ' + config.get('WEB_SERVER', 'host') + ':' + config.get('WEB_SERVER', 'port'))" 2>nul
if %errorlevel% neq 0 (
    echo [错误] 配置文件测试失败，请检查config.ini文件
)

echo.
echo 6. 清理测试文件...
if exist "test.db" (
    del "test.db"
    echo [成功] 测试数据库已清理
)

echo.
echo ========================================
echo 所有测试完成！
echo ========================================
echo.
echo 如果所有测试都显示[成功]，说明系统配置正确
echo 如果出现[错误]，请检查相应的配置和依赖
echo.
echo 按任意键退出...
pause >nul
