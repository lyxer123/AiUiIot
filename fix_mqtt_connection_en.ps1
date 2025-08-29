# MQTT Connection Fix Tool - English Version
# Set console to UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================"
Write-Host "MQTT Connection Fix Tool"
Write-Host "========================================"
Write-Host ""

Write-Host "Current MQTT Connection Issue Analysis:"
Write-Host "1. Mosquitto service is running"
Write-Host "2. Service is bound to localhost:1883"
Write-Host "3. Config file uses 10.1.95.252:1883"
Write-Host "4. Network interface mismatch causing connection failure"
Write-Host ""

Write-Host "Solution Options:"
Write-Host "1. Modify config file to use localhost (recommended)"
Write-Host "2. Configure Mosquitto to bind to all network interfaces"
Write-Host "3. Test current connection"
Write-Host ""

$choice = Read-Host "Please select a solution (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Fixing configuration file..."
        Write-Host "Changing MQTT broker address to localhost..."
        Write-Host ""

        # Backup original config file
        Copy-Item -Path "config.ini" -Destination "config.ini.backup"
        Write-Host "[INFO] Original config file backed up as config.ini.backup"

        # Modify config file
        (Get-Content "config.ini") -replace 'broker = 10.1.95.252', 'broker = localhost' | Set-Content "config.ini"
        Write-Host "[SUCCESS] Configuration file fixed"
        Write-Host ""
        Write-Host "You can now restart the system to test MQTT connection"
    }
    "2" {
        Write-Host ""
        Write-Host "Configuring Mosquitto to bind to all network interfaces..."
        Write-Host "This requires administrator privileges..."
        Write-Host ""

        # Check for admin privileges
        $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        if (-not $isAdmin) {
            Write-Host "[ERROR] Administrator privileges required to modify Mosquitto configuration" -ForegroundColor Red
            Write-Host "Please right-click this script and select 'Run as Administrator'" -ForegroundColor Red
            Write-Host ""
            Read-Host "Press Enter to exit"
            exit
        }

        Write-Host "[INFO] Modifying Mosquitto configuration..."
        Add-Content -Path "C:\Program Files\mosquitto\mosquitto.conf" -Value "listener 1883 0.0.0.0"
        Write-Host "[SUCCESS] Mosquitto configuration modified"
        Write-Host ""
        Write-Host "Mosquitto service needs to be restarted for changes to take effect"
        $restart = Read-Host "Restart service now? (y/n)"
        if ($restart -eq "y" -or $restart -eq "Y") {
            Write-Host "Restarting Mosquitto service..."
            Stop-Service -Name "mosquitto"
            Start-Sleep -Seconds 2
            Start-Service -Name "mosquitto"
            Write-Host "[SUCCESS] Mosquitto service restarted"
        }
    }
    "3" {
        Write-Host ""
        Write-Host "Testing MQTT connection..."
        Write-Host ""

        Write-Host "Testing localhost:1883 connection..."
        python -c @"
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('[SUCCESS] MQTT connection to localhost:1883 successful')
    else:
        print(f'[ERROR] MQTT connection failed, error code: {rc}')
    client.disconnect()

def on_disconnect(client, userdata, rc):
    print('Connection closed')

client = mqtt.Client('test_client')
client.on_connect = on_connect
client.on_disconnect = on_disconnect

try:
    client.connect('localhost', 1883, 60)
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
except Exception as e:
    print(f'[ERROR] Connection exception: {e}')
"@

        Write-Host ""
        Write-Host "Testing 10.1.95.252:1883 connection..."
        python -c @"
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('[SUCCESS] MQTT connection to 10.1.95.252:1883 successful')
    else:
        print(f'[ERROR] MQTT connection failed, error code: {rc}')
    client.disconnect()

def on_disconnect(client, userdata, rc):
    print('Connection closed')

client = mqtt.Client('test_client2')
client.on_connect = on_connect
client.on_disconnect = on_disconnect

try:
    client.connect('10.1.95.252', 1883, 60)
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
except Exception as e:
    print(f'[ERROR] Connection exception: {e}')
"@
    }
    default {
        Write-Host "[ERROR] Invalid choice, please enter 1-3" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host "Fix Complete"
Write-Host "========================================"
Write-Host ""
Write-Host "Recommendations:"
Write-Host "1. If you chose option 1, restart the system"
Write-Host "2. If you chose option 2, ensure Mosquitto service was restarted"
Write-Host "3. Run tests to confirm connection is working"
Write-Host ""
Read-Host "Press Enter to close"