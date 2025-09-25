#!/usr/bin/env python3
"""
Settings Display Component
=========================

Modular settings display widget for Tesla Stock App
V2 Compliant: ≤200 lines, focused settings display
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
    QGridLayout, QPushButton, QSpinBox, QCheckBox, QComboBox,
    QLineEdit, QSlider, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class SettingsDisplayWidget(QWidget):
    """Modular settings display widget"""

    # Signals
    settings_changed = pyqtSignal(dict)
    theme_changed = pyqtSignal(str)
    refresh_interval_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.settings = {
            'refresh_interval': 30,
            'auto_refresh': True,
            'theme': 'light',
            'chart_type': 'line',
            'show_volume': True,
            'show_indicators': True,
            'api_key': '',
            'notifications': True
        }
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #8B4513; margin: 10px;")
        layout.addWidget(title)
        
        # General settings
        general_group = QGroupBox("General Settings")
        general_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #8B4513;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        general_layout = QGridLayout()
        
        # Refresh interval
        general_layout.addWidget(QLabel("Refresh Interval (seconds):"), 0, 0)
        self.refresh_spinbox = QSpinBox()
        self.refresh_spinbox.setRange(5, 300)
        self.refresh_spinbox.setValue(self.settings['refresh_interval'])
        self.refresh_spinbox.setStyleSheet("padding: 5px; border: 1px solid #8B4513; border-radius: 3px;")
        general_layout.addWidget(self.refresh_spinbox, 0, 1)
        
        # Auto refresh
        self.auto_refresh_checkbox = QCheckBox("Auto Refresh")
        self.auto_refresh_checkbox.setChecked(self.settings['auto_refresh'])
        self.auto_refresh_checkbox.setStyleSheet("padding: 5px;")
        general_layout.addWidget(self.auto_refresh_checkbox, 1, 0, 1, 2)
        
        # Notifications
        self.notifications_checkbox = QCheckBox("Enable Notifications")
        self.notifications_checkbox.setChecked(self.settings['notifications'])
        self.notifications_checkbox.setStyleSheet("padding: 5px;")
        general_layout.addWidget(self.notifications_checkbox, 2, 0, 1, 2)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Display settings
        display_group = QGroupBox("Display Settings")
        display_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #8B4513;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        display_layout = QGridLayout()
        
        # Theme selection
        display_layout.addWidget(QLabel("Theme:"), 0, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Professional"])
        self.theme_combo.setCurrentText(self.settings['theme'].title())
        self.theme_combo.setStyleSheet("padding: 5px; border: 1px solid #8B4513; border-radius: 3px;")
        display_layout.addWidget(self.theme_combo, 0, 1)
        
        # Chart type
        display_layout.addWidget(QLabel("Chart Type:"), 1, 0)
        self.chart_combo = QComboBox()
        self.chart_combo.addItems(["Line", "Candlestick", "Bar"])
        self.chart_combo.setCurrentText(self.settings['chart_type'].title())
        self.chart_combo.setStyleSheet("padding: 5px; border: 1px solid #8B4513; border-radius: 3px;")
        display_layout.addWidget(self.chart_combo, 1, 1)
        
        # Show volume
        self.show_volume_checkbox = QCheckBox("Show Volume")
        self.show_volume_checkbox.setChecked(self.settings['show_volume'])
        self.show_volume_checkbox.setStyleSheet("padding: 5px;")
        display_layout.addWidget(self.show_volume_checkbox, 2, 0, 1, 2)
        
        # Show indicators
        self.show_indicators_checkbox = QCheckBox("Show Technical Indicators")
        self.show_indicators_checkbox.setChecked(self.settings['show_indicators'])
        self.show_indicators_checkbox.setStyleSheet("padding: 5px;")
        display_layout.addWidget(self.show_indicators_checkbox, 3, 0, 1, 2)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # API settings
        api_group = QGroupBox("API Settings")
        api_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #8B4513;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        api_layout = QGridLayout()
        
        # API key
        api_layout.addWidget(QLabel("API Key:"), 0, 0)
        self.api_key_input = QLineEdit()
        self.api_key_input.setText(self.settings['api_key'])
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setStyleSheet("padding: 5px; border: 1px solid #8B4513; border-radius: 3px;")
        api_layout.addWidget(self.api_key_input, 0, 1)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Action buttons
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout()
        
        # Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
        """)
        buttons_layout.addWidget(self.save_button)
        
        # Reset button
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        buttons_layout.addWidget(self.reset_button)
        
        buttons_frame.setLayout(buttons_layout)
        layout.addWidget(buttons_frame)
        
        # Connect signals
        self.save_button.clicked.connect(self.save_settings)
        self.reset_button.clicked.connect(self.reset_settings)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        self.refresh_spinbox.valueChanged.connect(self.on_refresh_interval_changed)
        
        self.setLayout(layout)

    def save_settings(self):
        """Save current settings"""
        self.settings.update({
            'refresh_interval': self.refresh_spinbox.value(),
            'auto_refresh': self.auto_refresh_checkbox.isChecked(),
            'theme': self.theme_combo.currentText().lower(),
            'chart_type': self.chart_combo.currentText().lower(),
            'show_volume': self.show_volume_checkbox.isChecked(),
            'show_indicators': self.show_indicators_checkbox.isChecked(),
            'api_key': self.api_key_input.text(),
            'notifications': self.notifications_checkbox.isChecked()
        })
        
        self.settings_changed.emit(self.settings)

    def reset_settings(self):
        """Reset settings to defaults"""
        self.settings = {
            'refresh_interval': 30,
            'auto_refresh': True,
            'theme': 'light',
            'chart_type': 'line',
            'show_volume': True,
            'show_indicators': True,
            'api_key': '',
            'notifications': True
        }
        
        self.refresh_spinbox.setValue(self.settings['refresh_interval'])
        self.auto_refresh_checkbox.setChecked(self.settings['auto_refresh'])
        self.theme_combo.setCurrentText(self.settings['theme'].title())
        self.chart_combo.setCurrentText(self.settings['chart_type'].title())
        self.show_volume_checkbox.setChecked(self.settings['show_volume'])
        self.show_indicators_checkbox.setChecked(self.settings['show_indicators'])
        self.api_key_input.setText(self.settings['api_key'])
        self.notifications_checkbox.setChecked(self.settings['notifications'])

    def on_theme_changed(self, theme):
        """Handle theme change"""
        self.theme_changed.emit(theme.lower())

    def on_refresh_interval_changed(self, interval):
        """Handle refresh interval change"""
        self.refresh_interval_changed.emit(interval)

    def get_settings(self):
        """Get current settings"""
        return self.settings.copy()