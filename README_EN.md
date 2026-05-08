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
  <strong>Lightweight Code Snapshot Management Tool</strong><br>
  Zero-dependency CLI tool for managing code snapshots with diff, restore, and export capabilities
</p>

---

## 🎉 Introduction

**SnapCode** is a lightweight code snapshot management tool designed for developers. It solves common pain points in the development process:

- 🔥 **Don't want Git?** Sometimes you just want to quickly save your current code state without full version control
- 🔥 **Experimental code?** When trying new approaches, quickly backup current state for easy rollback
- 🔥 **Temporary saves?** During refactoring or debugging, save multiple intermediate states for comparison
- 🔥 **Zero dependencies?** No third-party libraries needed, runs with Python standard library only

### ✨ Unique Features

| Feature | SnapCode | Git | Other Tools |
|---------|----------|-----|-------------|
| Zero Dependencies | ✅ | ❌ | ❌ |
| Learning Curve | Minimal | High | Medium |
| Snapshot Creation | Seconds | Minutes | Minutes |
| Diff Comparison | ✅ | ✅ | ❌ |
| One-click Restore | ✅ | ✅ | ❌ |
| Export Archive | ✅ | ❌ | ❌ |

---

## ✨ Core Features

### 📸 Snapshot Management
- **One-click Create** - Quickly create code snapshots with naming and notes
- **Smart Ignore** - Automatically ignores `.git`, `__pycache__`, `node_modules`, etc.
- **Efficient Storage** - Incremental storage without wasting space

### 🔄 Restore & Compare
- **One-click Restore** - Restore code state from any snapshot
- **Diff Comparison** - Compare file changes between two snapshots
- **File-level Diff** - View detailed differences for specific files

### 📦 Export & Share
- **Archive Export** - Export snapshots as `.tar.gz` archives
- **Snapshot Import** - Import snapshots from archives for sharing and backup

### 🛠️ Developer Friendly
- **Colorful Output** - Terminal colored output, clear and readable
- **Detailed Logs** - Complete operation logs and error messages
- **Preview Mode** - Preview files to be modified before restoring

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- No third-party dependencies required

### Installation

```bash
# Method 1: Run directly
git clone https://github.com/gitstq/SnapCode.git
cd SnapCode
python snapcode.py --help

# Method 2: pip install
pip install -e .
snapcode --help
```

### Basic Usage

```bash
# Create snapshot
snapcode create my-feature -m "Added login feature"

# List all snapshots
snapcode list

# Restore snapshot
snapcode restore 20260508_120000

# Compare two snapshots
snapcode diff snap1 snap2

# Export snapshot
snapcode export 20260508_120000 backup.tar.gz
```

---

## 📖 Detailed Usage Guide

### Creating Snapshots

```bash
# Basic creation
snapcode create feature-name

# Create with message
snapcode create feature-name -m "Implement user authentication module"

# Specify directory
snapcode create feature-name -d /path/to/project
```

Snapshots are saved in the `.snapcode` folder within your project directory.

### Listing Snapshots

```bash
snapcode list
```

Output example:
```
📸 Snapshots

ID                        Name            Files     Size       Created
--------------------------------------------------------------------------------
20260508_120000_feature   feature         42        156.2KB    2026-05-08 12:00:00
20260508_143000_bugfix    bugfix          38        142.8KB    2026-05-08 14:30:00
```

### Restoring Snapshots

```bash
# Restore to specified snapshot
snapcode restore 20260508_120000

# Preview mode (don't actually modify files)
snapcode restore 20260508_120000 --dry-run
```

### Comparing Snapshots

```bash
# Compare file changes between two snapshots
snapcode diff 20260508_120000 20260508_143000

# View diff for specific file
snapcode diff snap1 snap2 -f src/main.py
```

Output example:
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

### Deleting Snapshots

```bash
snapcode delete 20260508_120000
```

### Export & Import

```bash
# Export snapshot
snapcode export 20260508_120000 backup.tar.gz

# Import snapshot
snapcode import backup.tar.gz
```

---

## 💡 Design Philosophy & Roadmap

### Design Philosophy

SnapCode is designed with **simplicity, lightweight, and practicality**:

1. **Zero Dependencies** - Uses only Python standard library
2. **Single File** - Core code in one file for easy understanding and modification
3. **Non-intrusive** - Snapshot data stored in `.snapcode` directory, doesn't affect project structure

### Technology Choices

- **Python Standard Library** - `argparse` for CLI, `json` for metadata, `shutil` for file operations
- **MD5 Hash** - For detecting file changes
- **tar.gz Format** - For snapshot export, cross-platform compatible

### Roadmap

- [ ] Git integration with automatic commit association
- [ ] Snapshot tagging feature
- [ ] Remote storage support (S3, FTP, etc.)
- [ ] Web UI interface
- [ ] Incremental snapshots to save storage

---

## 📦 Build & Deployment

### Local Development

```bash
# Clone repository
git clone https://github.com/gitstq/SnapCode.git
cd SnapCode

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

### Building PyPI Package

```bash
# Install build tools
pip install build

# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### Cross-Platform Compatibility

SnapCode is pure Python and compatible with:
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, CentOS, Debian, etc.)

---

## 🤝 Contributing

Community contributions are welcome! Please follow these guidelines:

### Submitting PRs

1. Fork this repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Create Pull Request

### Reporting Issues

Please use GitHub Issues with:
- OS and Python version
- Steps to reproduce
- Expected and actual results

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

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
