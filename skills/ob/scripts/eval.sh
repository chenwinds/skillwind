#!/bin/bash
# OB 技能评估工具 - 快速启动脚本

PYTHON="/d/ai/miniconda/python.exe"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "OB 技能评估工具"
echo "============================================================"
echo ""

if [ -z "$1" ]; then
    echo "用法:"
    echo "  $0 eval  \"输入内容\" \"输出内容\"     - 评估输出质量"
    echo "  $0 add   \"输入内容\" \"输出内容\" \"名称\" - 收录高分输出"
    echo "  $0 batch                        - 批量测试所有用例"
    echo ""
    echo "示例:"
    echo "  $0 eval \"嗯今天我们开了一个会\" \"# 会议记录\\n\\n今天我们开了一个会\""
    echo "  $0 add \"嗯今天我们开了一个会\" \"# 会议记录\\n\\n今天我们开了一个会\" \"会议测试\""
    echo "  $0 batch"
    exit 0
fi

case "$1" in
    eval)
        echo "[模式] 评估输出质量"
        $PYTHON "$SCRIPT_DIR/run_eval.py" --mode eval --prompt "$2" --output "$3"
        ;;
    add)
        echo "[模式] 收录高分输出"
        $PYTHON "$SCRIPT_DIR/run_eval.py" --mode add --prompt "$2" --output "$3" --name "$4"
        ;;
    batch)
        echo "[模式] 批量测试"
        $PYTHON "$SCRIPT_DIR/run_eval.py" --mode batch
        ;;
    *)
        echo "未知模式：$1"
        echo "请使用：$0 --help 查看用法"
        exit 1
        ;;
esac
