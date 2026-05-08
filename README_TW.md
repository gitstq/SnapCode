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
  <strong>輕量級程式碼快照管理工具</strong><br>
  零依賴 CLI 工具，輕鬆管理程式碼快照，支援差異對比、一鍵復原、匯出歸檔
</p>

---

## 🎉 專案介紹

**SnapCode** 是一款專為開發者設計的輕量級程式碼快照管理工具。它解決了開發過程中常見的痛點：

- 🔥 **不想用 Git？** 有時候只想快速儲存當前程式碼狀態，不需要完整的版本控制
- 🔥 **實驗性程式碼？** 在嘗試新方案時，想快速備份當前狀態以便隨時回退
- 🔥 **臨時儲存？** 在重構或除錯時，需要儲存多個中間狀態進行對比
- 🔥 **零依賴？** 不需要安裝任何第三方函式庫，Python 標準函式庫即可執行

### ✨ 自研差異化亮點

| 特性 | SnapCode | Git | 其他工具 |
|------|----------|-----|----------|
| 零依賴 | ✅ | ❌ | ❌ |
| 學習成本 | 極低 | 較高 | 中等 |
| 快照建立 | 秒級 | 分鐘級 | 分鐘級 |
| 差異對比 | ✅ | ✅ | ❌ |
| 一鍵復原 | ✅ | ✅ | ❌ |
| 匯出歸檔 | ✅ | ❌ | ❌ |

---

## ✨ 核心特性

### 📸 快照管理
- **一鍵建立** - 快速建立程式碼快照，支援命名和備註
- **智慧忽略** - 自動忽略 `.git`、`__pycache__`、`node_modules` 等目錄
- **增量儲存** - 高效儲存，不佔用額外空間

### 🔄 復原與對比
- **一鍵復原** - 從任意快照復原程式碼狀態
- **差異對比** - 對比兩個快照之間的檔案變化
- **檔案級對比** - 檢視具體檔案的詳細差異

### 📦 匯出與分享
- **歸檔匯出** - 將快照匯出為 `.tar.gz` 壓縮檔
- **快照匯入** - 從壓縮檔匯入快照，方便分享和備份

### 🛠️ 開發者友善
- **彩色輸出** - 終端彩色輸出，清晰易讀
- **詳細日誌** - 完整的操作日誌和錯誤提示
- **預覽模式** - 復原前可預覽將要修改的檔案

---

## 🚀 快速開始

### 環境要求

- Python 3.8 或更高版本
- 無需安裝任何第三方依賴

### 安裝方式

```bash
# 方式一：直接執行
git clone https://github.com/gitstq/SnapCode.git
cd SnapCode
python snapcode.py --help

# 方式二：pip 安裝
pip install -e .
snapcode --help
```

### 基本使用

```bash
# 建立快照
snapcode create my-feature -m "新增登入功能"

# 檢視所有快照
snapcode list

# 復原快照
snapcode restore 20260508_120000

# 對比兩個快照
snapcode diff snap1 snap2

# 匯出快照
snapcode export 20260508_120000 backup.tar.gz
```

---

## 📖 詳細使用指南

### 建立快照

```bash
# 基本建立
snapcode create feature-name

# 帶備註建立
snapcode create feature-name -m "實作使用者認證模組"

# 指定目錄
snapcode create feature-name -d /path/to/project
```

建立的快照將儲存在專案目錄下的 `.snapcode` 資料夾中。

### 檢視快照列表

```bash
snapcode list
```

輸出範例：
```
📸 Snapshots

ID                        Name            Files     Size       Created
--------------------------------------------------------------------------------
20260508_120000_feature   feature         42        156.2KB    2026-05-08 12:00:00
20260508_143000_bugfix    bugfix          38        142.8KB    2026-05-08 14:30:00
```

### 復原快照

```bash
# 復原到指定快照
snapcode restore 20260508_120000

# 預覽模式（不實際修改檔案）
snapcode restore 20260508_120000 --dry-run
```

### 對比快照

```bash
# 對比兩個快照的檔案變化
snapcode diff 20260508_120000 20260508_143000

# 檢視具體檔案的差異
snapcode diff snap1 snap2 -f src/main.py
```

輸出範例：
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

### 刪除快照

```bash
snapcode delete 20260508_120000
```

### 匯出與匯入

```bash
# 匯出快照
snapcode export 20260508_120000 backup.tar.gz

# 匯入快照
snapcode import backup.tar.gz
```

---

## 💡 設計思路與迭代規劃

### 設計理念

SnapCode 的設計理念是**簡單、輕量、實用**：

1. **零依賴** - 僅使用 Python 標準函式庫，無需安裝任何第三方套件
2. **單檔案實作** - 核心程式碼在一個檔案中，易於理解和修改
3. **非侵入式** - 快照資料儲存在 `.snapcode` 目錄，不影響專案結構

### 技術選型

- **Python 標準函式庫** - `argparse` 處理命令列參數，`json` 儲存元資料，`shutil` 複製檔案
- **MD5 雜湊** - 用於檢測檔案變化
- **tar.gz 格式** - 用於快照匯出，跨平台相容

### 後續迭代計畫

- [ ] 支援 Git 整合，自動關聯 commit
- [ ] 新增快照標籤功能
- [ ] 支援遠端儲存（S3、FTP 等）
- [ ] 新增 Web UI 介面
- [ ] 支援增量快照，節省儲存空間

---

## 📦 打包與部署指南

### 本地開發

```bash
# 複製儲存庫
git clone https://github.com/gitstq/SnapCode.git
cd SnapCode

# 安裝開發模式
pip install -e .

# 執行測試
python -m pytest tests/
```

### 建構 PyPI 套件

```bash
# 安裝建構工具
pip install build

# 建構
python -m build

# 上傳到 PyPI
python -m twine upload dist/*
```

### 跨平台相容

SnapCode 使用純 Python 實作，相容以下平台：
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, CentOS, Debian 等)

---

## 🤝 貢獻指南

歡迎社群貢獻！請遵循以下規範：

### 提交 PR

1. Fork 本儲存庫
2. 建立功能分支：`git checkout -b feature/amazing-feature`
3. 提交變更：`git commit -m 'feat: 新增新功能'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 建立 Pull Request

### Issue 回饋

請使用 GitHub Issues 回饋問題，包含：
- 作業系統和 Python 版本
- 重現步驟
- 預期結果和實際結果

---

## 📄 開源協議說明

本專案採用 [MIT License](LICENSE) 開源協議。

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
