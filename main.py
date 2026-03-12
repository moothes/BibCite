import os
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QPainter, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QModelIndex, QSize, QRect

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

# 导入样式
from styles import *

# 这里导入各个界面
from tab_google_scholar import GoogleScholarTab
from tab_storage import StorageTab
from tab_bibtex import BibTeXTab


class EntryCardDelegate(QStyledItemDelegate):
	def paint(self, painter, option, index):
		title = index.data(Qt.DisplayRole) or ''
		subtitle = index.data(Qt.UserRole + 1) or 'No aliases'
		selected = bool(option.state & QStyle.State_Selected)
		hovered = bool(option.state & QStyle.State_MouseOver)

		card_rect = option.rect.adjusted(6, 4, -6, -4)
		if selected:
			bg_color = QColor('#2f7d65')
			border_color = QColor('#2a705b')
			title_color = QColor('#ffffff')
			subtitle_color = QColor('#e5f2ee')
		elif hovered:
			bg_color = QColor('#eff7f4')
			border_color = QColor('#d2e7df')
			title_color = QColor('#1f2d28')
			subtitle_color = QColor('#587168')
		else:
			bg_color = QColor('#f7faf9')
			border_color = QColor('#dce7e3')
			title_color = QColor('#1f2d28')
			subtitle_color = QColor('#6a7f77')

		painter.save()
		painter.setRenderHint(QPainter.Antialiasing, True)
		painter.setPen(border_color)
		painter.setBrush(bg_color)
		painter.drawRoundedRect(card_rect, 8, 8)

		inner_rect = card_rect.adjusted(12, 8, -12, -8)

		title_font = QFont(option.font)
		title_font.setPointSize(max(9, option.font.pointSize()))
		title_font.setBold(True)
		title_metrics = QFontMetrics(title_font)
		title_height = title_metrics.height()

		subtitle_font = QFont(option.font)
		subtitle_font.setPointSize(max(8, option.font.pointSize() - 1))
		subtitle_metrics = QFontMetrics(subtitle_font)
		subtitle_height = subtitle_metrics.height()

		line_gap = 1
		content_height = title_height + line_gap + subtitle_height
		start_y = inner_rect.top() + max(0, (inner_rect.height() - content_height) // 2)

		title_rect = QRect(inner_rect.left(), start_y, inner_rect.width(), title_height)
		subtitle_rect = QRect(inner_rect.left(), start_y + title_height + line_gap, inner_rect.width(), subtitle_height)

		painter.setFont(title_font)
		painter.setPen(title_color)
		title_text = painter.fontMetrics().elidedText(title, Qt.ElideRight, title_rect.width())
		painter.drawText(title_rect, Qt.AlignLeft | Qt.AlignVCenter, title_text)

		painter.setFont(subtitle_font)
		painter.setPen(subtitle_color)
		subtitle_text = painter.fontMetrics().elidedText(subtitle, Qt.ElideRight, subtitle_rect.width())
		painter.drawText(subtitle_rect, Qt.AlignLeft | Qt.AlignVCenter, subtitle_text)
		painter.restore()

	def sizeHint(self, option, index):
		return QSize(0, 90)

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.project_entry = {}

		self.database_path = 'data/database.json'
		if os.path.exists(self.database_path):
			with open(self.database_path, 'r') as f:
				self.database = json.load(f)
		else:
			self.database = {}
		self.initial_database_ids = set(self.database.keys())

		for entry in self.database.values():
			self.ensure_alias_list(entry)

		self.init_ui()
		
		# 设置 QMessageBox 全局样式
		QApplication.instance().setStyleSheet(QApplication.instance().styleSheet() + MESSAGEBOX_STYLE)

	def format_bibtex(self, entry):
		"""将条目格式化为 BibTeX 字符串"""
		if not entry:
			return ''
		serializable_entry = dict(entry)
		# alias 用于应用内部管理，不写入 BibTeX 正文字段。
		serializable_entry.pop('alias', None)
		db = BibDatabase()
		db.entries = [serializable_entry]
		writer = BibTexWriter()
		return writer.write(db)

	def normalize_aliases(self, aliases):
		"""将 alias 统一为字符串列表，支持 list 或分隔字符串输入。"""
		if aliases is None:
			return []
		if isinstance(aliases, str):
			raw_items = aliases.replace(';', ',').split(',')
		elif isinstance(aliases, list):
			raw_items = aliases
		else:
			return []

		normalized = []
		seen = set()
		for item in raw_items:
			alias = str(item).strip()
			if alias and alias not in seen:
				normalized.append(alias)
				seen.add(alias)
		return normalized

	def ensure_alias_list(self, entry):
		"""确保 entry 中始终包含 alias 列表字段。"""
		entry['alias'] = self.normalize_aliases(entry.get('alias', []))

	def format_entry_list_item(self, entry_id, entry):
		"""生成左侧列表显示文本：ID (alias1;alias2)。"""
		self.ensure_alias_list(entry)
		alias = entry.get('alias', [])
		alias_str = f" ({';'.join(alias)})" if alias else ''
		return f"{entry_id}{alias_str}"

	def extract_entry_id_from_item_text(self, text):
		"""从列表项显示文本中提取真实 entry ID。"""
		return text.split(' (', 1)[0].strip()

	def refresh_entry_list(self, select_id=None):
		"""刷新左侧条目列表，可选择指定条目"""
		self.list_model.clear()
		entry_list = list(self.project_entry.keys())
		for entry_name, value in self.project_entry.items():
			self.ensure_alias_list(value)
			alias_text = '; '.join(value.get('alias', [])) if value.get('alias', []) else 'No aliases'
			item = QStandardItem(entry_name)
			item.setData(entry_name, Qt.UserRole)
			item.setData(alias_text, Qt.UserRole + 1)
			self.list_model.appendRow(item)
		
		# 如果指定了要选择的条目，则选中它
		if select_id and select_id in entry_list:
			index = entry_list.index(select_id)
			model_index = self.list_model.index(index, 0)
			self.list_widget.setCurrentIndex(model_index)

	def save_database(self):
		"""仅在导出时追加历史库中不存在的新条目。"""
		for entry in self.database.values():
			self.ensure_alias_list(entry)
		for entry in self.project_entry.values():
			self.ensure_alias_list(entry)

		for entry_id, entry in self.project_entry.items():
			if entry_id not in self.initial_database_ids and entry_id not in self.database:
				self.database[entry_id] = entry
				self.initial_database_ids.add(entry_id)

		with open(self.database_path, 'w', encoding='utf-8') as f:
			json.dump(self.database, f, indent=4)

	def create_font(self, size):
		"""创建指定大小的字体"""
		font = QFont()
		font.setPointSize(size)
		return font

	def init_ui(self):
		self.setWindowTitle('BibCite for Windows')
		self.resize(1800, 1400)
		self.setStyleSheet(MAIN_WINDOW_STYLE)

		# 主水平布局
		main_layout = QHBoxLayout(self)
		main_layout.setSpacing(12)
		main_layout.setContentsMargins(12, 12, 12, 12)

		# 菜单栏
		menu_bar = self.create_main_menu()
		main_layout.setMenuBar(menu_bar)

		left_widget = self.create_main_panel()
		main_layout.addWidget(left_widget, 3)

		# 右侧Tab
		self.info_source_tabs = QTabWidget()
		self.info_source_tabs.setFont(self.create_font(10))
		self.info_source_tabs.addTab(StorageTab(self), 'Storage')
		self.info_source_tabs.addTab(GoogleScholarTab(self), 'Google Scholar')
		self.info_source_tabs.addTab(BibTeXTab(self), 'BibTeX')
		main_layout.addWidget(self.info_source_tabs, 2)

	def create_main_menu(self):
		menu_bar = QMenuBar(self)
		menu_bar.setFont(self.create_font(10))
		
		# Project 菜单
		project_menu = menu_bar.addMenu('📁 Project')
		project_menu.setFont(self.create_font(10))

		create_empty_action = QAction('🆕  New Project', self)
		create_empty_action.setShortcut('Ctrl+N')
		create_empty_action.triggered.connect(self.create_empty_project)
		project_menu.addAction(create_empty_action)

		from_template_action = QAction('📄  Open BibTeX File', self)
		from_template_action.setShortcut('Ctrl+O')
		from_template_action.triggered.connect(self.open_bibtex_file)
		project_menu.addAction(from_template_action)
		
		project_menu.addSeparator()

		exit_action = QAction('🚪  Exit', self)
		exit_action.setShortcut('Ctrl+Q')
		exit_action.triggered.connect(self.close)
		project_menu.addAction(exit_action)

		return menu_bar

	def create_empty_project(self):
		self.project_entry = {}
		self.list_model.clear()
				
	def open_bibtex_file(self):
		self.project_entry = {}
		file_path, _ = QFileDialog.getOpenFileName(self, 'Open BibTeX File', '', 'BibTeX Files (*.bib);;All Files (*)')
		if file_path:
			with open(file_path, 'r', encoding='utf-8') as f:
				bibtex_str = f.read()
				bib_database = bibtexparser.loads(bibtex_str)
				for entry in bib_database.entries:
					self.ensure_alias_list(entry)
					self.project_entry[entry['ID']] = entry
			self.refresh_entry_list()
		
	def create_main_panel(self):
		left_layout = QVBoxLayout()

		# 顶部按钮区
		button_layout = QHBoxLayout()
		button_layout.setSpacing(8)
		btn_font = self.create_font(11)
		
		self.btn_add_entry = QPushButton('+ New Entry')
		self.btn_add_entry.clicked.connect(self.add_entry)
		self.btn_add_entry.setFont(btn_font)
		self.btn_add_entry.setMinimumHeight(40)
		self.btn_add_entry.setStyleSheet(BUTTON_PRIMARY_STYLE)
		
		self.btn_export = QPushButton('Export')
		self.btn_export.clicked.connect(self.export_bibtex)
		self.btn_export.setFont(btn_font)
		self.btn_export.setMinimumHeight(40)
		self.btn_export.setStyleSheet(BUTTON_SECONDARY_STYLE)
		
		button_layout.addWidget(self.btn_add_entry)
		button_layout.addWidget(self.btn_export)
		left_layout.addLayout(button_layout)

		# 列表
		self.list_widget = QListView()
		self.list_model = QStandardItemModel(self.list_widget)
		self.list_widget.setFont(self.create_font(10))
		self.list_widget.setModel(self.list_model)
		self.list_widget.setItemDelegate(EntryCardDelegate(self.list_widget))
		self.list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
		self.list_widget.setMouseTracking(True)
		self.list_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.list_widget.setSpacing(4)
		self.list_widget.setStyleSheet(LISTVIEW_STYLE)
		self.list_widget.selectionModel().currentChanged.connect(self.update_info_label)
		self.list_widget.doubleClicked.connect(self.on_entry_double_clicked)
		self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.list_widget.customContextMenuRequested.connect(self.show_file_list_menu)
		left_layout.addWidget(self.list_widget, 3)

		# 信息显示区
		self.bibtex_display = QTextEdit('Please select an entry to view details')
		self.bibtex_display.setReadOnly(True)
		self.bibtex_display.setFont(self.create_font(10))
		self.bibtex_display.setStyleSheet(TEXTEDIT_STYLE)
		left_layout.addWidget(self.bibtex_display, 2)

		# 左侧容器
		left_widget = QWidget()
		left_widget.setLayout(left_layout)
		left_widget.setStyleSheet("""
			QWidget {
				background-color: transparent;
			}
		""")
		return left_widget

	def on_entry_double_clicked(self, index):
		"""双击列表项时编辑条目"""
		if not index.isValid():
			return
		entry_id = index.data(Qt.UserRole)
		if entry_id:
			self.edit_entry(entry_id)

	def show_file_list_menu(self, pos):
		index = self.list_widget.indexAt(pos)
		if not index.isValid():
			return
		entry_id = index.data(Qt.UserRole)

		menu = QMenu(self)
		menu.setStyleSheet(CONTEXT_MENU_STYLE)
		action_edit_entry = menu.addAction('✏️  Edit entry')
		action_add_alias = menu.addAction('🏷️  Add alias')
		action_remove_entry = menu.addAction('🗑️  Delete entry')
		action = menu.exec_(self.list_widget.mapToGlobal(pos))
		if action == action_remove_entry:
			self.remove_entry(entry_id)
		if action == action_add_alias:
			self.add_alias(entry_id)
		elif action == action_edit_entry:
			self.edit_entry(entry_id)

	def remove_entry(self, entry_id):
		if entry_id in self.project_entry:
			del self.project_entry[entry_id]
			self.refresh_entry_list()

	def validate_and_save_entry(self, text_edit, dialog, original_id=None):
		"""验证并保存条目，original_id 为 None 表示新增，否则为编辑"""
		entry_text = text_edit.toPlainText()
		try:
			parsed = bibtexparser.loads(entry_text)
		except Exception as e:
			QMessageBox.warning(dialog, '错误', f'BibTeX 解析失败: {e}')
			return

		if not parsed.entries:
			QMessageBox.warning(dialog, '错误', '未检测到有效 BibTeX 条目，请检查输入内容。')
			return

		new_entry = parsed.entries[0] if parsed.entries else None
		new_id = new_entry.get('ID', 'Unknown ID') if new_entry else 'Unknown ID'
		
		# 验证 ID
		if new_id in ('', 'Unknown ID'):
			QMessageBox.warning(dialog, '错误', '条目必须包含 ID 字段！')
			return
		
		# 编辑时先缓存 alias，避免 ID 变化时被删除旧条目后丢失
		existing_alias = []
		if original_id and original_id in self.project_entry:
			existing_alias = self.normalize_aliases(self.project_entry[original_id].get('alias', []))
		elif new_id in self.project_entry:
			existing_alias = self.normalize_aliases(self.project_entry[new_id].get('alias', []))

		# 检查 ID 冲突
		if original_id is None:  # 新增模式
			if new_id in self.project_entry:
				QMessageBox.warning(dialog, '错误', f'ID {new_id} 已存在！')
				return
		else:  # 编辑模式
			if new_id in self.project_entry and new_id != original_id:
				QMessageBox.warning(dialog, '错误', f'ID {new_id} 已存在！')
				return
			if new_id != original_id:
				# ID 发生变化，删除旧条目
				del self.project_entry[original_id]

		# 保存条目
		new_entry['alias'] = existing_alias
		self.project_entry[new_id] = new_entry
		
		# 更新界面
		self.refresh_entry_list(select_id=new_id)
		
		dialog.accept()

	def create_entry_dialog(self, title, initial_text='', save_callback=None):
		"""创建通用的条目编辑对话框"""
		dialog = QDialog(self)
		dialog.setWindowTitle(title)
		dialog.setGeometry(100, 100, 700, 500)
		dialog.setStyleSheet(DIALOG_STYLE)

		layout = QVBoxLayout(dialog)
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setSpacing(15)

		# 标题标签
		title_label = QLabel('BibTeX Entry Content:')
		layout.addWidget(title_label)

		# 文本编辑区
		text_edit = QTextEdit()
		text_edit.setPlainText(initial_text)
		text_edit.setFont(self.create_font(10))
		text_edit.setStyleSheet(TEXTEDIT_DIALOG_STYLE)
		layout.addWidget(text_edit)

		# 按钮布局
		btn_layout = QHBoxLayout()
		btn_layout.addStretch()
		
		btn_close = QPushButton('Close' if 'Add' in title else '关闭')
		btn_close.setFont(self.create_font(10))
		btn_close.setMinimumSize(100, 36)
		btn_close.setStyleSheet(BUTTON_DIALOG_CANCEL_STYLE)
		
		btn_save = QPushButton('Save' if 'Add' in title else '保存')
		btn_save.setFont(self.create_font(10))
		btn_save.setMinimumSize(100, 36)
		btn_save.setStyleSheet(BUTTON_DIALOG_OK_STYLE)
		
		btn_layout.addWidget(btn_close)
		btn_layout.addWidget(btn_save)
		layout.addLayout(btn_layout)

		if save_callback:
			btn_save.clicked.connect(lambda: save_callback(text_edit, dialog))
		btn_close.clicked.connect(dialog.reject)

		return dialog

	def add_entry(self):
		dialog = self.create_entry_dialog(
			'Add entry',
			save_callback=lambda text_edit, dlg: self.validate_and_save_entry(text_edit, dlg, original_id=None)
		)
		dialog.exec_()

	def add_alias(self, entry_id):
		entry = self.project_entry.get(entry_id)
		if not entry:
			QMessageBox.warning(self, '错误', f'未找到条目 {entry_id}！')
			return

		current_aliases = self.normalize_aliases(entry.get('alias', []))
		default_text = ';'.join(current_aliases)
		
		# 创建自定义输入对话框
		dialog = QDialog(self)
		dialog.setWindowTitle('Add Alias')
		dialog.setFixedSize(500, 180)
		dialog.setStyleSheet(DIALOG_STYLE + INPUT_DIALOG_STYLE + DIALOG_LABEL_STYLE)
		
		layout = QVBoxLayout(dialog)
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setSpacing(12)
		
		label = QLabel('Enter aliases (separate multiple with commas or semicolons):')
		layout.addWidget(label)
		
		line_edit = QLineEdit(default_text)
		line_edit.setFont(self.create_font(10))
		layout.addWidget(line_edit)
		
		btn_layout = QHBoxLayout()
		btn_layout.addStretch()
		
		btn_cancel = QPushButton('Cancel')
		btn_cancel.setFont(self.create_font(10))
		btn_cancel.setMinimumSize(80, 32)
		btn_cancel.setStyleSheet(BUTTON_DIALOG_CANCEL_STYLE)
		btn_cancel.clicked.connect(dialog.reject)
		
		btn_ok = QPushButton('OK')
		btn_ok.setFont(self.create_font(10))
		btn_ok.setMinimumSize(80, 32)
		btn_ok.setStyleSheet(BUTTON_DIALOG_OK_STYLE)
		btn_ok.clicked.connect(dialog.accept)
		
		btn_layout.addWidget(btn_cancel)
		btn_layout.addWidget(btn_ok)
		layout.addLayout(btn_layout)
		
		if dialog.exec_() == QDialog.Accepted:
			text = line_edit.text()
			entry['alias'] = self.normalize_aliases(text)
			self.refresh_entry_list(select_id=entry_id)
			self.update_info_label(self.list_widget.currentIndex(), QModelIndex())

	def edit_entry(self, entry_id):
		entry = self.project_entry.get(entry_id, None)
		if not entry:
			QMessageBox.warning(self, '错误', f'未找到条目 {entry_id}！')
			return None

		dialog = self.create_entry_dialog(
			'Edit entry',
			initial_text=self.format_bibtex(entry),
			save_callback=lambda text_edit, dlg: self.validate_and_save_entry(text_edit, dlg, original_id=entry_id)
		)
		dialog.exec_()
		self.update_info_label(self.list_widget.currentIndex(), QModelIndex())
        
	def update_info_label(self, current, previous):
		if current and current.isValid():
			entry_id = current.data(Qt.UserRole)
			entry = self.project_entry.get(entry_id, None)
			self.bibtex_display.setPlainText(self.format_bibtex(entry))
		else:
			self.bibtex_display.setPlainText('')

	def export_bibtex(self):
		file_path, _ = QFileDialog.getSaveFileName(self, '导出 BibTeX 文件', '', 'BibTeX Files (*.bib)')
		if file_path:
			with open('data/Prefix.bib', 'r') as f:
				prefix_content = f.read()
			
			with open(file_path, 'w', encoding='utf-8') as f:
				f.write(prefix_content)
				for entry in self.project_entry.values():
					f.write(self.format_bibtex(entry))

		self.save_database()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
