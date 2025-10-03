#!/usr/bin/env python3
"""
Tesla Stock App Main - V2 Compliant
==================================

Main Tesla Stock Forecast Application following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Backend API & Data Integration)
License: MIT
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem, QProgressBar, QGroupBox, QGridLayout, QFrame
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

from data.stock_data_worker import StockDataWorker


class TeslaStockApp(QMainWindow):
    """Main Tesla Stock Forecast Application."""
    
    def __init__(self):
        """Initialize Tesla Stock App."""
        super().__init__()
        self.stock_data = {}
        self.historical_data = []
        self.init_ui()
        self.start_data_worker()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Tesla Stock Forecast App - PyQt5")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QPushButton {
                background-color: #00ff88;
                color: #000000;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00cc6a;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #00ff88;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTableWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                gridline-color: #444444;
                border: 1px solid #444444;
            }
            QHeaderView::section {
                background-color: #00ff88;
                color: #000000;
                padding: 4px;
                border: none;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        self.create_header(main_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_chart_tab()
        self.create_forecast_tab()
        self.create_technical_tab()
        
        # Create status bar
        self.statusBar().showMessage("Tesla Stock Forecast App - Ready")
    
    def create_header(self, layout):
        """Create the header section."""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #00ff88;
                color: #000000;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("🚀 Tesla Stock Forecast App")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #000000;")
        header_layout.addWidget(title_label)
        
        # Status
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("font-size: 14px; color: #000000;")
        header_layout.addWidget(self.status_label)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addWidget(header_frame)
    
    def create_dashboard_tab(self):
        """Create the dashboard tab."""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        
        # Current price section
        price_group = QGroupBox("Current Price")
        price_layout = QGridLayout(price_group)
        
        self.price_label = QLabel("$0.00")
        self.price_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #00ff88;")
        price_layout.addWidget(QLabel("Price:"), 0, 0)
        price_layout.addWidget(self.price_label, 0, 1)
        
        self.change_label = QLabel("$0.00 (0.00%)")
        self.change_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")
        price_layout.addWidget(QLabel("Change:"), 1, 0)
        price_layout.addWidget(self.change_label, 1, 1)
        
        self.volume_label = QLabel("0")
        self.volume_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        price_layout.addWidget(QLabel("Volume:"), 2, 0)
        price_layout.addWidget(self.volume_label, 2, 1)
        
        layout.addWidget(price_group)
        
        # Market data table
        market_group = QGroupBox("Market Data")
        market_layout = QVBoxLayout(market_group)
        
        self.market_table = QTableWidget(0, 3)
        self.market_table.setHorizontalHeaderLabels(["Metric", "Value", "Change"])
        self.market_table.setStyleSheet("QTableWidget { background-color: #2a2a2a; color: #ffffff; }")
        market_layout.addWidget(self.market_table)
        
        layout.addWidget(market_group)
        
        self.tab_widget.addTab(dashboard_widget, "📊 Dashboard")
    
    def create_chart_tab(self):
        """Create the chart tab."""
        chart_widget = QWidget()
        layout = QVBoxLayout(chart_widget)
        
        # Chart placeholder
        chart_group = QGroupBox("Price Chart")
        chart_layout = QVBoxLayout(chart_group)
        
        self.chart_text = QTextEdit()
        self.chart_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;")
        self.chart_text.setText("📈 Chart will be displayed here\n\nThis is a placeholder for the price chart visualization.")
        chart_layout.addWidget(self.chart_text)
        
        layout.addWidget(chart_group)
        
        self.tab_widget.addTab(chart_widget, "📈 Chart")
    
    def create_forecast_tab(self):
        """Create the forecast tab."""
        forecast_widget = QWidget()
        layout = QVBoxLayout(forecast_widget)
        
        # Forecast section
        forecast_group = QGroupBox("Price Forecast")
        forecast_layout = QVBoxLayout(forecast_group)
        
        self.forecast_text = QTextEdit()
        self.forecast_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;")
        self.forecast_text.setText("🔮 Forecast will be displayed here\n\nThis is a placeholder for the price forecast.")
        forecast_layout.addWidget(self.forecast_text)
        
        layout.addWidget(forecast_group)
        
        self.tab_widget.addTab(forecast_widget, "🔮 Forecast")
    
    def create_technical_tab(self):
        """Create the technical analysis tab."""
        technical_widget = QWidget()
        layout = QVBoxLayout(technical_widget)
        
        # Technical indicators
        indicators_group = QGroupBox("Technical Indicators")
        indicators_layout = QVBoxLayout(indicators_group)
        
        self.indicators_text = QTextEdit()
        self.indicators_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444444; font-family: monospace;")
        self.indicators_text.setText("📊 Technical indicators will be displayed here\n\nThis is a placeholder for technical analysis.")
        indicators_layout.addWidget(self.indicators_text)
        
        layout.addWidget(indicators_group)
        
        self.tab_widget.addTab(technical_widget, "📊 Technical")
    
    def start_data_worker(self):
        """Start the data worker thread."""
        self.data_worker = StockDataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()
    
    def update_stock_data(self, data):
        """Update stock data display."""
        self.stock_data = data
        
        # Update price display
        self.price_label.setText(f"${data['current_price']}")
        
        change_text = f"${data['change']} ({data['change_percent']}%)"
        if data['change'] >= 0:
            self.change_label.setStyleSheet("font-size: 18px; color: #00ff88;")
        else:
            self.change_label.setStyleSheet("font-size: 18px; color: #ff6b6b;")
        self.change_label.setText(change_text)
        
        self.volume_label.setText(f"{data['volume']:,}")
        
        # Update market data table
        self.update_market_table(data)
        
        # Update status
        source = data.get('source', 'Unknown')
        self.status_label.setText(f"Updated: {data['timestamp'][:19]} | {source}")
        self.statusBar().showMessage(f"Tesla: ${data['current_price']} ({data['change_percent']:+.2f}%) | Source: {source}")
    
    def update_market_table(self, data):
        """Update market data table."""
        self.market_table.setRowCount(6)
        
        metrics = [
            ("Current Price", f"${data['current_price']}", f"{data['change_percent']:+.2f}%"),
            ("Previous Close", f"${data['previous_close']}", ""),
            ("Volume", f"{data['volume']:,}", ""),
            ("Market Cap", f"${data['market_cap']:,}" if data['market_cap'] > 0 else "N/A", ""),
            ("Change", f"${data['change']}", f"{data['change_percent']:+.2f}%"),
            ("Source", data['source'], "")
        ]
        
        for i, (metric, value, change) in enumerate(metrics):
            self.market_table.setItem(i, 0, QTableWidgetItem(metric))
            self.market_table.setItem(i, 1, QTableWidgetItem(value))
            self.market_table.setItem(i, 2, QTableWidgetItem(change))
    
    def refresh_data(self):
        """Refresh stock data."""
        self.status_label.setText("Refreshing...")
        if hasattr(self, 'data_worker'):
            self.data_worker.stop()
        self.data_worker = StockDataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()
    
    def closeEvent(self, event):
        """Handle application close."""
        if hasattr(self, 'data_worker'):
            self.data_worker.stop()
        event.accept()


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Tesla Stock Forecast App")
    app.setApplicationVersion("2.0.0")
    
    # Create and show main window
    window = TeslaStockApp()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()