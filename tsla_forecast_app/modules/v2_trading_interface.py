#!/usr/bin/env python3
"""
V2 Trading Interface
===================

Complete V2-compliant trading robot frontend
Integrates all modular UI components
V2 Compliant: ≤200 lines, focused interface integration
"""

from typing import Any

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QAction, QMainWindow, QStatusBar, QTabWidget

from .ui.chart_widget import ChartWidget
from .ui.mobile_responsive import MobileResponsiveWidget, MobileTradingCard, ResponsiveScrollArea

# Import V2 compliant UI components
from .ui.trading_dashboard import TradingDashboard


class V2TradingInterface(QMainWindow):
    """V2-compliant trading robot frontend interface"""

    # Signals
    trading_action = pyqtSignal(str, dict)  # action, data
    chart_update_requested = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.screen_size = "desktop"
        self.trading_data = {}
        self.init_ui()
        self.setup_connections()
        self.setup_timers()

    def init_ui(self):
        """Initialize V2-compliant UI"""
        self.setWindowTitle("🚀 Tesla Trading Robot V2")
        self.setGeometry(100, 100, 1200, 800)

        # Setup dark theme
        self.setup_dark_theme()

        # Create menu bar
        self.create_menu_bar()

        # Create central widget
        self.create_central_widget()

        # Create status bar
        self.create_status_bar()

    def setup_dark_theme(self):
        """Setup professional dark theme"""
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #ffffff;
                border-bottom: 1px solid #444444;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 16px;
            }
            QMenuBar::item:selected {
                background-color: #444444;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444444;
            }
            QMenu::item:selected {
                background-color: #444444;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #333333;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #2d2d2d;
                border-bottom: 2px solid #0078d4;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
                border-top: 1px solid #444444;
            }
        """
        )

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New Session", self)
        new_action.triggered.connect(self.new_session)
        file_menu.addAction(new_action)

        save_action = QAction("Save Data", self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        dashboard_action = QAction("Dashboard", self)
        dashboard_action.triggered.connect(self.show_dashboard)
        view_menu.addAction(dashboard_action)

        charts_action = QAction("Charts", self)
        charts_action.triggered.connect(self.show_charts)
        view_menu.addAction(charts_action)

        # Settings menu
        settings_menu = menubar.addMenu("Settings")

        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.show_preferences)
        settings_menu.addAction(preferences_action)

    def create_central_widget(self):
        """Create central widget with tabs"""
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Create main trading dashboard
        self.trading_dashboard = TradingDashboard()
        self.central_widget.addTab(self.trading_dashboard, "📊 Trading Dashboard")

        # Create chart widget
        self.chart_widget = ChartWidget()
        self.central_widget.addTab(self.chart_widget, "📈 Charts")

        # Create mobile responsive view
        self.mobile_view = self.create_mobile_view()
        self.central_widget.addTab(self.mobile_view, "📱 Mobile View")

    def create_mobile_view(self):
        """Create mobile-responsive view"""
        mobile_widget = MobileResponsiveWidget()

        # Create scroll area for mobile
        scroll_area = ResponsiveScrollArea()

        # Create mobile trading cards
        self.mobile_card = MobileTradingCard("Tesla Trading")
        scroll_area.add_responsive_widget(self.mobile_card)

        mobile_widget.main_layout.addWidget(scroll_area)
        return mobile_widget

    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Status labels
        self.connection_status = self.status_bar.addWidget("● Disconnected")
        self.data_status = self.status_bar.addWidget("Data: None")
        self.last_update = self.status_bar.addWidget("Last Update: Never")

    def setup_connections(self):
        """Setup signal connections"""
        # Connect trading dashboard signals
        self.trading_dashboard.buy_button.clicked.connect(
            lambda: self.trading_action.emit("buy", self.trading_data)
        )
        self.trading_dashboard.sell_button.clicked.connect(
            lambda: self.trading_action.emit("sell", self.trading_data)
        )
        self.trading_dashboard.hold_button.clicked.connect(
            lambda: self.trading_action.emit("hold", self.trading_data)
        )

        # Connect chart widget signals
        self.chart_widget.chart_updated.connect(self.chart_update_requested.emit)

    def setup_timers(self):
        """Setup update timers"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_interface)
        self.update_timer.start(1000)  # Update every second

    def update_trading_data(self, data: dict[str, Any]):
        """Update trading data across all components"""
        self.trading_data = data

        # Update trading dashboard
        self.trading_dashboard.update_trading_data(data)

        # Update mobile card
        self.mobile_card.update_data(data)

        # Update status bar
        self.update_status_bar(data)

    def update_chart_data(self, chart_data: list[dict[str, Any]]):
        """Update chart data"""
        self.chart_widget.update_chart_data(chart_data)

    def update_status_bar(self, data: dict[str, Any]):
        """Update status bar information"""
        if data:
            self.connection_status.setText("● Connected")
            self.data_status.setText(f"Data: {data.get('source', 'Unknown')}")
            self.last_update.setText(f"Last Update: {data.get('timestamp', 'Unknown')}")
        else:
            self.connection_status.setText("● Disconnected")
            self.data_status.setText("Data: None")

    def update_interface(self):
        """Update interface elements"""
        # Update dashboard
        self.trading_dashboard.update_display()

        # Update status
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_bar.showMessage(f"Trading Robot V2 - {current_time}")

    # Menu actions
    def new_session(self):
        """Start new trading session"""
        print("🆕 Starting new trading session...")

    def save_data(self):
        """Save trading data"""
        print("💾 Saving trading data...")

    def show_dashboard(self):
        """Show dashboard tab"""
        self.central_widget.setCurrentIndex(0)

    def show_charts(self):
        """Show charts tab"""
        self.central_widget.setCurrentIndex(1)

    def show_preferences(self):
        """Show preferences dialog"""
        print("⚙️ Opening preferences...")

    def set_screen_size(self, size: str):
        """Set responsive screen size"""
        self.screen_size = size
        if hasattr(self, "mobile_view"):
            self.mobile_view.update_screen_size(size)
