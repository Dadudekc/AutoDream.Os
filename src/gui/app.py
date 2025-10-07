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

# V2 Integration imports
try:
    from ..core.coordinate_loader import get_coordinate_loader
    from ..core.unified_config import get_unified_config
    from ..core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")

    def get_coordinate_loader():
        return None

    def get_unified_config():
        return type("MockConfig", (), {"get_env": lambda x, y=None: y})()

    def get_logger(name):
        return logging.getLogger(name)

from .components.agent_card import AgentCard
from .components.status_panel import StatusPanel
from .controllers.base import BaseGUIController
from .styles.themes import DarkTheme, ThemeManager


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
            self._create_header(main_layout)

            # Main content area
            content_splitter = QSplitter(Qt.Horizontal)
            main_layout.addWidget(content_splitter)

            # Left panel - Agent grid and controls
            left_panel = self._create_left_panel()
            content_splitter.addWidget(left_panel)

            # Right panel - Status and logs
            right_panel = self._create_right_panel()
            content_splitter.addWidget(right_panel)

            # Set splitter proportions
            content_splitter.setSizes([400, 800])

            # Status bar
            self.statusBar().showMessage("Ready - Dream.OS Cell Phone v2.0")

        def _create_header(self, layout: QVBoxLayout) -> None:
            """Create header section."""
            header_frame = QFrame()
            header_frame.setStyleSheet(
                """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #2C3E50, stop:1 #3498DB);
                    border-radius: 10px;
                    padding: 15px;
                }
            """
            )

            header_layout = QHBoxLayout(header_frame)

            # Title
            title_label = QLabel("📱 Dream.OS Cell Phone v2.0")
            title_label.setStyleSheet(
                """
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: white;
                }
            """
            )
            header_layout.addWidget(title_label)

            header_layout.addStretch()

            # System status
            self.system_status_label = QLabel("🟢 System Online")
            self.system_status_label.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                    color: #27AE60;
                    font-weight: bold;
                }
            """
            )
            header_layout.addWidget(self.system_status_label)

            layout.addWidget(header_frame)

        def _create_left_panel(self) -> QWidget:
            """Create left panel with agent grid and controls."""
            panel = QWidget()
            panel.setMaximumWidth(450)
            layout = QVBoxLayout(panel)

            # Agent selection group
            agents_group = QGroupBox("Agents")
            agents_group.setStyleSheet(self.theme.get_style("group_box"))
            agents_layout = QVBoxLayout(agents_group)

            # Agent grid (4x2 for 8 agents)
            from PyQt5.QtWidgets import QGridLayout

            agent_grid = QGridLayout()
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                agent_card = AgentCard(agent_id, self)
                self.agent_widgets[agent_id] = agent_card

                row = (i - 1) // 4
                col = (i - 1) % 4
                agent_grid.addWidget(agent_card, row, col)

            agents_layout.addLayout(agent_grid)

            # Selection controls
            controls_layout = QHBoxLayout()

            select_all_btn = QPushButton("Select All")
            select_all_btn.setStyleSheet(self.theme.get_style("button"))
            select_all_btn.clicked.connect(self.select_all_agents)
            controls_layout.addWidget(select_all_btn)

            clear_btn = QPushButton("Clear")
            clear_btn.setStyleSheet(self.theme.get_style("button_error"))
            clear_btn.clicked.connect(self.clear_selection)
            controls_layout.addWidget(clear_btn)

            agents_layout.addLayout(controls_layout)
            layout.addWidget(agents_group)

            # Action buttons group
            actions_group = QGroupBox("Actions")
            actions_group.setStyleSheet(self.theme.get_style("group_box"))
            actions_layout = QVBoxLayout(actions_group)

            actions = [
                ("🔍 Ping", self.ping_selected_agents),
                ("📊 Status", self.get_status_selected_agents),
                ("▶️ Resume", self.resume_selected_agents),
                ("⏸️ Pause", self.pause_selected_agents),
            ]

            for text, callback in actions:
                btn = QPushButton(text)
                btn.setStyleSheet(self.theme.get_style("button"))
                btn.clicked.connect(callback)
                actions_layout.addWidget(btn)

            layout.addWidget(actions_group)
            layout.addStretch()

            return panel

        def _create_right_panel(self) -> QWidget:
            """Create right panel with status and logs."""
            panel = QWidget()
            layout = QVBoxLayout(panel)

            # Status panel
            self.status_panel = StatusPanel(self)
            self.log_display = self.status_panel.log_display
            layout.addWidget(self.status_panel)

            return panel

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

