import paho.mqtt.client as mqtt
import json
import time
import random
import threading
import logging
import configparser
from datetime import datetime

class ESP32Simulator:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # MQTT配置
        self.broker = self.config.get('MQTT', 'broker')
        self.port = self.config.getint('MQTT', 'port')
        self.client_id = "esp32_simulator"
        self.username = self.config.get('MQTT', 'username')
        self.password = self.config.get('MQTT', 'password')
        self.keepalive = self.config.getint('MQTT', 'keepalive')
        
        # 主题配置
        self.ad1_topic = self.config.get('TOPICS', 'ad1_data')
        self.io1_control_topic = self.config.get('TOPICS', 'io1_control')
        self.status_topic = self.config.get('TOPICS', 'status')
        
        # 模拟器配置
        self.enabled = self.config.getboolean('ESP32_SIMULATOR', 'enabled')
        self.simulation_interval = self.config.getint('ESP32_SIMULATOR', 'simulation_interval')
        self.ad1_min = self.config.getint('ESP32_SIMULATOR', 'ad1_min')
        self.ad1_max = self.config.getint('ESP32_SIMULATOR', 'ad1_max')
        self.io1_default = self.config.getboolean('ESP32_SIMULATOR', 'io1_default')
        
        # 创建MQTT客户端
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # 设置认证信息
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        # 设备状态
        self.connected = False
        self.io1_state = self.io1_default
        self.simulation_running = False
        self.simulation_thread = None
        
        # 模拟数据生成器
        self.ad1_generator = self.create_ad1_generator()
        
    def create_ad1_generator(self):
        """创建AD1数据生成器"""
        base_value = random.randint(self.ad1_min, self.ad1_max)
        while True:
            # 模拟真实的AD值变化（缓慢变化，偶尔跳跃）
            if random.random() < 0.1:  # 10%概率跳跃
                base_value = random.randint(self.ad1_min, self.ad1_max)
            else:
                # 缓慢变化
                change = random.randint(-50, 50)
                base_value = max(self.ad1_min, min(self.ad1_max, base_value + change))
            
            yield base_value
    
    def on_connect(self, client, userdata, flags, rc):
        """MQTT连接回调"""
        if rc == 0:
            self.connected = True
            logging.info("ESP32模拟器MQTT连接成功")
            
            # 订阅IO1控制主题
            client.subscribe(self.io1_control_topic)
            
            # 发布上线状态
            self.publish_status("online")
            
            # 开始模拟
            if self.enabled:
                self.start_simulation()
            
        else:
            logging.error(f"ESP32模拟器MQTT连接失败，错误码: {rc}")
    
    def on_message(self, client, userdata, msg):
        """MQTT消息接收回调"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            if topic == self.io1_control_topic:
                self.handle_io1_control(payload)
                
        except Exception as e:
            logging.error(f"ESP32模拟器处理消息失败: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        """MQTT断开连接回调"""
        self.connected = False
        self.stop_simulation()
        logging.warning("ESP32模拟器MQTT连接断开")
    
    def handle_io1_control(self, payload):
        """处理IO1控制命令"""
        try:
            data = json.loads(payload)
            if 'command' in data and data['command'] == 'set_io1':
                if 'state' in data:
                    new_state = data['state']
                    if new_state != self.io1_state:
                        self.io1_state = new_state
                        logging.info(f"ESP32模拟器IO1状态已更新: {new_state}")
                        
                        # 发布状态确认
                        self.publish_io1_status()
                        
        except json.JSONDecodeError:
            logging.error("ESP32模拟器IO1控制数据JSON格式错误")
        except Exception as e:
            logging.error(f"ESP32模拟器处理IO1控制失败: {e}")
    
    def start_simulation(self):
        """开始模拟"""
        if self.simulation_running:
            return
        
        self.simulation_running = True
        self.simulation_thread = threading.Thread(target=self.simulation_loop, daemon=True)
        self.simulation_thread.start()
        logging.info("ESP32模拟器开始运行")
    
    def stop_simulation(self):
        """停止模拟"""
        self.simulation_running = False
        if self.simulation_thread:
            self.simulation_thread.join(timeout=1)
        logging.info("ESP32模拟器已停止")
    
    def simulation_loop(self):
        """模拟循环"""
        while self.simulation_running and self.connected:
            try:
                # 生成AD1数据
                ad1_value = next(self.ad1_generator)
                self.publish_ad1_data(ad1_value)
                
                # 发布设备状态
                self.publish_status("running")
                
                # 等待下次模拟
                time.sleep(self.simulation_interval)
                
            except Exception as e:
                logging.error(f"ESP32模拟器模拟循环错误: {e}")
                time.sleep(1)
    
    def publish_ad1_data(self, value):
        """发布AD1数据"""
        if not self.connected:
            return
        
        try:
            message = {
                "device_id": self.client_id,
                "channel": "AD1",
                "value": value,
                "unit": "ADC",
                "timestamp": datetime.now().isoformat()
            }
            payload = json.dumps(message)
            result = self.client.publish(self.ad1_topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.debug(f"ESP32模拟器AD1数据已发送: {value}")
            else:
                logging.error(f"ESP32模拟器AD1数据发送失败: {result.rc}")
                
        except Exception as e:
            logging.error(f"ESP32模拟器发送AD1数据失败: {e}")
    
    def publish_io1_status(self):
        """发布IO1状态"""
        if not self.connected:
            return
        
        try:
            message = {
                "device_id": self.client_id,
                "channel": "IO1",
                "state": self.io1_state,
                "timestamp": datetime.now().isoformat()
            }
            payload = json.dumps(message)
            result = self.client.publish(self.io1_control_topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"ESP32模拟器IO1状态已发布: {self.io1_state}")
            else:
                logging.error(f"ESP32模拟器IO1状态发布失败: {result.rc}")
                
        except Exception as e:
            logging.error(f"ESP32模拟器发布IO1状态失败: {e}")
    
    def publish_status(self, status):
        """发布设备状态"""
        if not self.connected:
            return
        
        try:
            message = {
                "device_id": self.client_id,
                "status": status,
                "io1_state": self.io1_state,
                "timestamp": datetime.now().isoformat()
            }
            payload = json.dumps(message)
            result = self.client.publish(self.status_topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.debug(f"ESP32模拟器状态已发布: {status}")
            else:
                logging.error(f"ESP32模拟器状态发布失败: {result.rc}")
                
        except Exception as e:
            logging.error(f"ESP32模拟器发布状态失败: {e}")
    
    def connect(self):
        """连接到MQTT代理"""
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            self.client.loop_start()
            logging.info(f"ESP32模拟器正在连接到MQTT代理: {self.broker}:{self.port}")
        except Exception as e:
            logging.error(f"ESP32模拟器MQTT连接失败: {e}")
    
    def disconnect(self):
        """断开MQTT连接"""
        try:
            self.stop_simulation()
            self.publish_status("offline")
            self.client.loop_stop()
            self.client.disconnect()
            logging.info("ESP32模拟器已断开连接")
        except Exception as e:
            logging.error(f"ESP32模拟器断开连接失败: {e}")
    
    def get_status(self):
        """获取模拟器状态"""
        return {
            "enabled": self.enabled,
            "connected": self.connected,
            "simulation_running": self.simulation_running,
            "io1_state": self.io1_state,
            "ad1_range": f"{self.ad1_min}-{self.ad1_max}",
            "simulation_interval": self.simulation_interval
        }
