import os
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

# 这里导入各个界面
from tab_google_scholar import GoogleScholarTab
from tab_storage import StorageTab
from tab_bibtex import BibTeXTab

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()

		database_path = 'data/database.json'
		if os.path.exists(database_path):
			with open(database_path, 'r') as f:
				self.database = json.load(f)
		else:
			self.database = {}

		self.project_entry = {}

		self.init_ui()

	def init_ui(self):
		self.setWindowTitle('Biblist for Windows')
		self.resize(1800, 1400)

		# 主水平布局
		main_layout = QHBoxLayout(self)

		# 菜单栏
		menu_bar = self.create_main_menu()
		main_layout.setMenuBar(menu_bar)

		left_widget = self.create_main_panel()
		main_layout.addWidget(left_widget, 3)

		# 右侧Tab
		self.info_source_tabs = QTabWidget()
		tab_font = QFont()
		tab_font.setPointSize(10)
		self.info_source_tabs.setFont(tab_font)
		self.info_source_tabs.addTab(GoogleScholarTab(self), 'Google Scholar')
		self.info_source_tabs.addTab(StorageTab(self), 'Storage')
		self.info_source_tabs.addTab(BibTeXTab(self), 'BibTeX')
		main_layout.addWidget(self.info_source_tabs, 2)

	def create_main_menu(self):
		menu_bar = QMenuBar(self)
		project_menu = menu_bar.addMenu('Project')

		open_submenu = project_menu.addMenu('Open')
		create_empty_action = QAction('New Project', self)
		create_empty_action.triggered.connect(self.create_empty_project)
		from_template_action = QAction('Template', self)
		from_template_action.triggered.connect(self.create_from_template)
		open_bibtex_action = QAction('BibTex', self)
		open_bibtex_action.triggered.connect(self.open_bibtex_file)
		#open_bibtex_action.triggered.connect(lambda: self.open_bibtex_file(param_value))
		open_submenu.addAction(create_empty_action)
		open_submenu.addAction(from_template_action)
		open_submenu.addAction(open_bibtex_action)

		#open_project_action = QAction('Open', self)
		#project_menu.addAction(open_project_action)

		exit_action = QAction('Exit', self)
		exit_action.triggered.connect(self.close)
		project_menu.addAction(exit_action)

		return menu_bar

	def create_empty_project(self):
		self.project_entry = {}
		

	def create_from_template(self):
		#TODO : 预设一些模板条目，供用户选择创建
		self.project_entry = {}
		
	def open_bibtex_file(self):
		self.project_entry = {}
		file_path, _ = QFileDialog.getOpenFileName(self, 'Open BibTeX File', '', 'BibTeX Files (*.bib);;All Files (*)')
		if file_path:
			with open(file_path, 'r', encoding='utf-8') as f:
				bibtex_str = f.read()
				bib_database = bibtexparser.loads(bibtex_str)
				for entry in bib_database.entries:
					self.project_entry[entry['ID']] = entry
			self.list_widget.clear()
			self.list_widget.addItems(list(self.project_entry.keys()))
		
	def create_main_panel(self):
		left_layout = QVBoxLayout()

		# 顶部按钮区
		button_layout = QHBoxLayout()
		btn_font = QFont()
		btn_font.setPointSize(12)
		self.btn_add_entry = QPushButton('New entry')
		self.btn_add_entry.clicked.connect(self.add_entry)
		self.btn_add_entry.setFont(btn_font)
		self.btn_export = QPushButton('Export')
		self.btn_export.clicked.connect(self.export_bibtex)
		self.btn_export.setFont(btn_font)
		button_layout.addWidget(self.btn_add_entry)
		button_layout.addWidget(self.btn_export)
		left_layout.addLayout(button_layout)

		# 列表
		self.list_widget = QListWidget()
		list_font = QFont()
		list_font.setPointSize(10)
		self.list_widget.setFont(list_font)
		self.list_widget.addItems([])
		self.list_widget.currentItemChanged.connect(self.update_info_label)
		self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.list_widget.customContextMenuRequested.connect(self.show_file_list_menu)
		left_layout.addWidget(self.list_widget, 3)

		# 信息显示区
		self.bibtex_display = QTextEdit('请选择左侧项目')
		self.bibtex_display.setReadOnly(True)
		font = QFont()
		font.setPointSize(10)
		self.bibtex_display.setFont(font)
		self.bibtex_display.setStyleSheet('border: 1px solid #ccc; padding: 8px;')
		left_layout.addWidget(self.bibtex_display, 2)

		# 左侧容器
		left_widget = QWidget()
		left_widget.setLayout(left_layout)
		return left_widget

	def show_file_list_menu(self, pos):
		item = self.list_widget.itemAt(pos)
		if not item:
			return
		menu = QMenu(self)
		action_edit_entry = menu.addAction('Edit entry')
		action_remove_entry = menu.addAction('Delete entry')
		action = menu.exec_(self.list_widget.mapToGlobal(pos))
		if action == action_remove_entry:
			self.remove_entry(item.text())
		elif action == action_edit_entry:
			entry = self.edit_entry(item.text())
			if entry:
				db = BibDatabase()
				db.entries = [entry]
				writer = BibTexWriter()
				bibtex_str = writer.write(db)
				QApplication.clipboard().setText(bibtex_str)

	def remove_entry(self, entry_id):
		if entry_id in self.project_entry:
			del self.project_entry[entry_id]
			self.list_widget.clear()
			entry_list = list(self.project_entry.keys())
			entry_list.sort()
			self.list_widget.addItems(entry_list)

	def add_entry(self):
		dialog = QDialog(self)
		dialog.setWindowTitle('Add entry')
		dialog.setGeometry(100, 100, 500, 400)

		layout = QVBoxLayout(dialog)

		text_edit = QTextEdit()
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
			elif new_id in self.project_entry:
				QMessageBox.warning(dialog, '错误', f'ID {new_id} 已存在！')
				return

			self.project_entry[new_id] = new_entry
			self.list_widget.clear()
			entry_list = list(self.project_entry.keys())
			entry_list.sort()
			self.list_widget.addItems(entry_list)
			# Find the index of new_id and set as current item
			new_id_index = entry_list.index(new_id) if new_id in entry_list else -1
			if new_id_index >= 0:
				self.list_widget.setCurrentItem(self.list_widget.item(new_id_index))
			#self.update_info_label(self.list_widget.currentItem(), None)

			dialog.accept()

		btn_save.clicked.connect(save_entry)
		btn_close.clicked.connect(dialog.reject)

		dialog.exec_()

	def edit_entry(self, entry_id):
		entry = self.project_entry.get(entry_id, None)
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
			elif new_id in self.project_entry and new_id != entry_id:
				QMessageBox.warning(dialog, '错误', f'ID {new_id} 已存在！')
				return
			elif new_id != entry_id:
				# ID 发生变化，更新列表和字典
				self.list_widget.currentItem().setText(new_id)
				del self.project_entry[entry_id]
				
			self.project_entry[new_id] = new_entry
			item = self.list_widget.currentItem()
			if item:
				item.setText(new_id)
			dialog.accept()

		btn_save.clicked.connect(save_entry)
		btn_close.clicked.connect(dialog.reject)

		dialog.exec_()
		self.update_info_label(self.list_widget.currentItem(), None)
		#return self.project_entry.get(new_id, None)
        
	def update_info_label(self, current, previous):
		if current:
			entry_id = current.text()
			entry = self.project_entry.get(entry_id, None)
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

	def export_bibtex(self):
		file_path, _ = QFileDialog.getSaveFileName(self, '导出 BibTeX 文件', '', 'BibTeX Files (*.bib)')
		if file_path:
			with open('data/Prefix.bib', 'r') as f:
				prefix_content = f.read()
			
			with open(file_path, 'w', encoding='utf-8') as f:
				f.write(prefix_content)
				for entry in self.project_entry.values():
					db = BibDatabase()
					db.entries = [entry]
					writer = BibTexWriter()
					f.write(writer.write(db))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
