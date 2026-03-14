@echo off
chcp 65001 >nul
REM OB 技能评估工具 - 快速启动脚本

echo ============================================================
echo OB 技能评估工具
echo ============================================================
echo.

if "%~1"=="" goto :usage

if "%~1"=="eval" (
    echo [模式] 评估输出质量
    D:\ai\miniconda\python.exe "%~dp0run_eval.py" --mode eval --prompt "%~2" --output "%~3"
    goto :end
)

if "%~1"=="add" (
    echo [模式] 收录高分输出
    D:\ai\miniconda\python.exe "%~dp0run_eval.py" --mode add --prompt "%~2" --output "%~3" --name "%~4"
    goto :end
)

if "%~1"=="batch" (
    echo [模式] 批量测试
    D:\ai\miniconda\python.exe "%~dp0run_eval.py" --mode batch
    goto :end
)

:usage
echo 用法:
echo   eval  "输入内容" "输出内容"     - 评估输出质量
echo   add   "输入内容" "输出内容" "名称" - 收录高分输出
echo   batch                        - 批量测试所有用例
echo.
echo 示例:
echo   eval "嗯今天我们开了一个会" "# 会议记录\n\n今天我们开了一个会"
echo   add "嗯今天我们开了一个会" "# 会议记录\n\n今天我们开了一个会" "会议测试"
echo   batch
echo.

:end
