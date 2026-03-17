---
name: tdd-flow
description: Guide users through Test-Driven Development (TDD) workflow with interactive Red-Green-Refactor cycles. Use this skill when the user wants to adopt TDD methodology, mentions "test-driven", "test first", "write tests first", requests unit testing, or at the start of a project when testing strategy is being discussed. This skill provides step-by-step interactive guidance for writing failing tests, making them pass, and refactoring code while maintaining test coverage.
license: Complete terms in LICENSE.txt
---

# TDD Flow - 测试驱动开发工作流

## 核心原则

TDD 遵循 **Red-Green-Refactor**（红-绿-重构）循环：
1. **Red（红）**: 编写一个失败的测试
2. **Green（绿）**: 编写最简单的代码让测试通过
3. **Refactor（重构）**: 优化代码，保持测试通过

---

## 触发条件

当检测到以下场景时激活此技能：
- 用户说"用TDD方式开发"
- 用户要求"先写测试"
- 用户提到"测试驱动"
- 项目初期讨论测试策略
- 用户要求单元测试

---

## 工作流程

### 阶段 0: 项目初始化与测试框架选择

**首次启动TDD时执行：**

1. **分析项目类型**
   - 检测项目语言（Python, JavaScript, TypeScript, Java, Go, Rust等）
   - 检查现有测试框架配置
   - 确定测试文件组织结构

2. **推荐测试框架**

   | 语言 | 推荐框架 | 安装命令 |
   |------|----------|----------|
   | Python | pytest | `pip install pytest` |
   | JavaScript | Jest | `npm install --save-dev jest` |
   | TypeScript | Vitest/Jest | `npm install --save-dev vitest` |
   | Java | JUnit 5 + AssertJ | Maven/Gradle依赖 |
   | Go | 内置 testing | 无需安装 |
   | Rust | 内置 test | 无需安装 |

3. **创建测试目录结构**
   ```
   推荐结构：
   - tests/ 目录或 __tests__/ 目录
   - 与被测代码对应的 test 文件命名
   - 测试辅助工具文件
   ```

4. **询问用户**
   - "这是一个 [检测到语言] 项目，推荐使用 [框架]，是否继续？"
   - "是否有特定的测试框架偏好？"
   - "测试覆盖率目标设置为多少？（建议 80% 以上）"

### 阶段 1: Red - 编写失败的测试

**目标**: 编写一个能够验证期望行为的测试，此时应该失败

**步骤**:

1. **理解需求**
   - 询问用户要实现的功能是什么
   - 确认输入和期望输出
   - 识别边界条件和异常情况

2. **编写测试**（遵循 AAA 模式）
   - **Arrange（准备）**: 设置测试数据和初始状态
   - **Act（执行）**: 调用被测函数/方法
   - **Assert（断言）**: 验证结果符合预期

3. **确认测试失败**
   - 运行测试，确保它按预期失败
   - 检查失败原因是否正确（应该是功能未实现，而非测试错误）

**检查清单**:
- [ ] 测试名称清晰描述行为
- [ ] 测试只验证一个概念
- [ ] 断言明确且具体
- [ ] 测试确实失败（Red）

### 阶段 2: Green - 让测试通过

**目标**: 编写最简单的代码让测试通过

**原则**:
- **先实现，再优化** - 此刻只关注让测试变绿
- **最简单的方案** - 不要过度设计
- **硬编码也可以** - 如果能让测试通过，先硬编码再泛化

**步骤**:

1. **实现功能代码**
   - 创建被测函数/类的最小实现
   - 只编写让当前测试通过的代码
   - 不要考虑未来可能的需求

2. **运行测试**
   - 确认所有测试通过（Green）
   - 如果失败，调试并修复

3. **快速检查**
   - 代码是否过于简单？没关系，下一步会重构
   - 是否引入了重复？没关系，下一步会处理

**检查清单**:
- [ ] 测试通过（Green）
- [ ] 实现代码存在（即使很粗糙）
- [ ] 没有编写超出当前测试需求的代码

### 阶段 3: Refactor - 重构

**目标**: 改进代码质量，同时保持所有测试通过

**重构方向**:
- **消除重复** - DRY 原则
- **提升可读性** - 清晰的命名和结构
- **降低复杂度** - 函数单一职责
- **改善设计** - 合适的设计模式

**步骤**:

1. **识别坏味道**
   - 重复代码
   - 过长函数
   - 过多参数
   - 魔法数字/字符串

2. **安全重构**
   - 小步前进，每次改动后运行测试
   - 使用 IDE 重构工具（重命名、提取方法等）
   - 保持测试始终通过

3. **验证**
   - 运行完整测试套件
   - 确认代码质量提升

**检查清单**:
- [ ] 代码无重复
- [ ] 命名清晰
- [ ] 函数职责单一
- [ ] 所有测试仍通过

### 阶段 4: 重复循环

**询问用户**:
- "当前功能已完成，是否继续下一个测试场景？"
- 如果有边界条件未覆盖："是否需要测试边界情况？"
- 如果有异常场景："是否需要测试错误处理？"

**返回阶段 1，开始下一个 Red-Green-Refactor 循环**

---

## 交互式引导模式

### 模式 A: 全程引导（推荐初学者）

**每个步骤都询问用户确认：**

```
[当前状态]: 🟡 准备编写第一个测试（Red阶段）

[任务]: 实现用户登录功能
[下一步]: 编写测试 - 验证正确的用户名密码应返回成功

请确认：
1. 这是正确的测试方向吗？
2. 是否需要调整测试场景？
3. 准备开始编写测试吗？（输入"开始"继续）
```

### 模式 B: 半自动（推荐有经验者）

**自动生成测试和代码骨架，用户填写实现：**

```
已生成测试文件 tests/auth.test.js:

// TODO: 请完成此测试
import { login } from '../src/auth';

test('正确的用户名密码应返回成功', () => {
  // Arrange
  const username = 'admin';
  const password = 'correct_password';

  // Act
  const result = login(username, password);

  // Assert
  expect(result).toBe(/* 请填写期望结果 */);
});

运行: npm test 查看失败测试
```

### 模式 C: 审查模式

**用户已编写代码，检查是否符合TDD原则：**

检查项：
- 测试是否在实现之前编写？
- 测试是否先失败后通过？
- 重构是否充分？
- 测试覆盖率如何？

---

## 最佳实践指导

### 测试编写原则

1. **FIRST 原则**
   - **F**ast - 测试运行快速
   - **I**ndependent - 测试相互独立
   - **R**epeatable - 可重复执行
   - **S**elf-validating - 自我验证（布尔结果）
   - **T**imely - 及时编写（与实现同时）

2. **测试命名规范**
   ```python
   # 好的命名
   test_should_return_success_when_credentials_are_valid
   test_should_throw_error_when_password_is_empty

   # 避免
   test_login  # 太模糊
   test1       # 无意义
   ```

3. **测试结构**
   ```python
   def test_should_do_something():
       # Arrange
       input_data = create_test_data()

       # Act
       result = function_under_test(input_data)

       # Assert
       assert result == expected_value
   ```

### 常见反模式警告

⚠️ **检测到以下情况时提醒用户：**

- **测试实现而非行为** - 测试调用了私有方法或检查了内部状态
- **过度Mock** - 所有依赖都被Mock，测试失去意义
- **测试过多** - 一个测试验证多个概念
- **不稳定的测试** - 依赖时间、随机数或外部服务
- **慢测试** - 涉及数据库、网络或复杂计算

### 重构检查清单

每次重构前确认：
- [ ] 所有测试通过
- [ ] 代码版本控制已提交（可选但推荐）
- [ ] 重构范围小且明确

重构后确认：
- [ ] 所有测试仍通过
- [ ] 代码更简洁或更清晰
- [ ] 没有引入新功能（纯重构）

---

## 特定语言指导

### Python + pytest

```python
# 推荐结构
def test_should_calculate_total_price_with_discount():
    """给定购物清单和折扣率，应计算正确的总价"""
    # Arrange
    cart = Cart(items=[Item("apple", 10), Item("banana", 20)])
    discount_rate = 0.1

    # Act
    total = cart.calculate_total(discount_rate)

    # Assert
    assert total == 27  # (10+20) * 0.9

# 参数化测试（边界条件）
@pytest.mark.parametrize("input,expected", [
    ("", False),      # 空字符串
    ("a", True),      # 最小有效值
    ("a" * 100, True), # 最大有效值
])
def test_should_validate_username_length(input, expected):
    assert is_valid_username(input) == expected
```

### JavaScript/TypeScript + Jest/Vitest

```javascript
// 推荐结构
describe('购物车总价计算', () => {
  test('给定购物清单和折扣率，应计算正确的总价', () => {
    // Arrange
    const cart = new Cart([
      new Item('apple', 10),
      new Item('banana', 20)
    ]);
    const discountRate = 0.1;

    // Act
    const total = cart.calculateTotal(discountRate);

    // Assert
    expect(total).toBe(27); // (10+20) * 0.9
  });

  // 边界条件测试
  test.each([
    ['', false],
    ['a', true],
    ['a'.repeat(100), true],
  ])('用户名 "%s" 的验证结果应为 %s', (input, expected) => {
    expect(isValidUsername(input)).toBe(expected);
  });
});
```

### Java + JUnit 5

```java
@DisplayName("购物车总价计算")
class CartTest {

    @Test
    @DisplayName("给定购物清单和折扣率，应计算正确的总价")
    void shouldCalculateTotalWithDiscount() {
        // Arrange
        Cart cart = new Cart(Arrays.asList(
            new Item("apple", 10),
            new Item("banana", 20)
        ));
        double discountRate = 0.1;

        // Act
        double total = cart.calculateTotal(discountRate);

        // Assert
        assertEquals(27.0, total, 0.001);
    }

    @ParameterizedTest
    @CsvSource({
        "'', false",
        "'a', true",
        "'aaaa...', true"  // 100个a
    })
    @DisplayName("用户名长度验证")
    void shouldValidateUsernameLength(String input, boolean expected) {
        assertEquals(expected, isValidUsername(input));
    }
}
```

---

## 工具集成

### 运行测试命令

根据不同语言和框架提供相应命令：

```bash
# Python
pytest                    # 运行所有测试
pytest -v                 # 详细输出
pytest --tb=short         # 简短错误信息
pytest tests/test_auth.py # 运行特定文件
pytest -k "login"         # 运行匹配名称的测试

# JavaScript/TypeScript
npm test                  # 运行所有测试
npm test -- --watch      # 监视模式
npm test -- --coverage   # 生成覆盖率报告

# Java
./mvnw test               # Maven
./gradlew test            # Gradle

# Go
go test ./...             # 运行所有测试
go test -v ./...          # 详细输出
go test -cover ./...      # 覆盖率

# Rust
cargo test                # 运行所有测试
cargo test -- --nocapture # 显示打印输出
```

### 覆盖率目标

- **行覆盖率**: ≥ 80%
- **分支覆盖率**: ≥ 70%
- **函数覆盖率**: ≥ 90%

---

## 输出示例

### 示例对话流程

```
用户: 我要用TDD方式实现一个用户注册功能

Claude: [TDD Flow 已激活]

📋 项目分析
检测到这是一个 JavaScript 项目，推荐使用 Jest 测试框架。

🎯 第1个测试场景（Red阶段）
我们从最简单的场景开始：有效注册信息应创建成功

我将生成测试文件 tests/registration.test.js:

[生成测试代码...]

✅ 下一步:
1. 运行: npm test
2. 确认测试失败（Red）
3. 告诉我结果，我将继续指导

用户: 测试失败了

Claude: 很好！现在进入 Green 阶段。

💚 实现代码
让我创建最简单的实现使测试通过:

[生成实现代码...]

✅ 下一步:
1. 运行: npm test
2. 确认测试通过（Green）
3. 然后我们进入重构阶段

用户: 测试通过了

Claude: 完美！现在检查是否需要重构。

🔍 代码审查
当前代码虽然简单但可工作。建议改进:
1. 添加输入验证
2. 错误处理

是否现在重构，还是继续下一个测试场景？

选项:
1. 重构当前代码
2. 继续下一个场景（边界条件：重复用户名）
3. 结束TDD流程

[根据用户选择继续...]
```

---

## 错误处理

### 常见错误及解决方案

1. **测试不失败**
   - 检查是否已存在实现代码
   - 检查测试断言是否正确
   - 检查测试是否被跳过

2. **测试无法通过**
   - 实现代码是否有语法错误
   - 逻辑是否正确
   - 测试断言是否过高（期望过多）

3. **重构后测试失败**
   - 回滚重构
   - 小步重构，每次运行测试
   - 检查是否意外改变了行为

4. **测试运行缓慢**
   - 检查是否有外部依赖（数据库、网络）
   - 考虑使用 Mock/Stub
   - 检查测试数据量是否过大

---

## 高级主题

### 测试替身（Test Doubles）

- **Dummy**: 占位对象，不使用
- **Fake**: 简化实现，如内存数据库
- **Stub**: 预设响应
- **Spy**: 记录调用信息
- **Mock**: 预设期望和验证

使用原则：只在必要时使用，优先使用真实对象

### 集成TDD与CI/CD

1. 每次提交前运行测试
2. CI 流水线执行测试套件
3. 覆盖率报告作为PR检查项
4. 自动化测试与部署

---

## 结束语

TDD 是一种思考方式，不仅是技术实践。

**记住**:
- 慢下来，小步前进
- 测试是文档，描述代码行为
- 重构是持续的过程
- 绿条（测试通过）给你重构的信心

**有问题？**
- 输入 "help" 查看当前阶段可用命令
- 输入 "skip" 跳过当前阶段（不推荐）
- 输入 "status" 查看TDD进度

---

*Happy Testing! 🧪*
