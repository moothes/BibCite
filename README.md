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
pip install pyqt5 bibtexparser scholarly pytest pytest-qt
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

## Google Scholar 代理（可选）

如果网络环境导致检索失败，可设置代理环境变量后再启动程序：

- `SCHOLAR_HTTP_PROXY`
- `SCHOLAR_HTTPS_PROXY`
- 或通用 `HTTP_PROXY` / `HTTPS_PROXY`

程序会在普通检索失败时尝试代理回退策略。

## 数据文件说明

- `data/database.json`：历史数据库（导出时仅追加新条目）
- `data/Prefix.bib`：导出时写入到文件头的 BibTeX 模板
- `data/mybibliography.bib` / `data/test.bib`：示例或测试用 BibTeX 文件

## 测试

```bash
pytest
```

当前仓库包含 `tests/test_gui_automation.py`，覆盖了 alias 处理、导出行为和异常输入等关键流程。

## 项目结构

```text
.
├─ main.py
├─ base_tab.py
├─ tab_storage.py
├─ tab_google_scholar.py
├─ tab_bibtex.py
├─ styles.py
├─ data/
│  ├─ database.json
│  ├─ Prefix.bib
│  └─ *.bib
└─ tests/
   └─ test_gui_automation.py
```

## License

如需开源发布，建议补充 `LICENSE` 文件并在此处声明许可证类型（例如 MIT）。
