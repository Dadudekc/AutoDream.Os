#!/usr/bin/env python3
"""
Professional Theme Component
===========================

Professional trading interface with dark theme
V2 Compliant: ≤200 lines, focused theme management
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class ProfessionalTheme:
    """Professional trading theme manager"""

    def __init__(self):
        self.themes = {
            'dark': self.get_dark_theme(),
            'light': self.get_light_theme(),
            'professional': self.get_professional_theme()
        }

    def get_dark_theme(self):
        """Get dark theme palette"""
        palette = QPalette()
        
        # Dark colors
        dark_bg = QColor(30, 30, 30)
        dark_fg = QColor(220, 220, 220)
        dark_alt = QColor(45, 45, 45)
        accent = QColor(0, 150, 255)
        
        # Base colors
        palette.setColor(QPalette.Window, dark_bg)
        palette.setColor(QPalette.WindowText, dark_fg)
        palette.setColor(QPalette.Base, dark_alt)
        palette.setColor(QPalette.AlternateBase, dark_bg)
        palette.setColor(QPalette.ToolTipBase, dark_bg)
        palette.setColor(QPalette.ToolTipText, dark_fg)
        palette.setColor(QPalette.Text, dark_fg)
        palette.setColor(QPalette.Button, dark_alt)
        palette.setColor(QPalette.ButtonText, dark_fg)
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, accent)
        palette.setColor(QPalette.Highlight, accent)
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        return palette

    def get_light_theme(self):
        """Get light theme palette"""
        palette = QPalette()
        
        # Light colors
        light_bg = QColor(255, 255, 255)
        light_fg = QColor(0, 0, 0)
        light_alt = QColor(240, 240, 240)
        accent = QColor(0, 100, 200)
        
        # Base colors
        palette.setColor(QPalette.Window, light_bg)
        palette.setColor(QPalette.WindowText, light_fg)
        palette.setColor(QPalette.Base, light_alt)
        palette.setColor(QPalette.AlternateBase, light_bg)
        palette.setColor(QPalette.ToolTipBase, light_bg)
        palette.setColor(QPalette.ToolTipText, light_fg)
        palette.setColor(QPalette.Text, light_fg)
        palette.setColor(QPalette.Button, light_alt)
        palette.setColor(QPalette.ButtonText, light_fg)
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, accent)
        palette.setColor(QPalette.Highlight, accent)
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        return palette

    def get_professional_theme(self):
        """Get professional trading theme palette"""
        palette = QPalette()
        
        # Professional colors
        pro_bg = QColor(20, 25, 35)  # Dark blue-gray
        pro_fg = QColor(200, 210, 220)  # Light blue-gray
        pro_alt = QColor(35, 45, 60)  # Medium blue-gray
        pro_accent = QColor(0, 200, 150)  # Teal accent
        pro_success = QColor(0, 200, 100)  # Green
        pro_warning = QColor(255, 180, 0)  # Orange
        pro_error = QColor(255, 100, 100)  # Red
        
        # Base colors
        palette.setColor(QPalette.Window, pro_bg)
        palette.setColor(QPalette.WindowText, pro_fg)
        palette.setColor(QPalette.Base, pro_alt)
        palette.setColor(QPalette.AlternateBase, pro_bg)
        palette.setColor(QPalette.ToolTipBase, pro_bg)
        palette.setColor(QPalette.ToolTipText, pro_fg)
        palette.setColor(QPalette.Text, pro_fg)
        palette.setColor(QPalette.Button, pro_alt)
        palette.setColor(QPalette.ButtonText, pro_fg)
        palette.setColor(QPalette.BrightText, pro_error)
        palette.setColor(QPalette.Link, pro_accent)
        palette.setColor(QPalette.Highlight, pro_accent)
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        return palette

    def apply_theme(self, app, theme_name='professional'):
        """Apply theme to application"""
        if theme_name in self.themes:
            app.setPalette(self.themes[theme_name])
            
            # Set additional stylesheet for professional look
            if theme_name == 'professional':
                app.setStyleSheet(self.get_professional_stylesheet())
            elif theme_name == 'dark':
                app.setStyleSheet(self.get_dark_stylesheet())
            else:
                app.setStyleSheet(self.get_light_stylesheet())

    def get_professional_stylesheet(self):
        """Get professional stylesheet"""
        return """
        QMainWindow {
            background-color: #141923;
            color: #c8d2dc;
        }
        
        QTabWidget::pane {
            border: 1px solid #232d3d;
            background-color: #141923;
        }
        
        QTabBar::tab {
            background-color: #232d3d;
            color: #c8d2dc;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #141923;
            border-bottom: 2px solid #00c896;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #00c896;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: #c8d2dc;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #00c896;
        }
        
        QPushButton {
            background-color: #232d3d;
            color: #c8d2dc;
            border: 1px solid #00c896;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #00c896;
            color: #141923;
        }
        
        QPushButton:pressed {
            background-color: #00a078;
        }
        
        QLabel {
            color: #c8d2dc;
        }
        
        QTextEdit {
            background-color: #232d3d;
            color: #c8d2dc;
            border: 1px solid #00c896;
            border-radius: 3px;
            padding: 5px;
        }
        
        QComboBox {
            background-color: #232d3d;
            color: #c8d2dc;
            border: 1px solid #00c896;
            border-radius: 3px;
            padding: 5px;
        }
        
        QSpinBox {
            background-color: #232d3d;
            color: #c8d2dc;
            border: 1px solid #00c896;
            border-radius: 3px;
            padding: 5px;
        }
        
        QCheckBox {
            color: #c8d2dc;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 2px solid #00c896;
            background-color: #232d3d;
            border-radius: 3px;
        }
        
        QCheckBox::indicator:checked {
            border: 2px solid #00c896;
            background-color: #00c896;
            border-radius: 3px;
        }
        
        QProgressBar {
            border: 2px solid #00c896;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
            background-color: #232d3d;
        }
        
        QProgressBar::chunk {
            background-color: #00c896;
            border-radius: 3px;
        }
        
        QStatusBar {
            background-color: #232d3d;
            color: #c8d2dc;
            border-top: 1px solid #00c896;
        }
        """

    def get_dark_stylesheet(self):
        """Get dark stylesheet"""
        return """
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QTabWidget::pane {
            border: 1px solid #333333;
            background-color: #1e1e1e;
        }
        
        QTabBar::tab {
            background-color: #333333;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #1e1e1e;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #666666;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: #ffffff;
        }
        
        QPushButton {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #666666;
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        QPushButton:hover {
            background-color: #555555;
        }
        """

    def get_light_stylesheet(self):
        """Get light stylesheet"""
        return """
        QMainWindow {
            background-color: #ffffff;
            color: #000000;
        }
        
        QTabWidget::pane {
            border: 1px solid #cccccc;
            background-color: #ffffff;
        }
        
        QTabBar::tab {
            background-color: #f0f0f0;
            color: #000000;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #ffffff;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: #000000;
        }
        
        QPushButton {
            background-color: #f0f0f0;
            color: #000000;
            border: 1px solid #cccccc;
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        """