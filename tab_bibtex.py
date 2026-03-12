
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import bibtexparser
from base_tab import BaseTab
from styles import *


class BibTeXTab(BaseTab):
    def __init__(self, mainpage=None):
        super().__init__(mainpage)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 标题标签
        title_label = QLabel('📚 Import BibTeX File')
        title_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        title_label.setStyleSheet('color: #2d3e38; margin-bottom: 4px;')
        layout.addWidget(title_label)

        # 文件选择区域
        top_row_layout = QHBoxLayout()
        top_row_layout.setSpacing(8)
        
        self.label_bib_path = QLabel('No file selected')
        self.label_bib_path.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.label_bib_path.setFont(QFont('Segoe UI', 10))
        self.label_bib_path.setStyleSheet(LABEL_INFO_STYLE)
        top_row_layout.addWidget(self.label_bib_path, 1)

        btn_open_bib = QPushButton('📂  Open BibTeX File')
        btn_open_bib.setFont(QFont('Segoe UI', 10, QFont.Bold))
        btn_open_bib.clicked.connect(self.open_file)
        btn_open_bib.setMinimumHeight(36)
        btn_open_bib.setMinimumWidth(160)
        btn_open_bib.setStyleSheet(BUTTON_PRIMARY_STYLE)
        top_row_layout.addWidget(btn_open_bib)
        layout.addLayout(top_row_layout)

        # 列表控件
        self.listwidget_entry = QListWidget()
        self.listwidget_entry.setFont(QFont('Segoe UI', 10))
        self.listwidget_entry.setStyleSheet(LISTWIDGET_STYLE)
        self.setup_list_widget()
        layout.addWidget(self.listwidget_entry)
        
        # BibTeX原文显示区
        bibtex_display = self.setup_bibtex_display()
        bibtex_display.setStyleSheet(TEXTEDIT_STYLE)
        layout.addWidget(bibtex_display)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择 BibTeX 文件", "", "BibTeX Files (*.bib);;All Files (*)", options=options)
        if file_name:
            self.label_bib_path.setText(file_name)
            with open(file_name, 'r', encoding='utf-8') as f:
                bibtex_str = f.read()
                parsed = bibtexparser.loads(bibtex_str)
                entries = parsed.entries
                for entry in entries:
                    if entry.get('ID', 'Unknown ID') in self.mainpage.project_entry.keys():
                        continue
                    self.entry_list[entry.get('ID', 'Unknown ID')] = entry
                    self.listwidget_entry.addItem(f"{entry.get('ID', 'Unknown ID')}")