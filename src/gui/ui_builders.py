"""
GUI UI Builders
===============

Builder functions for creating GUI panels and components.
Extracted from app.py for better modularity and V2 compliance.

V2 Compliance: ≤200 lines, builder pattern.

Author: Agent-7 - Repository Cloning Specialist (extracted from gui/app.py)
License: MIT
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QFrame,
        QGridLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )

    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False


def create_header(layout, theme, system_status_label_ref) -> None:
    """
    Create header section for GUI.

    Args:
        layout: Parent layout to add header to
        theme: Theme manager for styling
        system_status_label_ref: Reference list to store status label [label_obj]
    """
    if not PYQT5_AVAILABLE:
        return

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
    system_status_label = QLabel("🟢 System Online")
    system_status_label.setStyleSheet(
        """
        QLabel {
            font-size: 14px;
            color: #27AE60;
            font-weight: bold;
        }
        """
    )
    header_layout.addWidget(system_status_label)

    # Store reference for later use
    system_status_label_ref[0] = system_status_label

    layout.addWidget(header_frame)


def create_left_panel(theme, agent_widgets, callbacks) -> QWidget:
    """
    Create left panel with agent grid and controls.

    Args:
        theme: Theme manager for styling
        agent_widgets: Dict to store agent card widgets
        callbacks: Dict with callback functions

    Returns:
        Configured left panel widget
    """
    if not PYQT5_AVAILABLE:
        return None

    # Import here to avoid circular dependencies
    from .components.agent_card import AgentCard

    panel = QWidget()
    panel.setMaximumWidth(450)
    layout = QVBoxLayout(panel)

    # Agent selection group
    agents_group = QGroupBox("Agents")
    agents_group.setStyleSheet(theme.get_style("group_box"))
    agents_layout = QVBoxLayout(agents_group)

    # Agent grid (4x2 for 8 agents)
    agent_grid = QGridLayout()
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        agent_card = AgentCard(agent_id, callbacks.get("parent"))
        agent_widgets[agent_id] = agent_card

        row = (i - 1) // 4
        col = (i - 1) % 4
        agent_grid.addWidget(agent_card, row, col)

    agents_layout.addLayout(agent_grid)

    # Selection controls
    controls_layout = QHBoxLayout()

    select_all_btn = QPushButton("Select All")
    select_all_btn.setStyleSheet(theme.get_style("button"))
    select_all_btn.clicked.connect(callbacks.get("select_all"))
    controls_layout.addWidget(select_all_btn)

    clear_btn = QPushButton("Clear")
    clear_btn.setStyleSheet(theme.get_style("button_error"))
    clear_btn.clicked.connect(callbacks.get("clear_selection"))
    controls_layout.addWidget(clear_btn)

    agents_layout.addLayout(controls_layout)
    layout.addWidget(agents_group)

    # Action buttons group
    actions_group = QGroupBox("Actions")
    actions_group.setStyleSheet(theme.get_style("group_box"))
    actions_layout = QVBoxLayout(actions_group)

    actions = [
        ("🔍 Ping", callbacks.get("ping")),
        ("📊 Status", callbacks.get("get_status")),
        ("▶️ Resume", callbacks.get("resume")),
        ("⏸️ Pause", callbacks.get("pause")),
    ]

    for text, callback in actions:
        btn = QPushButton(text)
        btn.setStyleSheet(theme.get_style("button"))
        btn.clicked.connect(callback)
        actions_layout.addWidget(btn)

    layout.addWidget(actions_group)
    layout.addStretch()

    return panel


def create_right_panel(status_panel_widget) -> QWidget:
    """
    Create right panel with status and logs.

    Args:
        status_panel_widget: StatusPanel widget to display

    Returns:
        Configured right panel widget
    """
    if not PYQT5_AVAILABLE:
        return None

    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.addWidget(status_panel_widget)
    return panel
