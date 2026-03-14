# 项目结构保护规则

## 核心原则

**除了 `skills/` 目录内的内容外，保持其余文件和文件夹的结构不变。**

未经用户明确同意，**禁止**增加任何新的文件或文件夹到项目根目录或其他非 skills 目录中。

## 项目结构

```
skillwind/
├── .claude/                    # Claude 配置文件
├── .git/                       # Git 仓库
├── .gitignore                  # Git 忽略规则
├── CLAUDE.md                   # CLAUDE 配置说明
├── LICENSE                     # 许可证文件
├── README.md                   # 项目说明文档
├── skills/                     # 【可修改】技能文件目录
│   ├── ob/                     # OB 口述整理技能
│   ├── skill-creator/          # 技能创建技能
│   ├── claude-md-management/   # CLAUDE.md 管理技能
│   ├── claude-code-setup/      # Claude Code 配置技能
│   ├── frontend-design/        # 前端设计技能
│   └── registry.json           # 技能注册表
└── memory/                     # 【可修改】记忆文件目录
    └── PROJECT_STRUCTURE.md    # 本文件
```

## 允许的操作

| 目录 | 允许操作 |
|------|----------|
| `skills/` | 可以添加、修改、删除技能相关文件 |
| `memory/` | 可以添加、修改记忆文件 |
| 其他目录 | **禁止**添加新文件或文件夹 |

## 禁止的操作

- 在项目根目录创建新文件
- 在项目根目录创建新文件夹
- 在 `.claude/`、`.git/` 外的其他目录创建新文件
- 修改 `LICENSE`、`.gitignore` 等配置文件

## 例外情况

只有用户**明确表示同意**时，才可以：
1. 添加新文件到非 skills 目录
2. 创建新的文件夹结构
3. 修改项目配置文件

## 输出文件保存位置

整理口述内容等生成的输出文件，应保存到项目外部的目录：
- 推荐：`D:\output\Claudecode_skillwind\`
- 或其他用户指定的项目外位置

---

**此规则优先级：高**

在任何操作前，请检查是否违反此结构保护规则。
