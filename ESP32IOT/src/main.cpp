/*
 * ESP32IOT - ESP32物联网控制系统
 * 基于Arduino框架，实现与aiuiiot项目Python服务器的完整对接
 * 
 * 功能特性:
 * - WiFi连接管理
 * - MQTT客户端通信
 * - AD1模拟量采集 (GPIO36)
 * - IO1数字输出控制 (GPIO2)
 * - 自动重连机制
 * - 数据定时上传
 * - 状态LED指示
 * 
 * 硬件连接:
 * - AD1: GPIO36 (VP) - 模拟输入
 * - IO1: GPIO2 - 数字输出
 * - STATUS_LED: GPIO2 - 状态指示灯
 * 
 * 作者: AI Assistant
 * 版本: 2.0
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <EEPROM.h>
#include "../config.h"

// ==================== 全局变量 ====================
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// 系统状态
bool wifiConnected = false;
bool mqttConnected = false;
bool io1State = false;
unsigned long lastDataUpload = 0;
unsigned long lastWifiRetry = 0;
unsigned long lastMqttRetry = 0;
unsigned long lastStatusPublish = 0;
unsigned long systemStartTime = 0;

// 统计信息
unsigned long dataUploadCount = 0;
unsigned long mqttMessageCount = 0;
unsigned long wifiReconnectCount = 0;
unsigned long mqttReconnectCount = 0;

// ==================== 函数声明 ====================
void setupWiFi();
void setupMQTT();
void handleWiFiConnection();
void handleMQTTConnection();
bool connectMQTT();
void mqttCallback(char* topic, byte* payload, unsigned int length);
void handleIO1Control(const char* payload);
void uploadData();
void publishStatus(const char* status);
void publishIO1Status();
void updateStatusLED();
void printSystemInfo();
void loadConfig();
void saveConfig();

// ==================== 主程序 ====================
void setup() {
  // 初始化串口
  Serial.begin(SERIAL_BAUD_RATE);
  delay(1000); // 等待串口稳定
  
  Serial.println("\n");
  Serial.println("========================================");
  Serial.println("        ESP32IOT 系统启动");
  Serial.println("========================================");
  
  // 记录系统启动时间
  systemStartTime = millis();
  
  // 初始化EEPROM
  EEPROM.begin(EEPROM_SIZE);
  
  // 加载配置
  loadConfig();
  
  // 初始化引脚
  pinMode(IO1_PIN, OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(IO1_PIN, io1State);
  digitalWrite(STATUS_LED, LOW);
  
  // 初始化WiFi
  setupWiFi();
  
  // 初始化MQTT
  setupMQTT();
  
  // 打印系统信息
  printSystemInfo();
  
  Serial.println("系统初始化完成");
  Serial.println("========================================");
}

void loop() {
  // 检查WiFi连接状态
  if (!wifiConnected) {
    handleWiFiConnection();
  }
  
  // 检查MQTT连接状态
  if (wifiConnected && !mqttConnected) {
    handleMQTTConnection();
  }
  
  // 处理MQTT消息
  if (mqttConnected) {
    mqttClient.loop();
  }
  
  // 定时上传数据
  if (mqttConnected && millis() - lastDataUpload >= DATA_UPLOAD_INTERVAL) {
    uploadData();
    lastDataUpload = millis();
  }
  
  // 定时发布状态
  if (mqttConnected && millis() - lastStatusPublish >= 30000) { // 30秒发布一次状态
    publishStatus("running");
    lastStatusPublish = millis();
  }
  
  // 状态指示
  updateStatusLED();
  
  // 短暂延时
  delay(100);
}

// ==================== WiFi管理 ====================
void setupWiFi() {
  Serial.print("正在连接WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < MAX_WIFI_RETRY) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println("\nWiFi连接成功!");
    Serial.print("IP地址: ");
    Serial.println(WiFi.localIP());
    Serial.print("信号强度: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("\nWiFi连接失败!");
    wifiConnected = false;
  }
}

void handleWiFiConnection() {
  if (millis() - lastWifiRetry >= WIFI_RETRY_INTERVAL) {
    Serial.println("尝试重新连接WiFi...");
    WiFi.disconnect();
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    lastWifiRetry = millis();
    wifiReconnectCount++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    if (!wifiConnected) {
      wifiConnected = true;
      Serial.println("WiFi重连成功!");
      Serial.print("新IP地址: ");
      Serial.println(WiFi.localIP());
    }
  }
}

// ==================== MQTT管理 ====================
void setupMQTT() {
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  
  Serial.print("正在连接MQTT服务器: ");
  Serial.println(MQTT_BROKER);
  
  if (connectMQTT()) {
    mqttConnected = true;
    Serial.println("MQTT连接成功!");
    publishStatus("online");
  } else {
    Serial.println("MQTT连接失败!");
    mqttConnected = false;
  }
}

bool connectMQTT() {
  String clientId = String(MQTT_CLIENT_ID) + "-" + String(random(0xffff), HEX);
  
  if (mqttClient.connect(clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD)) {
    // 订阅IO控制主题
    mqttClient.subscribe(MQTT_TOPIC_IO1_CONTROL);
    Serial.println("已订阅主题: " + String(MQTT_TOPIC_IO1_CONTROL));
    return true;
  }
  return false;
}

void handleMQTTConnection() {
  if (millis() - lastMqttRetry >= MQTT_RETRY_INTERVAL) {
    Serial.println("尝试重新连接MQTT...");
    if (connectMQTT()) {
      mqttConnected = true;
      Serial.println("MQTT重连成功!");
      publishStatus("online");
    } else {
      Serial.println("MQTT重连失败!");
    }
    lastMqttRetry = millis();
    mqttReconnectCount++;
  }
}

// ==================== MQTT消息处理 ====================
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("收到MQTT消息: ");
  Serial.print(topic);
  Serial.print(" -> ");
  Serial.println(message);
  
  mqttMessageCount++;
  
  if (strcmp(topic, MQTT_TOPIC_IO1_CONTROL) == 0) {
    handleIO1Control(message.c_str());
  }
}

void handleIO1Control(const char* payload) {
  DynamicJsonDocument doc(JSON_DOC_SIZE);
  DeserializationError error = deserializeJson(doc, payload);
  
  if (!error) {
    if (doc.containsKey("state")) {
      bool newState = doc["state"];
      if (newState != io1State) {
        io1State = newState;
        digitalWrite(IO1_PIN, io1State);
        digitalWrite(STATUS_LED, io1State);
        
        Serial.print("IO1状态设置为: ");
        Serial.println(io1State ? "ON" : "OFF");
        
        // 发送状态确认
        publishIO1Status();
        
        // 保存配置
        saveConfig();
      }
    } else if (doc.containsKey("command") && doc["command"] == "set_io1") {
      if (doc.containsKey("state")) {
        bool newState = doc["state"];
        if (newState != io1State) {
          io1State = newState;
          digitalWrite(IO1_PIN, io1State);
          digitalWrite(STATUS_LED, io1State);
          
          Serial.print("IO1状态设置为: ");
          Serial.println(io1State ? "ON" : "OFF");
          
          // 发送状态确认
          publishIO1Status();
          
          // 保存配置
          saveConfig();
        }
      }
    }
  } else {
    Serial.println("JSON解析失败");
  }
}

// ==================== 数据上传 ====================
void uploadData() {
  // 读取AD1值
  int ad1Value = analogRead(AD1_PIN);
  
  // 创建JSON数据 - 与Python服务器格式保持一致
  DynamicJsonDocument doc(JSON_DOC_SIZE);
  doc["device_id"] = MQTT_CLIENT_ID;
  doc["channel"] = "AD1";
  doc["value"] = ad1Value;
  doc["unit"] = "ADC";
  doc["timestamp"] = millis();
  doc["io1_state"] = io1State;
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = (millis() - systemStartTime) / 1000;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  // 发布数据
  if (mqttClient.publish(MQTT_TOPIC_AD1_DATA, jsonString.c_str())) {
    Serial.print("数据上传成功: ");
    Serial.println(jsonString);
    dataUploadCount++;
  } else {
    Serial.println("数据上传失败");
  }
}

// ==================== 状态发布 ====================
void publishStatus(const char* status) {
  DynamicJsonDocument doc(JSON_DOC_SIZE);
  doc["device_id"] = MQTT_CLIENT_ID;
  doc["status"] = status;
  doc["timestamp"] = millis();
  doc["ip"] = WiFi.localIP().toString();
  doc["io1_state"] = io1State;
  doc["uptime"] = (millis() - systemStartTime) / 1000;
  doc["wifi_rssi"] = WiFi.RSSI();
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  mqttClient.publish(MQTT_TOPIC_STATUS, jsonString.c_str());
}

void publishIO1Status() {
  DynamicJsonDocument doc(JSON_DOC_SIZE);
  doc["device_id"] = MQTT_CLIENT_ID;
  doc["channel"] = "IO1";
  doc["state"] = io1State;
  doc["timestamp"] = millis();
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  mqttClient.publish(MQTT_TOPIC_IO1_CONTROL, jsonString.c_str());
}

// ==================== 状态指示 ====================
void updateStatusLED() {
  static unsigned long lastBlink = 0;
  static bool ledState = false;
  
  if (wifiConnected && mqttConnected) {
    // 系统正常 - LED常亮
    digitalWrite(STATUS_LED, HIGH);
  } else if (wifiConnected && !mqttConnected) {
    // WiFi已连接，MQTT未连接 - LED慢闪
    if (millis() - lastBlink >= 1000) {
      ledState = !ledState;
      digitalWrite(STATUS_LED, ledState);
      lastBlink = millis();
    }
  } else {
    // WiFi未连接 - LED快闪
    if (millis() - lastBlink >= 200) {
      ledState = !ledState;
      digitalWrite(STATUS_LED, ledState);
      lastBlink = millis();
    }
  }
}

// ==================== 系统信息 ====================
void printSystemInfo() {
  Serial.println("系统信息:");
  Serial.print("  芯片型号: ");
  Serial.println(ESP.getChipModel());
  Serial.print("  芯片版本: ");
  Serial.println(ESP.getChipRevision());
  Serial.print("  CPU频率: ");
  Serial.print(ESP.getCpuFreqMHz());
  Serial.println(" MHz");
  Serial.print("  闪存大小: ");
  Serial.print(ESP.getFlashChipSize() / 1024 / 1024);
  Serial.println(" MB");
  Serial.print("  可用内存: ");
  Serial.print(ESP.getFreeHeap() / 1024);
  Serial.println(" KB");
  Serial.print("  数据上传间隔: ");
  Serial.print(DATA_UPLOAD_INTERVAL);
  Serial.println(" ms");
  Serial.print("  MQTT服务器: ");
  Serial.print(MQTT_BROKER);
  Serial.print(":");
  Serial.println(MQTT_PORT);
}

// ==================== 配置管理 ====================
void loadConfig() {
  // 从EEPROM读取IO1默认状态
  if (EEPROM.read(0) == 0xAA) {
    io1State = EEPROM.read(1);
    Serial.println("从EEPROM加载配置");
  } else {
    Serial.println("使用默认配置");
    io1State = false;
  }
}

void saveConfig() {
  EEPROM.write(0, 0xAA);  // 配置标识
  EEPROM.write(1, io1State);
  EEPROM.commit();
  Serial.println("配置已保存到EEPROM");
}
 