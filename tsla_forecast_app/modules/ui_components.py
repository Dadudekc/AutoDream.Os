#!/usr/bin/env python3
"""
UI Components
=============

UI components for Tesla Stock Forecast App
V2 Compliant: ≤400 lines, focused UI components
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem,
    QProgressBar, QGroupBox, QGridLayout, QFrame
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QPalette, QColor


class StockDisplayWidget(QWidget):
    """Main stock display widget"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🚀 Tesla Stock Forecast")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Stock info display
        self.stock_info_group = QGroupBox("Current Stock Information")
        stock_layout = QGridLayout()
        
        self.price_label = QLabel("Price: $0.00")
        self.price_label.setFont(QFont("Arial", 14, QFont.Bold))
        stock_layout.addWidget(self.price_label, 0, 0)
        
        self.change_label = QLabel("Change: $0.00 (0.00%)")
        stock_layout.addWidget(self.change_label, 0, 1)
        
        self.volume_label = QLabel("Volume: 0")
        stock_layout.addWidget(self.volume_label, 1, 0)
        
        self.timestamp_label = QLabel("Last Update: Never")
        stock_layout.addWidget(self.timestamp_label, 1, 1)
        
        self.stock_info_group.setLayout(stock_layout)
        layout.addWidget(self.stock_info_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("🔄 Refresh Data")
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        button_layout.addWidget(self.refresh_button)
        
        self.forecast_button = QPushButton("📈 Generate Forecast")
        self.forecast_button.clicked.connect(self.on_forecast_clicked)
        button_layout.addWidget(self.forecast_button)
        
        layout.addLayout(button_layout)
        
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
        change_color = "green" if change >= 0 else "red"
        self.change_label.setText(f"Change: ${change:.2f} ({change_percent:.2f}%)")
        self.change_label.setStyleSheet(f"color: {change_color}")
        
        # Update volume
        volume = data.get('volume', 0)
        self.volume_label.setText(f"Volume: {volume:,}")
        
        # Update timestamp
        timestamp = data.get('timestamp', 'Unknown')
        self.timestamp_label.setText(f"Last Update: {timestamp}")
        
        # Update source
        source = data.get('source', 'Unknown')
        self.stock_info_group.setTitle(f"Current Stock Information (Source: {source})")

    def on_refresh_clicked(self):
        """Handle refresh button click"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.refresh_button.setEnabled(False)

    def on_forecast_clicked(self):
        """Handle forecast button click"""
        print("📈 Generating forecast...")

    def hide_progress(self):
        """Hide progress bar"""
        self.progress_bar.setVisible(False)
        self.refresh_button.setEnabled(True)


class ForecastWidget(QWidget):
    """Forecast display widget"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("📈 Tesla Stock Forecast")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Forecast table
        self.forecast_table = QTableWidget()
        self.forecast_table.setColumnCount(4)
        self.forecast_table.setHorizontalHeaderLabels([
            "Date", "Predicted Price", "Confidence", "Trend"
        ])
        layout.addWidget(self.forecast_table)
        
        # Forecast controls
        control_layout = QHBoxLayout()
        
        self.generate_button = QPushButton("🎯 Generate Forecast")
        self.generate_button.clicked.connect(self.generate_forecast)
        control_layout.addWidget(self.generate_button)
        
        self.clear_button = QPushButton("🗑️ Clear Forecast")
        self.clear_button.clicked.connect(self.clear_forecast)
        control_layout.addWidget(self.clear_button)
        
        layout.addLayout(control_layout)
        
        self.setLayout(layout)

    def generate_forecast(self):
        """Generate stock forecast"""
        print("🎯 Generating forecast...")
        
        # Mock forecast data
        import random
        from datetime import datetime, timedelta
        
        base_price = 200.0
        forecast_data = []
        
        for i in range(7):  # 7-day forecast
            date = datetime.now() + timedelta(days=i+1)
            price_change = random.uniform(-5, 5)
            predicted_price = base_price + price_change
            confidence = random.uniform(70, 95)
            trend = "📈 Bullish" if price_change > 0 else "📉 Bearish"
            
            forecast_data.append([
                date.strftime("%Y-%m-%d"),
                f"${predicted_price:.2f}",
                f"{confidence:.1f}%",
                trend
            ])
        
        # Update table
        self.forecast_table.setRowCount(len(forecast_data))
        for row, data in enumerate(forecast_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.forecast_table.setItem(row, col, item)

    def clear_forecast(self):
        """Clear forecast data"""
        self.forecast_table.setRowCount(0)


class LogWidget(QWidget):
    """Log display widget"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("📋 Application Log")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # Log controls
        control_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("🗑️ Clear Log")
        self.clear_button.clicked.connect(self.clear_log)
        control_layout.addWidget(self.clear_button)
        
        self.save_button = QPushButton("💾 Save Log")
        self.save_button.clicked.connect(self.save_log)
        control_layout.addWidget(self.save_button)
        
        layout.addLayout(control_layout)
        
        self.setLayout(layout)

    def add_log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.append(log_entry)

    def clear_log(self):
        """Clear log text"""
        self.log_text.clear()

    def save_log(self):
        """Save log to file"""
        print("💾 Saving log...")
        # Implementation would save log to file


class SettingsWidget(QWidget):
    """Settings widget"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Settings group
        settings_group = QGroupBox("API Configuration")
        settings_layout = QGridLayout()
        
        # API key status
        self.api_status_label = QLabel("API Keys Status: Checking...")
        settings_layout.addWidget(self.api_status_label, 0, 0)
        
        # Refresh interval
        self.refresh_interval_label = QLabel("Refresh Interval: 10 seconds")
        settings_layout.addWidget(self.refresh_interval_label, 1, 0)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # About group
        about_group = QGroupBox("About")
        about_layout = QVBoxLayout()
        
        about_text = QLabel("""
        Tesla Stock Forecast App v1.0
        
        Author: Agent-1 (Backend API & Data Integration)
        License: MIT
        
        Features:
        • Real-time stock data from multiple APIs
        • 7-day price forecasting
        • Cross-platform compatibility
        • Mock data fallback
        """)
        about_layout.addWidget(about_text)
        
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)
        
        self.setLayout(layout)

    def update_api_status(self, status):
        """Update API status display"""
        self.api_status_label.setText(f"API Keys Status: {status}")