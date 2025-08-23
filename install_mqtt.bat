@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo ESP32后台系统 - MQTT代理安装脚本
echo ========================================
echo.

echo 正在检查是否已安装Mosquitto MQTT代理...
echo 正在检查Mosquitto安装状态...
timeout /t 2 /nobreak >nul 2>&1

REM 使用更快的检查方法
if exist "C:\Program Files\mosquitto\mosquitto.exe" (
    set MOSQUITTO_PATH="C:\Program Files\mosquitto\mosquitto.exe"
) else if exist "C:\Program Files (x86)\mosquitto\mosquitto.exe" (
    set MOSQUITTO_PATH="C:\Program Files (x86)\mosquitto\mosquitto.exe"
) else (
    goto :not_installed
)

echo Mosquitto已安装，版本信息：
!MOSQUITTO_PATH! -h
echo.
echo 正在启动Mosquitto服务...
net start mosquitto >nul 2>&1
if %errorlevel% == 0 (
    echo [成功] Mosquitto服务已启动
) else (
    echo [警告] Mosquitto服务启动失败，错误代码: %errorlevel%
    if %errorlevel% == 2 (
        echo [错误] 系统找不到指定的文件 - Mosquitto服务未安装
        echo.
        echo 解决方案：
        echo 1. 重新安装Mosquitto，确保选择"Service"选项
        echo 2. 或者手动安装服务：
echo    - 以管理员身份打开命令提示符
echo    - 运行: sc create mosquitto binPath= "C:\Program Files\mosquitto\mosquitto.exe -v" start= auto
echo    - 然后运行: net start mosquitto
        echo.
        echo 3. 检查服务是否已安装：
        echo    - 按 Win+R，输入 services.msc
        echo    - 查找是否有 "mosquitto" 服务
    ) else if %errorlevel% == 5 (
        echo [错误] 权限不足，请以管理员身份运行此脚本
        echo 右键点击脚本 -> "以管理员身份运行"
        echo.
        echo 或者手动启动服务：
        echo 1. 按 Win+R，输入 services.msc
        echo 2. 找到 "mosquitto" 服务
        echo 3. 右键选择 "启动"
    ) else if %errorlevel% == 1060 (
        echo [信息] 服务未配置为自动启动，正在尝试手动启动...
        sc start mosquitto >nul 2>&1
        if !errorlevel! == 0 (
            echo [成功] MQTT服务手动启动成功
        ) else (
            echo [错误] MQTT服务启动失败
        )
    ) else (
        echo [信息] 可能服务已在运行，正在检查状态...
        sc query mosquitto >nul 2>&1
        if %errorlevel% == 0 (
            sc query mosquitto | find "RUNNING" >nul 2>&1
            if %errorlevel% == 0 (
                echo [成功] MQTT服务已在运行
            ) else (
                echo [信息] MQTT服务已安装但未运行，正在尝试启动...
                sc start mosquitto >nul 2>&1
                if !errorlevel! == 0 (
                    echo [成功] MQTT服务启动成功
                ) else (
                    echo [错误] MQTT服务启动失败
                )
            )
        ) else (
            echo [错误] MQTT服务未安装，请重新安装Mosquitto
        )
    )
)
goto :end

:not_installed

echo Mosquitto未安装，正在下载安装包...
echo.

echo 请按照以下步骤手动安装Mosquitto：
echo 1. 访问 https://mosquitto.org/download/
echo 2. 下载Windows版本的安装包
echo 3. 运行安装程序，选择"Service"选项
echo 4. 安装完成后，Mosquitto会自动作为Windows服务运行
echo.

echo 或者使用Chocolatey包管理器安装：
echo choco install mosquitto
echo.

echo 安装完成后，请重新运行此脚本
echo.

:end
echo.
echo 按任意键退出...
pause >nul
