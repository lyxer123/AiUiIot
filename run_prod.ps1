# 终止现有服务
Stop-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess -ErrorAction SilentlyContinue

# 启动Gunicorn
$env:FLASK_APP="server.py"
Start-Process python -ArgumentList "-m gunicorn -w 2 -b 127.0.0.1:5000 --timeout 120 server:app"

# 验证启动
Start-Sleep -Seconds 3
Test-NetConnection -ComputerName 127.0.0.1 -Port 5000