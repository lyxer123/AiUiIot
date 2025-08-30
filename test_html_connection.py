#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML连接测试脚本
测试web_test_improved.html文件中的API连接配置
"""

import os
import re

def test_html_connection():
    """测试HTML文件的连接配置"""
    
    # 读取HTML文件
    html_file = "web_test_improved.html"
    if not os.path.exists(html_file):
        print(f"❌ HTML文件不存在: {html_file}")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查API_BASE配置
    api_base_match = re.search(r"let API_BASE = 'http://([^:]+):(\d+)/api';", content)
    if api_base_match:
        ip = api_base_match.group(1)
        port = api_base_match.group(2)
        print(f"✅ HTML文件中的API配置: IP={ip}, 端口={port}")
        
        # 检查端口是否为8080
        if port == "8080":
            print("✅ 端口配置正确 (8080)")
        else:
            print(f"❌ 端口配置错误，应为8080，实际为{port}")
            return False
        
        # 检查IP地址是否为当前IP
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            current_ip = s.getsockname()[0]
            s.close()
            
            if ip == current_ip:
                print(f"✅ IP地址配置正确 ({current_ip})")
            else:
                print(f"⚠️  IP地址可能已变化: 配置={ip}, 当前={current_ip}")
                
        except Exception as e:
            print(f"⚠️  无法获取当前IP: {e}")
    
    else:
        print("❌ 未找到API_BASE配置")
        return False
    
    # 检查默认配置表单
    port_input_match = re.search(r'<input type="number" id="serverPort" value="(\d+)"', content)
    if port_input_match:
        default_port = port_input_match.group(1)
        if default_port == "8080":
            print("✅ 默认端口配置正确 (8080)")
        else:
            print(f"❌ 默认端口配置错误，应为8080，实际为{default_port}")
            return False
    else:
        print("❌ 未找到端口输入框配置")
        return False
    
    print("\n✅ HTML文件连接配置测试通过！")
    print(f"📋 访问地址: http://{ip}:{port}/web_test_improved.html")
    return True

if __name__ == "__main__":
    print("🔧 HTML连接配置测试")
    print("=" * 50)
    
    success = test_html_connection()
    
    if success:
        print("\n🎉 所有测试通过！HTML文件已正确配置")
    else:
        print("\n❌ 测试失败，请检查HTML文件配置")
        exit(1)