# MQTT Setup PowerShell Script
# Run this script as Administrator if you need to install/start services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MQTT Broker Setup - PowerShell Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking Mosquitto installation..." -ForegroundColor Yellow
Write-Host ""

# Check if mosquitto.exe exists
$mosquittoPath = $null
if (Test-Path "C:\Program Files\mosquitto\mosquitto.exe") {
    $mosquittoPath = "C:\Program Files\mosquitto\mosquitto.exe"
    Write-Host "[SUCCESS] Mosquitto executable found in Program Files" -ForegroundColor Green
} elseif (Test-Path "C:\Program Files (x86)\mosquitto\mosquitto.exe") {
    $mosquittoPath = "C:\Program Files (x86)\mosquitto\mosquitto.exe"
    Write-Host "[SUCCESS] Mosquitto executable found in Program Files (x86)" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Mosquitto executable not found" -ForegroundColor Red
    Write-Host "Please install from: https://mosquitto.org/download/" -ForegroundColor Red
    Write-Host "Make sure to select 'Service' option during installation" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Checking Mosquitto service status..." -ForegroundColor Yellow
Write-Host ""

# Check if mosquitto service exists
try {
    $service = Get-Service -Name "mosquitto" -ErrorAction Stop
    Write-Host "[SUCCESS] Mosquitto service is installed" -ForegroundColor Green
    Write-Host ""
    Write-Host "Service Name: $($service.Name)" -ForegroundColor White
    Write-Host "Display Name: $($service.DisplayName)" -ForegroundColor White
    Write-Host "Status: $($service.Status)" -ForegroundColor White
    Write-Host "Start Type: $($service.StartType)" -ForegroundColor White
    Write-Host ""
    
    if ($service.Status -eq "Running") {
        Write-Host "[SUCCESS] Mosquitto service is already running" -ForegroundColor Green
        Write-Host "No need to start it again" -ForegroundColor White
    } else {
        Write-Host "[INFO] Service is installed but not running" -ForegroundColor Yellow
        Write-Host "Attempting to start service..." -ForegroundColor White
        
        try {
            Start-Service -Name "mosquitto" -ErrorAction Stop
            Write-Host "[SUCCESS] Service started successfully" -ForegroundColor Green
        } catch {
            Write-Host "[WARNING] Could not start service: $($_.Exception.Message)" -ForegroundColor Yellow
            Write-Host "You may need to run this script as Administrator" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "[ERROR] Mosquitto service not found" -ForegroundColor Red
    Write-Host "Please reinstall Mosquitto with 'Service' option selected" -ForegroundColor Red
    Write-Host "Or run this script as Administrator to install the service" -ForegroundColor Red
}

Write-Host ""
Write-Host "Testing MQTT connection..." -ForegroundColor Yellow
Write-Host ""

# Test if mosquitto is responding on default port 1883
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $tcpClient.Connect("localhost", 1883)
    if ($tcpClient.Connected) {
        Write-Host "[SUCCESS] MQTT broker is responding on port 1883" -ForegroundColor Green
        $tcpClient.Close()
    }
} catch {
    Write-Host "[INFO] Could not connect to MQTT broker on port 1883" -ForegroundColor Yellow
    Write-Host "This might be normal if the broker is not configured for this port" -ForegroundColor White
}

Write-Host "[INFO] MQTT setup check completed" -ForegroundColor White

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close..." -ForegroundColor White
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")



