@echo off
chcp 65001 >nul

REM 注意：将下面的路径替换为你实际的仓库路径
REM 例如：cd /d "D:\1-Project-materials\Claude_code\skillwind"
cd /d "D:\1-Project-materials\Claude_code\skillwind"

echo ===================================
echo   Claude Skill Sync Tool
echo ===================================
echo.

REM 获取当前设备名
set /p DEVICE=<config\device.name
echo [Device: %DEVICE%]
echo.

echo [Step 1/4] Pulling latest changes from GitHub...
git pull
if %errorlevel% neq 0 (
    echo [ERROR] Pull failed. Please resolve conflicts manually.
    pause
    exit /b 1
)
echo [OK] Pull completed
echo.

echo [Step 2/4] Checking for local changes...
git status --short
setlocal enabledelayedexpansion
set CHANGES=0
for /f %%a in ('git status --short ^| find /c /v ""') do set CHANGES=%%a

if !CHANGES! gtr 0 (
    echo.
    echo [!] Found !CHANGES! changed files
    echo.
    set /p COMMIT_MSG="Enter commit message (or 'skip' to skip): "

    if "!COMMIT_MSG!"=="skip" (
        echo [INFO] Skipping commit
    ) else (
        git add .
        git commit -m "!COMMIT_MSG! [%DEVICE%]"
        echo.
        echo [Step 3/4] Pushing to GitHub...
        git push
        if !errorlevel! neq 0 (
            echo [ERROR] Push failed
            pause
            exit /b 1
        )
        echo [OK] Push completed
    )
) else (
    echo [OK] No local changes to commit
)
echo.

echo [Step 4/4] Showing available skills...
echo.
dir /b skills\
echo.
echo ===================================
echo Sync completed! [%DEVICE%]
echo ===================================
pause