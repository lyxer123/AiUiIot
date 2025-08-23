# ESP32智能控制系统 - Android APP

## 📱 项目简介

这是一个专为ESP32智能控制系统设计的Android原生应用，提供以下核心功能：

- **用户管理**: 本地用户注册和登录系统
- **实时监控**: 显示AD1通道的实时数据
- **远程控制**: 通过手机控制IO1开关状态
- **状态同步**: 实时同步设备状态和控制状态
- **网络配置**: 可配置服务器IP地址和端口

## 🏗️ 技术架构

### 开发环境
- **语言**: Java 8+
- **最低SDK**: Android 7.0 (API 24)
- **目标SDK**: Android 14 (API 34)
- **开发工具**: Android Studio

### 核心技术
- **网络通信**: OkHttp3 + JSON
- **数据存储**: SharedPreferences
- **UI框架**: Material Design + RecyclerView
- **异步处理**: Handler + Runnable

### 项目结构
```
android_app/
├── app/
│   ├── src/main/
│   │   ├── java/com/esp32/control/
│   │   │   ├── MainActivity.java          # 主活动
│   │   │   ├── ControlActivity.java       # 控制页面
│   │   │   ├── DataActivity.java          # 数据监控
│   │   │   ├── SettingsActivity.java      # 设置页面
│   │   │   ├── network/
│   │   │   │   └── NetworkManager.java    # 网络管理
│   │   │   ├── model/
│   │   │   │   └── AD1Data.java          # 数据模型
│   │   │   └── adapter/
│   │   │       └── DataAdapter.java       # 数据适配器
│   │   ├── res/                           # 资源文件
│   │   └── AndroidManifest.xml            # 应用清单
│   ├── build.gradle                       # 构建配置
│   └── proguard-rules.pro                 # 混淆规则
└── README.md                              # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

#### Android Studio
1. 下载并安装 [Android Studio](https://developer.android.com/studio)
2. 确保已安装Android SDK 24-34

#### 后端服务
确保你的ESP32后端系统正在运行：
```bash
python main.py
```

### 2. 导入项目

1. 打开Android Studio
2. 选择"Open an existing Android Studio project"
3. 选择项目目录：`android_app/`
4. 等待Gradle同步完成

### 3. 配置网络

#### 修改默认服务器地址
编辑 `NetworkManager.java` 中的默认服务器地址：
```java
this.baseUrl = prefs.getString("server_url", "http://YOUR_IP:5000/api");
```

#### 或在运行时配置
1. 启动应用
2. 进入"设置"页面
3. 修改服务器地址
4. 点击"保存"和"测试连接"

### 4. 构建运行

1. 连接Android设备或启动模拟器
2. 点击"Run"按钮
3. 选择目标设备
4. 等待应用安装和启动

## 📋 功能说明

### 主页面 (MainActivity)
- **用户登录**: 用户名密码登录
- **用户注册**: 新用户注册
- **功能导航**: 跳转到各个功能页面
- **状态显示**: 显示当前登录用户

### 控制页面 (ControlActivity)
- **连接状态**: 实时监控MQTT和设备连接
- **IO1控制**: 开关控制界面
- **状态同步**: 自动同步设备状态
- **连接测试**: 测试网络连接

### 数据监控页面 (DataActivity)
- **实时数据**: 显示AD1通道的实时数值
- **历史数据**: 查看数据采集历史记录
- **数据列表**: 支持分页加载
- **自动刷新**: 定时更新数据

### 设置页面 (SettingsActivity)
- **服务器配置**: 修改服务器IP地址
- **连接测试**: 测试网络连接状态
- **设置重置**: 恢复默认配置
- **状态显示**: 显示当前连接状态

## 🔧 配置说明

### 网络配置
```java
// NetworkManager.java
serverConfig: {
  baseUrl: 'http://10.1.95.252:5000/api', // 修改为你的服务器IP
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

## 📱 使用说明

### 基本操作流程

1. **启动应用**
   - 首次使用需要注册账号
   - 输入用户名和密码登录

2. **配置网络**
   - 进入"设置"页面
   - 输入服务器IP地址
   - 测试连接是否正常

3. **监控数据**
   - 进入"数据监控"页面
   - 查看AD1通道实时数据
   - 浏览历史数据记录

4. **控制设备**
   - 进入"设备控制"页面
   - 查看连接状态
   - 使用开关控制IO1

### 注意事项

- **网络要求**: 手机和服务器必须在同一WiFi网络
- **权限要求**: 需要网络访问权限
- **实时性**: 数据每5-10秒自动刷新，也可手动刷新
- **错误处理**: 网络异常时会显示错误提示

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
