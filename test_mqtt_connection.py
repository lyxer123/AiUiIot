import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"连接结果: {'成功' if rc == 0 else '失败'} (代码: {rc})")
    if rc == 0:
        print("正在订阅测试主题...")
        client.subscribe("test/topic")
    else:
        print("连接错误:", mqtt.error_string(rc))

def on_disconnect(client, userdata, rc):
    print(f"连接断开 (代码: {rc})")

def on_message(client, userdata, msg):
    print(f"收到消息: {msg.topic} -> {msg.payload.decode()}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"订阅确认 (ID: {mid})")
    print("发布测试消息...")
    client.publish("test/topic", "测试消息")

client = mqtt.Client("test_client")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_subscribe = on_subscribe

print("尝试连接到 localhost:1883...")
try:
    client.connect("localhost", 1883, 60)
    client.loop_start()
    time.sleep(3)  # 等待连接和消息
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print("连接异常:", str(e))

print("\n尝试连接到 192.168.124.1:1883...")
try:
    client.connect("192.168.124.1", 1883, 60)
    client.loop_start()
    time.sleep(3)
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print("连接异常:", str(e))