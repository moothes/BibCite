
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from base_tab import BaseTab
from styles import *

import os
import json

class StorageTab(BaseTab):
    def __init__(self, mainpage=None):
        super().__init__(mainpage)
        self.entry_list = mainpage.database
        self.init_ui()

    def _entry_matches_keyword(self, entry, keyword):
        """在 title、alias、author 三个字段中进行关键字匹配。"""
        title = str(entry.get('title', ''))
        author = str(entry.get('author', ''))

        raw_alias = entry.get('alias', [])
        if isinstance(raw_alias, list):
            alias_text = ';'.join(str(a) for a in raw_alias)
        else:
            alias_text = str(raw_alias or '')

        haystack = ' '.join([title, author, alias_text]).lower()
        return keyword.lower() in haystack

    def refresh_list(self, keyword=''):
        """根据关键字刷新列表；关键字为空时显示全部。"""
        self.listwidget_entry.clear()
        clean_keyword = keyword.strip()

        for entry_id, entry in self.entry_list.items():
            if not clean_keyword or self._entry_matches_keyword(entry, clean_keyword):
                self.listwidget_entry.addItem(entry_id)

    def search_entries(self):
        """触发关键字搜索。"""
        self.refresh_list(self.input.text())

    def clear_search(self):
        """清空搜索输入并恢复全部条目。"""
        self.input.clear()
        self.refresh_list()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # 搜索标签
        search_label = QLabel('🔍 Search in Storage')
        search_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        search_label.setStyleSheet('color: #2d3e38; margin-bottom: 4px;')
        layout.addWidget(search_label)
        
        # 输入区
        label_font = QFont()
        label_font.setPointSize(10)
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        self.input = QLineEdit()
        self.input.setFont(label_font)
        self.input.setPlaceholderText('Search by title, author, or alias...')
        self.input.returnPressed.connect(self.search_entries)
        self.input.setMinimumHeight(36)
        self.input.setStyleSheet(INPUT_STYLE)
        
        self.btn = QPushButton('Search')
        self.btn.setFont(label_font)
        self.btn.clicked.connect(self.search_entries)
        self.btn.setMinimumHeight(36)
        self.btn.setMinimumWidth(100)
        self.btn.setStyleSheet(BUTTON_PRIMARY_STYLE)
        
        self.btn_clear = QPushButton('Clear')
        self.btn_clear.setFont(label_font)
        self.btn_clear.clicked.connect(self.clear_search)
        self.btn_clear.setMinimumHeight(36)
        self.btn_clear.setMinimumWidth(100)
        self.btn_clear.setStyleSheet(BUTTON_SECONDARY_STYLE)
        
        input_layout.addWidget(self.input, 1)
        input_layout.addWidget(self.btn)
        input_layout.addWidget(self.btn_clear)
        layout.addLayout(input_layout)

        # 列表控件
        self.listwidget_entry = QListWidget()
        self.listwidget_entry.setFont(label_font)
        self.listwidget_entry.setStyleSheet(LISTWIDGET_STYLE)
        self.setup_list_widget()
        self.refresh_list()
        
        layout.addWidget(self.listwidget_entry)
        
        # BibTeX原文显示区
        bibtex_display = self.setup_bibtex_display()
        bibtex_display.setStyleSheet(TEXTEDIT_STYLE)
        layout.addWidget(bibtex_display)
