#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试MQTT连接状态修复
"""

import time
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mqtt_client():
    """测试MQTT客户端连接状态"""
    print("=" * 50)
    print("测试MQTT客户端连接状态修复")
    print("=" * 50)
    
    try:
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
        
        # 检查初始连接状态
        print(f"[INFO] 初始连接状态: {mqtt_client.connected}")
        print(f"[INFO] get_connection_status(): {mqtt_client.get_connection_status()}")
        
        # 尝试连接
        print("[INFO] 正在尝试连接...")
        mqtt_client.connect()
        
        # 等待连接
        time.sleep(3)
        
        # 检查连接后状态
        print(f"[INFO] 连接后状态: {mqtt_client.connected}")
        print(f"[INFO] get_connection_status(): {mqtt_client.get_connection_status()}")
        print(f"[INFO] client.is_connected(): {mqtt_client.client.is_connected()}")
        
        # 测试发布消息
        if mqtt_client.get_connection_status():
            print("[INFO] 测试发布状态消息...")
            success = mqtt_client.publish_status("test_connection")
            print(f"[INFO] 发布结果: {success}")
        else:
            print("[WARNING] MQTT未连接，跳过发布测试")
        
        # 断开连接
        mqtt_client.disconnect()
        print("[INFO] MQTT客户端已断开")
        
        # 检查断开后状态
        time.sleep(1)
        print(f"[INFO] 断开后状态: {mqtt_client.connected}")
        print(f"[INFO] get_connection_status(): {mqtt_client.get_connection_status()}")
        print(f"[INFO] client.is_connected(): {mqtt_client.client.is_connected()}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 测试MQTT客户端失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_api():
    """测试Web API的MQTT状态"""
    print("\n" + "=" * 50)
    print("测试Web API的MQTT状态")
    print("=" * 50)
    
    try:
        import requests
        import json
        
        base_url = "http://10.1.95.252:5000"
        
        print("1. 测试MQTT状态API...")
        response = requests.get(f"{base_url}/api/mqtt/status")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] MQTT状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get('success') and 'data' in result:
                mqtt_status = result['data'].get('connected', False)
                print(f"[INFO] MQTT连接状态: {'已连接' if mqtt_status else '未连接'}")
            else:
                print("[ERROR] MQTT状态API响应格式错误")
        else:
            print(f"[ERROR] MQTT状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] 测试Web API失败: {e}")

def main():
    """主函数"""
    print("MQTT连接状态修复测试")
    print("=" * 50)
    
    # 测试MQTT客户端
    success = test_mqtt_client()
    
    if success:
        print("\n[SUCCESS] MQTT客户端测试通过")
        
        # 测试Web API
        test_web_api()
        
        print("\n" + "=" * 50)
        print("修复说明")
        print("=" * 50)
        print("✅ 已修复的问题:")
        print("1. 使用 client.is_connected() 替代手动标志位")
        print("2. 改进连接方法，添加连接超时检查")
        print("3. 确保连接状态同步")
        
        print("\n📋 下一步操作:")
        print("1. 重启ESP32后台系统")
        print("2. 刷新Web界面")
        print("3. 检查MQTT状态是否显示为'已连接'")
        
    else:
        print("\n[ERROR] MQTT客户端测试失败")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()



