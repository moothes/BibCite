# BibCite for Windows

一个基于 `PyQt5` 的桌面文献管理工具，面向 BibTeX 工作流。你可以从本地库或 Google Scholar 检索文献，维护项目条目与 alias，并导出为 `.bib` 文件。

## 功能特性

- 可视化管理项目条目（新增、编辑、删除）
- 支持为条目维护多个 alias（自动去重、支持 `,` / `;` 分隔输入）
- 三个信息来源标签页：
  - `Storage`：在历史数据库中按标题/作者/alias 搜索
  - `Google Scholar`：在线检索并加入项目
  - `BibTeX`：从本地 `.bib` 文件批量导入
- BibTeX 实时预览与双击快速加入项目
- 导出时自动写入 `data/Prefix.bib` 头部模板
- 导出后仅将“新增条目”追加到历史数据库 `data/database.json`

## 界面概览

- 左侧：项目条目卡片列表 + 当前条目 BibTeX 预览
- 右侧：`Storage` / `Google Scholar` / `BibTeX` 三个数据源页签
- 菜单：
  - `Project -> New Project`
  - `Project -> Open BibTeX File`
  - `Project -> Exit`

## 运行环境

- Python 3.9+
- Windows（当前命名与默认体验面向 Windows，其他平台理论可运行）

## 安装依赖

```bash
pip install pyqt5 bibtexparser scholarly 
```

## 快速开始

```bash
python main.py
```

应用启动后建议流程：

1. 通过 `+ New Entry` 手动新增条目，或在右侧标签页导入/检索。
2. 双击候选条目加入项目。
3. 右键项目条目可编辑、添加 alias、删除。
4. 点击 `Export` 导出 `.bib` 文件。




