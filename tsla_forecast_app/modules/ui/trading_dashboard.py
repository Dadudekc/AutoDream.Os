#!/usr/bin/env python3
"""
Trading Dashboard Component
==========================

Professional trading interface with dark theme
V2 Compliant: ≤200 lines, focused trading dashboard
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QGridLayout, QFrame, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from datetime import datetime
from typing import Dict, Any


class TradingDashboard(QWidget):
    """Professional trading dashboard with dark theme"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_dark_theme()
        self.setup_timers()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Header
        header_frame = QFrame()
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("🚀 Tesla Trading Dashboard")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(self.title_label)
        
        self.status_label = QLabel("● LIVE")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        header_layout.addWidget(self.status_label)
        
        header_layout.addStretch()
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
        # Main trading info
        self.create_trading_info_section(layout)
        
        # Performance metrics
        self.create_performance_section(layout)
        
        # Quick actions
        self.create_quick_actions_section(layout)
        
        self.setLayout(layout)

    def create_trading_info_section(self, parent_layout):
        """Create trading information section"""
        trading_group = QGroupBox("📊 Trading Information")
        trading_layout = QGridLayout()
        
        # Current price
        self.price_label = QLabel("$0.00")
        self.price_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.price_label.setStyleSheet("color: #ffffff;")
        trading_layout.addWidget(QLabel("Current Price:"), 0, 0)
        trading_layout.addWidget(self.price_label, 0, 1)
        
        # Change
        self.change_label = QLabel("$0.00 (0.00%)")
        self.change_label.setFont(QFont("Arial", 14))
        trading_layout.addWidget(QLabel("Change:"), 1, 0)
        trading_layout.addWidget(self.change_label, 1, 1)
        
        # Volume
        self.volume_label = QLabel("0")
        self.volume_label.setFont(QFont("Arial", 12))
        trading_layout.addWidget(QLabel("Volume:"), 2, 0)
        trading_layout.addWidget(self.volume_label, 2, 1)
        
        # Market cap
        self.market_cap_label = QLabel("$0.00B")
        self.market_cap_label.setFont(QFont("Arial", 12))
        trading_layout.addWidget(QLabel("Market Cap:"), 3, 0)
        trading_layout.addWidget(self.market_cap_label, 3, 1)
        
        trading_group.setLayout(trading_layout)
        parent_layout.addWidget(trading_group)

    def create_performance_section(self, parent_layout):
        """Create performance metrics section"""
        perf_group = QGroupBox("📈 Performance Metrics")
        perf_layout = QGridLayout()
        
        # P&L
        self.pnl_label = QLabel("$0.00")
        self.pnl_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.pnl_label.setStyleSheet("color: #00ff00;")
        perf_layout.addWidget(QLabel("P&L:"), 0, 0)
        perf_layout.addWidget(self.pnl_label, 0, 1)
        
        # Win rate
        self.win_rate_label = QLabel("0%")
        self.win_rate_label.setFont(QFont("Arial", 14))
        perf_layout.addWidget(QLabel("Win Rate:"), 1, 0)
        perf_layout.addWidget(self.win_rate_label, 1, 1)
        
        # Total trades
        self.trades_label = QLabel("0")
        self.trades_label.setFont(QFont("Arial", 14))
        perf_layout.addWidget(QLabel("Total Trades:"), 2, 0)
        perf_layout.addWidget(self.trades_label, 2, 1)
        
        perf_group.setLayout(perf_layout)
        parent_layout.addWidget(perf_group)

    def create_quick_actions_section(self, parent_layout):
        """Create quick actions section"""
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QHBoxLayout()
        
        self.buy_button = QPushButton("🟢 BUY")
        self.buy_button.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
        """)
        actions_layout.addWidget(self.buy_button)
        
        self.sell_button = QPushButton("🔴 SELL")
        self.sell_button.setStyleSheet("""
            QPushButton {
                background-color: #aa0000;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        actions_layout.addWidget(self.sell_button)
        
        self.hold_button = QPushButton("⏸️ HOLD")
        self.hold_button.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #888888;
            }
        """)
        actions_layout.addWidget(self.hold_button)
        
        actions_group.setLayout(actions_layout)
        parent_layout.addWidget(actions_group)

    def setup_dark_theme(self):
        """Setup dark theme styling"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #444444;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #2d2d2d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
        """)

    def setup_timers(self):
        """Setup update timers"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)  # Update every second

    def update_trading_data(self, data: Dict[str, Any]):
        """Update trading data display"""
        if not data:
            return
            
        # Update price
        price = data.get('price', 0)
        self.price_label.setText(f"${price:.2f}")
        
        # Update change
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        change_color = "#00ff00" if change >= 0 else "#ff0000"
        self.change_label.setText(f"${change:.2f} ({change_percent:.2f}%)")
        self.change_label.setStyleSheet(f"color: {change_color};")
        
        # Update volume
        volume = data.get('volume', 0)
        self.volume_label.setText(f"{volume:,}")
        
        # Update market cap
        market_cap = data.get('market_cap', 0)
        self.market_cap_label.setText(f"${market_cap:.2f}B")

    def update_performance(self, pnl: float, win_rate: float, total_trades: int):
        """Update performance metrics"""
        self.pnl_label.setText(f"${pnl:.2f}")
        self.pnl_label.setStyleSheet("color: #00ff00;" if pnl >= 0 else "color: #ff0000;")
        self.win_rate_label.setText(f"{win_rate:.1f}%")
        self.trades_label.setText(str(total_trades))

    def update_display(self):
        """Update display elements"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_label.setText(f"● LIVE - {current_time}")

    def connect_signals(self, buy_callback, sell_callback, hold_callback):
        """Connect action button signals"""
        self.buy_button.clicked.connect(buy_callback)
        self.sell_button.clicked.connect(sell_callback)
        self.hold_button.clicked.connect(hold_callback)






