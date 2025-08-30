import sys
import os
import logging
import configparser
import socket

# 设置详细日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_port_availability():
    """测试端口是否可用"""
    print("测试端口可用性...")
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    port = config.getint('WEB_SERVER', 'port')
    host = config.get('WEB_SERVER', 'host')
    
    print(f"测试端口: {host}:{port}")
    
    try:
        # 检查端口是否被占用
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"❌ 端口 {port} 已被占用")
            return False
        else:
            print(f"✅ 端口 {port} 可用")
            return True
            
    except Exception as e:
        print(f"❌ 端口检查失败: {e}")
        return False

def test_flask_import():
    """测试Flask导入"""
    print("测试Flask导入...")
    try:
        from flask import Flask
        print("✅ Flask导入成功")
        return True
    except ImportError as e:
        print(f"❌ Flask导入失败: {e}")
        return False

def test_waitress_import():
    """测试Waitress导入"""
    print("测试Waitress导入...")
    try:
        from waitress import serve
        print("✅ Waitress导入成功")
        return True
    except ImportError as e:
        print(f"❌ Waitress导入失败: {e}")
        return False

def test_simple_web_server():
    """测试简单的web服务器"""
    print("测试简单web服务器...")
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return "Hello World!"
        
        # 在后台线程中启动
        import threading
        import time
        
        def run_server():
            try:
                app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)
            except Exception as e:
                print(f"服务器启动错误: {e}")
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        
        # 等待服务器启动
        time.sleep(3)
        
        # 测试连接
        try:
            import requests
            response = requests.get('http://127.0.0.1:8080', timeout=5)
            print(f"✅ 简单web服务器测试成功: {response.text}")
            return True
        except Exception as e:
            print(f"❌ 简单web服务器测试失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 简单web服务器设置失败: {e}")
        return False

if __name__ == "__main__":
    print("开始Web服务器诊断...")
    print("=" * 50)
    
    # 测试1: 端口可用性
    port_ok = test_port_availability()
    print()
    
    # 测试2: Flask导入
    flask_ok = test_flask_import()
    print()
    
    # 测试3: Waitress导入
    waitress_ok = test_waitress_import()
    print()
    
    # 测试4: 简单web服务器
    simple_ok = test_simple_web_server()
    print()
    
    print("=" * 50)
    print("诊断结果:")
    print(f"端口可用性: {'✅' if port_ok else '❌'}")
    print(f"Flask导入: {'✅' if flask_ok else '❌'}")
    print(f"Waitress导入: {'✅' if waitress_ok else '❌'}")
    print(f"简单web服务器: {'✅' if simple_ok else '❌'}")
    
    if all([port_ok, flask_ok, simple_ok]):
        print("✅ 所有基本测试通过")
    else:
        print("❌ 存在配置问题")