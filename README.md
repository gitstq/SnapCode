<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen.svg" alt="Dependencies">
</p>

<p align="center">
  <a href="README.md">简体中文</a> | 
  <a href="README_EN.md">English</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">📸 SnapCode</h1>

<p align="center">
  <strong>轻量级代码快照管理工具</strong><br>
  零依赖 CLI 工具，轻松管理代码快照，支持差异对比、一键恢复、导出归档
</p>

---

## 🎉 项目介绍

**SnapCode** 是一款专为开发者设计的轻量级代码快照管理工具。它解决了开发过程中常见的痛点：

- 🔥 **不想用 Git？** 有时候只想快速保存当前代码状态，不需要完整的版本控制
- 🔥 **实验性代码？** 在尝试新方案时，想快速备份当前状态以便随时回退
- 🔥 **临时保存？** 在重构或调试时，需要保存多个中间状态进行对比
- 🔥 **零依赖？** 不需要安装任何第三方库，Python 标准库即可运行

### ✨ 自研差异化亮点

| 特性 | SnapCode | Git | 其他工具 |
|------|----------|-----|----------|
| 零依赖 | ✅ | ❌ | ❌ |
| 学习成本 | 极低 | 较高 | 中等 |
| 快照创建 | 秒级 | 分钟级 | 分钟级 |
| 差异对比 | ✅ | ✅ | ❌ |
| 一键恢复 | ✅ | ✅ | ❌ |
| 导出归档 | ✅ | ❌ | ❌ |

---

## ✨ 核心特性

### 📸 快照管理
- **一键创建** - 快速创建代码快照，支持命名和备注
- **智能忽略** - 自动忽略 `.git`、`__pycache__`、`node_modules` 等目录
- **增量存储** - 高效存储，不占用额外空间

### 🔄 恢复与对比
- **一键恢复** - 从任意快照恢复代码状态
- **差异对比** - 对比两个快照之间的文件变化
- **文件级对比** - 查看具体文件的详细差异

### 📦 导出与分享
- **归档导出** - 将快照导出为 `.tar.gz` 压缩包
- **快照导入** - 从压缩包导入快照，方便分享和备份

### 🛠️ 开发者友好
- **彩色输出** - 终端彩色输出，清晰易读
- **详细日志** - 完整的操作日志和错误提示
- **预览模式** - 恢复前可预览将要修改的文件

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 无需安装任何第三方依赖

### 安装方式

```bash
# 方式一：直接运行
git clone https://github.com/gitstq/SnapCode.git
cd SnapCode
python snapcode.py --help

# 方式二：pip 安装
pip install -e .
snapcode --help
```

### 基本使用

```bash
# 创建快照
snapcode create my-feature -m "添加登录功能"

# 查看所有快照
snapcode list

# 恢复快照
snapcode restore 20260508_120000

# 对比两个快照
snapcode diff snap1 snap2

# 导出快照
snapcode export 20260508_120000 backup.tar.gz
```

---

## 📖 详细使用指南

### 创建快照

```bash
# 基本创建
snapcode create feature-name

# 带备注创建
snapcode create feature-name -m "实现用户认证模块"

# 指定目录
snapcode create feature-name -d /path/to/project
```

创建的快照将保存在项目目录下的 `.snapcode` 文件夹中。

### 查看快照列表

```bash
snapcode list
```

输出示例：
```
📸 Snapshots

ID                        Name            Files     Size       Created
--------------------------------------------------------------------------------
20260508_120000_feature   feature         42        156.2KB    2026-05-08 12:00:00
20260508_143000_bugfix    bugfix          38        142.8KB    2026-05-08 14:30:00
```

### 恢复快照

```bash
# 恢复到指定快照
snapcode restore 20260508_120000

# 预览模式（不实际修改文件）
snapcode restore 20260508_120000 --dry-run
```

### 对比快照

```bash
# 对比两个快照的文件变化
snapcode diff 20260508_120000 20260508_143000

# 查看具体文件的差异
snapcode diff snap1 snap2 -f src/main.py
```

输出示例：
```
📊 Diff Result

Added:
  + src/new_feature.py
  + config/settings.json

Removed:
  - old_module.py

Modified:
  ~ src/main.py
  ~ README.md
```

### 删除快照

```bash
snapcode delete 20260508_120000
```

### 导出与导入

```bash
# 导出快照
snapcode export 20260508_120000 backup.tar.gz

# 导入快照
snapcode import backup.tar.gz
```

---

## 💡 设计思路与迭代规划

### 设计理念

SnapCode 的设计理念是**简单、轻量、实用**：

1. **零依赖** - 仅使用 Python 标准库，无需安装任何第三方包
2. **单文件实现** - 核心代码在一个文件中，易于理解和修改
3. **非侵入式** - 快照数据存储在 `.snapcode` 目录，不影响项目结构

### 技术选型

- **Python 标准库** - `argparse` 处理命令行参数，`json` 存储元数据，`shutil` 复制文件
- **MD5 哈希** - 用于检测文件变化
- **tar.gz 格式** - 用于快照导出，跨平台兼容

### 后续迭代计划

- [ ] 支持 Git 集成，自动关联 commit
- [ ] 添加快照标签功能
- [ ] 支持远程存储（S3、FTP 等）
- [ ] 添加 Web UI 界面
- [ ] 支持增量快照，节省存储空间

---

## 📦 打包与部署指南

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/gitstq/SnapCode.git
cd SnapCode

# 安装开发模式
pip install -e .

# 运行测试
python -m pytest tests/
```

### 构建 PyPI 包

```bash
# 安装构建工具
pip install build

# 构建
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

### 跨平台兼容

SnapCode 使用纯 Python 实现，兼容以下平台：
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, CentOS, Debian 等)

---

## 🤝 贡献指南

欢迎社区贡献！请遵循以下规范：

### 提交 PR

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'feat: 添加新功能'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request

### Issue 反馈

请使用 GitHub Issues 反馈问题，包含：
- 操作系统和 Python 版本
- 复现步骤
- 期望结果和实际结果

---

## 📄 开源协议说明

本项目采用 [MIT License](LICENSE) 开源协议。

```
MIT License

Copyright (c) 2026 SnapCode Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<p align="center">
  Made with ❤️ by SnapCode Team
</p>
