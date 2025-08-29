/*
 * ESP32IOT 配置文件
 * 用户可以根据需要修改以下配置参数
 */

#ifndef CONFIG_H
#define CONFIG_H

// ==================== WiFi配置 ====================
#define WIFI_SSID "YourWiFiSSID"           // WiFi网络名称
#define WIFI_PASSWORD "YourWiFiPassword"    // WiFi网络密码

// ==================== MQTT配置 ====================
#define MQTT_BROKER "192.168.1.100"        // MQTT服务器IP地址
#define MQTT_PORT 1883                     // MQTT服务器端口
#define MQTT_CLIENT_ID "ESP32_Device"      // MQTT客户端ID
#define MQTT_USERNAME ""                   // MQTT用户名（可选）
#define MQTT_PASSWORD ""                   // MQTT密码（可选）

// ==================== 引脚配置 ====================
#define AD1_PIN 36                         // AD1模拟输入引脚 (GPIO36/VP)
#define IO1_PIN 2                          // IO1数字输出引脚 (GPIO2)
#define STATUS_LED 2                        // 状态指示灯引脚 (与IO1共用)

// ==================== 系统参数 ====================
#define DATA_UPLOAD_INTERVAL 5000          // 数据上传间隔(毫秒)
#define WIFI_RETRY_INTERVAL 5000           // WiFi重连间隔(毫秒)
#define MQTT_RETRY_INTERVAL 5000           // MQTT重连间隔(毫秒)
#define SERIAL_BAUD_RATE 115200            // 串口波特率

// ==================== MQTT主题配置 ====================
#define MQTT_TOPIC_AD1_DATA "esp32/ad1/data"           // AD数据上传主题
#define MQTT_TOPIC_IO1_CONTROL "esp32/io1/control"     // IO控制主题
#define MQTT_TOPIC_STATUS "esp32/status"                // 状态上报主题

// ==================== 调试配置 ====================
#define DEBUG_ENABLED true                 // 启用调试输出
#define DEBUG_LEVEL 3                      // 调试级别 (0-5)

// ==================== 高级配置 ====================
#define EEPROM_SIZE 512                    // EEPROM大小
#define JSON_DOC_SIZE 200                  // JSON文档大小
#define MAX_WIFI_RETRY 20                  // 最大WiFi重连次数
#define MQTT_KEEPALIVE 60                  // MQTT保活时间

// ==================== 功能开关 ====================
#define FEATURE_AUTO_RECONNECT true        // 启用自动重连
#define FEATURE_STATUS_LED true            // 启用状态LED
#define FEATURE_EEPROM_CONFIG true         // 启用EEPROM配置存储
#define FEATURE_SYSTEM_INFO true           // 启用系统信息显示

#endif // CONFIG_H

