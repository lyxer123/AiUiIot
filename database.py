import sqlite3
import json
from datetime import datetime
import logging

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """初始化数据库表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建AD1数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ad1_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建IO1控制状态表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS io1_control (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建设备状态表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS device_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logging.info("数据库初始化成功")
            
        except Exception as e:
            logging.error(f"数据库初始化失败: {e}")
    
    def save_ad1_data(self, value):
        """保存AD1数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO ad1_data (value) VALUES (?)', (value,))
            conn.commit()
            conn.close()
            logging.info(f"AD1数据保存成功: {value}")
            return True
        except Exception as e:
            logging.error(f"AD1数据保存失败: {e}")
            return False
    
    def save_io1_control(self, state):
        """保存IO1控制状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO io1_control (state) VALUES (?)', (state,))
            conn.commit()
            conn.close()
            logging.info(f"IO1控制状态保存成功: {state}")
            return True
        except Exception as e:
            logging.error(f"IO1控制状态保存失败: {e}")
            return False
    
    def save_device_status(self, status):
        """保存设备状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO device_status (status) VALUES (?)', (status,))
            conn.commit()
            conn.close()
            logging.info(f"设备状态保存成功: {status}")
            return True
        except Exception as e:
            logging.error(f"设备状态保存失败: {e}")
            return False
    
    def get_latest_ad1_data(self, limit=100):
        """获取最新的AD1数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT value, timestamp FROM ad1_data 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            logging.error(f"获取AD1数据失败: {e}")
            return []
    
    def get_latest_io1_control(self, limit=50):
        """获取最新的IO1控制状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT state, timestamp FROM io1_control 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            logging.error(f"获取IO1控制状态失败: {e}")
            return []
    
    def get_device_status_history(self, limit=50):
        """获取设备状态历史"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT status, timestamp FROM device_status 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            logging.error(f"获取设备状态历史失败: {e}")
            return []
