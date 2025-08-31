from flask import Flask, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

# 模拟数据存储
class DataStore:
    def __init__(self):
        self.ad_history = []
        self.io_history = []
        self.system_status = {
            'mqtt_connected': True,
            'last_update': datetime.now().isoformat()
        }
        self.init_sample_data()
    
    def init_sample_data(self):
        # 初始化AD历史数据
        for i in range(100):
            self.record_ad_data({
                '温度': f'{round(25 + random.uniform(-2, 2), 1)}°C',
                '湿度': f'{random.randint(40, 60)}%',
                '光照': f'{random.randint(500, 1000)}lux',
                '电压': f'{round(3.3 + random.uniform(-0.5, 0.5), 2)}V',
                'timestamp': datetime.now().isoformat()
            })
        
        # 初始化IO历史数据
        for i in range(1, 5):
            for _ in range(10):
                self.record_io_control(i, random.choice([True, False]))
    
    def record_ad_data(self, data):
        self.ad_history.append(data)
        if len(self.ad_history) > 1000:
            self.ad_history.pop(0)
    
    def record_io_control(self, device_id, state):
        self.io_history.append({
            'device_id': device_id,
            'state': state,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.io_history) > 1000:
            self.io_history.pop(0)
    
    def get_ad_history(self, limit=50):
        return self.ad_history[-limit:]
    
    def get_io_history(self, device_id=None, limit=50):
        history = self.io_history.copy()
        if device_id:
            history = [x for x in history if x['device_id'] == device_id]
        return history[-limit:]

db = DataStore()

# 系统状态API
@app.route('/api/status', methods=['GET'])
def get_system_status():
    db.system_status['last_update'] = datetime.now().isoformat()
    return jsonify({
        'success': True,
        'data': db.system_status
    })

# AD数据API
@app.route('/api/ad1/current', methods=['GET'])
def get_current_ad1():
    current = db.ad_history[-1] if db.ad_history else {}
    return jsonify({
        'success': True,
        'data': current
    })

@app.route('/api/ad1/data', methods=['GET'])
def get_ad1_history():
    limit = request.args.get('limit', default=50, type=int)
    return jsonify({
        'success': True,
        'data': db.get_ad_history(limit)
    })

# IO控制API
@app.route('/api/io1/current', methods=['GET'])
def get_current_io1_state():
    history = db.get_io_history(1, 1)
    current = history[0]['state'] if history else False
    return jsonify({
        'success': True,
        'data': {'state': current}
    })

@app.route('/api/io1/control', methods=['GET', 'POST'])
def io1_control():
    if request.method == 'GET':
        limit = request.args.get('limit', default=50, type=int)
        return jsonify({
            'success': True,
            'data': db.get_io_history(1, limit)
        })
    else:
        data = request.get_json()
        state = data.get('state', False)
        db.record_io_control(1, state)
        return jsonify({
            'success': True,
            'message': f'IO1状态已设置为 {state}'
        })

# MQTT状态API
@app.route('/api/mqtt/status', methods=['GET'])
def get_mqtt_status():
    return jsonify({
        'success': True,
        'data': {
            'connected': db.system_status['mqtt_connected'],
            'last_activity': db.system_status['last_update']
        }
    })

# 测试API
@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({
        'success': True,
        'message': 'API服务运行正常',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)