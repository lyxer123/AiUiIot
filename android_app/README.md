# ESP32智能控制系统 - Android应用

## 📱 项目简介

这是一个基于Android Studio开发的ESP32智能控制系统移动应用，提供完整的用户管理、设备控制和数据监控功能。

## ✨ 主要功能

### 1. 用户管理
- **用户注册**: 支持新用户注册，包含用户名、密码和邮箱
- **用户登录**: 安全的用户身份验证系统
- **本地存储**: 使用SQLite数据库存储用户信息
- **会话管理**: 自动保存登录状态

### 2. 网络连接
- **服务器连接**: 通过WiFi连接到ESP32后端服务器
- **IP配置**: 可配置服务器IP地址和端口
- **连接测试**: 实时测试网络连接状态
- **HTTP通信**: 使用OkHttp3进行REST API调用

### 3. 设备控制
- **IO1控制**: 实时控制ESP32的IO1引脚开关状态
- **状态监控**: 实时显示MQTT连接状态和系统运行状态
- **自动刷新**: 每5秒自动刷新设备状态
- **手动控制**: 支持手动开关控制

### 4. 数据监控
- **AD1数据**: 实时显示ESP32的AD1通道数据
- **历史记录**: 查看数据采集的历史记录
- **分页加载**: 支持分页加载更多历史数据
- **自动更新**: 每10秒自动刷新数据

## 🏗️ 技术架构

### 开发环境
- **语言**: Java 8+
- **最低SDK**: Android 7.0 (API 24)
- **目标SDK**: Android 14 (API 36)
- **开发工具**: Android Studio

### 核心技术
- **网络通信**: OkHttp3 + JSON
- **数据存储**: SQLite + SharedPreferences
- **UI框架**: Material Design + RecyclerView + CardView
- **异步处理**: Handler + Runnable
- **架构模式**: MVC模式

### 项目结构
```
AIIOT/
├── app/src/main/java/com/example/aiiot/
│   ├── MainActivity.java              # 主活动（登录/注册）
│   ├── ControlActivity.java           # 设备控制页面
│   ├── DataMonitorActivity.java       # 数据监控页面
│   ├── SettingsActivity.java          # 设置页面
│   ├── model/
│   │   ├── User.java                  # 用户数据模型
│   │   └── ESP32Data.java            # ESP32数据模型
│   ├── network/
│   │   └── NetworkManager.java        # 网络管理器
│   ├── database/
│   │   └── UserDatabaseHelper.java    # 用户数据库管理器
│   └── adapter/
│       └── DataAdapter.java           # 数据适配器
├── app/src/main/res/
│   ├── layout/                        # 布局文件
│   └── drawable/                      # 资源文件
└── README.md                          # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

#### Android Studio
1. 下载并安装 [Android Studio](https://developer.android.com/studio)
2. 确保已安装Android SDK 24-36

#### 后端服务
确保你的ESP32后端系统正在运行：
```bash
cd AiUiIot
python main.py
```

### 2. 导入项目

1. 打开Android Studio
2. 选择"Open an existing Android Studio project"
3. 选择项目目录：`AIIOT/`
4. 等待Gradle同步完成

### 3. 配置网络

#### 修改默认服务器地址
编辑 `NetworkManager.java` 中的默认服务器地址：
```java
this.baseUrl = prefs.getString("server_url", "http://YOUR_IP:5000/api");
```

#### 或在运行时配置
1. 启动应用
2. 注册并登录账号
3. 进入"系统设置"页面
4. 修改服务器地址
5. 点击"保存"和"测试连接"

### 4. 构建运行

1. 连接Android设备或启动模拟器
2. 点击"Run"按钮
3. 选择目标设备
4. 等待应用安装和启动

## 📋 使用说明

### 基本操作流程

1. **启动应用**
   - 首次使用需要注册账号
   - 输入用户名和密码登录

2. **配置网络**
   - 进入"系统设置"页面
   - 输入服务器IP地址（例如：http://192.168.1.100:5000/api）
   - 测试连接是否正常

3. **监控数据**
   - 进入"数据监控"页面
   - 查看AD1通道实时数据
   - 浏览历史数据记录

4. **控制设备**
   - 进入"设备控制"页面
   - 查看连接状态
   - 使用开关控制IO1

### 网络配置说明

#### 本地网络连接
- 手机和服务器必须在同一WiFi网络
- 服务器默认端口：5000
- 支持HTTP和HTTPS协议
- 默认服务器地址：http://192.168.1.100:5000/api

#### 修改服务器地址
在设置页面输入完整的API地址，格式如下：
```
http://[服务器IP]:[端口]/api
例如：http://192.168.1.100:5000/api
```

## 🔧 配置说明

### 网络配置
```java
// NetworkManager.java
serverConfig: {
  baseUrl: 'http://192.168.1.100:5000/api', // 修改为你的服务器IP
  timeout: 10000  // 请求超时时间(毫秒)
}
```

### 自动刷新配置
```java
// 控制页面自动刷新间隔(毫秒)
private static final int REFRESH_INTERVAL = 5000; // 5秒

// 数据页面自动刷新间隔(毫秒)
private static final int REFRESH_INTERVAL = 10000; // 10秒
```

### 用户管理配置
```java
// 密码最小长度
if (password.length() < 6) {
    Toast.makeText(this, "密码长度至少6位", Toast.LENGTH_SHORT).show();
    return;
}
```

## 📱 界面说明

### 主界面
- **登录/注册**: 用户身份验证
- **功能导航**: 跳转到各个功能页面
- **用户状态**: 显示当前登录用户

### 设备控制界面
- **系统状态**: 显示MQTT连接和设备状态
- **IO1控制**: 开关控制界面
- **连接测试**: 测试网络连接

### 数据监控界面
- **实时数据**: 显示当前AD值和更新时间
- **历史数据**: 分页显示历史记录
- **数据操作**: 刷新和加载更多

### 设置界面
- **服务器配置**: 修改服务器地址
- **连接测试**: 测试网络连接
- **设置重置**: 恢复默认配置

## 🐛 常见问题

### Q: 应用无法连接到服务器
**A**: 检查以下配置：
1. 服务器IP地址是否正确
2. 手机和服务器是否在同一网络
3. 防火墙是否阻止了5000端口
4. 后端服务是否正在运行

### Q: 控制命令执行失败
**A**: 可能的原因：
1. MQTT连接断开
2. ESP32设备离线
3. 网络延迟过高
4. 后端服务异常

### Q: 数据不更新
**A**: 解决方案：
1. 检查自动刷新是否开启
2. 手动点击刷新按钮
3. 检查网络连接状态
4. 重启应用

### Q: 应用崩溃
**A**: 处理方法：
1. 检查Android版本兼容性
2. 查看Logcat错误信息
3. 清除应用数据重新配置
4. 重新安装应用

## 🔄 更新维护

### 版本更新
1. 修改代码后重新构建
2. 测试功能正常后生成APK
3. 发布新版本

### 功能扩展
- 支持更多传感器数据
- 添加设备管理功能
- 实现用户权限控制
- 增加数据分析和报警功能
- 支持推送通知

## 📞 技术支持

如有问题或建议，请联系开发团队或查看项目文档。

---

**版本**: 1.0.0  
**更新时间**: 2024年1月  
**兼容性**: Android 7.0+ (API 24+)  
**后端要求**: ESP32 Python后端系统
