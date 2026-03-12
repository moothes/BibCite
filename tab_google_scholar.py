from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal
from scholarly import scholarly, ProxyGenerator
import bibtexparser
import os
from base_tab import BaseTab
from styles import *


class SearchWorker(QThread):
    """Google Scholar 搜索工作线程"""
    search_finished = pyqtSignal(list)  # 搜索完成信号，传递结果列表
    search_error = pyqtSignal(str)  # 搜索错误信号，传递错误信息
    
    def __init__(self, query_text, max_results=3):
        super().__init__()
        self.query_text = query_text
        self.max_results = max_results

    def _fetch_results(self):
        results = []
        query = scholarly.search_pubs(self.query_text)
        current_item = 0
        for pub in query[:5]:
            bibtex = scholarly.bibtex(pub)
            parsed = bibtexparser.loads(bibtex)
            entry = parsed.entries[0] if parsed.entries else {}
            results.append(entry)
            current_item += 1
            if current_item >= self.max_results:
                break
        return results

    def _try_proxy_fallback(self):
        # 1) 优先使用环境变量代理（如果用户已配置）
        http_proxy = os.getenv('SCHOLAR_HTTP_PROXY') or os.getenv('HTTP_PROXY') or os.getenv('http_proxy')
        https_proxy = os.getenv('SCHOLAR_HTTPS_PROXY') or os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')

        if http_proxy or https_proxy:
            pg = ProxyGenerator()
            try:
                if hasattr(pg, 'SingleProxy'):
                    success = pg.SingleProxy(http=http_proxy, https=https_proxy)
                    if success:
                        scholarly.use_proxy(pg)
                        return self._fetch_results()
            except Exception:
                pass

        # 2) 使用 scholarly 的免费代理池
        pg = ProxyGenerator()
        if hasattr(pg, 'FreeProxies'):
            success = pg.FreeProxies()
            if success:
                scholarly.use_proxy(pg)
                return self._fetch_results()

        raise RuntimeError('普通搜索失败，且代理搜索不可用')
    
    def run(self):
        """在线程中执行搜索"""
        try:
            results = self._fetch_results()
            self.search_finished.emit(results)
        except Exception as e:
            try:
                results = self._try_proxy_fallback()
                self.search_finished.emit(results)
            except Exception as fallback_error:
                self.search_error.emit(f'{e}; 代理重试失败: {fallback_error}')


class GoogleScholarTab(BaseTab):
    def __init__(self, mainpage=None):
        super().__init__(mainpage)
        self.search_worker = None  # 搜索工作线程
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        label_font = QFont()
        label_font.setPointSize(10)

        # 搜索标签
        search_label = QLabel('🎓 Search Google Scholar')
        search_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        search_label.setStyleSheet('color: #2d3e38; margin-bottom: 4px;')
        layout.addWidget(search_label)

        # 输入区
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        self.input = QLineEdit()
        self.input.setFont(label_font)
        self.input.setPlaceholderText('Enter search query...')
        self.input.returnPressed.connect(self.search_from_google_scholar)
        self.input.setMinimumHeight(36)
        self.input.setStyleSheet(INPUT_STYLE)
        
        self.btn = QPushButton('Search')
        self.btn.setFont(label_font)
        self.btn.setMinimumHeight(36)
        self.btn.setMinimumWidth(100)
        self.btn.setStyleSheet(BUTTON_PRIMARY_STYLE)
        
        input_layout.addWidget(self.input, 1)
        input_layout.addWidget(self.btn)
        layout.addLayout(input_layout)
        
        # 状态标签
        self.status_label = QLabel('')
        self.status_label.setFont(label_font)
        self.status_label.setStyleSheet(LABEL_STATUS_STYLE)
        self.status_label.setMinimumHeight(32)
        layout.addWidget(self.status_label)

        # 结果列表
        self.listwidget_entry = QListWidget()
        self.listwidget_entry.setFont(label_font)
        self.listwidget_entry.setStyleSheet(LISTWIDGET_STYLE)
        self.setup_list_widget()
        layout.addWidget(self.listwidget_entry)

        # 信息显示区
        self.bibtex_display = self.setup_bibtex_display()
        self.bibtex_display.setPlainText('Please select an entry to view details')
        self.bibtex_display.setStyleSheet(TEXTEDIT_STYLE)
        layout.addWidget(self.bibtex_display)

        # 信号连接
        self.btn.clicked.connect(self.search_from_google_scholar)

    def search_from_google_scholar(self):
        """启动搜索（在新线程中执行）"""
        query_text = self.input.text().strip()
        if not query_text:
            self.status_label.setText('Please enter search keywords')
            return
        
        # 如果已有线程在运行，先停止
        if self.search_worker and self.search_worker.isRunning():
            self.search_worker.terminate()
            self.search_worker.wait()
        
        # 清空当前结果
        self.listwidget_entry.clear()
        self.entry_list.clear()
        self.bibtex_display.setPlainText('Searching...')
        
        # 禁用搜索按钮，防止重复点击
        self.btn.setEnabled(False)
        self.input.setEnabled(False)
        self.status_label.setText('Searching...')
        
        # 创建并启动工作线程
        self.search_worker = SearchWorker(query_text, max_results=3)
        self.search_worker.search_finished.connect(self.on_search_finished)
        self.search_worker.search_error.connect(self.on_search_error)
        self.search_worker.start()
    
    def on_search_finished(self, results):
        """搜索完成，处理结果"""
        # 启用搜索按钮
        self.btn.setEnabled(True)
        self.input.setEnabled(True)
        
        if not results:
            self.status_label.setText('No results found')
            self.bibtex_display.setPlainText('No results found')
            return
        
        # 显示结果
        for entry in results:
            entry_id = self.get_entry_id(entry)
            self.entry_list[entry_id] = entry
            self.listwidget_entry.addItem(entry_id)
        
        self.status_label.setText(f'Found {len(results)} results')
        self.bibtex_display.setPlainText('Please select an entry to view details')
    
    def on_search_error(self, error_msg):
        """搜索出错，显示错误信息"""
        # 启用搜索按钮
        self.btn.setEnabled(True)
        self.input.setEnabled(True)
        
        self.status_label.setText(f'Search error: {error_msg}')
        self.bibtex_display.setPlainText(f'Error: {error_msg}')
