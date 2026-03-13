@echo off
chcp 65001 >nul

echo ===================================
echo   Claude Skills Center - Setup
echo   Claude 技能中心 - 初始化设置
echo ===================================
echo.

REM 检查 Git 是否安装
echo [Step 1/5] Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in PATH.
    echo [错误] 未检测到 Git，请先安装 Git: https://git-scm.com/
    pause
    exit /b 1
)
echo [OK] Git is installed
echo.

REM 获取当前设备名
echo [Step 2/5] Detecting device name...
setlocal enabledelayedexpansion
set DEVICE=%COMPUTERNAME%
echo [Device: %DEVICE%]

REM 检查设备名是否包含常见标识
echo !DEVICE! | findstr /i "desktop" >nul
if not errorlevel 1 set DEVICETYPE=desktop

echo !DEVICE! | findstr /i "laptop" >nul
if not errorlevel 1 set DEVICETYPE=laptop

if "!DEVICETYPE!"=="" (
    echo.
    set /p DEVICETYPE="Enter device type (desktop/laptop): "
)
echo [Device Type: !DEVICETYPE!]
echo.

REM 创建必要的目录
echo [Step 3/5] Creating directory structure...
if not exist "skills" (
    mkdir "skills"
    echo [Created] skills/
) else (
    echo [Exists] skills/
)

if not exist "config" (
    mkdir "config"
    echo [Created] config/
) else (
    echo [Exists] config/
)

if not exist "logs" (
    mkdir "logs"
    echo [Created] logs/
) else (
    echo [Exists] logs/
)

if not exist "tools" (
    mkdir "tools"
    echo [Created] tools/
) else (
    echo [Exists] tools/
)
echo.

REM 初始化设备配置文件
echo [Step 4/5] Initializing device configuration...
if not exist "config\device.name" (
    echo !DEVICETYPE! > config\device.name
    echo [Created] config\device.name
) else (
    echo [Exists] config\device.name
)

REM 检查全局配置
if not exist "config\global.config.json" (
    (
        echo {
        echo   "sync": {
        echo     "auto_pull": true,
        echo     "auto_pull_interval": "30m"
        echo   },
        echo   "security": {
        echo     "install_confirmation": true,
        echo     "allow_downgrade": false
        echo   }
        echo }
    ) > config\global.config.json
    echo [Created] config\global.config.json
) else (
    echo [Exists] config\global.config.json
)

REM 检查设备特定配置
if not exist "config\desktop.config.json" (
    (
        echo {
        echo   "device_name": "desktop",
        echo   "can_create_skill": true,
        echo   "can_modify_skill": true,
        echo   "preferred_skills": [],
        echo   "auto_install_new": true,
        echo   "never_install": [],
        echo   "install_confirmation": false
        echo }
    ) > config\desktop.config.json
    echo [Created] config\desktop.config.json
) else (
    echo [Exists] config\desktop.config.json
)

if not exist "config\laptop.config.json" (
    (
        echo {
        echo   "device_name": "laptop",
        echo   "can_create_skill": true,
        echo   "can_modify_skill": true,
        echo   "preferred_skills": [],
        echo   "auto_install_new": true,
        echo   "never_install": [],
        echo   "install_confirmation": true
        echo }
    ) > config\laptop.config.json
    echo [Created] config\laptop.config.json
) else (
    echo [Exists] config\laptop.config.json
)

REM 检查技能注册表
if not exist "skills\registry.json" (
    (
        echo {
        echo   "version": "1.0.0",
        echo   "last_updated": "2026-03-13T00:00:00Z",
        echo   "skills": {},
        echo   "sync_history": [],
        echo   "device_preferences": {
        echo     "desktop": {},
        echo     "laptop": {}
        echo   }
        echo }
    ) > skills\registry.json
    echo [Created] skills\registry.json
) else (
    echo [Exists] skills\registry.json
)
echo.

REM 配置 Git 全局 alias
echo [Step 5/5] Configuring Git aliases...
git config --global alias.up "!git add -A && (git diff --cached --quiet || git commit -m \"auto update [%COMPUTERNAME%]\") && git push" 2>/dev/null
if %errorlevel% equ 0 (
    echo [OK] Git alias 'git up' configured globally
) else (
    echo [WARN] Could not configure global git alias (you may need to configure manually)
)
echo.

REM 完成
echo ===================================
echo   Setup Completed!
echo   设置完成！
echo ===================================
echo.
echo Next steps / 下一步:
echo   1. Review config\device.name and update if needed
echo      检查 config\device.name 并根据需要更新
echo.
echo   2. Add your skills to the skills\ folder
echo      将技能文件添加到 skills\ 目录
echo.
echo   3. Run 'git up' to sync your changes
echo      运行 'git up' 同步更改
echo.
pause
