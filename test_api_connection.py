#!/usr/bin/env python3
import requests
import sys

def test_api_connection():
    try:
        # 测试本地连接
        print("测试本地API连接...")
        response = requests.get("http://localhost:5000/api/test", timeout=5)
        if response.status_code == 200:
            print("✅ 本地API连接成功!")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ 本地API连接失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到本地API服务器 - 服务器可能未运行")
        return False
    except requests.exceptions.Timeout:
        print("❌ 连接超时 - 服务器可能未响应")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_network_connection(ip):
    try:
        # 测试网络连接
        print(f"测试网络API连接 ({ip})...")
        response = requests.get(f"http://{ip}:5000/api/test", timeout=5)
        if response.status_code == 200:
            print(f"✅ 网络API连接成功!")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ 网络API连接失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 网络连接错误: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("API连接测试工具")
    print("=" * 50)
    
    # 测试本地连接
    local_success = test_api_connection()
    
    # 测试网络连接（使用配置中的IP）
    network_success = test_network_connection("10.1.95.252")
    
    print("=" * 50)
    if local_success and network_success:
        print("✅ 所有连接测试通过!")
        sys.exit(0)
    else:
        print("❌ 连接测试失败!")
        sys.exit(1)