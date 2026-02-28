
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter


class BibTeXTab(QWidget):
    def __init__(self, mainpage=None):
        super().__init__(mainpage)
        self.mainpage = mainpage
        self.entry_list = {}
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        btn_open_bib = QPushButton('打开文件')
        btn_open_bib.clicked.connect(self.open_file)
        layout.addWidget(btn_open_bib)

        self.listwidget_entry = QListWidget()
        self.listwidget_entry.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget_entry.customContextMenuRequested.connect(self.show_file_list_menu)
        layout.addWidget(self.listwidget_entry)
        self.listwidget_entry.currentItemChanged.connect(self.show_bibtex)
        
        # BibTeX原文显示区
        self.bibtex_display = QTextEdit()
        self.bibtex_display.setReadOnly(True)
        font = QFont()
        font.setPointSize(10)
        self.bibtex_display.setFont(font)
        self.bibtex_display.setStyleSheet('border: 1px solid #ccc; padding: 8px;')
        layout.addWidget(self.bibtex_display)

    
    def show_file_list_menu(self, pos):
        item = self.listwidget_entry.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        action_add_to_project = menu.addAction('添加到项目')
        action_edit_entry = menu.addAction('编辑条目')
        action = menu.exec_(self.listwidget_entry.mapToGlobal(pos))
        if action == action_add_to_project:
            self.add_to_project(item.text())
        elif action == action_edit_entry:
            entry = self.edit_entry(item.text())
            if entry:
                db = BibDatabase()
                db.entries = [entry]
                writer = BibTexWriter()
                bibtex_str = writer.write(db)
                QApplication.clipboard().setText(bibtex_str)

    def add_to_project(self, entry_id):
        entry = self.entry_list.get(entry_id, None)
        if entry:
            self.mainpage.project_entry[entry.get('ID', 'Unknown ID')] = entry
            self.mainpage.list_widget.addItem(entry_id)
        else:
            QMessageBox.warning(self, '错误', f'未找到条目 {entry_id}！')
    
    def edit_entry(self, entry_id):
        entry = self.entry_list.get(entry_id, None)
        if not entry:
            QMessageBox.warning(self, '错误', f'未找到条目 {entry_id}！')
            return None

        dialog = QDialog(self)
        dialog.setWindowTitle('编辑条目')
        dialog.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        db = BibDatabase()
        db.entries = [entry]
        writer = BibTexWriter()
        bibtex_str = writer.write(db)
        text_edit.setPlainText(bibtex_str)
        layout.addWidget(text_edit)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton('保存')
        btn_close = QPushButton('关闭')
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

        def save_entry():
            entry_text = text_edit.toPlainText()
            parsed = bibtexparser.loads(entry_text)
            new_entry = parsed.entries[0] if parsed.entries else None
            new_id = new_entry.get('ID', 'Unknown ID') if new_entry else 'Unknown ID'
            if new_id == '':
                QMessageBox.warning(dialog, '错误', '条目必须包含 ID 字段！')
                return
            elif new_id in self.entry_list and new_id != entry_id:
                QMessageBox.warning(dialog, '错误', f'ID {new_id} 已存在！')
                return
            elif new_id != entry_id:
                # ID 发生变化，更新列表和字典
                self.listwidget_entry.currentItem().setText(new_id)
                del self.entry_list[entry_id]
                
            self.entry_list[new_id] = new_entry
            dialog.accept()

        btn_save.clicked.connect(save_entry)
        btn_close.clicked.connect(dialog.reject)

        dialog.exec_()
        self.show_bibtex(self.listwidget_entry.currentItem(), None)
        #return self.entry_list.get(new_id, None)
        
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

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择 BibTeX 文件", "", "BibTeX Files (*.bib);;All Files (*)", options=options)
        if file_name:            
            with open(file_name, 'r', encoding='utf-8') as f:
                bibtex_str = f.read()
                parsed = bibtexparser.loads(bibtex_str)
                entries = parsed.entries
                for entry in entries:
                    self.entry_list[entry.get('ID', 'Unknown ID')] = entry
                    self.listwidget_entry.addItem(f"{entry.get('ID', 'Unknown ID')}")