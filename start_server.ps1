$env:FLASK_APP="server.py"
gunicorn -w 4 -b 127.0.0.1:5000 server:app