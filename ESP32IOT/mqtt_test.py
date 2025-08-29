#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESP32IOT MQTT测试客户端
用于测试ESP32的MQTT通信功能
"""

import paho.mqtt.client as mqtt
import json
import time
import threading
from datetime import datetime

class ESP32MQTTTester:
    def __init__(self, broker="localhost", port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        self.connected = False
        self.ad_data = []
        self.io_status = False
        
    def on_connect(self, client, userdata, flags, rc):
        """MQTT连接回调"""
        if rc == 0:
            self.connected = True
            print(f"[{datetime.now().strftime('%H:%M:%S')}] MQTT连接成功")
            
            # 订阅ESP32相关主题
            client.subscribe("esp32/+/+")
            print("已订阅主题: esp32/+/+")
            
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] MQTT连接失败，错误码: {rc}")
    
    def on_message(self, client, userdata, msg):
        """MQTT消息接收回调"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 收到消息:")
            print(f"主题: {topic}")
            print(f"内容: {payload}")
            
            # 解析JSON数据
            try:
                data = json.loads(payload)
                self.handle_message(topic, data)
            except json.JSONDecodeError:
                print("消息格式不是有效的JSON")
                
        except Exception as e:
            print(f"处理消息失败: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        """MQTT断开连接回调"""
        self.connected = False
        print(f"[{datetime.now().strftime('%H:%M:%S')}] MQTT连接断开")
    
    def handle_message(self, topic, data):
        """处理不同类型的消息"""
        if "ad1/data" in topic:
            self.handle_ad_data(data)
        elif "io1/control" in topic:
            self.handle_io_status(data)
        elif "status" in topic:
            self.handle_status(data)
    
    def handle_ad_data(self, data):
        """处理AD数据"""
        if 'ad1_value' in data:
            value = data['ad1_value']
            timestamp = data.get('timestamp', 0)
            device_id = data.get('device_id', 'Unknown')
            
            self.ad_data.append({
                'timestamp': timestamp,
                'value': value,
                'device_id': device_id
            })
            
            print(f"AD1数据: {value} (设备: {device_id})")
            
            # 保持最近10条数据
            if len(self.ad_data) > 10:
                self.ad_data.pop(0)
    
    def handle_io_status(self, data):
        """处理IO状态"""
        if 'io1_state' in data:
            self.io_status = data['io1_state']
            device_id = data.get('device_id', 'Unknown')
            print(f"IO1状态: {'ON' if self.io_status else 'OFF'} (设备: {device_id})")
    
    def handle_status(self, data):
        """处理状态信息"""
        status = data.get('status', 'Unknown')
        device_id = data.get('device_id', 'Unknown')
        ip = data.get('ip', 'Unknown')
        print(f"设备状态: {status} (设备: {device_id}, IP: {ip})")
    
    def connect(self):
        """连接到MQTT服务器"""
        try:
            print(f"正在连接到MQTT服务器: {self.broker}:{self.port}")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            # 等待连接
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(1)
                timeout -= 1
            
            return self.connected
            
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开MQTT连接"""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            print("已断开MQTT连接")
    
    def send_io_control(self, state):
        """发送IO控制命令"""
        if not self.connected:
            print("MQTT未连接，无法发送命令")
            return False
        
        message = {
            "state": state,
            "timestamp": int(time.time() * 1000),
            "source": "mqtt_tester"
        }
        
        payload = json.dumps(message)
        result = self.client.publish("esp32/io1/control", payload)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"IO控制命令已发送: {'ON' if state else 'OFF'}")
            return True
        else:
            print(f"发送失败，错误码: {result.rc}")
            return False
    
    def get_statistics(self):
        """获取统计信息"""
        print("\n=== 统计信息 ===")
        print(f"MQTT连接状态: {'已连接' if self.connected else '未连接'}")
        print(f"当前IO1状态: {'ON' if self.io_status else 'OFF'}")
        print(f"AD数据记录数: {len(self.ad_data)}")
        
        if self.ad_data:
            print("最近AD数据:")
            for i, data in enumerate(self.ad_data[-5:], 1):
                print(f"  {i}. 值: {data['value']}, 设备: {data['device_id']}")
    
    def interactive_mode(self):
        """交互模式"""
        print("\n=== ESP32 MQTT测试工具 ===")
        print("可用命令:")
        print("  on     - 打开IO1")
        print("  off    - 关闭IO1")
        print("  toggle - 切换IO1状态")
        print("  status - 显示状态信息")
        print("  quit   - 退出程序")
        print("  help   - 显示帮助信息")
        
        while True:
            try:
                command = input("\n请输入命令: ").strip().lower()
                
                if command == 'on':
                    self.send_io_control(True)
                elif command == 'off':
                    self.send_io_control(False)
                elif command == 'toggle':
                    new_state = not self.io_status
                    self.send_io_control(new_state)
                elif command == 'status':
                    self.get_statistics()
                elif command == 'quit':
                    break
                elif command == 'help':
                    print("可用命令:")
                    print("  on     - 打开IO1")
                    print("  off    - 关闭IO1")
                    print("  toggle - 切换IO1状态")
                    print("  status - 显示状态信息")
                    print("  quit   - 退出程序")
                    print("  help   - 显示帮助信息")
                else:
                    print("未知命令，输入 'help' 查看可用命令")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"命令执行失败: {e}")
        
        print("正在退出...")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ESP32 MQTT测试工具')
    parser.add_argument('--broker', default='localhost', help='MQTT服务器地址')
    parser.add_argument('--port', type=int, default=1883, help='MQTT服务器端口')
    parser.add_argument('--command', choices=['on', 'off', 'toggle'], help='直接执行IO控制命令')
    
    args = parser.parse_args()
    
    # 创建测试器
    tester = ESP32MQTTTester(args.broker, args.port)
    
    try:
        # 连接到MQTT服务器
        if not tester.connect():
            print("无法连接到MQTT服务器，程序退出")
            return
        
        # 如果指定了命令，直接执行
        if args.command:
            if args.command == 'on':
                tester.send_io_control(True)
            elif args.command == 'off':
                tester.send_io_control(False)
            elif args.command == 'toggle':
                tester.send_io_control(not tester.io_status)
            
            # 等待一段时间查看结果
            time.sleep(3)
            tester.get_statistics()
        else:
            # 进入交互模式
            tester.interactive_mode()
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行错误: {e}")
    finally:
        tester.disconnect()

if __name__ == "__main__":
    main()

