#!/usr/bin/env python3
"""
Log Display Component
====================

Modular log display widget for Tesla Stock App
V2 Compliant: ≤200 lines, focused log display
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QGroupBox, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QTextCursor
from datetime import datetime


class LogDisplayWidget(QWidget):
    """Modular log display widget"""

    def __init__(self):
        super().__init__()
        self.log_buffer = []
        self.max_log_entries = 1000
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("System Log")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #8B4513; margin: 10px;")
        layout.addWidget(title)
        
        # Log controls
        controls_group = QGroupBox("Log Controls")
        controls_group.setStyleSheet("""
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
        
        controls_layout = QHBoxLayout()
        
        # Log level filter
        self.level_filter = QComboBox()
        self.level_filter.addItems(["All", "INFO", "WARNING", "ERROR", "DEBUG"])
        self.level_filter.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #8B4513;
                border-radius: 3px;
            }
        """)
        controls_layout.addWidget(QLabel("Level:"))
        controls_layout.addWidget(self.level_filter)
        
        # Auto-scroll checkbox
        self.auto_scroll_checkbox = QCheckBox("Auto-scroll")
        self.auto_scroll_checkbox.setChecked(True)
        self.auto_scroll_checkbox.setStyleSheet("padding: 5px;")
        controls_layout.addWidget(self.auto_scroll_checkbox)
        
        # Clear button
        self.clear_button = QPushButton("Clear Log")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        controls_layout.addWidget(self.clear_button)
        
        # Export button
        self.export_button = QPushButton("Export Log")
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
        """)
        controls_layout.addWidget(self.export_button)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #8B4513;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.log_text)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; padding: 5px; font-size: 10px;")
        layout.addWidget(self.status_label)
        
        # Connect signals
        self.clear_button.clicked.connect(self.clear_log)
        self.export_button.clicked.connect(self.export_log)
        self.level_filter.currentTextChanged.connect(self.filter_logs)
        
        self.setLayout(layout)

    def add_log_entry(self, message, level="INFO"):
        """Add a new log entry"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Add to buffer
        self.log_buffer.append({
            'timestamp': timestamp,
            'level': level,
            'message': message,
            'full_entry': log_entry
        })
        
        # Limit buffer size
        if len(self.log_buffer) > self.max_log_entries:
            self.log_buffer.pop(0)
        
        # Update display
        self.update_log_display()
        
        # Auto-scroll if enabled
        if self.auto_scroll_checkbox.isChecked():
            self.log_text.moveCursor(QTextCursor.End)

    def update_log_display(self):
        """Update the log display"""
        # Get current filter
        current_filter = self.level_filter.currentText()
        
        # Filter logs
        filtered_logs = []
        for entry in self.log_buffer:
            if current_filter == "All" or entry['level'] == current_filter:
                filtered_logs.append(entry['full_entry'])
        
        # Update text
        self.log_text.setPlainText('\n'.join(filtered_logs))
        
        # Update status
        self.status_label.setText(f"Log entries: {len(self.log_buffer)} (showing {len(filtered_logs)})")

    def filter_logs(self):
        """Filter logs by level"""
        self.update_log_display()

    def clear_log(self):
        """Clear all log entries"""
        self.log_buffer.clear()
        self.log_text.clear()
        self.status_label.setText("Log cleared")
        self.add_log_entry("Log cleared by user", "INFO")

    def export_log(self):
        """Export log to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tesla_app_log_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write("Tesla Stock App Log Export\n")
                f.write("=" * 50 + "\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Entries: {len(self.log_buffer)}\n")
                f.write("=" * 50 + "\n\n")
                
                for entry in self.log_buffer:
                    f.write(entry['full_entry'] + "\n")
            
            self.add_log_entry(f"Log exported to {filename}", "INFO")
            self.status_label.setText(f"Log exported to {filename}")
            
        except Exception as e:
            self.add_log_entry(f"Failed to export log: {str(e)}", "ERROR")

    def log_info(self, message):
        """Log info message"""
        self.add_log_entry(message, "INFO")

    def log_warning(self, message):
        """Log warning message"""
        self.add_log_entry(message, "WARNING")

    def log_error(self, message):
        """Log error message"""
        self.add_log_entry(message, "ERROR")

    def log_debug(self, message):
        """Log debug message"""
        self.add_log_entry(message, "DEBUG")