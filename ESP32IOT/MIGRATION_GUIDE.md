# ESP32IOT 迁移指南

## 从Python模拟器迁移到ESP32硬件

本指南说明如何将aiuiiot项目中的Python ESP32模拟器替换为真实的ESP32硬件设备。

## 🚀 迁移步骤

### 1. 停止Python模拟器

在aiuiiot项目中，需要禁用ESP32模拟器：

```python
# 在config.ini中设置
[ESP32_SIMULATOR]
enabled = False  # 改为False禁用模拟器
```

或者在main.py中注释掉模拟器相关代码：

```python
# 注释掉这些行
# self.esp32_simulator = ESP32Simulator(self.config_file)
# logging.info("ESP32模拟器初始化完成")
```

### 2. 配置ESP32设备

在ESP32IOT项目中修改`config.h`：

```cpp
// WiFi配置
#define WIFI_SSID "你的WiFi名称"
#define WIFI_PASSWORD "你的WiFi密码"

// MQTT配置
#define MQTT_BROKER "你的MQTT服务器IP"
#define MQTT_PORT 1883
#define MQTT_CLIENT_ID "ESP32_Device"
```

### 3. 编译和上传

使用PlatformIO编译并上传到ESP32：

```bash
# 编译项目
pio run

# 上传到ESP32
pio run --target upload

# 监控输出
pio device monitor
```

## 🔄 功能对比

### Python模拟器功能
- ✅ 模拟AD1数据生成
- ✅ 模拟IO1状态控制
- ✅ MQTT通信
- ✅ 数据统计

### ESP32硬件功能
- ✅ 真实AD1数据采集 (GPIO36)
- ✅ 真实IO1控制 (GPIO2)
- ✅ MQTT通信
- ✅ 状态LED指示
- ✅ 自动重连机制
- ✅ EEPROM配置存储
- ✅ 系统信息显示

## 📊 数据格式兼容性

### AD数据格式
ESP32发送的数据格式与Python模拟器完全兼容：

```json
{
  "device_id": "ESP32_Device",
  "channel": "AD1",
  "value": 2048,
  "unit": "ADC",
  "timestamp": 1234567890,
  "io1_state": false,
  "wifi_rssi": -45,
  "uptime": 120
}
```

### IO控制格式
支持两种控制格式：

**格式1 (简单):**
```json
{
  "state": true
}
```

**格式2 (兼容):**
```json
{
  "command": "set_io1",
  "state": true
}
```

### 状态格式
```json
{
  "device_id": "ESP32_Device",
  "status": "running",
  "timestamp": 1234567890,
  "ip": "192.168.1.100",
  "io1_state": false,
  "uptime": 120,
  "wifi_rssi": -45
}
```

## 🛠️ 硬件连接

### 必需连接
- **USB数据线**: 连接ESP32到电脑
- **电源**: 通过USB供电

### 可选连接
- **模拟传感器**: 连接到GPIO36 (VP)
- **继电器/LED**: 连接到GPIO2
- **外部电源**: 如果需要独立供电

## 🔧 配置参数

### 可调整参数
在`config.h`中可以调整：

```cpp
#define DATA_UPLOAD_INTERVAL 5000      // 数据上传间隔
#define WIFI_RETRY_INTERVAL 5000       // WiFi重连间隔
#define MQTT_RETRY_INTERVAL 5000       // MQTT重连间隔
#define MAX_WIFI_RETRY 20              // 最大重连次数
```

### 引脚配置
```cpp
#define AD1_PIN 36                     // 模拟输入引脚
#define IO1_PIN 2                      // 数字输出引脚
#define STATUS_LED 2                    // 状态LED引脚
```

## 📱 测试验证

### 1. 连接测试
- 观察串口输出
- 确认WiFi连接成功
- 确认MQTT连接成功

### 2. 功能测试
- 测试AD数据采集
- 测试IO控制功能
- 测试状态LED指示

### 3. 集成测试
- 使用MQTT客户端工具测试
- 验证数据格式兼容性
- 测试自动重连功能

## 🚨 注意事项

### 1. 网络配置
- 确保WiFi网络稳定
- 检查MQTT服务器可达性
- 确认防火墙设置

### 2. 硬件限制
- ESP32的ADC精度为12位 (0-4095)
- GPIO2有内置LED，注意电平逻辑
- 确保电源供应充足

### 3. 性能考虑
- 数据上传间隔不要太频繁
- 监控内存使用情况
- 注意WiFi信号强度

## 🔍 故障排除

### 常见问题

1. **WiFi连接失败**
   - 检查SSID和密码
   - 确认WiFi信号强度
   - 检查网络配置

2. **MQTT连接失败**
   - 检查服务器IP和端口
   - 确认网络连通性
   - 检查MQTT服务器状态

3. **数据上传失败**
   - 检查MQTT连接状态
   - 确认主题配置正确
   - 检查JSON数据格式

### 调试方法

1. **串口监控**
   - 波特率：115200
   - 观察详细日志输出

2. **LED状态指示**
   - 常亮：系统正常
   - 慢闪：WiFi已连接，MQTT未连接
   - 快闪：WiFi未连接

3. **网络诊断**
   - 使用ping测试网络连通性
   - 检查MQTT服务器状态

## 📈 性能优化

### 1. 数据上传频率
根据应用需求调整上传间隔：
- 实时监控：1-5秒
- 一般监控：5-30秒
- 长期记录：1-5分钟

### 2. 重连策略
优化重连间隔避免过于频繁：
- WiFi重连：5-10秒
- MQTT重连：5-10秒

### 3. 内存管理
- 合理设置JSON文档大小
- 避免长时间运行内存泄漏

## 🎯 下一步

### 扩展功能
1. **添加更多传感器**
   - 温湿度传感器
   - 光照传感器
   - 距离传感器

2. **增强控制功能**
   - 多路IO控制
   - PWM输出控制
   - 串口通信

3. **本地功能**
   - Web配置界面
   - OTA固件更新
   - 本地数据存储

### 集成应用
1. **智能家居**
   - Home Assistant集成
   - 自动化控制

2. **工业监控**
   - 数据采集
   - 远程控制
   - 报警功能

---

**迁移完成后，您的系统将使用真实的ESP32硬件，获得更好的性能和可靠性！** 🎉

