#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试模板生成器 - 根据项目类型生成标准的TDD测试模板
"""

import sys
import os
import io
from pathlib import Path

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def generate_python_test(function_name, params, expected_type="返回值"):
    """生成Python测试模板"""
    param_str = ", ".join([f"{p['name']}={repr(p['value'])}" for p in params])
    param_names = ", ".join([p['name'] for p in params])

    template = f'''import pytest
from src.{function_name.split("_")[0]} import {function_name}


def test_should_{function_name}_success():
    """测试 {function_name} 正常情况"""
    # Arrange - 准备
    {chr(10).join([f"    {p['name']} = {repr(p['value'])}  # 请调整测试数据" for p in params])}

    # Act - 执行
    result = {function_name}({param_names})

    # Assert - 验证
    assert result == "expected_value"  # TODO: 请填写期望的{expected_type}


def test_should_{function_name}_with_invalid_input():
    """测试 {function_name} 无效输入情况"""
    # Arrange
    {params[0]['name'] if params else 'input_value'} = None  # 无效输入

    # Act & Assert
    with pytest.raises(ValueError):  # 请调整异常类型
        {function_name}({param_names if params else 'invalid_input'})


@pytest.mark.parametrize("input_val,expected", [
    ("边界值1", "期望结果1"),
    ("边界值2", "期望结果2"),
])
def test_should_{function_name}_with_edge_cases(input_val, expected):
    """测试 {function_name} 边界条件"""
    result = {function_name}(input_val)
    assert result == expected
'''
    return template


def generate_javascript_test(function_name, params, expected_type="返回值"):
    """生成JavaScript/TypeScript测试模板"""
    param_str = ", ".join([p['name'] for p in params])

    template = f'''import {{ {function_name} }} from '../src/{function_name.split("_")[0]}';

describe('{function_name}', () => {{
  test('正常情况应返回正确的{expected_type}', () => {{
    // Arrange
    {chr(10).join([f"    const {p['name']} = {repr(p['value'])};  // 请调整测试数据" for p in params])}

    // Act
    const result = {function_name}({param_str});

    // Assert
    expect(result).toBe('expected_value');  // TODO: 请填写期望的{expected_type}
  }});

  test('无效输入应抛出错误', () => {{
    // Arrange
    const invalidInput = null;  // 无效输入

    // Act & Assert
    expect(() => {{
      {function_name}({param_str if params else 'invalidInput'});
    }}).toThrow('expected error message');  // TODO: 请调整错误信息
  }});

  test.each([
    ['边界值1', '期望结果1'],
    ['边界值2', '期望结果2'],
  ])('边界条件测试: 输入 %s 应返回 %s', (input, expected) => {{
    const result = {function_name}(input);
    expect(result).toBe(expected);
  }});
}});
'''
    return template


def generate_java_test(class_name, method_name, params):
    """生成Java测试模板"""
    param_str = ", ".join([p['name'] for p in params])

    template = f'''import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.assertj.core.api.Assertions.*;

@DisplayName("{class_name} 测试")
class {class_name}Test {{

    @Test
    @DisplayName("正常情况应返回正确结果")
    void shouldReturnCorrectResult() {{
        // Arrange
        {class_name} instance = new {class_name}();
        {chr(10).join([f"        // TODO: 设置参数 {p['name']}" for p in params])}

        // Act
        var result = instance.{method_name}({param_str});

        // Assert
        assertThat(result).isEqualTo("expected");  // TODO: 请填写期望结果
    }}

    @Test
    @DisplayName("无效输入应抛出异常")
    void shouldThrowExceptionForInvalidInput() {{
        // Arrange
        {class_name} instance = new {class_name}();

        // Act & Assert
        assertThatThrownBy(() -> {{
            instance.{method_name}(/* 无效参数 */);
        }}).isInstanceOf(IllegalArgumentException.class)  // TODO: 请调整异常类型
          .hasMessageContaining("expected message");  // TODO: 请调整错误信息
    }}

    @ParameterizedTest
    @CsvSource({{
        "边界值1, 期望结果1",
        "边界值2, 期望结果2"
    }})
    @DisplayName("边界条件测试")
    void shouldHandleEdgeCases(String input, String expected) {{
        // Arrange
        {class_name} instance = new {class_name}();

        // Act
        var result = instance.{method_name}(input);

        // Assert
        assertThat(result).isEqualTo(expected);
    }}
}}
'''
    return template


def generate_go_test(function_name, params):
    """生成Go测试模板"""
    param_str = ", ".join([p['name'] for p in params])

    template = f'''package main

import (
    "testing"
)

func Test_{function_name}_Success(t *testing.T) {{
    // Arrange
    {chr(10).join([f"    {p['name']} := {repr(p['value'])}  // 请调整测试数据" for p in params])}

    // Act
    result, err := {function_name}({param_str})

    // Assert
    if err != nil {{
        t.Errorf("预期无错误，但得到: %v", err)
    }}
    if result != "expected" {{  // TODO: 请填写期望结果
        t.Errorf("预期结果为 'expected'，但得到: %v", result)
    }}
}}

func Test_{function_name}_InvalidInput(t *testing.T) {{
    // Arrange
    invalidInput := ""  // 无效输入

    // Act
    _, err := {function_name}(invalidInput)

    // Assert
    if err == nil {{
        t.Error("预期返回错误，但未返回")
    }}
}}

func Test_{function_name}_EdgeCases(t *testing.T) {{
    tests := []struct {{
        name     string
        input    string
        expected string
    }}{{
        {{"边界值1", "input1", "expected1"}},
        {{"边界值2", "input2", "expected2"}},
    }}

    for _, tt := range tests {{
        t.Run(tt.name, func(t *testing.T) {{
            result, _ := {function_name}(tt.input)
            if result != tt.expected {{
                t.Errorf("预期 %s，但得到 %s", tt.expected, result)
            }}
        }})
    }}
}}
'''
    return template


def generate_rust_test(function_name, params):
    """生成Rust测试模板"""
    param_str = ", ".join([p['name'] for p in params])

    template = f'''#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    fn test_{function_name}_success() {{
        // Arrange
        {chr(10).join([f"        let {p['name']} = {repr(p['value'])};  // 请调整测试数据" for p in params])}

        // Act
        let result = {function_name}({param_str});

        // Assert
        assert_eq!(result, "expected");  // TODO: 请填写期望结果
    }}

    #[test]
    fn test_{function_name}_invalid_input() {{
        // Arrange
        let invalid_input = "";  // 无效输入

        // Act
        let result = {function_name}(invalid_input);

        // Assert
        assert!(result.is_err());  // 假设返回 Result 类型
    }}

    #[test]
    fn test_{function_name}_edge_cases() {{
        let test_cases = vec![
            ("边界值1", "期望结果1"),
            ("边界值2", "期望结果2"),
        ];

        for (input, expected) in test_cases {{
            let result = {function_name}(input);
            assert_eq!(result.unwrap(), expected);
        }}
    }}
}}
'''
    return template


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python generate_test_template.py <语言> <函数名> [参数1,参数2,...]")
        print("示例: python generate_test_template.py python calculate_sum a:10,b:20")
        sys.exit(1)

    lang = sys.argv[1].lower()
    function_name = sys.argv[2]

    # 解析参数
    params = []
    if len(sys.argv) > 3:
        for param in sys.argv[3].split(","):
            if ":" in param:
                name, value = param.split(":", 1)
                params.append({"name": name, "value": value})

    generators = {
        "python": generate_python_test,
        "py": generate_python_test,
        "javascript": generate_javascript_test,
        "js": generate_javascript_test,
        "typescript": generate_javascript_test,
        "ts": generate_javascript_test,
        "java": generate_java_test,
        "go": generate_go_test,
        "golang": generate_go_test,
        "rust": generate_rust_test,
        "rs": generate_rust_test,
    }

    if lang not in generators:
        print(f"❌ 不支持的语言: {lang}")
        print(f"支持的语言: {', '.join(set(generators.keys()))}")
        sys.exit(1)

    template = generators[lang](function_name, params)

    # 输出到文件或控制台
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(template)
            print(f"✅ 测试模板已生成: {output_path}")
    else:
        print(template)


if __name__ == "__main__":
    main()
