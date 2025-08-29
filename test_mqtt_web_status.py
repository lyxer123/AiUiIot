#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Web界面MQTT状态显示修复
"""

import requests
import json
import time

def test_mqtt_apis():
    """测试MQTT相关API"""
    print("=" * 50)
    print("测试Web界面MQTT状态显示修复")
    print("=" * 50)
    
    base_url = "http://10.1.95.252:5000"
    
    print("1. 测试MQTT状态API...")
    try:
        response = requests.get(f"{base_url}/api/mqtt/status")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] MQTT状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get('success') and 'data' in result:
                mqtt_status = result['data'].get('connected', False)
                print(f"[INFO] MQTT连接状态: {'已连接' if mqtt_status else '未连接'}")
                
                if mqtt_status:
                    print("[SUCCESS] MQTT状态API返回正确的连接状态")
                else:
                    print("[WARNING] MQTT状态API返回未连接状态")
            else:
                print("[ERROR] MQTT状态API响应格式错误")
        else:
            print(f"[ERROR] MQTT状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] MQTT状态API测试失败: {e}")
    
    print("\n2. 测试系统状态API...")
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] 系统状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get('success') and 'data' in result:
                mqtt_status = result['data'].get('mqtt_connected', False)
                print(f"[INFO] 系统MQTT状态: {'已连接' if mqtt_status else '未连接'}")
                
                if mqtt_status:
                    print("[SUCCESS] 系统状态API返回正确的MQTT状态")
                else:
                    print("[WARNING] 系统状态API返回未连接状态")
            else:
                print("[ERROR] 系统状态API响应格式错误")
        else:
            print(f"[ERROR] 系统状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] 系统状态API测试失败: {e}")
    
    print("\n3. 测试IO1当前状态API...")
    try:
        response = requests.get(f"{base_url}/api/io1/current")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] IO1状态API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"[ERROR] IO1状态API失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] IO1状态API测试失败: {e}")

def provide_fix_instructions():
    """提供修复说明"""
    print("\n" + "=" * 50)
    print("修复完成说明")
    print("=" * 50)
    
    print("\n✅ 已修复的问题:")
    print("1. 改进了MQTT状态显示逻辑")
    print("2. 添加了调试日志输出")
    print("3. 优化了状态更新机制")
    print("4. 修复了自动刷新中的MQTT状态更新")
    
    print("\n🔧 修复的文件:")
    print("1. web_test_improved.html - 改进版Web界面")
    print("2. web_test.html - 原版Web界面")
    
    print("\n📋 下一步操作:")
    print("1. 刷新Web界面")
    print("2. 点击'获取MQTT状态'按钮")
    print("3. 查看浏览器控制台的调试信息")
    print("4. 确认MQTT状态显示为'已连接'")
    
    print("\n🐛 如果仍有问题:")
    print("1. 打开浏览器开发者工具 (F12)")
    print("2. 查看Console标签页的日志信息")
    print("3. 检查Network标签页的API请求")
    print("4. 确认API返回的MQTT状态值")

def main():
    """主函数"""
    # 测试API
    test_mqtt_apis()
    
    # 提供修复说明
    provide_fix_instructions()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()



