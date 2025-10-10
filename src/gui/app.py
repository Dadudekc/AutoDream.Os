"""
Dream.OS GUI Application - V2 Compliant
=======================================

Main GUI application for agent management and monitoring.
Optional visual layer over V2's CLI-first design.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - GUI Specialist
License: MIT
"""

import logging
import sys
from typing import Any

# Optional PyQt5 dependency
try:
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtWidgets import (
        QApplication,
        QFrame,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QMainWindow,
        QPushButton,
        QSplitter,
        QVBoxLayout,
        QWidget,
    )

    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False
    logging.warning("PyQt5 not available - GUI disabled")

# V2 Integration imports (uses shared utils for fallbacks)
from .utils import get_coordinate_loader, get_unified_config, get_logger
from .components.status_panel import StatusPanel
from .controllers.base import BaseGUIController
from .styles.themes import ThemeManager
from .ui_builders import create_header, create_left_panel, create_right_panel


if PYQT5_AVAILABLE:

    class DreamOSGUI(QMainWindow, BaseGUIController):
        """
        Main GUI application for Dream.OS Cell Phone v2.0.

        Provides visual management interface for:
        - 8-agent swarm coordination
        - Real-time status monitoring
        - Command execution
        - Log viewing
        """

        def __init__(self):
            """Initialize Dream.OS GUI."""
            QMainWindow.__init__(self)
            BaseGUIController.__init__(self)

            self.logger = get_logger(__name__)
            self.config = get_unified_config()
            self.coordinate_loader = get_coordinate_loader()

            # Theme management
            self.theme_manager = ThemeManager()
            self.theme = self.theme_manager.get_theme()

            # Initialize UI
            self._init_ui()
            self._setup_status_updates()

            self.logger.info("Dream.OS GUI initialized")

        def _init_ui(self) -> None:
            """Initialize the main UI."""
            self.setWindowTitle("Dream.OS Cell Phone v2.0 - Agent Management")
            self.setGeometry(100, 100, 1200, 800)
            self.setStyleSheet(self.theme.get_style("main_window"))

            # Central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            # Main layout
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(20)

            # Header
            system_status_ref = [None]  # Reference to store label
            create_header(main_layout, self.theme, system_status_ref)
            self.system_status_label = system_status_ref[0]

            # Main content area
            content_splitter = QSplitter(Qt.Horizontal)
            main_layout.addWidget(content_splitter)

            # Left panel - Agent grid and controls
            callbacks = {
                'parent': self,
                'select_all': self.select_all_agents,
                'clear_selection': self.clear_selection,
                'ping': self.ping_selected_agents,
                'get_status': self.get_status_selected_agents,
                'resume': self.resume_selected_agents,
                'pause': self.pause_selected_agents
            }
            left_panel = create_left_panel(self.theme, self.agent_widgets, callbacks)
            content_splitter.addWidget(left_panel)

            # Right panel - Status and logs
            right_panel = create_right_panel(self.status_panel)
            content_splitter.addWidget(right_panel)

            # Set splitter proportions
            content_splitter.setSizes([400, 800])

            # Status bar
            self.statusBar().showMessage("Ready - Dream.OS Cell Phone v2.0")

        def _setup_status_updates(self) -> None:
            """Setup periodic status updates."""
            # Create timer for status updates
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self._update_agent_statuses)
            self.status_timer.start(5000)  # 5 seconds

            self.log_message("System", "Dream.OS Cell Phone v2.0 initialized")
            self.log_message("System", "8 agents ready for coordination")

        def _update_agent_statuses(self) -> None:
            """Update agent status displays."""
            # This would integrate with actual agent status checking
            # For now, just demonstrate the capability
            pass

        def log_message(self, sender: str, message: str) -> None:
            """Add message to log."""
            if self.status_panel:
                self.status_panel.add_log_message(sender, message)

        def closeEvent(self, event) -> None:
            """Handle window close event."""
            self.log_message("System", "Shutting down GUI")
            super().closeEvent(event)

else:
    # Fallback when PyQt5 is not available
    class DreamOSGUI:
        """Fallback GUI (PyQt5 not available)."""

        def __init__(self):
            self.logger = logging.getLogger(__name__)
            self.logger.error("PyQt5 not available - GUI cannot start")
            print("ERROR: PyQt5 not available. Install with: pip install PyQt5")
            sys.exit(1)


def main():
    """Main entry point for GUI application."""
    if not PYQT5_AVAILABLE:
        print("ERROR: PyQt5 not available. Install with: pip install PyQt5")
        return

    app = QApplication(sys.argv)
    gui = DreamOSGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

