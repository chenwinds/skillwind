# Claude Skills Center / Claude 技能中心

## Overview / 简介

**English**: A personal Claude Code skill repository for collecting and managing custom skills. Supports syncing skills to multiple devices (desktop, laptop) for easy installation into the Claude Code CLI programming tool.

**中文**: 个人 Claude Code 技能仓库，用于收集和管理自定义技能（Skill）。支持将技能同步到多台设备（台式电脑、笔记本），方便安装到 Claude Code CLI 等编程工具中。

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

**Create Skills (创建技能)**:
1. Add skill files to `skills/` directory / 将技能文件添加到 `skills/` 目录
2. Run `git up` to sync to GitHub / 运行 `git up` 同步到 GitHub

**Install Skills (安装技能)**:
1. On any device (desktop/laptop), pull latest changes / 在任意设备（台式机/笔记本）拉取最新更改
2. Install skills into Claude Code CLI / 将技能安装到 Claude Code CLI

**Manage Devices (管理设备)**:
- Configure device preferences in `config/` directory / 在 `config/` 目录配置设备偏好
- Each device can have its own settings / 每台设备可以有独立的设置

---

## Skills / 技能列表

| Skill Name | Description | Author | Date Added |
|------------|-------------|--------|------------|
| *Add your skills here* | *Add your skills here* | *Add your skills here* | *Add your skills here* |

> **Tip**: Update this table when you add, modify, or remove skills.
>
> **提示**: 当添加、修改或删除技能时，请更新此表格。

---

## Full Documentation / 完整文档

See `claude-skill-sync-guide.md` for detailed instructions.

详细使用说明请查看 `claude-skill-sync-guide.md` 文件。

---

## License / 许可证

MIT

---

## Special Note / 特别说明

### Design Principles / 设计原则

This repository is designed and built based on the **[Application Design Principles](https://github.com/chenwinds/skillwind/blob/main/docs/design-principles.md)** document. The core philosophy is to externalize human cognitive patterns into system rules.

本仓库基于 **《应用设计原则》** 文档进行设计和构建。核心理念是将人类的认知模式外化为系统规则。

#### Three-Layer Principle Architecture / 三层原则架构

```
┌─────────────────────────────────────────────┐
│  Layer 1: Safety Principles (Highest Priority)
│  第一层：安全原则（最高优先级）
│  · Safety First / 安全优先
│  · Least Privilege / 最小权限
│  · Zero Trust / 零信任
├─────────────────────────────────────────────┤
│  Layer 2: Architecture Principles (High Priority)
│  第二层：架构原则（高优先级）
│  · Separation of Concerns / 分层隔离
│  · Defensive Design / 防御性设计
├─────────────────────────────────────────────┤
│  Layer 3: Experience Principles (Medium Priority)
│  第三层：体验原则（中优先级）
│  · Auditability / 可追溯
│  · Progressive Personalization / 渐进式个性化
│  · Context First / 项目上下文优先
└─────────────────────────────────────────────┘
```

#### Achieved Effects / 达到的效果

| Principle / 原则 | Effect / 效果 |
|-----------------|--------------|
| **安全优先** | 危险操作默认需要确认，安全限制无法被绕过 |
| **最小权限** | 默认无权限，所有权限需显式申请和授权 |
| **零信任** | 首次进入新项目需要信任确认，所有输入需校验 |
| **分层隔离** | 认证信息与功能配置分离，各层独立管理 |
| **防御性设计** | 配置修改前自动备份，失败操作可恢复 |
| **可追溯** | 完整历史记录，配置变更可追踪 |
| **渐进式个性化** | 自动学习使用习惯，避免重复提示 |
| **上下文优先** | 每个项目独立配置，项目间数据隔离 |

#### Core Insight / 核心洞察

> **All design principles are decision templates that externalize human cognitive patterns.**
>
> **所有设计原则都是将人类认知模式外化为决策模板。**

- Safety principles → Reduce uncertainty / 安全原则 → 降低不确定性
- Architecture principles → Reduce cognitive load / 架构原则 → 减少认知负荷
- Experience principles → Improve adaptation efficiency / 体验原则 → 提高适应效率

---
