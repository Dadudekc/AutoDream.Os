#!/usr/bin/env python3
"""
Main Tesla Stock App
===================

Main application class for Tesla Stock Forecast App
V2 Compliant: ≤400 lines, focused main application logic
"""

import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QStatusBar
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
try:
    from .data_worker import StockDataWorker
    from .ui_components import (
        StockDisplayWidget, ForecastDisplayWidget, LogDisplayWidget, 
        SettingsDisplayWidget, ChartDisplayWidget, ProfessionalTheme
    )
    from .flag_display import TradingFlagsDisplay
except ImportError:
    # Handle direct execution
    import os
    import sys
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from tsla_forecast_app.modules.data_worker import StockDataWorker
    from tsla_forecast_app.modules.ui_components import (
        StockDisplayWidget, ForecastDisplayWidget, LogDisplayWidget, 
        SettingsDisplayWidget, ChartDisplayWidget, ProfessionalTheme
    )
    from tsla_forecast_app.modules.flag_display import TradingFlagsDisplay


class TeslaStockApp(QMainWindow):
    """Main Tesla Stock Forecast Application"""

    def __init__(self):
        super().__init__()
        self.data_worker = None
        self.theme_manager = ProfessionalTheme()
        self.init_ui()
        self.init_data_worker()
        self.setup_timers()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🚀 Tesla Stock Forecast App - Professional Trading Interface")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply professional theme
        self.theme_manager.apply_theme(QApplication.instance(), 'professional')
        
        # Professional theme is applied above

        # Create central widget with tabs
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Create tab widgets using new modular components
        self.stock_widget = StockDisplayWidget()
        self.forecast_widget = ForecastDisplayWidget()
        self.chart_widget = ChartDisplayWidget()
        self.flags_widget = TradingFlagsDisplay()
        self.log_widget = LogDisplayWidget()
        self.settings_widget = SettingsDisplayWidget()

        # Add tabs with professional layout
        self.central_widget.addTab(self.stock_widget, "📊 Stock Data")
        self.central_widget.addTab(self.chart_widget, "📈 Real-Time Charts")
        self.central_widget.addTab(self.forecast_widget, "🔮 AI Forecast")
        self.central_widget.addTab(self.flags_widget, "🚩 Trading Flags")
        self.central_widget.addTab(self.log_widget, "📝 System Log")
        self.central_widget.addTab(self.settings_widget, "⚙️ Settings")

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Tesla Stock Forecast App")

        # Connect signals
        self.stock_widget.refresh_button.clicked.connect(self.refresh_data)
        self.settings_widget.theme_changed.connect(self.change_theme)
        self.settings_widget.refresh_interval_changed.connect(self.update_refresh_interval)

    def init_data_worker(self):
        """Initialize data worker thread"""
        self.data_worker = StockDataWorker()
        self.data_worker.data_updated.connect(self.update_stock_data)
        self.data_worker.start()
        
        self.log_message("Data worker started")

    def setup_timers(self):
        """Setup application timers"""
        # Status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # Update every 5 seconds

        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.start(30000)  # Auto-refresh every 30 seconds

    def update_stock_data(self, data):
        """Update stock data in UI"""
        if data:
            self.stock_widget.update_stock_data(data)
            self.log_message(f"Stock data updated: ${data.get('price', 0):.2f}")
            
            # Update trading flags with new data
            self.flags_widget.update_stock_data(data)
            
            # Update status bar
            price = data.get('price', 0)
            change = data.get('change', 0)
            self.status_bar.showMessage(f"TSLA: ${price:.2f} ({change:+.2f}) - {data.get('source', 'Unknown')}")
            
            # Hide progress bar
            self.stock_widget.hide_progress()

    def refresh_data(self):
        """Manually refresh stock data"""
        self.log_message("Manual refresh requested")
        if self.data_worker and self.data_worker.isRunning():
            # Force immediate update
            self.data_worker.msleep(100)  # Small delay to allow UI update

    def generate_forecast(self):
        """Generate stock forecast"""
        self.log_message("Generating forecast...")
        self.forecast_widget.generate_forecast()
        self.log_message("Forecast generated")

    def auto_refresh(self):
        """Auto-refresh data"""
        self.log_message("Auto-refresh triggered")

    def update_status(self):
        """Update application status"""
        current_time = datetime.now().strftime("%H:%M:%S")
        if self.data_worker and self.data_worker.isRunning():
            status = f"Data worker active - {current_time}"
        else:
            status = f"Data worker inactive - {current_time}"
        
        # Update settings widget
        self.settings_widget.update_api_status("Active" if self.data_worker and self.data_worker.isRunning() else "Inactive")

    def log_message(self, message):
        """Add message to log"""
        self.log_widget.add_log_message(message)

    def change_theme(self, theme_name):
        """Change application theme"""
        self.theme_manager.apply_theme(QApplication.instance(), theme_name)
        self.log_message(f"Theme changed to: {theme_name}")

    def update_refresh_interval(self, interval):
        """Update data refresh interval"""
        if self.data_worker:
            self.data_worker.set_refresh_interval(interval)
        self.log_message(f"Refresh interval updated to: {interval} seconds")

    def closeEvent(self, event):
        """Handle application close event"""
        self.log_message("Application closing...")
        
        # Stop data worker
        if self.data_worker and self.data_worker.isRunning():
            self.data_worker.stop()
            self.log_message("Data worker stopped")
        
        # Stop timers
        if hasattr(self, 'status_timer'):
            self.status_timer.stop()
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        
        self.log_message("Application closed")
        event.accept()


def create_app():
    """Create and configure the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Tesla Stock Forecast App")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Agent-1 Development")
    
    # Set application font
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Create main window
    window = TeslaStockApp()
    window.show()
    
    return app, window


def main():
    """Main application entry point"""
    print("🚀 Starting Tesla Stock Forecast App...")
    
    try:
        app, window = create_app()
        
        # Show initial message
        window.log_message("Application started successfully")
        window.log_message("Loading stock data...")
        
        # Run application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)