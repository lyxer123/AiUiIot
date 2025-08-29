# ESP32IOT - ESP32物联网控制系统

基于Arduino框架的ESP32物联网控制系统，支持WiFi连接、MQTT通信、AD采集和IO控制。

## 功能特性

- WiFi连接管理
- MQTT客户端通信
- 模拟量采集（AD1）
- 数字IO控制（IO1）
- 状态LED指示
- JSON数据格式
- 自动重连机制

## 硬件要求

- ESP32开发板
- 连接线
- 可选：传感器、继电器等外设

## 引脚定义

- `AD1_PIN`: GPIO36 (VP) - 模拟量输入
- `IO1_PIN`: GPIO2 - 数字输出控制
- `STATUS_LED`: GPIO2 - 状态指示LED

## 软件环境

- PlatformIO Core
- Arduino框架
- 依赖库：ArduinoJson, PubSubClient

## 编译和上传

### 使用PlatformIO CLI

```bash
# 编译项目
pio run

# 上传到ESP32
pio run --target upload

# 监控串口输出
pio device monitor

# 清理编译文件
pio run --target clean
```

### 使用PlatformIO IDE

1. 在Cursor中安装PlatformIO扩展
2. 打开项目文件夹
3. 使用PlatformIO工具栏进行编译、上传和监控

## 配置说明

在`src/main.cpp`中修改以下配置：

```cpp
#define WIFI_SSID "YourWiFiSSID"        // WiFi名称
#define WIFI_PASSWORD "YourWiFiPassword" // WiFi密码
#define MQTT_BROKER "192.168.1.100"     // MQTT服务器地址
#define MQTT_PORT 1883                  // MQTT端口
#define MQTT_CLIENT_ID "ESP32_Device"   // 客户端ID
```

## MQTT主题

- `esp32/ad1/data` - 传感器数据发布
- `esp32/io1/control` - IO控制订阅
- `esp32/status` - 设备状态发布

## 数据格式

传感器数据JSON格式：
```json
{
  "ad1": 2048,
  "io1": false,
  "timestamp": 1234567890
}
```

## 故障排除

### 编译问题
1. 确保PlatformIO扩展已正确安装
2. 检查依赖库是否正确安装
3. 重新构建IntelliSense索引

### 上传问题
1. 检查USB连接
2. 确认开发板型号选择正确
3. 检查串口驱动

### 运行问题
1. 检查WiFi配置
2. 确认MQTT服务器地址和端口
3. 查看串口输出日志

## 许可证

MIT License
