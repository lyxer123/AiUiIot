import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_server import WebServer
import configparser
from database import DatabaseManager
from mqtt_client import MQTTClient
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_web_server():
    print("测试Web服务器启动...")
    
    # 创建配置
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # 创建依赖组件（简化版本）
    db_manager = DatabaseManager('esp32_data.db')
    mqtt_client = MQTTClient(config)
    
    # 创建web服务器
    web_server = WebServer('config.ini', db_manager, mqtt_client)
    
    print(f"Web服务器配置: host={web_server.host}, port={web_server.port}")
    
    # 测试启动
    try:
        print("正在启动Web服务器...")
        # 使用线程启动，避免阻塞
        import threading
        def start_server():
            web_server.start()
        
        thread = threading.Thread(target=start_server, daemon=True)
        thread.start()
        
        # 等待服务器启动
        import time
        time.sleep(3)
        
        # 测试连接
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', web_server.port))
        
        if result == 0:
            print(f"✅ Web服务器成功启动在端口 {web_server.port}")
            return True
        else:
            print(f"❌ Web服务器端口 {web_server.port} 未响应")
            return False
            
    except Exception as e:
        print(f"❌ Web服务器启动失败: {e}")
        return False

if __name__ == "__main__":
    success = test_web_server()
    if success:
        print("Web服务器测试成功！")
    else:
        print("Web服务器测试失败")