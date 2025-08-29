# MQTT连接修复工具 - PowerShell版本
# 设置控制台为UTF-8编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================"
Write-Host "MQTT连接问题修复工具"
Write-Host "========================================"
Write-Host ""

Write-Host "当前MQTT连接问题分析:"
Write-Host "1. Mosquitto服务正在运行"
Write-Host "2. 服务绑定在localhost:1883"
Write-Host "3. 配置文件使用10.1.95.252:1883"
Write-Host "4. 网络接口不匹配导致连接失败"
Write-Host ""

Write-Host "解决方案选择:"
Write-Host "1. 修改配置文件使用localhost (推荐)"
Write-Host "2. 配置Mosquitto绑定到所有网络接口"
Write-Host "3. 测试当前连接"
Write-Host ""

$choice = Read-Host "请选择解决方案 (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "正在修复配置文件..."
        Write-Host "将MQTT broker地址改为localhost..."
        Write-Host ""

        # 备份原配置文件
        Copy-Item -Path "config.ini" -Destination "config.ini.backup"
        Write-Host "[INFO] 原配置文件已备份为 config.ini.backup"

        # 修改配置文件
        (Get-Content "config.ini") -replace 'broker = 10.1.95.252', 'broker = localhost' | Set-Content "config.ini"
        Write-Host "[SUCCESS] 配置文件已修复"
        Write-Host ""
        Write-Host "现在可以重新启动系统测试MQTT连接"
    }
    "2" {
        Write-Host ""
        Write-Host "正在配置Mosquitto绑定到所有网络接口..."
        Write-Host "这需要管理员权限..."
        Write-Host ""

        # 检查管理员权限
        $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        if (-not $isAdmin) {
            Write-Host "[ERROR] 需要管理员权限来修改Mosquitto配置" -ForegroundColor Red
            Write-Host "请右键点击此脚本，选择'以管理员身份运行'" -ForegroundColor Red
            Write-Host ""
            Read-Host "按Enter键退出"
            exit
        }

        Write-Host "[INFO] 正在修改Mosquitto配置..."
        Add-Content -Path "C:\Program Files\mosquitto\mosquitto.conf" -Value "listener 1883 0.0.0.0"
        Write-Host "[SUCCESS] Mosquitto配置已修改"
        Write-Host ""
        Write-Host "需要重启Mosquitto服务使配置生效"
        $restart = Read-Host "是否现在重启服务? (y/n)"
        if ($restart -eq "y" -or $restart -eq "Y") {
            Write-Host "正在重启Mosquitto服务..."
            Stop-Service -Name "mosquitto"
            Start-Sleep -Seconds 2
            Start-Service -Name "mosquitto"
            Write-Host "[SUCCESS] Mosquitto服务已重启"
        }
    }
    "3" {
        Write-Host ""
        Write-Host "正在测试MQTT连接..."
        Write-Host ""

        Write-Host "测试localhost:1883连接..."
        python -c @"
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
"@

        Write-Host ""
        Write-Host "测试10.1.95.252:1883连接..."
        python -c @"
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
"@
    }
    default {
        Write-Host "[ERROR] 无效选择，请输入1-3" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host "修复完成"
Write-Host "========================================"
Write-Host ""
Write-Host "建议:"
Write-Host "1. 如果选择方案1，直接重启系统即可"
Write-Host "2. 如果选择方案2，确保重启Mosquitto服务"
Write-Host "3. 运行测试确认连接正常"
Write-Host ""
Read-Host "按Enter键关闭"