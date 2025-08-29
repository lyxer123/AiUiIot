import socket
import os
import re
import logging
import configparser
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/ip_config.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("IP_CONFIG")

class IPConfigManager:
    """IP配置管理器，用于动态获取和更新服务器IP地址"""
    
    def __init__(self, config_file="config.ini"):
        """初始化IP配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        # 创建日志目录
        Path("logs").mkdir(exist_ok=True)
        
        # 读取配置文件
        if os.path.exists(config_file):
            self.config.read(config_file)
        else:
            logger.warning(f"配置文件不存在: {config_file}，将使用默认配置")
            self._create_default_config()
        
        # 确保配置文件中有MQTT部分
        if 'MQTT' not in self.config:
            self.config['MQTT'] = {}
        
        # 获取当前IP并更新配置
        self.current_ip = get_local_ip()
        self._update_config_ip()
    
    def _create_default_config(self):
        """创建默认配置文件"""
        self.config['MQTT'] = {
            'broker': '127.0.0.1',
            'port': '1883',
            'client_id': 'esp32_backend',
            'username': '',
            'password': '',
            'keepalive': '60'
        }
        
        self.config['TOPICS'] = {
            'ad1_data': 'esp32/ad1/data',
            'io1_control': 'esp32/io1/control',
            'status': 'esp32/status'
        }
        
        with open(self.config_file, 'w') as f:
            self.config.write(f)
        
        logger.info(f"已创建默认配置文件: {self.config_file}")
    
    def _update_config_ip(self):
        """更新配置文件中的IP地址"""
        if 'broker' in self.config['MQTT']:
            old_ip = self.config['MQTT']['broker']
            if old_ip != self.current_ip:
                self.config['MQTT']['broker'] = self.current_ip
                with open(self.config_file, 'w') as f:
                    self.config.write(f)
                logger.info(f"已更新配置文件中的MQTT代理IP: {old_ip} -> {self.current_ip}")
    
    def get_mqtt_broker(self):
        """获取MQTT代理地址"""
        return self.current_ip
    
    def update_project_files(self):
        """更新项目中所有需要IP地址的文件"""
        return update_project_ip()
    
    def update_config_with_dynamic_ip(self, force_update=False):
        """更新配置和项目文件中的IP地址
        
        这个方法会:
        1. 获取当前服务器IP
        2. 更新配置文件中的MQTT代理IP
        3. 更新项目中所有需要IP地址的文件
        
        Args:
            force_update: 是否强制更新，即使IP没有变化
        
        Returns:
            str: 当前服务器IP
        """
        try:
            # 重新获取当前IP（可能已经变化）
            old_ip = self.current_ip
            self.current_ip = get_local_ip()
            
            # 如果强制更新或IP已变化，则更新配置
            if force_update or old_ip != self.current_ip:
                # 更新配置文件中的IP
                self._update_config_ip()
                
                # 更新项目文件中的IP
                update_project_ip()
                
                logger.info(f"IP配置已{'强制' if force_update else ''}更新: {old_ip} -> {self.current_ip}")
            else:
                logger.info(f"IP未变化，无需更新: {self.current_ip}")
            
            return self.current_ip
        except Exception as e:
            logger.error(f"更新动态IP配置失败: {e}")
            return self.current_ip

    def update_esp32_config(self, esp32_ip=None):
        """更新ESP32设备的配置
        
        Args:
            esp32_ip: ESP32设备的IP地址，如果为None则使用当前服务器IP
        
        Returns:
            bool: 更新是否成功
        """
        try:
            target_ip = esp32_ip if esp32_ip else self.current_ip
            logger.info(f"正在更新ESP32配置，目标IP: {target_ip}")
            
            # 这里可以添加ESP32特定的配置更新逻辑
            # 例如通过SSH或HTTP API更新ESP32设备的配置
            
            return True
        except Exception as e:
            logger.error(f"更新ESP32配置失败: {e}")
            return False

    def get_primary_ip(self):
        """获取主IP地址
        
        Returns:
            str: 主IP地址
        """
        return self.current_ip

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 创建一个临时socket连接来确定使用哪个IP地址连接到外部网络
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要真正连接
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logger.error(f"获取本地IP失败: {e}")
        # 如果上述方法失败，尝试获取所有非回环IP地址
        try:
            hostname = socket.gethostname()
            ip_list = socket.gethostbyname_ex(hostname)[2]
            for ip in ip_list:
                if not ip.startswith("127."):
                    return ip
            return "127.0.0.1"  # 如果找不到非回环地址，返回本地回环地址
        except Exception as e:
            logger.error(f"获取备用IP失败: {e}")
            return "127.0.0.1"

def update_file_ip(file_path, old_ip_pattern, replacement_pattern, new_ip):
    """更新文件中的IP地址
    
    Args:
        file_path: 文件路径
        old_ip_pattern: 匹配旧IP的正则表达式
        replacement_pattern: 替换模式，使用 {ip} 作为占位符
        new_ip: 新的IP地址
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            return False
            
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 检查是否需要更新
        matches = re.findall(old_ip_pattern, content)
        if not matches:
            logger.info(f"文件 {file_path} 中没有找到匹配的IP地址")
            return False
            
        # 替换IP地址
        actual_replacement = replacement_pattern.format(ip=new_ip)
        updated_content = re.sub(old_ip_pattern, actual_replacement, content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
            
        logger.info(f"已更新文件 {file_path} 中的IP地址: {matches[0]} -> {new_ip}")
        return True
    except Exception as e:
        logger.error(f"更新文件 {file_path} 中的IP地址失败: {e}")
        return False

def update_project_ip():
    """更新项目中所有需要IP地址的文件"""
    current_ip = get_local_ip()
    logger.info(f"当前服务器IP: {current_ip}")
    
    # 定义需要更新的文件和对应的IP正则表达式
    files_to_update = [
        # ESP32 相关配置文件
        {
            "path": "ESP32IOT/src/config.h",
            "pattern": r'#define MQTT_SERVER\s+"(\d+\.\d+\.\d+\.\d+)"',
            "replacement": '#define MQTT_SERVER "{ip}"'
        },
        # Android App 配置
        {
            "path": "android_app/app/src/main/java/com/example/iotapp/utils/Constants.java",
            "pattern": r'public static final String MQTT_SERVER = "(\d+\.\d+\.\d+\.\d+)";',
            "replacement": 'public static final String MQTT_SERVER = "{ip}";'
        },
        # 小程序配置
        {
            "path": "miniprogram/app.js",
            "pattern": r'mqttServer:\s*[\'"](\d+\.\d+\.\d+\.\d+)[\'"]',
            "replacement": 'mqttServer: "{ip}"'
        },
        # Web 配置文件
        {
            "path": "web/config.js",
            "pattern": r'const serverIp = [\'"](\d+\.\d+\.\d+\.\d+)[\'"];',
            "replacement": 'const serverIp = "{ip}";'
        }
    ]
    
    # 创建日志目录
    Path("logs").mkdir(exist_ok=True)
    
    updated_count = 0
    # 更新每个文件
    for file_info in files_to_update:
        file_path = file_info["path"]
        pattern = file_info["pattern"]
        replacement = file_info["replacement"]
        
        if update_file_ip(file_path, pattern, replacement, current_ip):
            updated_count += 1
    
    logger.info(f"IP地址更新完成，共更新 {updated_count} 个文件")
    return current_ip

if __name__ == "__main__":
    ip = update_project_ip()
    print(f"服务器IP已更新为: {ip}")