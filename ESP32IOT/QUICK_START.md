# ESP32IOT 快速启动指南

## 🚀 5分钟快速开始

### 1. 环境准备
- 确保已安装PlatformIO扩展
- 连接ESP32开发板到电脑
- 确认开发板型号（ESP32 Dev Module）

### 2. 项目配置
编辑 `src/main.cpp` 中的配置参数：
```cpp
#define WIFI_SSID "你的WiFi名称"
#define WIFI_PASSWORD "你的WiFi密码"
#define MQTT_BROKER "你的MQTT服务器IP"
```

### 3. 编译项目
在Cursor中按 `Ctrl+Shift+P`，然后：
1. 输入 "PlatformIO: Build"
2. 选择并执行

### 4. 上传程序
编译成功后：
1. 按 `Ctrl+Shift+P`
2. 输入 "PlatformIO: Upload"
3. 选择并执行

### 5. 监控输出
上传完成后：
1. 按 `Ctrl+Shift+P`
2. 输入 "PlatformIO: Monitor"
3. 观察串口输出

## 🔧 常见问题解决

### PlatformIO扩展没有编译按钮？
1. 重新加载窗口：`Ctrl+Shift+P` → "Developer: Reload Window"
2. 重建索引：`Ctrl+Shift+P` → "PlatformIO: Rebuild IntelliSense Index"
3. 检查项目根目录是否有 `platformio.ini` 文件

### 编译失败？
1. 检查依赖库是否正确安装
2. 确认ESP32开发板选择正确
3. 查看错误日志，根据提示修复

### 上传失败？
1. 检查USB连接
2. 按住ESP32的BOOT按钮再点击上传
3. 确认COM端口选择正确

## 📱 测试功能

### WiFi连接测试
- 观察串口输出中的WiFi连接状态
- 确认获取到IP地址

### MQTT通信测试
- 使用MQTT客户端工具订阅主题
- 发送控制命令测试IO功能

### 传感器测试
- 连接模拟传感器到GPIO36
- 观察数据上传情况

## 🎯 下一步

- 阅读完整README文档
- 自定义配置参数
- 添加更多传感器
- 开发Web控制界面

## 📞 获取帮助

- 查看项目README文档
- 提交GitHub Issue
- 参考PlatformIO官方文档

