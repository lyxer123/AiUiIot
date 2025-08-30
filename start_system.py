#!/usr/bin/env python3
# 简化的系统启动脚本

import os
import sys
import time
import logging
import configparser

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('system_start.log', mode='w')
    ]
)

# 导入自定义模块
try:
    from database import DatabaseManager
    from mqtt_client import MQTTClient
    from esp32_simulator import ESP32Simulator
    from web_server import WebServer
    from ip_config import IPConfigManager
except ImportError as e:
    logging.error(f"导入模块失败: {e}")
    sys.exit(1)

def main():
    """主函数"""
    logging.info("=" * 60)
    logging.info("ESP32数据采集和控制系统 - 简化启动")
    logging.info("=" * 60)
    
    try:
        # 读取配置
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # 初始化组件
        logging.info("正在初始化组件...")
        
        # 数据库
        db_manager = DatabaseManager(config.get('DATABASE', 'db_path'))
        logging.info("✅ 数据库初始化成功")
        
        # MQTT客户端
        mqtt_client = MQTTClient(config)
        logging.info("✅ MQTT客户端初始化成功")
        
        # Web服务器
        web_server = WebServer('config.ini', db_manager, mqtt_client)
        logging.info("✅ Web服务器初始化成功")
        
        # ESP32模拟器
        esp32_simulator = ESP32Simulator(config, db_manager, mqtt_client)
        logging.info("✅ ESP32模拟器初始化成功")
        
        # 启动组件
        logging.info("正在启动组件...")
        
        # 启动MQTT
        mqtt_client.connect()
        time.sleep(2)
        logging.info("✅ MQTT客户端启动成功")
        
        # 启动ESP32模拟器
        esp32_simulator.connect()
        time.sleep(2)
        logging.info("✅ ESP32模拟器启动成功")
        
        # 启动Web服务器（在新线程中）
        import threading
        web_thread = threading.Thread(target=web_server.start, daemon=True)
        web_thread.start()
        time.sleep(5)  # 等待服务器启动
        
        # 检查web服务器是否启动
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', web_server.port))
            if result == 0:
                logging.info(f"✅ Web服务器已成功启动，端口 {web_server.port}")
                logging.info(f"🌐 访问地址: http://localhost:{web_server.port}")
            else:
                logging.warning(f"⚠️ Web服务器端口 {web_server.port} 未响应")
        except Exception as e:
            logging.error(f"❌ Web服务器状态检查失败: {e}")
        
        logging.info("系统启动完成！")
        logging.info("按 Ctrl+C 停止系统")
        
        # 保持主线程运行
        while True:
            time.sleep(1)
            
    except Exception as e:
        logging.error(f"系统启动失败: {e}")
        import traceback
        logging.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()