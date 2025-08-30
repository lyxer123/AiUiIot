from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    file_path = os.path.abspath('web_test_improved.html')
    if not os.path.exists(file_path):
        return "Error: HTML file not found", 404
    return send_file(file_path, mimetype='text/html')

if __name__ == '__main__':
    # 开发模式
    app.run(host='127.0.0.1', port=5000)