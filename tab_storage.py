from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class StorageTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label_font = QFont()
        label_font.setPointSize(10)
        label = QLabel('Storage 区域内容')
        label.setFont(label_font)
        layout.addWidget(label)
