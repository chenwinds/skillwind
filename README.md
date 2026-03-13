# Claude Skills Center / Claude 技能中心

## Overview / 简介

**English**: A personal Claude Code skill repository for bidirectional synchronization between desktop and laptop.

**中文**: 个人 Claude Code 技能仓库，用于台式电脑和笔记本之间的双向同步。

---

## Quick Start / 快速开始

### 1. Clone the Repository / 克隆仓库

```bash
git clone git@github.com:chenwinds/skillwind.git
cd skillwind
```

### 2. Run Setup / 运行设置

```bash
setup.bat
```

This creates all required folders and configuration files.

这会创建所有必需的文件夹和配置文件。

### 3. Sync Your Changes / 同步更改

```bash
# Make your changes / 修改内容后
git up
```

The `git up` command automatically:
- Adds all changes (`git add .`)
- Commits with computer name (`git commit -m "auto update [COMPUTERNAME]"`)
- Pushes to GitHub (`git push`)

`git up` 命令自动完成：
- 添加所有更改
- 提交并附带电脑名称
- 推送到 GitHub

---

## Directory Structure / 目录结构

```
skillwind/
├── skills/          # Skill files / Skill 文件
├── config/          # Configuration / 配置文件
├── logs/            # Sync logs / 同步日志
├── tools/           # Helper scripts / 辅助脚本
│   └── sync.bat     # Auto sync script / 自动同步脚本
├── setup.bat        # One-click setup / 一键设置脚本
└── README.md        # This file
```

---

## Workflow / 工作流程

**Desktop (台式电脑)**:
1. Create or modify skills / 创建或修改技能
2. Run `git up` to sync / 运行 `git up` 同步
3. Pull before working / 工作前先拉取

**Laptop (笔记本)**:
1. Pull latest changes / 拉取最新更改
2. Create or modify skills / 创建或修改技能
3. Run `git up` to sync / 运行 `git up` 同步

---

## Full Documentation / 完整文档

See `claude-skill-sync-guide.md` for detailed instructions.

详细使用说明请查看 `claude-skill-sync-guide.md` 文件。

---

## License / 许可证

MIT
