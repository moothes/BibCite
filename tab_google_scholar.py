from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QTextEdit, QMenu, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from scholarly import scholarly
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

class GoogleScholarTab(QWidget):
    def __init__(self, mainpage=None):
        super().__init__(mainpage)
        self.mainpage = mainpage
        self.search_list = {}
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label_font = QFont()
        label_font.setPointSize(10)

        # 输入区
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setFont(label_font)
        self.btn = QPushButton('搜索')
        self.btn.setFont(label_font)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.btn)
        layout.addLayout(input_layout)

        # 结果列表
        self.listwidget_entry = QListWidget()
        self.listwidget_entry.setFont(label_font)
        self.listwidget_entry.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget_entry.customContextMenuRequested.connect(self.show_file_list_menu)
        self.listwidget_entry.currentItemChanged.connect(self.update_info)
        self.listwidget_entry.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.listwidget_entry)

        # 信息显示区
        self.info = QTextEdit('请输入关键词搜索')
        self.info.setReadOnly(True)
        self.info.setFont(label_font)
        self.info.setStyleSheet('border: 1px solid #ccc; padding: 8px;')
        layout.addWidget(self.info)

        # 信号连接
        self.btn.clicked.connect(self.search_from_google_scholar)

    def on_item_double_clicked(self, item):
        entry_id = item.text()
        self.add_to_project(entry_id)
        
    def show_file_list_menu(self, pos):
        item = self.listwidget_entry.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        action_add_to_project = menu.addAction('添加到项目')
        #action_edit_entry = menu.addAction('编辑条目')
        action = menu.exec_(self.listwidget_entry.mapToGlobal(pos))
        if action == action_add_to_project:
            self.add_to_project(item.text())

    def add_to_project(self, entry_id):
        entry = self.search_list.get(entry_id, None)
        if entry:
            self.mainpage.project_entry[entry.get('ID', 'Unknown ID')] = entry
            self.mainpage.list_widget.addItem(entry_id)
        else:
            QMessageBox.warning(self, '错误', f'未找到条目 {entry_id}！')

    def search_from_google_scholar(self):
        self.listwidget_entry.clear()
        query = scholarly.search_pubs(self.input.text())
        
        max_item = 3
        current_item = 0
        for pub in query:
            bibtex = scholarly.bibtex(pub)
            parsed = bibtexparser.loads(bibtex)
            entry = parsed.entries[0] if parsed.entries else {}
            
            self.search_list[entry.get('ID', 'Unknown ID')] = entry
            self.listwidget_entry.addItem(f"{entry.get('ID', 'Unknown ID')}")
            current_item += 1
            if current_item >= max_item:
                break

    def update_info(self, current, previous):
        if current:
            entry = self.search_list.get(current.text(), None)
            if entry:
                db = BibDatabase()
                db.entries = [entry]
                writer = BibTexWriter()
                bibtex_str = writer.write(db)
                #QApplication.clipboard().setText(bibtex_str)
            
                self.info.setText(bibtex_str)
        else:
            self.info.setText('请选择上方列表项')
