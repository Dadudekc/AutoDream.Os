"""
Agent Card Component - V2 Compliant
===================================

Visual widget for individual agent status and selection.
Displays agent information with status indicators and selection controls.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - GUI Specialist
License: MIT
"""

import logging
from typing import Any

# Optional PyQt5 dependency
try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QCheckBox, QFrame, QLabel, QVBoxLayout

    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False
    logging.warning("PyQt5 not available - GUI components disabled")

# V2 Integration imports
try:
    from ...core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")

    def get_logger(name):
        return logging.getLogger(name)


if PYQT5_AVAILABLE:

    class AgentCard(QFrame):
        """
        Agent status card widget.

        Displays:
        - Agent ID and name
        - Status indicator
        - Selection checkbox
        - Activity information
        """

        def __init__(self, agent_id: str, parent: Any = None):
            """
            Initialize agent card.

            Args:
                agent_id: Agent identifier (e.g., "Agent-1")
                parent: Parent widget
            """
            super().__init__(parent)
            self.agent_id = agent_id
            self.logger = get_logger(__name__)
            self.current_status = "unknown"
            self.is_selected = False

            self._init_ui()

        def _init_ui(self) -> None:
            """Initialize the UI components."""
            # Card styling
            self.setStyleSheet(
                """
                QFrame {
                    background-color: #2C3E50;
                    border: 2px solid #34495E;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px;
                }
                QFrame:hover {
                    border-color: #3498DB;
                }
            """
            )

            self.setMinimumSize(150, 100)
            self.setMaximumSize(200, 150)

            # Main layout
            layout = QVBoxLayout(self)
            layout.setSpacing(5)

            # Selection checkbox
            self.checkbox = QCheckBox(self.agent_id)
            self.checkbox.setStyleSheet(
                """
                QCheckBox {
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border-radius: 3px;
                    border: 2px solid #3498DB;
                }
                QCheckBox::indicator:checked {
                    background-color: #3498DB;
                }
            """
            )
            self.checkbox.stateChanged.connect(self._on_selection_changed)
            layout.addWidget(self.checkbox)

            # Status indicator
            self.status_label = QLabel("⚪ Unknown")
            self.status_label.setStyleSheet(
                """
                QLabel {
                    color: #BDC3C7;
                    font-size: 11px;
                }
            """
            )
            layout.addWidget(self.status_label)

            # Activity label
            self.activity_label = QLabel("Idle")
            self.activity_label.setStyleSheet(
                """
                QLabel {
                    color: #7F8C8D;
                    font-size: 10px;
                    font-style: italic;
                }
            """
            )
            layout.addWidget(self.activity_label)

            layout.addStretch()

        def _on_selection_changed(self, state: int) -> None:
            """Handle selection state change."""
            self.is_selected = state == Qt.Checked

            if self.parent() and hasattr(self.parent(), "toggle_agent_selection"):
                self.parent().toggle_agent_selection(self.agent_id)

        def set_selected(self, selected: bool) -> None:
            """Set selection state programmatically."""
            self.is_selected = selected
            self.checkbox.setChecked(selected)

        def update_status(self, status: str) -> None:
            """
            Update agent status display.

            Args:
                status: Status string (e.g., "online", "busy", "offline")
            """
            self.current_status = status

            status_icons = {"online": "🟢", "busy": "🟡", "offline": "🔴", "unknown": "⚪"}

            status_colors = {"online": "#27AE60", "busy": "#F39C12", "offline": "#E74C3C", "unknown": "#BDC3C7"}

            icon = status_icons.get(status, "⚪")
            color = status_colors.get(status, "#BDC3C7")

            self.status_label.setText(f"{icon} {status.title()}")
            self.status_label.setStyleSheet(
                f"""
                QLabel {{
                    color: {color};
                    font-size: 11px;
                    font-weight: bold;
                }}
            """
            )

        def update_activity(self, activity: str) -> None:
            """
            Update activity display.

            Args:
                activity: Activity description
            """
            self.activity_label.setText(activity)

        def get_agent_info(self) -> dict[str, Any]:
            """Get agent card information."""
            return {
                "agent_id": self.agent_id,
                "current_status": self.current_status,
                "is_selected": self.is_selected,
            }

else:
    # Fallback when PyQt5 is not available
    class AgentCard:
        """Fallback agent card (PyQt5 not available)."""

        def __init__(self, agent_id: str, parent: Any = None):
            self.agent_id = agent_id
            self.logger = logging.getLogger(__name__)
            self.logger.warning("PyQt5 not available - AgentCard disabled")

        def update_status(self, status: str) -> None:
            pass

        def set_selected(self, selected: bool) -> None:
            pass

