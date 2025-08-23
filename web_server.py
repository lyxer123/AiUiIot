from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import configparser
from database import DatabaseManager
from mqtt_client import MQTTClient

class WebServer:
    def __init__(self, config_file, database_manager, mqtt_client):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # 创建Flask应用
        self.app = Flask(__name__)
        CORS(self.app)  # 启用跨域支持
        
        # 配置
        self.host = self.config.get('WEB_SERVER', 'host')
        self.port = self.config.getint('WEB_SERVER', 'port')
        self.debug = self.config.getboolean('WEB_SERVER', 'debug')
        
        # 依赖组件
        self.database_manager = database_manager
        self.mqtt_client = mqtt_client
        
        # 注册路由
        self.register_routes()
        
    def register_routes(self):
        """注册API路由"""
        
        @self.app.route('/api/status', methods=['GET'])
        def get_system_status():
            """获取系统状态"""
            try:
                mqtt_status = self.mqtt_client.get_connection_status()
                io1_state = self.mqtt_client.get_current_io1_state()
                
                status = {
                    "mqtt_connected": mqtt_status,
                    "io1_current_state": io1_state,
                    "system_status": "running"
                }
                return jsonify({"success": True, "data": status})
            except Exception as e:
                logging.error(f"获取系统状态失败: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.app.route('/api/ad1/data', methods=['GET'])
        def get_ad1_data():
            """获取AD1数据"""
            try:
                limit = request.args.get('limit', 100, type=int)
                data = self.database_manager.get_latest_ad1_data(limit)
                
                # 格式化数据
                formatted_data = []
                for value, timestamp in data:
                    formatted_data.append({
                        "value": value,
                        "timestamp": timestamp
                    })
                
                return jsonify({"success": True, "data": formatted_data})
            except Exception as e:
                logging.error(f"获取AD1数据失败: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.app.route('/api/io1/control', methods=['GET'])
        def get_io1_control_history():
            """获取IO1控制历史"""
            try:
                limit = request.args.get('limit', 50, type=int)
                data = self.database_manager.get_latest_io1_control(limit)
                
                # 格式化数据
                formatted_data = []
                for state, timestamp in data:
                    formatted_data.append({
                        "state": state,
                        "timestamp": timestamp
                    })
                
                return jsonify({"success": True, "data": formatted_data})
            except Exception as e:
                logging.error(f"获取IO1控制历史失败: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.app.route('/api/io1/control', methods=['POST'])
        def set_io1_control():
            """设置IO1控制状态"""
            try:
                data = request.get_json()
                if not data or 'state' not in data:
                    return jsonify({"success": False, "error": "缺少state参数"}), 400
                
                state = data['state']
                if not isinstance(state, bool):
                    return jsonify({"success": False, "error": "state必须是布尔值"}), 400
                
                # 发送MQTT控制命令
                success = self.mqtt_client.publish_io1_control(state)
                
                if success:
                    return jsonify({"success": True, "message": f"IO1控制命令已发送: {state}"})
                else:
                    return jsonify({"success": False, "error": "MQTT未连接，无法发送控制命令"}), 500
                    
            except Exception as e:
                logging.error(f"设置IO1控制失败: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.app.route('/api/device/status', methods=['GET'])
        def get_device_status_history():
            """获取设备状态历史"""
            try:
                limit = request.args.get('limit', 50, type=int)
                data = self.database_manager.get_device_status_history(limit)
                
                # 格式化数据
                formatted_data = []
                for status, timestamp in data:
                    formatted_data.append({
                        "status": status,
                        "timestamp": timestamp
                    })
                
                return jsonify({"success": True, "data": formatted_data})
            except Exception as e:
                logging.error(f"获取设备状态历史失败: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.app.route('/api/io1/current', methods=['GET'])
        def get_current_io1_state():
            """获取当前IO1状态"""
            try:
                state = self.mqtt_client.get_current_io1_state()
                return jsonify({"success": True, "data": {"state": state}})
            except Exception as e:
                logging.error(f"获取当前IO1状态失败: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.app.route('/api/mqtt/status', methods=['GET'])
        def get_mqtt_status():
            """获取MQTT连接状态"""
            try:
                connected = self.mqtt_client.get_connection_status()
                return jsonify({"success": True, "data": {"connected": connected}})
            except Exception as e:
                logging.error(f"获取MQTT状态失败: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.app.route('/api/test', methods=['GET'])
        def test_api():
            """测试API接口"""
            return jsonify({
                "success": True,
                "message": "ESP32后台系统API运行正常",
                "timestamp": "2024-01-01T00:00:00Z"
            })
    
    def start(self):
        """启动Web服务器"""
        try:
            logging.info(f"Web服务器正在启动: {self.host}:{self.port}")
            # 在非主线程中运行Flask时，使用更兼容的配置
            self.app.run(
                host=self.host, 
                port=self.port, 
                debug=False, 
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            logging.error(f"Web服务器启动失败: {e}")
            # 尝试使用更简单的启动方式
            try:
                logging.info("尝试使用备用启动方式...")
                from werkzeug.serving import run_simple
                run_simple(self.host, self.port, self.app, use_reloader=False, threaded=True)
            except Exception as e2:
                logging.error(f"备用启动方式也失败: {e2}")
    
    def stop(self):
        """停止Web服务器"""
        logging.info("Web服务器正在停止")
        # Flask应用会在主线程结束时自动停止
