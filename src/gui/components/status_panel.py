"""
Status Panel Component - V2 Compliant
=====================================

Log and status display panel for GUI applications.
Provides formatted log display with auto-scroll and export capabilities.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - GUI Specialist
License: MIT
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

# Optional PyQt5 dependency
try:
    from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout

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

    class StatusPanel(QFrame):
        """
        Status and log display panel.

        Provides:
        - Log message display with formatting
        - Auto-scroll functionality
        - Log clearing
        - Log export to file
        - Timestamp formatting
        """

        def __init__(self, parent: Any = None):
            """
            Initialize status panel.

            Args:
                parent: Parent widget
            """
            super().__init__(parent)
            self.logger = get_logger(__name__)
            self.max_log_lines = 1000
            self.log_count = 0

            self._init_ui()

        def _init_ui(self) -> None:
            """Initialize the UI components."""
            self._setup_panel_styling()
            layout = self._create_main_layout()
            self._add_log_display(layout)
            self._add_control_buttons(layout)

        def _setup_panel_styling(self) -> None:
            """Setup panel frame styling."""
            self.setStyleSheet(
                """
                QFrame {
                    background-color: #1A1A1A;
                    border: 2px solid #34495E;
                    border-radius: 8px;
                    padding: 10px;
                }
            """
            )

        def _create_main_layout(self) -> QVBoxLayout:
            """Create main layout."""
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            return layout

        def _add_log_display(self, layout: QVBoxLayout) -> None:
            """Add log display text edit."""
            self.log_display = QTextEdit()
            self.log_display.setStyleSheet(
                """
                QTextEdit {
                    background-color: #2C3E50;
                    color: #ECF0F1;
                    border: 1px solid #34495E;
                    border-radius: 5px;
                    font-family: Consolas, Monaco, monospace;
                    font-size: 10pt;
                    padding: 5px;
                }
            """
            )
            self.log_display.setReadOnly(True)
            layout.addWidget(self.log_display)

        def _add_control_buttons(self, layout: QVBoxLayout) -> None:
            """Add control buttons."""
            control_layout = QHBoxLayout()

            # Clear button
            self.clear_btn = QPushButton("🗑️ Clear Log")
            self.clear_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #C0392B;
                }
            """
            )
            self.clear_btn.clicked.connect(self.clear_log)
            control_layout.addWidget(self.clear_btn)

            # Save button
            self.save_btn = QPushButton("💾 Save Log")
            self.save_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #27AE60;
                    color: white;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
            """
            )
            self.save_btn.clicked.connect(self.save_log)
            control_layout.addWidget(self.save_btn)

            control_layout.addStretch()

            layout.addLayout(control_layout)

        def add_log_message(self, sender: str, message: str) -> None:
            """
            Add a log message with timestamp.

            Args:
                sender: Message sender
                message: Message content
            """
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {sender}: {message}"

            self.log_display.append(log_entry)
            self.log_count += 1

            # Trim log if too long
            if self.log_count > self.max_log_lines:
                self._trim_log()

            # Auto-scroll to bottom
            self._scroll_to_bottom()

        def clear_log(self) -> None:
            """Clear all log messages."""
            self.log_display.clear()
            self.log_count = 0
            self.add_log_message("System", "Log cleared")

        def save_log(self) -> None:
            """Save log to file."""
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"gui_log_{timestamp}.txt"

                # Create logs directory
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)

                log_path = log_dir / filename

                # Save log content
                log_content = self.log_display.toPlainText()
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(log_content)

                self.add_log_message("System", f"Log saved to {log_path}")

            except Exception as e:
                self.logger.error(f"Failed to save log: {e}")
                self.add_log_message("Error", f"Failed to save log: {e}")

        def _scroll_to_bottom(self) -> None:
            """Scroll log display to bottom."""
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

        def _trim_log(self) -> None:
            """Trim log to maximum lines."""
            try:
                log_content = self.log_display.toPlainText()
                lines = log_content.split("\n")

                # Keep only the last max_log_lines
                if len(lines) > self.max_log_lines:
                    trimmed_lines = lines[-self.max_log_lines :]
                    self.log_display.setPlainText("\n".join(trimmed_lines))
                    self.log_count = self.max_log_lines

            except Exception as e:
                self.logger.error(f"Failed to trim log: {e}")

        def set_max_lines(self, max_lines: int) -> None:
            """Set maximum number of log lines."""
            self.max_log_lines = max_lines

        def get_log_content(self) -> str:
            """Get current log content."""
            return self.log_display.toPlainText()

else:
    # Fallback when PyQt5 is not available
    class AgentCard:
        """Fallback agent card (PyQt5 not available)."""

        def __init__(self, agent_id: str, parent: Any = None):
            self.agent_id = agent_id
            self.logger = logging.getLogger(__name__)
            self.logger.warning("PyQt5 not available - AgentCard disabled")
