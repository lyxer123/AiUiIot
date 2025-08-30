#!/usr/bin/env python3
import sys
import time
import threading
from flask import Flask

def run_flask_server():
    """运行简单的Flask服务器"""
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return 'Hello World!'
    
    @app.route('/api/test')
    def test():
        return {'success': True, 'message': 'API测试成功'}
    
    print(f"启动Flask服务器在端口 5001...")
    try:
        app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
    except Exception as e:
        print(f"服务器启动错误: {e}")

def test_server():
    """测试服务器连接"""
    time.sleep(3)  # 等待服务器启动
    
    try:
        import requests
        response = requests.get('http://127.0.0.1:5001/api/test', timeout=5)
        print(f"✅ 服务器响应: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ 服务器测试失败: {e}")
        return False

if __name__ == "__main__":
    print("启动简单Flask服务器测试...")
    
    # 在后台线程中启动服务器
    server_thread = threading.Thread(target=run_flask_server, daemon=True)
    server_thread.start()
    
    # 测试服务器
    success = test_server()
    
    if success:
        print("✅ Flask服务器测试成功！")
        print("现在可以访问: http://127.0.0.1:5001")
        print("API测试: http://127.0.0.1:5001/api/test")
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n服务器已停止")
    else:
        print("❌ Flask服务器测试失败")
        sys.exit(1)