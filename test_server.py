import requests
import time

def test_server():
    url = "http://127.0.0.1:5000/api/test"
    
    try:
        print(f"正在测试服务器连接: {url}")
        response = requests.get(url, timeout=5)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return True
    except requests.exceptions.ConnectionError:
        print("连接错误: 无法连接到服务器")
        return False
    except requests.exceptions.Timeout:
        print("连接超时: 服务器响应时间过长")
        return False
    except Exception as e:
        print(f"其他错误: {e}")
        return False

if __name__ == "__main__":
    print("开始测试web服务器连接...")
    success = test_server()
    if success:
        print("✅ 服务器连接测试成功！")
    else:
        print("❌ 服务器连接测试失败")