"""
UI 样式定义
集中管理所有 PyQt5 组件的 QSS 样式
"""

# 主题配色
COLORS = {
    'primary': '#2f7d65',
    'primary_hover': '#3a9278',
    'primary_pressed': '#266955',
    'primary_light': '#eff7f4',
    'primary_lighter': '#e5f2ee',
    
    'background': '#f0f4f2',
    'surface': '#ffffff',
    'surface_alt': '#f7faf9',
    'surface_disabled': '#b8c5c1',
    
    'border': '#d5e2dd',
    'border_light': '#e8eeed',
    'border_focus': '#2f7d65',
    
    'text_primary': '#2d3e38',
    'text_secondary': '#587168',
    'text_disabled': '#6a7f77',
    'text_on_primary': '#ffffff',
}

# 主窗口样式
MAIN_WINDOW_STYLE = f"""
    QWidget {{
        background-color: {COLORS['background']};
    }}
    QMenuBar {{
        background-color: {COLORS['surface']};
        border-bottom: 2px solid {COLORS['border']};
        padding: 6px 4px;
        font-weight: 500;
    }}
    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 16px;
        color: {COLORS['text_primary']};
        margin: 2px 4px;
        border-radius: 6px;
    }}
    QMenuBar::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['primary']};
    }}
    QMenuBar::item:pressed {{
        background-color: #dae3e0;
    }}
    QMenu {{
        background-color: {COLORS['surface']};
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        padding: 8px;
    }}
    QMenu::item {{
        padding: 10px 40px 10px 16px;
        color: {COLORS['text_primary']};
        border-radius: 6px;
        margin: 2px 0px;
    }}
    QMenu::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['primary']};
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {COLORS['border_light']};
        margin: 6px 12px;
    }}
    QTabWidget::pane {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        background-color: {COLORS['surface']};
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: {COLORS['border_light']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-bottom: none;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }}
    QTabBar::tab:selected {{
        background-color: {COLORS['surface']};
        border-bottom: 1px solid {COLORS['surface']};
    }}
    QTabBar::tab:hover:!selected {{
        background-color: #f5f7f6;
    }}
"""

# 按钮样式
BUTTON_PRIMARY_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['text_on_primary']};
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_hover']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['primary_pressed']};
    }}
    QPushButton:disabled {{
        background-color: {COLORS['surface_disabled']};
    }}
"""

BUTTON_SECONDARY_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_light']};
        border: 2px solid {COLORS['primary']};
    }}
    QPushButton:pressed {{
        background-color: #dae3e0;
    }}
"""

BUTTON_DIALOG_OK_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['text_on_primary']};
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        min-width: 70px;
        min-height: 28px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_hover']};
    }}
"""

BUTTON_DIALOG_CANCEL_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['border_light']};
        color: {COLORS['text_primary']};
        border: 1px solid #d0d9d6;
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #dae3e0;
    }}
"""

# 输入框样式
INPUT_STYLE = f"""
    QLineEdit {{
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        padding: 6px 12px;
        background-color: {COLORS['surface']};
        color: {COLORS['text_primary']};
        font-size: 10pt;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['border_focus']};
    }}
"""

INPUT_DIALOG_STYLE = f"""
    QLineEdit {{
        border: 2px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 12px;
        background-color: {COLORS['surface']};
        font-size: 10pt;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['primary']};
    }}
"""

# 文本编辑区样式
TEXTEDIT_STYLE = f"""
    QTextEdit {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        background-color: {COLORS['surface']};
        padding: 12px;
        color: {COLORS['text_primary']};
        selection-background-color: {COLORS['primary']};
        selection-color: {COLORS['text_on_primary']};
    }}
"""

TEXTEDIT_DIALOG_STYLE = f"""
    QTextEdit {{
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        background-color: {COLORS['surface']};
        padding: 12px;
        selection-background-color: {COLORS['primary']};
        selection-color: {COLORS['text_on_primary']};
    }}
    QTextEdit:focus {{
        border: 2px solid {COLORS['primary']};
    }}
"""

# 列表控件样式
LISTWIDGET_STYLE = f"""
    QListWidget {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        background-color: {COLORS['surface']};
        padding: 6px;
    }}
    QListWidget::item {{
        padding: 10px;
        border-radius: 6px;
        margin: 2px 0px;
        color: {COLORS['text_primary']};
    }}
    QListWidget::item:selected {{
        background-color: {COLORS['primary']};
        color: {COLORS['text_on_primary']};
    }}
    QListWidget::item:hover:!selected {{
        background-color: {COLORS['primary_light']};
    }}
"""

# ListView 样式（主页面卡片列表）
LISTVIEW_STYLE = f"""
    QListView {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        background: {COLORS['surface']};
        padding: 6px;
    }}
"""

# 标签样式
LABEL_INFO_STYLE = f"""
    QLabel {{
        color: {COLORS['text_secondary']};
        padding: 8px 12px;
        background-color: {COLORS['surface_alt']};
        border-radius: 6px;
        border: 1px solid {COLORS['border_light']};
    }}
"""

LABEL_STATUS_STYLE = f"""
    QLabel {{
        color: {COLORS['text_secondary']};
        padding: 6px 12px;
        background-color: {COLORS['surface_alt']};
        border-radius: 6px;
        border: 1px solid {COLORS['border_light']};
    }}
"""

# 对话框样式
DIALOG_STYLE = f"""
    QDialog {{
        background-color: #f5f7f6;
    }}
    QLabel {{
        color: {COLORS['text_primary']};
        font-size: 11pt;
        font-weight: bold;
    }}
"""

DIALOG_LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_primary']};
        font-size: 10pt;
    }}
"""

# 右键菜单样式
CONTEXT_MENU_STYLE = f"""
    QMenu {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 8px 32px 8px 16px;
        color: {COLORS['text_primary']};
        border-radius: 4px;
    }}
    QMenu::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['primary']};
    }}
"""

# QMessageBox 全局样式
MESSAGEBOX_STYLE = f"""
    QMessageBox {{
        background-color: #f5f7f6;
    }}
    QMessageBox QLabel {{
        color: {COLORS['text_primary']};
        font-size: 10pt;
    }}
    QMessageBox QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['text_on_primary']};
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        min-width: 70px;
        min-height: 28px;
        font-weight: bold;
    }}
    QMessageBox QPushButton:hover {{
        background-color: {COLORS['primary_hover']};
    }}
"""
