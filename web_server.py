from flask import Flask, send_from_directory
from flask_cors import CORS
import configparser
import logging

class WebServer:
    def __init__(self, config_file, database_manager, mqtt_client):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # 获取端口配置
        self.port = self.config.getint('WEB_SERVER', 'port')
        
        # 创建Flask应用
        self.app = Flask(__name__, static_folder='static')
        
        # CORS配置
        CORS(self.app, resources={
            r"/*": {"origins": "*"}
        })

        # 路由配置
        @self.app.route('/')
        def index():
            return send_from_directory('static', 'web_accessible.html')
            
        @self.app.route('/web_accessible.html')
        def serve_html():
            return send_from_directory('static', 'web_accessible.html')
            
        @self.app.route('/static/<path:filename>')
        def static_files(filename):
            return send_from_directory('static', filename)

        # 其他原有API路由保持不变...
        # [保留原有的API路由代码]

    def start(self):
        self.app.run(host=self.config.get('WEB_SERVER', 'host'),
                   port=self.config.getint('WEB_SERVER', 'port'),
                   debug=False)