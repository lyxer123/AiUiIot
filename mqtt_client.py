import paho.mqtt.client as mqtt
import json
import logging
import configparser
from datetime import datetime

class MQTTClient:
    def __init__(self, config_file, database_manager):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.database_manager = database_manager
        
        # MQTT配置
        self.broker = self.config.get('MQTT', 'broker')
        self.port = self.config.getint('MQTT', 'port')
        self.client_id = self.config.get('MQTT', 'client_id')
        self.username = self.config.get('MQTT', 'username')
        self.password = self.config.get('MQTT', 'password')
        self.keepalive = self.config.getint('MQTT', 'keepalive')
        
        # 主题配置
        self.ad1_topic = self.config.get('TOPICS', 'ad1_data')
        self.io1_control_topic = self.config.get('TOPICS', 'io1_control')
        self.status_topic = self.config.get('TOPICS', 'status')
        
        # 创建MQTT客户端
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # 设置认证信息
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        # 连接状态
        self.connected = False
        self.current_io1_state = False
        
    def on_connect(self, client, userdata, flags, rc):
        """MQTT连接回调"""
        if rc == 0:
            self.connected = True
            logging.info("MQTT连接成功")
            
            # 订阅相关主题
            client.subscribe(self.ad1_topic)
            client.subscribe(self.io1_control_topic)
            client.subscribe(self.status_topic)
            
            # 发布上线状态
            self.publish_status("online")
            
        else:
            logging.error(f"MQTT连接失败，错误码: {rc}")
    
    def on_message(self, client, userdata, msg):
        """MQTT消息接收回调"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            logging.info(f"收到消息: {topic} -> {payload}")
            
            if topic == self.ad1_topic:
                self.handle_ad1_data(payload)
            elif topic == self.io1_control_topic:
                self.handle_io1_control(payload)
            elif topic == self.status_topic:
                self.handle_status(payload)
                
        except Exception as e:
            logging.error(f"处理MQTT消息失败: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        """MQTT断开连接回调"""
        self.connected = False
        logging.warning("MQTT连接断开")
        
        if rc != 0:
            logging.error(f"意外断开连接，错误码: {rc}")
    
    def handle_ad1_data(self, payload):
        """处理AD1数据"""
        try:
            data = json.loads(payload)
            if 'value' in data:
                value = data['value']
                # 保存到数据库
                self.database_manager.save_ad1_data(value)
                logging.info(f"AD1数据已保存: {value}")
            else:
                logging.warning("AD1数据格式错误，缺少value字段")
        except json.JSONDecodeError:
            logging.error("AD1数据JSON格式错误")
        except Exception as e:
            logging.error(f"处理AD1数据失败: {e}")
    
    def handle_io1_control(self, payload):
        """处理IO1控制状态"""
        try:
            data = json.loads(payload)
            if 'state' in data:
                state = data['state']
                self.current_io1_state = state
                # 保存到数据库
                self.database_manager.save_io1_control(state)
                logging.info(f"IO1控制状态已保存: {state}")
            else:
                logging.warning("IO1控制数据格式错误，缺少state字段")
        except json.JSONDecodeError:
            logging.error("IO1控制数据JSON格式错误")
        except Exception as e:
            logging.error(f"处理IO1控制数据失败: {e}")
    
    def handle_status(self, payload):
        """处理设备状态"""
        try:
            data = json.loads(payload)
            if 'status' in data:
                status = data['status']
                # 保存到数据库
                self.database_manager.save_device_status(status)
                logging.info(f"设备状态已保存: {status}")
            else:
                logging.warning("设备状态数据格式错误，缺少status字段")
        except json.JSONDecodeError:
            logging.error("设备状态数据JSON格式错误")
        except Exception as e:
            logging.error(f"处理设备状态失败: {e}")
    
    def connect(self):
        """连接到MQTT代理"""
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            self.client.loop_start()
            logging.info(f"正在连接到MQTT代理: {self.broker}:{self.port}")
        except Exception as e:
            logging.error(f"MQTT连接失败: {e}")
    
    def disconnect(self):
        """断开MQTT连接"""
        try:
            self.publish_status("offline")
            self.client.loop_stop()
            self.client.disconnect()
            logging.info("MQTT连接已断开")
        except Exception as e:
            logging.error(f"MQTT断开连接失败: {e}")
    
    def publish_io1_control(self, state):
        """发布IO1控制命令"""
        if not self.connected:
            logging.warning("MQTT未连接，无法发送控制命令")
            return False
        
        try:
            message = {
                "command": "set_io1",
                "state": state,
                "timestamp": datetime.now().isoformat()
            }
            payload = json.dumps(message)
            result = self.client.publish(self.io1_control_topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"IO1控制命令已发送: {state}")
                return True
            else:
                logging.error(f"IO1控制命令发送失败: {result.rc}")
                return False
                
        except Exception as e:
            logging.error(f"发送IO1控制命令失败: {e}")
            return False
    
    def publish_status(self, status):
        """发布状态信息"""
        if not self.connected:
            return False
        
        try:
            message = {
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "client_id": self.client_id
            }
            payload = json.dumps(message)
            result = self.client.publish(self.status_topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"状态信息已发送: {status}")
                return True
            else:
                logging.error(f"状态信息发送失败: {result.rc}")
                return False
                
        except Exception as e:
            logging.error(f"发送状态信息失败: {e}")
            return False
    
    def get_connection_status(self):
        """获取连接状态"""
        return self.connected
    
    def get_current_io1_state(self):
        """获取当前IO1状态"""
        return self.current_io1_state
