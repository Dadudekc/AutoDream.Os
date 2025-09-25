#!/usr/bin/env python3
"""
Trading Robot Core - Core Trading Logic and State Management
===========================================================

Core trading functionality extracted from trading_robot.py for V2 compliance.
Contains the main TradingRobot class and essential trading operations.

Author: Agent-7 (Integration Specialist)
License: MIT
"""

import sys
import json
import os
import time
import threading
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QTabWidget, QTableWidget, QTableWidgetItem,
                             QProgressBar, QGroupBox, QGridLayout, QFrame,
                             QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox,
                             QSlider, QLineEdit, QMessageBox, QSplitter)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
import requests
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()


class TradingRobot(QMainWindow):
    """Main trading robot application with core functionality."""
    
    def __init__(self):
        """Initialize the trading robot."""
        super().__init__()
        
        # Core state
        self.is_trading = False
        self.portfolio = {
            'cash': 10000.0,
            'shares': 0,
            'total_value': 10000.0,
            'daily_pnl': 0.0,
            'total_pnl': 0.0
        }
        
        # Risk management
        self.risk_params = {
            'max_position_size': 0.1,  # 10% of portfolio
            'stop_loss': 0.05,        # 5% stop loss
            'take_profit': 0.15,      # 15% take profit
            'max_daily_loss': 0.02    # 2% max daily loss
        }
        
        # Data management
        self.current_data = None
        self.data_worker = None
        self.data_mutex = QMutex()
        
        # Strategies (will be injected)
        self.strategies = []
        
        # UI components
        self.init_ui()
        self.start_data_worker()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Tesla Trading Robot V2")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Header
        self.create_header(layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_portfolio_tab()
        self.create_trading_tab()
        self.create_risk_tab()
        
    def create_header(self, layout):
        """Create the header section."""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("🚀 Tesla Trading Robot V2")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(title_label)
        
        # Status
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        header_layout.addWidget(self.status_label)
        
        # Trading toggle
        self.trading_button = QPushButton("Start Trading")
        self.trading_button.clicked.connect(self.toggle_trading)
        header_layout.addWidget(self.trading_button)
        
        layout.addWidget(header_frame)
        
    def create_dashboard_tab(self):
        """Create the dashboard tab."""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        
        # Market data section
        market_group = QGroupBox("Market Data")
        market_layout = QGridLayout(market_group)
        
        self.price_label = QLabel("Price: $0.00")
        self.change_label = QLabel("Change: $0.00 (0.00%)")
        self.volume_label = QLabel("Volume: 0")
        
        market_layout.addWidget(self.price_label, 0, 0)
        market_layout.addWidget(self.change_label, 0, 1)
        market_layout.addWidget(self.volume_label, 1, 0)
        
        layout.addWidget(market_group)
        
        # Performance metrics
        perf_group = QGroupBox("Performance")
        perf_layout = QGridLayout(perf_group)
        
        self.total_value_label = QLabel("Total Value: $10,000.00")
        self.daily_pnl_label = QLabel("Daily P&L: $0.00")
        self.total_pnl_label = QLabel("Total P&L: $0.00")
        
        perf_layout.addWidget(self.total_value_label, 0, 0)
        perf_layout.addWidget(self.daily_pnl_label, 0, 1)
        perf_layout.addWidget(self.total_pnl_label, 1, 0)
        
        layout.addWidget(perf_group)
        
        self.tab_widget.addTab(dashboard_widget, "Dashboard")
        
    def create_portfolio_tab(self):
        """Create the portfolio tab."""
        portfolio_widget = QWidget()
        layout = QVBoxLayout(portfolio_widget)
        
        # Portfolio table
        self.portfolio_table = QTableWidget()
        self.portfolio_table.setColumnCount(4)
        self.portfolio_table.setHorizontalHeaderLabels([
            "Asset", "Quantity", "Price", "Value"
        ])
        
        layout.addWidget(self.portfolio_table)
        
        self.tab_widget.addTab(portfolio_widget, "Portfolio")
        
    def create_trading_tab(self):
        """Create the trading tab."""
        trading_widget = QWidget()
        layout = QVBoxLayout(trading_widget)
        
        # Manual trading controls
        manual_group = QGroupBox("Manual Trading")
        manual_layout = QGridLayout(manual_group)
        
        # Buy/Sell controls
        self.buy_button = QPushButton("Buy")
        self.sell_button = QPushButton("Sell")
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setRange(1, 1000)
        self.quantity_spinbox.setValue(10)
        
        manual_layout.addWidget(QLabel("Quantity:"), 0, 0)
        manual_layout.addWidget(self.quantity_spinbox, 0, 1)
        manual_layout.addWidget(self.buy_button, 0, 2)
        manual_layout.addWidget(self.sell_button, 0, 3)
        
        layout.addWidget(manual_group)
        
        # Trading log
        self.trading_log = QTextEdit()
        self.trading_log.setReadOnly(True)
        layout.addWidget(QLabel("Trading Log:"))
        layout.addWidget(self.trading_log)
        
        self.tab_widget.addTab(trading_widget, "Trading")
        
    def create_risk_tab(self):
        """Create the risk management tab."""
        risk_widget = QWidget()
        layout = QVBoxLayout(risk_widget)
        
        # Risk parameters
        risk_group = QGroupBox("Risk Parameters")
        risk_layout = QGridLayout(risk_group)
        
        # Max position size
        risk_layout.addWidget(QLabel("Max Position Size:"), 0, 0)
        self.max_position_spinbox = QDoubleSpinBox()
        self.max_position_spinbox.setRange(0.01, 1.0)
        self.max_position_spinbox.setValue(0.1)
        self.max_position_spinbox.setSuffix(" (10%)")
        risk_layout.addWidget(self.max_position_spinbox, 0, 1)
        
        # Stop loss
        risk_layout.addWidget(QLabel("Stop Loss:"), 1, 0)
        self.stop_loss_spinbox = QDoubleSpinBox()
        self.stop_loss_spinbox.setRange(0.01, 0.5)
        self.stop_loss_spinbox.setValue(0.05)
        self.stop_loss_spinbox.setSuffix(" (5%)")
        risk_layout.addWidget(self.stop_loss_spinbox, 1, 1)
        
        # Take profit
        risk_layout.addWidget(QLabel("Take Profit:"), 2, 0)
        self.take_profit_spinbox = QDoubleSpinBox()
        self.take_profit_spinbox.setRange(0.01, 1.0)
        self.take_profit_spinbox.setValue(0.15)
        self.take_profit_spinbox.setSuffix(" (15%)")
        risk_layout.addWidget(self.take_profit_spinbox, 2, 1)
        
        # Update button
        update_button = QPushButton("Update Risk Parameters")
        update_button.clicked.connect(self.update_risk_params)
        risk_layout.addWidget(update_button, 3, 0, 1, 2)
        
        layout.addWidget(risk_group)
        
        self.tab_widget.addTab(risk_widget, "Risk Management")
        
    def start_data_worker(self):
        """Start the data update worker thread."""
        self.data_worker = DataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()
        
    def update_stock_data(self, data):
        """Update stock data display."""
        self.data_mutex.lock()
        self.current_data = data
        self.data_mutex.unlock()
        
        # Update UI
        if data:
            self.price_label.setText(f"Price: ${data.get('price', 0):.2f}")
            change = data.get('change', 0)
            change_pct = data.get('change_percent', 0)
            self.change_label.setText(f"Change: ${change:.2f} ({change_pct:.2f}%)")
            self.volume_label.setText(f"Volume: {data.get('volume', 0):,}")
            
            # Update portfolio value
            self.update_portfolio_display()
            
    def update_portfolio_display(self):
        """Update portfolio display."""
        if self.current_data:
            current_price = self.current_data.get('price', 0)
            portfolio_value = self.portfolio['cash'] + (self.portfolio['shares'] * current_price)
            self.portfolio['total_value'] = portfolio_value
            
            self.total_value_label.setText(f"Total Value: ${portfolio_value:,.2f}")
            self.daily_pnl_label.setText(f"Daily P&L: ${self.portfolio['daily_pnl']:.2f}")
            self.total_pnl_label.setText(f"Total P&L: ${self.portfolio['total_pnl']:.2f}")
            
    def toggle_trading(self):
        """Toggle trading on/off."""
        self.is_trading = not self.is_trading
        
        if self.is_trading:
            self.trading_button.setText("Stop Trading")
            self.status_label.setText("Status: Trading")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.log_message("Trading started")
        else:
            self.trading_button.setText("Start Trading")
            self.status_label.setText("Status: Stopped")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.log_message("Trading stopped")
            
    def update_risk_params(self):
        """Update risk management parameters."""
        self.risk_params['max_position_size'] = self.max_position_spinbox.value()
        self.risk_params['stop_loss'] = self.stop_loss_spinbox.value()
        self.risk_params['take_profit'] = self.take_profit_spinbox.value()
        
        self.log_message(f"Risk parameters updated: {self.risk_params}")
        
    def log_message(self, message):
        """Log a message to the trading log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.trading_log.append(f"[{timestamp}] {message}")
        
    def get_portfolio_value(self):
        """Get current portfolio value."""
        if self.current_data:
            current_price = self.current_data.get('price', 0)
            return self.portfolio['cash'] + (self.portfolio['shares'] * current_price)
        return self.portfolio['cash']
        
    def can_trade(self, action, quantity):
        """Check if trade is allowed based on risk parameters."""
        if action == 'buy':
            required_cash = quantity * (self.current_data.get('price', 0) if self.current_data else 0)
            return self.portfolio['cash'] >= required_cash
        elif action == 'sell':
            return self.portfolio['shares'] >= quantity
        return False


class DataWorker(QThread):
    """Worker thread for fetching market data."""
    
    data_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        """Main worker loop."""
        while self.running:
            try:
                # Simulate data fetch (replace with real API)
                data = self.fetch_market_data()
                self.data_updated.emit(data)
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                print(f"Data worker error: {e}")
                time.sleep(10)
                
    def fetch_market_data(self):
        """Fetch market data (simulated)."""
        # Simulate Tesla stock data
        base_price = 250.0
        change = random.uniform(-5, 5)
        price = base_price + change
        change_percent = (change / base_price) * 100
        
        return {
            'price': price,
            'change': change,
            'change_percent': change_percent,
            'volume': random.randint(1000000, 5000000),
            'timestamp': datetime.now().isoformat()
        }
        
    def stop(self):
        """Stop the worker thread."""
        self.running = False




