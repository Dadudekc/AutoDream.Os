#!/usr/bin/env python3
"""
Dashboard UI Components - V2 Compliant
=====================================

Dashboard UI components following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem,
    QProgressBar, QGroupBox, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DashboardUI:
    """Dashboard UI components."""
    
    def __init__(self, parent_widget):
        """Initialize dashboard UI."""
        self.parent = parent_widget
        self.setup_styles()
    
    def setup_styles(self):
        """Setup UI styles."""
        self.styles = {
            'header': """
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #00ff88;
                    padding: 10px;
                }
            """,
            'metric': """
                QLabel {
                    font-size: 14px;
                    color: #ffffff;
                    padding: 5px;
                }
            """,
            'button': """
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
                QPushButton:pressed {
                    background-color: #00aa55;
                }
            """
        }
    
    def create_header(self, layout):
        """Create dashboard header."""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("🚀 Tesla Trading Robot Dashboard")
        title_label.setStyleSheet(self.styles['header'])
        
        status_label = QLabel("Status: Ready")
        status_label.setStyleSheet(self.styles['metric'])
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        layout.addWidget(header_frame)
        return header_frame
    
    def create_metrics_grid(self, layout):
        """Create metrics grid."""
        metrics_group = QGroupBox("Portfolio Metrics")
        metrics_layout = QGridLayout(metrics_group)
        
        # Portfolio value
        metrics_layout.addWidget(QLabel("Portfolio Value:"), 0, 0)
        self.portfolio_value_label = QLabel("$100,000.00")
        self.portfolio_value_label.setStyleSheet(self.styles['metric'])
        metrics_layout.addWidget(self.portfolio_value_label, 0, 1)
        
        # Cash
        metrics_layout.addWidget(QLabel("Cash:"), 0, 2)
        self.cash_label = QLabel("$100,000.00")
        self.cash_label.setStyleSheet(self.styles['metric'])
        metrics_layout.addWidget(self.cash_label, 0, 3)
        
        # Shares
        metrics_layout.addWidget(QLabel("Shares:"), 1, 0)
        self.shares_label = QLabel("0")
        self.shares_label.setStyleSheet(self.styles['metric'])
        metrics_layout.addWidget(self.shares_label, 1, 1)
        
        # Daily P&L
        metrics_layout.addWidget(QLabel("Daily P&L:"), 1, 2)
        self.daily_pnl_label = QLabel("$0.00")
        self.daily_pnl_label.setStyleSheet(self.styles['metric'])
        metrics_layout.addWidget(self.daily_pnl_label, 1, 3)
        
        # Total P&L
        metrics_layout.addWidget(QLabel("Total P&L:"), 2, 0)
        self.total_pnl_label = QLabel("$0.00")
        self.total_pnl_label.setStyleSheet(self.styles['metric'])
        metrics_layout.addWidget(self.total_pnl_label, 2, 1)
        
        # Win Rate
        metrics_layout.addWidget(QLabel("Win Rate:"), 2, 2)
        self.win_rate_label = QLabel("0%")
        self.win_rate_label.setStyleSheet(self.styles['metric'])
        metrics_layout.addWidget(self.win_rate_label, 2, 3)
        
        layout.addWidget(metrics_group)
        return metrics_group
    
    def create_control_panel(self, layout):
        """Create control panel."""
        control_group = QGroupBox("Trading Controls")
        control_layout = QHBoxLayout(control_group)
        
        self.start_button = QPushButton("Start Trading")
        self.start_button.setStyleSheet(self.styles['button'])
        
        self.stop_button = QPushButton("Stop Trading")
        self.stop_button.setStyleSheet(self.styles['button'])
        self.stop_button.setEnabled(False)
        
        self.emergency_stop_button = QPushButton("🚨 Emergency Stop")
        self.emergency_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.emergency_stop_button)
        control_layout.addStretch()
        
        layout.addWidget(control_group)
        return control_group
    
    def create_log_display(self, layout):
        """Create log display."""
        log_group = QGroupBox("Trading Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444444;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group)
        return log_group
    
    def update_portfolio_metrics(self, portfolio_data):
        """Update portfolio metrics display."""
        self.portfolio_value_label.setText(f"${portfolio_data['total_value']:,.2f}")
        self.cash_label.setText(f"${portfolio_data['cash']:,.2f}")
        self.shares_label.setText(f"{portfolio_data['shares']}")
        self.daily_pnl_label.setText(f"${portfolio_data['daily_pnl']:,.2f}")
        self.total_pnl_label.setText(f"${portfolio_data['total_pnl']:,.2f}")
        
        # Calculate win rate
        total_trades = len(portfolio_data.get('trades', []))
        if total_trades > 0:
            winning_trades = sum(1 for trade in portfolio_data['trades'] if trade.get('profit', 0) > 0)
            win_rate = (winning_trades / total_trades) * 100
            self.win_rate_label.setText(f"{win_rate:.1f}%")
        else:
            self.win_rate_label.setText("0%")
    
    def add_log_message(self, message):
        """Add message to log display."""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())