#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESP32模拟器禁用脚本
用于禁用aiuiiot项目中的ESP32模拟器，改为使用真实的ESP32硬件
"""

import os
import sys
import configparser
import shutil
from datetime import datetime

def backup_file(file_path):
    """备份文件"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"已备份文件: {backup_path}")
        return backup_path
    return None

def disable_simulator_in_config(config_file):
    """在config.ini中禁用模拟器"""
    if not os.path.exists(config_file):
        print(f"配置文件不存在: {config_file}")
        return False
    
    # 备份原文件
    backup_file(config_file)
    
    # 读取配置
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # 检查是否有ESP32_SIMULATOR节
    if 'ESP32_SIMULATOR' not in config:
        print("配置文件中没有找到ESP32_SIMULATOR节")
        return False
    
    # 禁用模拟器
    config['ESP32_SIMULATOR']['enabled'] = 'False'
    
    # 保存配置
    with open(config_file, 'w', encoding='utf-8') as f:
        config.write(f)
    
    print(f"已在 {config_file} 中禁用ESP32模拟器")
    return True

def comment_simulator_in_main(main_file):
    """在main.py中注释掉模拟器相关代码"""
    if not os.path.exists(main_file):
        print(f"主程序文件不存在: {main_file}")
        return False
    
    # 备份原文件
    backup_file(main_file)
    
    # 读取文件内容
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 需要注释的行
    lines_to_comment = [
        'self.esp32_simulator = ESP32Simulator(self.config_file)',
        'logging.info("ESP32模拟器初始化完成")',
        'self.esp32_simulator.connect()',
        'self.esp32_simulator.disconnect()',
        'self.esp32_simulator.get_status()'
    ]
    
    # 注释相关行
    modified = False
    for line in lines_to_comment:
        if line in content and not line.startswith('#'):
            content = content.replace(line, f'# {line}')
            modified = True
            print(f"已注释: {line}")
    
    if modified:
        # 保存修改后的文件
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已在 {main_file} 中注释掉模拟器相关代码")
        return True
    else:
        print("未找到需要注释的模拟器代码")
        return False

def create_migration_note(project_dir):
    """创建迁移说明文件"""
    note_file = os.path.join(project_dir, "ESP32_MIGRATION_NOTE.md")
    
    note_content = """# ESP32模拟器迁移说明

## 已完成的更改

1. **配置文件修改**
   - 在 `config.ini` 中设置 `enabled = False`
   - ESP32模拟器已被禁用

2. **代码修改**
   - 在 `main.py` 中注释掉模拟器相关代码
   - 模拟器不再启动和运行

## 下一步操作

### 1. 配置ESP32硬件
在ESP32IOT项目中修改 `config.h`：
```cpp
#define WIFI_SSID "你的WiFi名称"
#define WIFI_PASSWORD "你的WiFi密码"
#define MQTT_BROKER "你的MQTT服务器IP"
```

### 2. 编译和上传ESP32
```bash
cd ESP32IOT
pio run --target upload
```

### 3. 测试连接
- 确保ESP32连接到网络
- 验证MQTT通信正常
- 测试AD数据采集和IO控制

## 注意事项

- 原文件已备份，如需恢复请查看 `.backup_*` 文件
- 确保ESP32硬件正常工作后再完全禁用模拟器
- 建议先在测试环境中验证迁移效果

## 获取帮助

如有问题，请参考：
- ESP32IOT项目文档
- MIGRATION_GUIDE.md
- 项目README文件

---
迁移时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""".format(datetime=datetime)
    
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(note_content)
    
    print(f"已创建迁移说明文件: {note_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("        ESP32模拟器禁用工具")
    print("=" * 60)
    print()
    
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查是否在aiuiiot项目目录中
    config_file = "config.ini"
    main_file = "main.py"
    
    if not os.path.exists(config_file):
        print("错误: 未找到config.ini文件")
        print("请确保在aiuiiot项目根目录中运行此脚本")
        return
    
    print("检测到aiuiiot项目，开始禁用ESP32模拟器...")
    print()
    
    # 禁用配置文件中的模拟器
    if disable_simulator_in_config(config_file):
        print("✅ 配置文件修改成功")
    else:
        print("❌ 配置文件修改失败")
    
    print()
    
    # 注释main.py中的模拟器代码
    if comment_simulator_in_main(main_file):
        print("✅ 主程序代码修改成功")
    else:
        print("❌ 主程序代码修改失败")
    
    print()
    
    # 创建迁移说明
    create_migration_note(current_dir)
    
    print("=" * 60)
    print("🎉 ESP32模拟器禁用完成！")
    print("=" * 60)
    print()
    print("下一步操作:")
    print("1. 配置ESP32硬件 (修改ESP32IOT/config.h)")
    print("2. 编译并上传ESP32程序")
    print("3. 测试硬件连接和通信")
    print("4. 查看ESP32_MIGRATION_NOTE.md了解详细信息")
    print()
    print("注意: 原文件已备份，如需恢复请查看.backup_*文件")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        print("请检查文件权限和项目结构")

