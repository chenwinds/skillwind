#!/usr/bin/env python3
"""
OB 技能自动化评估与迭代工具

功能：
1. 评估技能输出质量
2. 高分输出自动收录为测试用例
3. 低分输出提示改进建议

使用方法:
    python run_eval.py --mode eval --prompt "要整理的内容"
    python run_eval.py --mode add --prompt "要整理的内容" --output "整理后的输出"
    python run_eval.py --mode batch  # 运行所有预设测试用例
"""

import json
import subprocess
import re
import sys
import io
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

# 设置 Windows 命令行输出为 UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# ============== 评估标准定义 ==============

EVALUATION_CRITERIA = {
    "basic": [
        {"name": "有标点符号", "check": lambda x: bool(re.search(r'[,.，。？！]', x)), "weight": 2},
        {"name": "有合理分段", "check": lambda x: len(x.split('\n\n')) >= 2, "weight": 1},
        {"name": "无多余开场白", "check": lambda x: not any(s in x[:50] for s in ['好的', '以下是', '我来', '让我']), "weight": 2},
    ],
    "tone_removal": [
        {"name": "无语气词", "check": lambda x: not any(p in x for p in ['呃', '哦', '啊', '嗯', '嘛', '哎', '诶', '呀', '哇']), "weight": 3},
        {"name": "无填充词", "check": lambda x: not any(p in x for p in ['那个', '然后', '就是', '其实', 'basically']), "weight": 2},
    ],
    "format": [
        {"name": "使用 Markdown 标题", "check": lambda x: bool(re.search(r'^#{1,6}\s+', x, re.MULTILINE)), "weight": 2},
        {"name": "使用列表", "check": lambda x: bool(re.search(r'^(\d+\.|\-|\*)\s+', x, re.MULTILINE)), "weight": 1},
    ]
}

# 满分 15 分，80% 通过线 = 12 分
PASS_THRESHOLD = 0.8


def load_evals(evals_path: str) -> dict:
    """加载评估配置文件"""
    with open(evals_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_evals(evals_path: str, data: dict):
    """保存评估配置"""
    with open(evals_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def evaluate_output(output: str) -> tuple[int, int, list[dict]]:
    """
    评估输出质量

    Returns:
        (score, total, details) 得分、总分、详情
    """
    score = 0
    total = 0
    details = []

    all_criteria = (
        EVALUATION_CRITERIA["basic"] +
        EVALUATION_CRITERIA["tone_removal"] +
        EVALUATION_CRITERIA["format"]
    )

    for criterion in all_criteria:
        name = criterion["name"]
        check = criterion["check"]
        weight = criterion["weight"]
        total += weight

        try:
            passed = check(output)
        except Exception:
            passed = False

        if passed:
            score += weight

        details.append({
            "name": name,
            "weight": weight,
            "passed": passed,
            "score": weight if passed else 0
        })

    return score, total, details


def format_result(score: int, total: int, details: list, prompt: str = None, output: str = None):
    """格式化评估结果为文字报告"""
    pass_rate = score / total * 100 if total > 0 else 0
    passed = pass_rate >= PASS_THRESHOLD * 100

    lines = []
    lines.append("=" * 60)
    lines.append("OB 技能评估结果")
    lines.append("=" * 60)

    if prompt:
        lines.append(f"\n输入：{prompt[:80]}..." if len(prompt) > 80 else f"\n输入：{prompt}")

    lines.append(f"\n得分：{score}/{total} ({pass_rate:.1f}%)")
    lines.append(f"状态：{'[OK] 通过' if passed else '[FAIL] 未通过'}（通过线：{PASS_THRESHOLD*100:.0f}%）")

    lines.append("\n详细评分：")
    for d in details:
        status = "[OK]" if d["passed"] else "[FAIL]"
        lines.append(f"  {status} {d['name']}: {d['score']}/{d['weight']}分")

    if not passed:
        failed = [d["name"] for d in details if not d["passed"]]
        lines.append(f"\n需要改进：{', '.join(failed)}")

    if passed and score == total:
        lines.append("\n建议：此输出质量优秀，可收录为测试用例")
        lines.append("命令：python run_eval.py --mode add --prompt \"...\" --output \"...\"")

    lines.append("=" * 60)

    return "\n".join(lines)


def add_to_evals(prompt: str, output: str, evals_path: str, name: str = None):
    """将高分输出添加到测试用例"""
    data = load_evals(evals_path)

    # 自动生成评估标准
    expectations = []
    if re.search(r'^#{1,6}\s+', output, re.MULTILINE):
        expectations.append({"criterion": "包含 Markdown 标题", "weight": 2, "type": "binary"})
    if re.search(r'^\d+\.\s+', output, re.MULTILINE):
        expectations.append({"criterion": "使用有序列表", "weight": 2, "type": "binary"})
    if not any(p in output for p in ['呃', '哦', '啊', '嗯', '嘛']):
        expectations.append({"criterion": "删除语气词", "weight": 2, "type": "binary"})
    if re.search(r'[,.，。？！]', output):
        expectations.append({"criterion": "添加正确标点", "weight": 2, "type": "binary"})

    # 计算总分
    total_score = sum(e["weight"] for e in expectations)

    new_eval = {
        "id": len(data["evals"]) + 1,
        "name": name or f"用户添加_{datetime.now().strftime('%Y%m%d%H%M')}",
        "prompt": prompt,
        "expected_output": "结构化 Markdown 文章",
        "expectations": expectations,
        "total_score": total_score,
        "added_date": datetime.now().isoformat(),
        "source": "user_contributed"
    }

    data["evals"].append(new_eval)
    data["version"] = "1.2.0"

    save_evals(evals_path, data)

    return new_eval


def run_batch_test(evals_path: str):
    """运行所有预设测试用例的批量测试"""
    data = load_evals(evals_path)

    print("=" * 60)
    print("OB 技能 - 批量测试")
    print("=" * 60)
    print(f"测试用例数量：{len(data['evals'])}")
    print()

    results = []

    for i, eval_item in enumerate(data["evals"], 1):
        print(f"[{i}/{len(data['evals'])}] {eval_item.get('name', f'测试{i}')}")
        print(f"提示词：{eval_item['prompt'][:60]}...")

        # 需要用户输入技能输出
        output = input("请输入技能输出（直接回车跳过）：")

        if output.strip():
            score, total, details = evaluate_output(output)
            pass_rate = score / total * 100 if total > 0 else 0
            passed = pass_rate >= PASS_THRESHOLD * 100

            status = "[OK] 通过" if passed else "[FAIL] 未通过"
            print(f"得分：{score}/{total} ({pass_rate:.1f}%) - {status}")

            results.append({
                "name": eval_item.get('name', f'测试{i}'),
                "score": score,
                "total": total,
                "passed": passed
            })

            if passed and score == total:
                print("-> 此输出质量优秀，建议收录")
        else:
            print("  (跳过)")

        print()

    # 汇总报告
    print("=" * 60)
    print("测试汇总")
    print("=" * 60)

    total_passed = sum(1 for r in results if r["passed"])
    total_run = len(results)

    print(f"运行测试：{total_run}")
    print(f"通过：{total_passed}")
    print(f"失败：{total_run - total_passed}")
    print(f"通过率：{total_passed/total_run*100:.1f}%" if total_run > 0 else "N/A")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='OB 技能评估与迭代工具')
    parser.add_argument('--mode', choices=['eval', 'add', 'batch'], required=True,
                        help='eval=评估输出，add=添加到测试用例，batch=批量测试')
    parser.add_argument('--prompt', type=str, help='输入提示词')
    parser.add_argument('--output', type=str, help='技能输出内容')
    parser.add_argument('--name', type=str, help='测试用例名称（用于 add 模式）')
    parser.add_argument('--evals-path', default='evals.json', help='评估配置文件路径')

    args = parser.parse_args()

    # 模式 1: 评估输出
    if args.mode == 'eval':
        if not args.output:
            print("错误：--output 参数必填")
            print("用法：python run_eval.py --mode eval --prompt \"...\" --output \"...\"")
            return 1

        score, total, details = evaluate_output(args.output)
        report = format_result(score, total, details, args.prompt, args.output)
        print(report)

        return 0 if score/total >= PASS_THRESHOLD else 1

    # 模式 2: 添加到测试用例
    elif args.mode == 'add':
        if not args.prompt or not args.output:
            print("错误：--prompt 和 --output 参数必填")
            print("用法：python run_eval.py --mode add --prompt \"...\" --output \"...\"")
            return 1

        # 先评估
        score, total, details = evaluate_output(args.output)
        report = format_result(score, total, details, args.prompt, args.output)
        print(report)

        # 高分才允许添加
        if score == total:
            new_eval = add_to_evals(args.prompt, args.output, args.evals_path, args.name)
            print(f"\n[OK] 已添加到测试用例 #{new_eval['id']}: {new_eval['name']}")
        else:
            print(f"\n[FAIL] 得分{score}/{total}未达到满分，建议改进后再收录")

        return 0

    # 模式 3: 批量测试
    elif args.mode == 'batch':
        run_batch_test(args.evals_path)
        return 0


if __name__ == '__main__':
    sys.exit(main())
