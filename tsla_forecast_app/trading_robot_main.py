#!/usr/bin/env python3
"""
Trading Robot Main Application - V2 Compliant
============================================

Main trading robot application following V2 compliance principles.
Maximum 300 lines per file.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

from trading_robot_core import TradingRobotCore
from ui.dashboard_ui import DashboardUI


class TradingRobotMain(QMainWindow):
    """Main Trading Robot Application."""
    
    def __init__(self):
        """Initialize main application."""
        super().__init__()
        self.core = TradingRobotCore()
        self.setup_ui()
        self.setup_timers()
        self.connect_signals()
    
    def setup_ui(self):
        """Setup user interface."""
        self.setWindowTitle("Tesla Trading Robot - Advanced Trading System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
                background-color: #2a2a2a;
            }
            QTabBar::tab {
                background-color: #333333;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #00ff88;
                color: #000000;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create dashboard UI
        self.dashboard_ui = DashboardUI(self)
        
        # Create header
        self.dashboard_ui.create_header(main_layout)
        
        # Create metrics grid
        self.dashboard_ui.create_metrics_grid(main_layout)
        
        # Create control panel
        self.dashboard_ui.create_control_panel(main_layout)
        
        # Create log display
        self.dashboard_ui.create_log_display(main_layout)
        
        # Create tab widget for additional features
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Add placeholder tabs (to be implemented)
        self.tab_widget.addTab(QWidget(), "Strategies")
        self.tab_widget.addTab(QWidget(), "Portfolio")
        self.tab_widget.addTab(QWidget(), "Risk Management")
        self.tab_widget.addTab(QWidget(), "Backtesting")
    
    def setup_timers(self):
        """Setup update timers."""
        # Update UI every second
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui)
        self.ui_timer.start(1000)  # 1 second
        
        # Update log every 5 seconds
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.update_log)
        self.log_timer.start(5000)  # 5 seconds
    
    def connect_signals(self):
        """Connect UI signals."""
        # Connect control buttons
        self.dashboard_ui.start_button.clicked.connect(self.start_trading)
        self.dashboard_ui.stop_button.clicked.connect(self.stop_trading)
        self.dashboard_ui.emergency_stop_button.clicked.connect(self.emergency_stop)
    
    def start_trading(self):
        """Start automated trading."""
        self.core.start_trading()
        self.dashboard_ui.start_button.setEnabled(False)
        self.dashboard_ui.stop_button.setEnabled(True)
        self.dashboard_ui.add_log_message("🚀 Trading started")
        
        # Enable default strategies
        self.core.enable_strategy('ma_crossover')
        self.core.enable_strategy('rsi_mean_reversion')
    
    def stop_trading(self):
        """Stop automated trading."""
        self.core.stop_trading()
        self.dashboard_ui.start_button.setEnabled(True)
        self.dashboard_ui.stop_button.setEnabled(False)
        self.dashboard_ui.add_log_message("⏹️ Trading stopped")
    
    def emergency_stop(self):
        """Emergency stop all trading."""
        self.core.stop_trading()
        # Disable all strategies
        for strategy_name in self.core.strategies.keys():
            self.core.disable_strategy(strategy_name)
        
        self.dashboard_ui.start_button.setEnabled(True)
        self.dashboard_ui.stop_button.setEnabled(False)
        self.dashboard_ui.add_log_message("🚨 EMERGENCY STOP - All trading halted")
    
    def update_ui(self):
        """Update UI with current data."""
        try:
            # Update portfolio metrics
            portfolio_summary = self.core.get_portfolio_summary()
            self.dashboard_ui.update_portfolio_metrics(portfolio_summary)
            
        except Exception as e:
            print(f"Error updating UI: {e}")
    
    def update_log(self):
        """Update log with recent activity."""
        try:
            if self.core.stock_data:
                price = self.core.stock_data['current_price']
                change = self.core.stock_data.get('change', 0)
                change_pct = self.core.stock_data.get('change_percent', 0)
                
                log_message = f"TSLA: ${price:.2f} ({change:+.2f}, {change_pct:+.2f}%)"
                self.dashboard_ui.add_log_message(log_message)
                
        except Exception as e:
            print(f"Error updating log: {e}")
    
    def closeEvent(self, event):
        """Handle application close."""
        self.core.stop_data_worker()
        event.accept()


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Tesla Trading Robot")
    app.setApplicationVersion("2.0.0")
    
    # Create and show main window
    window = TradingRobotMain()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()