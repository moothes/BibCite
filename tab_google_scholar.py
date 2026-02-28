from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel
from PyQt5.QtGui import QFont
from scholarly import scholarly
import bibtexparser

class GoogleScholarTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.list = QListWidget()
        self.list.setFont(label_font)
        layout.addWidget(self.list)

        # 信息显示区
        self.info = QLabel('请选择上方列表项')
        self.info.setFont(label_font)
        self.info.setStyleSheet('border: 1px solid #ccc; padding: 8px;')
        layout.addWidget(self.info)

        # 信号连接
        self.btn.clicked.connect(self.search_from_google_scholar)
        self.list.currentItemChanged.connect(self.update_info)

    def search_from_google_scholar(self):
        self.list.clear()
        query = scholarly.search_pubs(self.input.text())
        max_item = 3
        current_item = 0
        for pub in query:
            bibtex = scholarly.bibtex(pub)
            parsed = bibtexparser.loads(bibtex)
            result = parsed.entries[0] if parsed.entries else {}
            self.list.addItem(f"{result.get('title', 'Unknown Title')} - {result.get('author', 'Unknown Author')}")
            current_item += 1
            if current_item >= max_item:
                break

    def update_info(self, current, previous):
        if current:
            self.info.setText(f'当前选中：{current.text()} 的详细信息')
        else:
            self.info.setText('请选择上方列表项')
