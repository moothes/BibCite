
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import os
import json
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

class StorageTab(QWidget):
    def __init__(self, mainpage=None):
        super().__init__(mainpage)
        self.mainpage = mainpage
        self.entry_list = mainpage.database

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 输入区
        label_font = QFont()
        label_font.setPointSize(10)
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setFont(label_font)
        self.btn = QPushButton('Search')
        self.btn.setFont(label_font)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.btn)
        layout.addLayout(input_layout)

        self.listwidget_entry = QListWidget()
        self.listwidget_entry.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget_entry.customContextMenuRequested.connect(self.show_file_list_menu)
        self.listwidget_entry.currentItemChanged.connect(self.show_bibtex)
        self.listwidget_entry.itemDoubleClicked.connect(self.on_item_double_clicked)
        for entry_id, entry in self.entry_list.items():
            self.listwidget_entry.addItem(entry_id)
        
        layout.addWidget(self.listwidget_entry)
        
        # BibTeX原文显示区
        self.bibtex_display = QTextEdit()
        self.bibtex_display.setReadOnly(True)
        font = QFont()
        font.setPointSize(10)
        self.bibtex_display.setFont(font)
        self.bibtex_display.setStyleSheet('border: 1px solid #ccc; padding: 8px;')
        layout.addWidget(self.bibtex_display)

    def on_item_double_clicked(self, item):
        entry_id = item.text()
        self.add_to_project(entry_id)
    
    def show_file_list_menu(self, pos):
        item = self.listwidget_entry.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        action_add_to_project = menu.addAction('Add to project')
        #action_edit_entry = menu.addAction('编辑条目')
        action = menu.exec_(self.listwidget_entry.mapToGlobal(pos))
        if action == action_add_to_project:
            self.add_to_project(item.text())
        '''
        elif action == action_edit_entry:
            entry = self.edit_entry(item.text())
            if entry:
                db = BibDatabase()
                db.entries = [entry]
                writer = BibTexWriter()
                bibtex_str = writer.write(db)
                QApplication.clipboard().setText(bibtex_str)
        '''

    def add_to_project(self, entry_id):
        entry = self.entry_list.get(entry_id, None)
        if entry:
            if entry.get('ID', 'Unknown ID') in self.mainpage.project_entry.keys():
                QMessageBox.warning(self, '提示', f'条目 {entry_id} 已经在项目中！')
                return
            self.mainpage.project_entry[entry.get('ID', 'Unknown ID')] = entry
            self.mainpage.list_widget.addItem(entry_id)
        else:
            QMessageBox.warning(self, '错误', f'未找到条目 {entry_id}！')
    
    def show_bibtex(self, current, previous):
        if current:
            entry_id = current.text()
            entry = self.entry_list.get(entry_id, None)
            if entry:
                db = BibDatabase()
                db.entries = [entry]
                writer = BibTexWriter()
                bibtex_str = writer.write(db)
                self.bibtex_display.setPlainText(bibtex_str)
            else:
                self.bibtex_display.setPlainText('')
        else:
            self.bibtex_display.setPlainText('')
