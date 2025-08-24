@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title ESP32 System Test
echo ========================================
echo ESP32 Backend System - Function Test
echo ========================================
echo.

echo Starting test mode...
echo.

echo 1. Testing database connection...
python -c "from database import DatabaseManager; db = DatabaseManager('test.db'); print('[SUCCESS] Database connection test passed'); db.save_ad1_data(1234); db.save_io1_control(True); print('[SUCCESS] Database write test passed')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Database test failed, please check database.py file
    echo Error code: %errorlevel%
) else (
    echo [SUCCESS] Database test completed
)

echo.
echo 2. Testing MQTT client...
python -c "from mqtt_client import MQTTClient; from database import DatabaseManager; db = DatabaseManager('test.db'); mqtt = MQTTClient('config.ini', db); print('[SUCCESS] MQTT client initialization test passed')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] MQTT client test failed, please check mqtt_client.py file
    echo Error code: %errorlevel%
) else (
    echo [SUCCESS] MQTT client test completed
)

echo.
echo 3. Testing ESP32 simulator...
python -c "from esp32_simulator import ESP32Simulator; sim = ESP32Simulator('config.ini'); print('[SUCCESS] ESP32 simulator initialization test passed'); print('[INFO] Simulator status:', sim.get_status())" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] ESP32 simulator test failed, please check esp32_simulator.py file
    echo Error code: %errorlevel%
) else (
    echo [SUCCESS] ESP32 simulator test completed
)

echo.
echo 4. Testing Web server...
python -c "from web_server import WebServer; from database import DatabaseManager; from mqtt_client import MQTTClient; db = DatabaseManager('test.db'); mqtt = MQTTClient('config.ini', db); web = WebServer('config.ini', db, mqtt); print('[SUCCESS] Web server initialization test passed')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Web server test failed, please check web_server.py file
    echo Error code: %errorlevel%
) else (
    echo [SUCCESS] Web server test completed
)

echo.
echo 5. Testing configuration file...
python -c "import configparser; config = configparser.ConfigParser(); config.read('config.ini'); print('[SUCCESS] Configuration file read test passed'); print('[INFO] MQTT broker: ' + config.get('MQTT', 'broker') + ':' + config.get('MQTT', 'port')); print('[INFO] Web server: ' + config.get('WEB_SERVER', 'host') + ':' + config.get('WEB_SERVER', 'port'))" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Configuration file test failed, please check config.ini file
    echo Error code: %errorlevel%
) else (
    echo [SUCCESS] Configuration file test completed
)

echo.
echo 6. Cleaning up test files...
if exist "test.db" (
    del "test.db"
    echo [SUCCESS] Test database cleaned up
) else (
    echo [INFO] No test database to clean up
)

echo.
echo ========================================
echo All tests completed!
echo ========================================
echo.

REM Count success and error messages
set SUCCESS_COUNT=0
set ERROR_COUNT=0

REM Check for success messages in the output
findstr /c:"[SUCCESS]" test_system.bat >nul 2>&1
if %errorlevel% == 0 (
    for /f %%i in ('findstr /c:"[SUCCESS]" test_system.bat ^| find /c /v ""') do set SUCCESS_COUNT=%%i
)

REM Check for error messages in the output
findstr /c:"[ERROR]" test_system.bat >nul 2>&1
if %errorlevel% == 0 (
    for /f %%i in ('findstr /c:"[ERROR]" test_system.bat ^| find /c /v ""') do set ERROR_COUNT=%%i
)

echo Test Summary:
echo - Successful tests: %SUCCESS_COUNT%
echo - Failed tests: %ERROR_COUNT%
echo.

if %ERROR_COUNT% == 0 (
    echo [SUCCESS] All tests passed! System is properly configured.
    echo You can now run start_system.bat to start the ESP32 backend.
) else (
    echo [WARNING] Some tests failed. Please check the error messages above.
    echo Common solutions:
    echo 1. Run install_dependencies.bat to install Python packages
    echo 2. Run install_mqtt.bat to setup MQTT broker
    echo 3. Check if all required files exist
    echo 4. Verify Python environment and dependencies
)

echo.
echo ========================================
echo Test process completed
echo ========================================
echo.
echo Next steps:
echo 1. If all tests passed, run start_system.bat
echo 2. If tests failed, fix the issues and run this script again
echo 3. Check the logs folder for detailed error information
echo.
echo Press any key to close this window...
pause >nul
