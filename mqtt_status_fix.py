#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MQTT状态修复脚本
用于修复Web界面MQTT状态显示问题
"""

import os
import sys
import time
import logging

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_mqtt_status():
    """修复MQTT状态显示问题"""
    try:
        from mqtt_client import MQTTClient
        from database import DatabaseManager
        
        print("[INFO] 正在修复MQTT状态...")
        
        # 创建数据库管理器
        db_manager = DatabaseManager("esp32_data.db")
        
        # 创建新的MQTT客户端实例
        mqtt_client = MQTTClient("config.ini", db_manager)
        
        print(f"[INFO] MQTT客户端创建成功")
        print(f"[INFO] Broker地址: {mqtt_client.broker}")
        print(f"[INFO] Broker端口: {mqtt_client.port}")
        
        # 连接到MQTT broker
        print("[INFO] 正在连接到MQTT broker...")
        mqtt_client.connect()
        
        # 等待连接建立
        time.sleep(3)
        
        # 检查连接状态
        connected = mqtt_client.get_connection_status()
        print(f"[INFO] MQTT连接状态: {connected}")
        
        if connected:
            print("[SUCCESS] MQTT连接成功，状态已修复")
            
            # 发布测试消息
            success = mqtt_client.publish_status("status_fixed")
            if success:
                print("[SUCCESS] 状态修复消息发布成功")
            else:
                print("[WARNING] 状态修复消息发布失败")
        else:
            print("[ERROR] MQTT连接失败，无法修复状态")
            
        # 断开连接
        mqtt_client.disconnect()
        print("[INFO] MQTT客户端已断开")
        
        return connected
        
    except Exception as e:
        print(f"[ERROR] 修复MQTT状态失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("MQTT状态修复工具")
    print("=" * 50)
    
    success = fix_mqtt_status()
    
    if success:
        print("
[SUCCESS] MQTT状态修复完成")
        print("现在可以刷新Web界面查看MQTT状态")
    else:
        print("
[ERROR] MQTT状态修复失败")
        print("请检查系统日志了解详细错误信息")
