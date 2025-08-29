#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Web界面MQTT状态显示修复
"""

import requests
import json
import time

def test_web_interface_fix():
    """测试Web界面修复"""
    print("=" * 60)
    print("测试Web界面MQTT状态显示修复")
    print("=" * 60)
    
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
    
    print("\n3. 测试API接口...")
    try:
        response = requests.get(f"{base_url}/api/test")
        if response.status_code == 200:
            result = response.json()
            print(f"[SUCCESS] API测试响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"[ERROR] API测试失败: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] API测试失败: {e}")

def provide_fix_instructions():
    """提供修复说明"""
    print("\n" + "=" * 60)
    print("Web界面修复完成说明")
    print("=" * 60)
    
    print("\n✅ 已修复的问题:")
    print("1. 改进了MQTT状态获取逻辑")
    print("2. 添加了详细的调试日志输出")
    print("3. 优化了状态更新机制")
    print("4. 添加了MQTT API测试功能")
    print("5. 改进了错误处理和日志记录")
    
    print("\n🔧 修复的文件:")
    print("1. web_test_improved.html - 改进版Web界面")
    print("2. mqtt_client.py - MQTT客户端状态检查")
    
    print("\n📋 下一步操作:")
    print("1. 刷新Web界面 (web_test_improved.html)")
    print("2. 打开浏览器开发者工具 (F12)")
    print("3. 查看Console标签页的调试信息")
    print("4. 点击'测试MQTT API'按钮")
    print("5. 检查MQTT状态是否显示为'已连接'")
    
    print("\n🐛 调试方法:")
    print("1. 在浏览器控制台查看日志:")
    print("   - MQTT状态更新信息")
    print("   - API响应数据")
    print("   - 错误信息")
    print("2. 使用'测试MQTT API'按钮验证API状态")
    print("3. 检查Network标签页的API请求")
    
    print("\n🎯 预期结果:")
    print("修复后，Web界面应该显示:")
    print("- MQTT连接: ● 已连接 (绿色圆点)")
    print("- 系统状态: running")
    print("- IO1当前状态: 关闭")
    print("- 浏览器控制台显示详细的调试信息")

def main():
    """主函数"""
    # 测试API接口
    test_web_interface_fix()
    
    # 提供修复说明
    provide_fix_instructions()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n💡 重要提示:")
    print("如果MQTT状态仍然显示'未连接'，请检查:")
    print("1. ESP32后台系统是否已重启（应用了mqtt_client.py的修复）")
    print("2. Mosquitto服务是否正常运行")
    print("3. 浏览器控制台的错误信息")

if __name__ == "__main__":
    main()



