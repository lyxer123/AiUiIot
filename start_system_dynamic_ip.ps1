# ESP32后台系统 - 动态IP配置启动脚本 (PowerShell版本)
Write-Host "========================================" -ForegroundColor Green
Write-Host "ESP32后台系统 - 动态IP配置启动脚本" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "正在检测本机IP地址..." -ForegroundColor Yellow
try {
    $hostname = [System.Net.Dns]::GetHostName()
    $localIP = [System.Net.Dns]::GetHostAddresses($hostname) | Where-Object {$_.AddressFamily -eq "InterNetwork"} | Select-Object -First 1
    Write-Host "本机IP地址: $($localIP.IPAddressToString)" -ForegroundColor Green
} catch {
    Write-Host "无法获取本机IP地址" -ForegroundColor Red
}

Write-Host ""
Write-Host "正在更新IP配置..." -ForegroundColor Yellow
try {
    python ip_config.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "IP配置更新成功" -ForegroundColor Green
    } else {
        Write-Host "IP配置更新失败" -ForegroundColor Red
    }
} catch {
    Write-Host "IP配置更新出错: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "正在启动ESP32后台系统..." -ForegroundColor Yellow
try {
    python main.py
} catch {
    Write-Host "系统启动出错: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")



