#!/usr/bin/env python3
"""简单的Web服务器测试"""

import socket
import requests

def test_port(host='127.0.0.1', port=5000):
    """测试端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_api():
    """测试API接口"""
    try:
        response = requests.get("http://localhost:5000/api/test", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)

# 主测试
print("🔍 测试Web服务器连接...")
if test_port():
    print("✅ 端口5000正在监听")
    
    success, result = test_api()
    if success:
        print("✅ API接口测试成功")
        print(f"响应: {result}")
    else:
        print("❌ API接口测试失败")
        print(f"错误: {result}")
else:
    print("❌ 端口5000未开放 - Web服务器可能未启动")

print("\n💡 建议: 请确保已经运行了 'restart_system_with_fix.bat' 来启动完整系统")