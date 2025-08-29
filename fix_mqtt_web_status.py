#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Web界面MQTT状态显示问题
"""

import requests
import json
import time

def test_mqtt_status_api():
    """测试MQTT状态API"""
    print("=" * 50)
    print("测试MQTT状态API")
    print("=" * 50)
    
    base_url = "http://10.1.95.252:5000"
    
    try:
        # 测试系统状态API
        print("1. 测试系统状态API...")
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] 系统状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查MQTT状态
            if result.get('success') and 'data' in result:
                mqtt_status = result['data'].get('mqtt_connected', False)
                print(f"[INFO] MQTT状态: {'已连接' if mqtt_status else '未连接'}")
        else:
            print(f"[ERROR] 系统状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] 系统状态API测试失败: {e}")
    
    try:
        # 测试MQTT状态API
        print("\n2. 测试MQTT状态API...")
        response = requests.get(f"{base_url}/api/mqtt/status")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] MQTT状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查MQTT状态
            if result.get('success') and 'data' in result:
                mqtt_status = result['data'].get('connected', False)
                print(f"[INFO] MQTT连接状态: {'已连接' if mqtt_status else '未连接'}")
        else:
            print(f"[ERROR] MQTT状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] MQTT状态API测试失败: {e}")
    
    try:
        # 测试IO1当前状态API
        print("\n3. 测试IO1当前状态API...")
        response = requests.get(f"{base_url}/api/io1/current")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] IO1状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"[ERROR] IO1状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] IO1状态API测试失败: {e}")

def check_mqtt_client_status():
    """检查MQTT客户端状态"""
    print("\n" + "=" * 50)
    print("检查MQTT客户端状态")
    print("=" * 50)
    
    try:
        # 导入MQTT客户端模块
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from mqtt_client import MQTTClient
        from database import DatabaseManager
        
        print("[INFO] 正在创建MQTT客户端实例...")
        
        # 创建数据库管理器
        db_manager = DatabaseManager("esp32_data.db")
        
        # 创建MQTT客户端
        mqtt_client = MQTTClient("config.ini", db_manager)
        
        print(f"[INFO] MQTT客户端创建成功")
        print(f"[INFO] Broker地址: {mqtt_client.broker}")
        print(f"[INFO] Broker端口: {mqtt_client.port}")
        print(f"[INFO] 客户端ID: {mqtt_client.client_id}")
        
        # 检查连接状态
        print(f"[INFO] 当前连接状态: {mqtt_client.connected}")
        
        # 尝试连接
        print("[INFO] 正在尝试连接...")
        mqtt_client.connect()
        
        # 等待连接
        time.sleep(3)
        
        # 再次检查状态
        print(f"[INFO] 连接后状态: {mqtt_client.connected}")
        print(f"[INFO] get_connection_status(): {mqtt_client.get_connection_status()}")
        
        # 测试发布消息
        if mqtt_client.connected:
            print("[INFO] 测试发布状态消息...")
            success = mqtt_client.publish_status("test")
            print(f"[INFO] 发布结果: {success}")
        
        # 断开连接
        mqtt_client.disconnect()
        print("[INFO] MQTT客户端已断开")
        
    except Exception as e:
        print(f"[ERROR] 检查MQTT客户端状态失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("Web界面MQTT状态修复工具")
    print("=" * 50)
    
    # 测试API接口
    test_mqtt_status_api()
    
    # 检查MQTT客户端状态
    check_mqtt_client_status()
    
    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)
    
    print("\n可能的问题和解决方案:")
    print("1. 如果API返回正确的MQTT状态，问题在Web界面JavaScript")
    print("2. 如果API返回错误的MQTT状态，问题在MQTT客户端状态管理")
    print("3. 如果MQTT客户端状态正确，问题在Web服务器状态传递")

if __name__ == "__main__":
    main()


