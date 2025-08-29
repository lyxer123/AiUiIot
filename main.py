#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESP32数据采集和控制系统主程序
作者: AI Assistant
功能: 北向采集AD1数据，南向控制IO1开关
"""

import os
import sys
import time
import signal
import logging
import configparser
import threading
from datetime import datetime

# 导入自定义模块
from database import DatabaseManager
from mqtt_client import MQTTClient
from esp32_simulator import ESP32Simulator  # ESP32模拟器已重新启用
from web_server import WebServer
from ip_config import IPConfigManager  # 导入动态IP配置管理器

class ESP32BackendSystem:
    def __init__(self, config_file="config.ini"):
        """初始化ESP32后台系统"""
        self.config_file = config_file
        
        # 初始化IP配置管理器
        self.ip_manager = IPConfigManager(config_file)
        
        # 动态更新IP配置
        self.update_ip_config()
        
        # 重新加载配置
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # 设置日志
        self.setup_logging()
        
        # 系统组件
        self.database_manager = None
        self.mqtt_client = None
        self.esp32_simulator = None  # ESP32模拟器已重新启用
        self.web_server = None
        
        # 运行状态
        self.running = False
        self.shutdown_event = threading.Event()
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logging.info("ESP32后台系统初始化完成")
    
    def update_ip_config(self):
        """动态更新IP配置"""
        try:
            logging.info("正在更新IP配置...")
            
            # 更新主配置文件
            new_ip = self.ip_manager.update_config_with_dynamic_ip(force_update=True)
            
            # 更新ESP32配置文件
            esp32_updated = self.ip_manager.update_esp32_config()
            
            # 更新微信小程序配置文件
            miniprogram_updated = self.ip_manager.update_miniprogram_config()
            
            logging.info(f"IP配置更新完成 - 主要IP: {new_ip}")
            logging.info(f"ESP32配置: {'已更新' if esp32_updated else '无需更新'}")
            logging.info(f"微信小程序配置: {'已更新' if miniprogram_updated else '无需更新'}")
            
        except Exception as e:
            logging.error(f"IP配置更新失败: {e}")
    
    def setup_logging(self):
        """设置日志配置"""
        log_level = logging.INFO
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # 创建logs目录
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # 文件处理器
        log_file = f"logs/esp32_backend_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # 根日志器配置
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[file_handler, console_handler]
        )
        
        logging.info(f"日志系统初始化完成，日志文件: {log_file}")
    
    def initialize_components(self):
        """初始化系统组件"""
        try:
            logging.info("正在初始化系统组件...")
            
            # 初始化数据库管理器
            db_path = self.config.get('DATABASE', 'db_path')
            self.database_manager = DatabaseManager(db_path)
            logging.info("数据库管理器初始化完成")
            
            # 初始化MQTT客户端
            self.mqtt_client = MQTTClient(self.config_file, self.database_manager)
            logging.info("MQTT客户端初始化完成")
            
            # 初始化ESP32模拟器
            self.esp32_simulator = ESP32Simulator(self.config_file)
            logging.info("ESP32模拟器初始化完成")
            
            # 初始化Web服务器
            self.web_server = WebServer(self.config_file, self.database_manager, self.mqtt_client)
            logging.info("Web服务器初始化完成")
            
            logging.info("所有系统组件初始化完成")
            return True
            
        except Exception as e:
            logging.error(f"系统组件初始化失败: {e}")
            return False
    
    def start_components(self):
        """启动系统组件"""
        try:
            logging.info("正在启动系统组件...")
            
            # 启动MQTT客户端
            self.mqtt_client.connect()
            time.sleep(2)  # 等待连接建立
            
            # 启动ESP32模拟器
            self.esp32_simulator.connect()
            time.sleep(2)  # 等待连接建立
            
            # 启动Web服务器（在新线程中）
            web_thread = threading.Thread(target=self.web_server.start, daemon=True)
            web_thread.start()
            time.sleep(2)  # 等待服务器启动
            
            logging.info("所有系统组件启动完成")
            return True
            
        except Exception as e:
            logging.error(f"系统组件启动失败: {e}")
            return False
    
    def stop_components(self):
        """停止系统组件"""
        try:
            logging.info("正在停止系统组件...")
            
            # 停止ESP32模拟器
            if self.esp32_simulator:
                self.esp32_simulator.disconnect()
            
            # 停止MQTT客户端
            if self.mqtt_client:
                self.mqtt_client.disconnect()
            
            logging.info("所有系统组件已停止")
            
        except Exception as e:
            logging.error(f"停止系统组件时出错: {e}")
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        logging.info(f"收到信号 {signum}，正在关闭系统...")
        self.shutdown()
    
    def shutdown(self):
        """关闭系统"""
        logging.info("系统正在关闭...")
        self.running = False
        self.shutdown_event.set()
        self.stop_components()
        logging.info("系统已关闭")
        sys.exit(0)
    
    def run(self):
        """运行主循环"""
        try:
            # 初始化组件
            if not self.initialize_components():
                logging.error("系统组件初始化失败，退出")
                return False
            
            # 启动组件
            if not self.start_components():
                logging.error("系统组件启动失败，退出")
                return False
            
            self.running = True
            logging.info("ESP32后台系统启动成功！")
            
            # 获取当前IP配置
            current_ip = self.ip_manager.get_primary_ip()
            web_port = self.config.get('WEB_SERVER', 'port')
            logging.info(f"Web服务器地址: http://{current_ip}:{web_port}")
            logging.info(f"本地访问: http://localhost:{web_port}")
            logging.info("按 Ctrl+C 停止系统")
            
            # 主循环
            while self.running and not self.shutdown_event.is_set():
                try:
                    # 检查组件状态
                    mqtt_connected = self.mqtt_client.get_connection_status()
                    simulator_connected = self.esp32_simulator.connected if self.esp32_simulator else False
                    
                    # 输出状态信息
                    if self.running and time.time() % 60 < 1:  # 每分钟输出一次状态
                        logging.info(f"系统状态 - MQTT: {'已连接' if mqtt_connected else '未连接'}, "
                                   f"模拟器: {'已连接' if simulator_connected else '未连接'}")
                    
                    time.sleep(1)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logging.error(f"主循环错误: {e}")
                    time.sleep(5)
            
            return True
            
        except Exception as e:
            logging.error(f"系统运行错误: {e}")
            return False
        finally:
            self.shutdown()

def main():
    """主函数"""
    print("=" * 60)
    print("ESP32数据采集和控制系统")
    print("=" * 60)
    print("功能: 北向采集AD1数据，南向控制IO1开关")
    print("协议: MQTT + JSON")
    print("=" * 60)
    
    # 创建并运行系统
    system = ESP32BackendSystem()
    success = system.run()
    
    if success:
        print("系统运行完成")
    else:
        print("系统运行失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
