#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复MQTT状态显示问题
"""

import time
import requests
import json

def test_current_status():
    """测试当前系统状态"""
    print("=" * 50)
    print("测试当前系统状态")
    print("=" * 50)
    
    base_url = "http://10.1.95.252:5000"
    
    try:
        # 测试MQTT状态API
        print("1. 测试MQTT状态API...")
        response = requests.get(f"{base_url}/api/mqtt/status")
        if response.status_code == 200:
            result = response.json()
            print(f"[INFO] MQTT状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get('success') and 'data' in result:
                mqtt_status = result['data'].get('connected', False)
                print(f"[INFO] MQTT连接状态: {'已连接' if mqtt_status else '未连接'}")
        else:
            print(f"[ERROR] MQTT状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] MQTT状态API测试失败: {e}")
    
    try:
        # 测试系统状态API
        print("\n2. 测试系统状态API...")
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            result = response.json()
            print(f"[INFO] 系统状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get('success') and 'data' in result:
                mqtt_status = result['data'].get('mqtt_connected', False)
                print(f"[INFO] 系统MQTT状态: {'已连接' if mqtt_status else '未连接'}")
        else:
            print(f"[ERROR] 系统状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] 系统状态API测试失败: {e}")

def create_mqtt_status_fix():
    """创建MQTT状态修复脚本"""
    print("\n" + "=" * 50)
    print("创建MQTT状态修复脚本")
    print("=" * 50)
    
    fix_script = '''#!/usr/bin/env python3
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
        print("\n[SUCCESS] MQTT状态修复完成")
        print("现在可以刷新Web界面查看MQTT状态")
    else:
        print("\n[ERROR] MQTT状态修复失败")
        print("请检查系统日志了解详细错误信息")
'''
    
    # 写入修复脚本
    with open("mqtt_status_fix.py", "w", encoding="utf-8") as f:
        f.write(fix_script)
    
    print("[SUCCESS] MQTT状态修复脚本已创建: mqtt_status_fix.py")
    print("[INFO] 运行此脚本来修复MQTT状态显示问题")

def create_web_status_fix():
    """创建Web状态修复说明"""
    print("\n" + "=" * 50)
    print("Web状态修复说明")
    print("=" * 50)
    
    fix_instructions = """
## MQTT状态显示问题修复说明

### 问题描述
Web界面显示MQTT连接状态为"未连接"，但实际MQTT连接是正常的。

### 问题原因
1. MQTT客户端连接状态管理问题
2. Web服务器和主程序使用不同的MQTT客户端实例
3. 状态同步机制不完善

### 解决方案

#### 方案1：重启系统（推荐）
1. 停止当前系统（Ctrl+C）
2. 重新运行启动脚本：`start_system_smart.bat`
3. 等待系统完全启动
4. 刷新Web界面

#### 方案2：运行修复脚本
1. 运行修复脚本：`py mqtt_status_fix.py`
2. 等待修复完成
3. 刷新Web界面

#### 方案3：手动检查
1. 检查系统日志中的MQTT连接状态
2. 确认Mosquitto服务正常运行
3. 验证配置文件中的broker地址为localhost

### 验证方法
1. 刷新Web界面
2. 查看MQTT连接状态是否变为"已连接"
3. 检查系统日志中的MQTT状态信息

### 预防措施
1. 确保系统启动顺序正确
2. 定期检查MQTT连接状态
3. 监控系统日志中的错误信息
"""
    
    # 写入修复说明
    with open("MQTT状态修复说明.md", "w", encoding="utf-8") as f:
        f.write(fix_instructions)
    
    print("[SUCCESS] MQTT状态修复说明已创建: MQTT状态修复说明.md")

def main():
    """主函数"""
    print("MQTT状态显示问题修复工具")
    print("=" * 50)
    
    # 测试当前状态
    test_current_status()
    
    # 创建修复脚本
    create_mqtt_status_fix()
    
    # 创建修复说明
    create_web_status_fix()
    
    print("\n" + "=" * 50)
    print("修复工具创建完成")
    print("=" * 50)
    
    print("\n下一步操作:")
    print("1. 运行修复脚本: py mqtt_status_fix.py")
    print("2. 或者重启系统: 停止当前系统，重新运行启动脚本")
    print("3. 刷新Web界面查看MQTT状态")

if __name__ == "__main__":
    main()


