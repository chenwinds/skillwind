#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目类型检测脚本 - 为TDD流程检测项目语言和推荐测试框架
"""

import os
import sys
import json
import io
from pathlib import Path

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def detect_project_type(project_path="."):
    """检测项目类型和推荐的测试框架"""
    project_path = Path(project_path).resolve()

    indicators = {
        "python": {
            "files": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile", "poetry.lock"],
            "extensions": [".py"],
            "frameworks": [
                {"name": "pytest", "install": "pip install pytest", "popularity": 95},
                {"name": "unittest", "install": "内置，无需安装", "popularity": 80},
                {"name": "nose2", "install": "pip install nose2", "popularity": 30}
            ]
        },
        "javascript": {
            "files": ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
            "extensions": [".js", ".mjs"],
            "frameworks": [
                {"name": "jest", "install": "npm install --save-dev jest", "popularity": 90},
                {"name": "vitest", "install": "npm install --save-dev vitest", "popularity": 75},
                {"name": "mocha", "install": "npm install --save-dev mocha", "popularity": 60}
            ]
        },
        "typescript": {
            "files": ["tsconfig.json", "package.json"],
            "extensions": [".ts", ".tsx"],
            "frameworks": [
                {"name": "vitest", "install": "npm install --save-dev vitest", "popularity": 85},
                {"name": "jest", "install": "npm install --save-dev jest ts-jest @types/jest", "popularity": 80},
                {"name": "mocha + chai", "install": "npm install --save-dev mocha chai @types/mocha @types/chai", "popularity": 50}
            ]
        },
        "java": {
            "files": ["pom.xml", "build.gradle", "gradlew", "mvnw"],
            "extensions": [".java"],
            "frameworks": [
                {"name": "JUnit 5 + AssertJ", "install": "Maven/Gradle依赖", "popularity": 95},
                {"name": "TestNG", "install": "Maven/Gradle依赖", "popularity": 40}
            ]
        },
        "go": {
            "files": ["go.mod", "go.sum"],
            "extensions": [".go"],
            "frameworks": [
                {"name": "testing (内置)", "install": "无需安装", "popularity": 100},
                {"name": "testify", "install": "go get github.com/stretchr/testify", "popularity": 80}
            ]
        },
        "rust": {
            "files": ["Cargo.toml", "Cargo.lock"],
            "extensions": [".rs"],
            "frameworks": [
                {"name": "内置测试", "install": "无需安装", "popularity": 100}
            ]
        },
        "ruby": {
            "files": ["Gemfile", "Gemfile.lock", ".gemspec"],
            "extensions": [".rb"],
            "frameworks": [
                {"name": "RSpec", "install": "gem install rspec", "popularity": 90},
                {"name": "Minitest", "install": "内置", "popularity": 70}
            ]
        },
        "php": {
            "files": ["composer.json", "composer.lock"],
            "extensions": [".php"],
            "frameworks": [
                {"name": "PHPUnit", "install": "composer require --dev phpunit/phpunit", "popularity": 95}
            ]
        },
        "csharp": {
            "files": [".csproj", ".sln"],
            "extensions": [".cs"],
            "frameworks": [
                {"name": "xUnit", "install": "dotnet add package xunit", "popularity": 85},
                {"name": "NUnit", "install": "dotnet add package NUnit", "popularity": 60},
                {"name": "MSTest", "install": "dotnet add package MSTest", "popularity": 50}
            ]
        }
    }

    results = {}

    for lang, config in indicators.items():
        score = 0
        found_files = []
        found_extensions = []

        # 检查特征文件
        for file in config["files"]:
            if (project_path / file).exists():
                score += 10
                found_files.append(file)

        # 检查文件扩展名
        for ext in config["extensions"]:
            if list(project_path.rglob(f"*{ext}")):
                score += 5
                found_extensions.append(ext)

        if score > 0:
            results[lang] = {
                "score": score,
                "files": found_files,
                "extensions": found_extensions,
                "frameworks": config["frameworks"]
            }

    # 按分数排序
    sorted_results = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)

    return sorted_results


def print_recommendations(results):
    """打印推荐结果"""
    if not results:
        print("❓ 无法确定项目类型")
        print("请手动指定项目语言")
        return

    primary_lang, primary_info = results[0]

    print(f"\n🔍 检测到项目类型: {primary_lang.upper()}")
    print(f"   置信度: {'⭐' * min(primary_info['score'] // 5, 10)}")

    if primary_info['files']:
        print(f"\n📄 发现配置文件: {', '.join(primary_info['files'])}")

    print("\n🧪 推荐测试框架（按流行度排序）:")
    for i, fw in enumerate(primary_info['frameworks'][:3], 1):
        print(f"   {i}. {fw['name']}")
        print(f"      安装: {fw['install']}")
        print(f"      流行度: {fw['popularity']}%")

    # 显示其他可能的类型
    if len(results) > 1:
        print("\n📝 其他可能的项目类型:")
        for lang, info in results[1:3]:
            print(f"   - {lang}: 置信度 {info['score']}")


def check_existing_tests(project_path="."):
    """检查项目中是否已有测试"""
    project_path = Path(project_path).resolve()

    test_patterns = [
        "**/test*.py",
        "**/*_test.py",
        "**/tests/**/*.py",
        "**/__tests__/**/*.js",
        "**/*.test.js",
        "**/*.spec.js",
        "**/*.test.ts",
        "**/*.spec.ts",
        "**/src/test/**/*.java",
        "**/*Test.java",
        "**/*_test.go",
        "**/tests/**/*.rs"
    ]

    existing_tests = []
    for pattern in test_patterns:
        matches = list(project_path.glob(pattern))
        existing_tests.extend(matches)

    if existing_tests:
        print(f"\n✅ 发现 {len(existing_tests)} 个现有测试文件")
        print("   示例:")
        for test_file in existing_tests[:3]:
            print(f"   - {test_file.relative_to(project_path)}")
    else:
        print("\n🆕 未发现现有测试文件，将创建新的测试结构")

    return existing_tests


def generate_test_config(project_path=".", lang=None):
    """生成测试配置文件建议"""
    configs = {
        "python": {
            "files": {
                "pytest.ini": "[pytest]\ntestpaths = tests\npython_files = test_*.py\naddopts = -v --tb=short",
                "tests/conftest.py": "# 测试配置文件和共享夹具"
            }
        },
        "javascript": {
            "files": {
                "jest.config.js": "module.exports = {\n  testEnvironment: 'node',\n  testMatch: ['**/tests/**/*.test.js'],\n  collectCoverageFrom: ['src/**/*.js'],\n};"
            }
        },
        "typescript": {
            "files": {
                "vitest.config.ts": "import { defineConfig } from 'vitest/config'\n\nexport default defineConfig({\n  test: {\n    globals: true,\n    environment: 'node',\n  },\n})"
            }
        }
    }

    if lang and lang in configs:
        print(f"\n🔧 {lang} 项目建议配置:")
        for filename, content in configs[lang]["files"].items():
            print(f"\n📄 {filename}:")
            print("─" * 40)
            print(content)
            print("─" * 40)


def main():
    """主函数"""
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."

    print("=" * 60)
    print("🧪 TDD Flow - 项目类型检测工具")
    print("=" * 60)

    print(f"\n📁 项目路径: {Path(project_path).resolve()}")

    # 检测项目类型
    results = detect_project_type(project_path)
    print_recommendations(results)

    # 检查现有测试
    check_existing_tests(project_path)

    # 生成配置建议
    if results:
        generate_test_config(project_path, results[0][0])

    print("\n" + "=" * 60)

    # 输出JSON格式（供程序调用）
    if "--json" in sys.argv:
        output = {
            "primary_language": results[0][0] if results else None,
            "confidence": results[0][1]["score"] if results else 0,
            "recommendations": [
                {"language": lang, "score": info["score"], "frameworks": info["frameworks"][:2]}
                for lang, info in results[:3]
            ]
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
