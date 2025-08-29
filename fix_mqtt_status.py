#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MQTT状态检查修复脚本
用于诊断和修复MQTT连接状态显示问题
"""

import paho.mqtt.client as mqtt
import time
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_mqtt_connection():
    """测试MQTT连接"""
    print("=" * 50)
    print("MQTT连接测试")
    print("=" * 50)
    
    # 创建测试客户端
    client = mqtt.Client('test_client')
    connected = False
    
    def on_connect(client, userdata, flags, rc):
        nonlocal connected
        if rc == 0:
            connected = True
            print(f"[SUCCESS] MQTT连接成功，返回码: {rc}")
            print(f"[INFO] 连接标志: {flags}")
        else:
            print(f"[ERROR] MQTT连接失败，返回码: {rc}")
    
    def on_disconnect(client, userdata, rc):
        nonlocal connected
        connected = False
        print(f"[INFO] MQTT连接断开，返回码: {rc}")
    
    def on_message(client, userdata, msg):
        print(f"[INFO] 收到消息: {msg.topic} -> {msg.payload.decode()}")
    
    # 设置回调
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    try:
        print("[INFO] 正在连接到 localhost:1883...")
        client.connect('localhost', 1883, 60)
        client.loop_start()
        
        # 等待连接
        timeout = 10
        start_time = time.time()
        while not connected and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        if connected:
            print("[SUCCESS] MQTT连接测试通过")
            
            # 测试发布消息
            test_topic = "test/connection"
            test_message = {"test": True, "timestamp": time.time()}
            result = client.publish(test_topic, json.dumps(test_message))
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[SUCCESS] 测试消息发布成功: {test_topic}")
            else:
                print(f"[ERROR] 测试消息发布失败，返回码: {result.rc}")
            
            # 测试订阅
            client.subscribe("esp32/status")
            print("[INFO] 已订阅 esp32/status 主题")
            
            # 等待一段时间接收消息
            time.sleep(3)
            
        else:
            print("[ERROR] MQTT连接超时")
            
    except Exception as e:
        print(f"[ERROR] MQTT连接异常: {e}")
    
    finally:
        client.loop_stop()
        client.disconnect()
        print("[INFO] 测试客户端已断开")

def check_mqtt_broker_status():
    """检查MQTT broker状态"""
    print("\n" + "=" * 50)
    print("MQTT Broker状态检查")
    print("=" * 50)
    
    import subprocess
    import sys
    
    try:
        # 检查Mosquitto服务状态
        result = subprocess.run(['sc', 'query', 'mosquitto'], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print("[SUCCESS] Mosquitto服务查询成功")
            if "RUNNING" in result.stdout:
                print("[SUCCESS] Mosquitto服务正在运行")
            else:
                print("[WARNING] Mosquitto服务状态异常")
                print(result.stdout)
        else:
            print("[ERROR] 无法查询Mosquitto服务状态")
            
    except Exception as e:
        print(f"[ERROR] 检查服务状态失败: {e}")
    
    try:
        # 检查端口监听状态
        result = subprocess.run(['netstat', '-an'], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            if ":1883" in result.stdout:
                print("[SUCCESS] 端口1883正在监听")
                # 显示相关行
                for line in result.stdout.split('\n'):
                    if ':1883' in line:
                        print(f"  {line.strip()}")
            else:
                print("[ERROR] 端口1883未监听")
        else:
            print("[ERROR] 无法检查端口状态")
            
    except Exception as e:
        print(f"[ERROR] 检查端口状态失败: {e}")

def main():
    """主函数"""
    print("MQTT状态诊断和修复工具")
    print("=" * 50)
    
    # 检查MQTT broker状态
    check_mqtt_broker_status()
    
    # 测试MQTT连接
    test_mqtt_connection()
    
    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)
    
    print("\n建议:")
    print("1. 如果MQTT连接测试成功，问题可能在Web界面状态检查逻辑")
    print("2. 如果连接失败，检查Mosquitto服务配置")
    print("3. 检查防火墙设置是否阻止了1883端口")

if __name__ == "__main__":
    main()


