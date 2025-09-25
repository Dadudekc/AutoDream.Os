#!/usr/bin/env python3
"""
Stock Display Component
======================

Modular stock display widget for Tesla Stock App
V2 Compliant: ≤200 lines, focused stock display
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
    QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor


class StockDisplayWidget(QWidget):
    """Modular stock display widget"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Tesla Stock Forecast")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2E8B57; margin: 10px;")
        layout.addWidget(title)
        
        # Stock info display
        self.stock_info_group = QGroupBox("Current Stock Information")
        self.stock_info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2E8B57;
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
        
        stock_layout = QGridLayout()
        
        # Price display
        self.price_label = QLabel("Price: $0.00")
        self.price_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.price_label.setStyleSheet("color: #2E8B57; padding: 5px;")
        stock_layout.addWidget(self.price_label, 0, 0)
        
        # Change display
        self.change_label = QLabel("Change: $0.00 (0.00%)")
        self.change_label.setFont(QFont("Arial", 12))
        self.change_label.setStyleSheet("padding: 5px;")
        stock_layout.addWidget(self.change_label, 0, 1)
        
        # Volume display
        self.volume_label = QLabel("Volume: 0")
        self.volume_label.setFont(QFont("Arial", 12))
        self.volume_label.setStyleSheet("padding: 5px;")
        stock_layout.addWidget(self.volume_label, 1, 0)
        
        # Timestamp display
        self.timestamp_label = QLabel("Last Update: Never")
        self.timestamp_label.setFont(QFont("Arial", 10))
        self.timestamp_label.setStyleSheet("color: #666; padding: 5px;")
        stock_layout.addWidget(self.timestamp_label, 1, 1)
        
        self.stock_info_group.setLayout(stock_layout)
        layout.addWidget(self.stock_info_group)
        
        # Status indicator
        self.status_frame = QFrame()
        self.status_frame.setFrameStyle(QFrame.Box)
        self.status_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: #f9f9f9;
                margin: 5px;
            }
        """)
        
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        status_layout.addWidget(self.status_label)
        
        self.status_frame.setLayout(status_layout)
        layout.addWidget(self.status_frame)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh Data")
        self.refresh_button.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #006400;
            }
        """)
        layout.addWidget(self.refresh_button)
        
        self.setLayout(layout)

    def update_stock_data(self, data):
        """Update stock data display"""
        if not data:
            return
        
        # Update price
        price = data.get('price', 0)
        self.price_label.setText(f"Price: ${price:.2f}")
        
        # Update change
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        change_text = f"Change: ${change:.2f} ({change_percent:.2f}%)"
        self.change_label.setText(change_text)
        
        # Color code the change
        if change > 0:
            self.change_label.setStyleSheet("color: #228B22; padding: 5px; font-weight: bold;")
        elif change < 0:
            self.change_label.setStyleSheet("color: #DC143C; padding: 5px; font-weight: bold;")
        else:
            self.change_label.setStyleSheet("color: #666; padding: 5px;")
        
        # Update volume
        volume = data.get('volume', 0)
        self.volume_label.setText(f"Volume: {volume:,}")
        
        # Update timestamp
        timestamp = data.get('timestamp', 'Unknown')
        self.timestamp_label.setText(f"Last Update: {timestamp}")

    def update_status(self, status, connected=True):
        """Update connection status"""
        if connected:
            self.status_label.setText(f"Status: {status}")
            self.status_label.setStyleSheet("color: #228B22; padding: 5px; font-weight: bold;")
        else:
            self.status_label.setText(f"Status: {status}")
            self.status_label.setStyleSheet("color: #DC143C; padding: 5px; font-weight: bold;")

    def set_refresh_callback(self, callback):
        """Set refresh button callback"""
        self.refresh_button.clicked.connect(callback)