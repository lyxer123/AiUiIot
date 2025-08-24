# ESP32模拟器功能已禁用

## 说明
由于项目已经建立了Android Studio项目，不再需要ESP32模拟数据功能，因此已将ESP32模拟器功能完全禁用。

## 已完成的修改

### 1. 配置文件 (config.ini)
- 将 `[ESP32_SIMULATOR]` 部分的 `enabled` 设置为 `False`

### 2. 主程序 (main.py)
- 注释掉ESP32模拟器的导入语句
- 注释掉ESP32模拟器的初始化代码
- 注释掉ESP32模拟器的启动代码
- 注释掉ESP32模拟器的停止代码
- 修改状态输出，显示模拟器已禁用

### 3. 启动脚本 (start_system.bat)
- 添加说明，提示ESP32模拟器功能已禁用

### 4. 测试脚本 (test_system.bat)
- 移除ESP32模拟器的测试代码
- 显示跳过测试的信息

### 5. 文件重命名
- 将 `esp32_simulator.py` 重命名为 `esp32_simulator.py.disabled`

## 影响
- 系统启动时不会初始化ESP32模拟器
- 不会生成模拟的AD1数据
- 不会模拟IO1控制状态
- 系统将只依赖真实的ESP32设备或MQTT消息

## 如需重新启用
如果需要重新启用ESP32模拟器功能，请：
1. 将 `esp32_simulator.py.disabled` 重命名为 `esp32_simulator.py`
2. 在 `config.ini` 中将 `enabled` 设置为 `True`
3. 在 `main.py` 中取消相关代码的注释
4. 恢复启动脚本和测试脚本中的相关代码

## 注意事项
- 禁用ESP32模拟器后，系统将无法生成测试数据
- 确保有真实的ESP32设备或MQTT消息源来提供数据
- 如果系统依赖模拟数据进行测试，请先重新启用模拟器功能
