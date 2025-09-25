#!/usr/bin/env python3
"""
Trading Flags Display
=====================

UI component for displaying trading flags and agent predictions
V2 Compliant: ≤400 lines, focused flag display logic
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout,
    QProgressBar, QTextEdit, QComboBox, QSpinBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from datetime import datetime
from typing import List, Dict, Any
from .trading_flags import TradingFlag, FlagType, AgentFlag, TradingFlagEngine


class TradingFlagsDisplay(QWidget):
    """Trading flags display widget"""

    def __init__(self):
        super().__init__()
        self.flag_engine = TradingFlagEngine()
        self.init_ui()
        self.setup_timers()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🚩 Agent Trading Flags")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Control panel
        control_group = QGroupBox("Flag Controls")
        control_layout = QHBoxLayout()
        
        self.generate_button = QPushButton("🎯 Generate Agent Flags")
        self.generate_button.clicked.connect(self.generate_flags)
        control_layout.addWidget(self.generate_button)
        
        self.consensus_button = QPushButton("🤝 Show Consensus")
        self.consensus_button.clicked.connect(self.show_consensus)
        control_layout.addWidget(self.consensus_button)
        
        self.refresh_button = QPushButton("🔄 Refresh Flags")
        self.refresh_button.clicked.connect(self.refresh_flags)
        control_layout.addWidget(self.refresh_button)
        
        self.save_button = QPushButton("💾 Save Flags")
        self.save_button.clicked.connect(self.save_flags)
        control_layout.addWidget(self.save_button)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Agent filter
        filter_group = QGroupBox("Filter Options")
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Agent:"))
        self.agent_filter = QComboBox()
        self.agent_filter.addItem("All Agents")
        for agent in AgentFlag:
            self.agent_filter.addItem(agent.value.replace("_", "-").title())
        self.agent_filter.currentTextChanged.connect(self.filter_flags)
        filter_layout.addWidget(self.agent_filter)
        
        filter_layout.addWidget(QLabel("Flag Type:"))
        self.flag_type_filter = QComboBox()
        self.flag_type_filter.addItem("All Types")
        for flag_type in FlagType:
            self.flag_type_filter.addItem(flag_type.value.replace("_", " ").title())
        self.flag_type_filter.currentTextChanged.connect(self.filter_flags)
        filter_layout.addWidget(self.flag_type_filter)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Flags table
        self.flags_table = QTableWidget()
        self.flags_table.setColumnCount(8)
        self.flags_table.setHorizontalHeaderLabels([
            "Agent", "Flag Type", "Strength", "Price Target", 
            "Confidence", "Reasoning", "Timestamp", "Expires"
        ])
        self.flags_table.setAlternatingRowColors(True)
        self.flags_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.flags_table)
        
        # Consensus display
        consensus_group = QGroupBox("Consensus Analysis")
        consensus_layout = QVBoxLayout()
        
        self.consensus_label = QLabel("No consensus available")
        self.consensus_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.consensus_label.setAlignment(Qt.AlignCenter)
        consensus_layout.addWidget(self.consensus_label)
        
        self.consensus_details = QTextEdit()
        self.consensus_details.setMaximumHeight(100)
        self.consensus_details.setReadOnly(True)
        consensus_layout.addWidget(self.consensus_details)
        
        consensus_group.setLayout(consensus_layout)
        layout.addWidget(consensus_group)
        
        # Status bar
        self.status_label = QLabel("Ready - No flags generated")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def setup_timers(self):
        """Setup refresh timers"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds

    def generate_flags(self, stock_data: Dict[str, Any] = None):
        """Generate trading flags for all agents"""
        if stock_data is None:
            # Mock stock data for testing
            stock_data = {
                'price': 200.0,
                'change': 5.0,
                'volume': 15000000,
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Analyze market data
            market_analysis = self.flag_engine.analyze_market_data(stock_data)
            
            # Generate flags for all agents
            flags = self.flag_engine.generate_all_agent_flags(market_analysis)
            
            # Update display
            self.update_flags_display(flags)
            
            # Update status
            self.status_label.setText(f"Generated {len(flags)} flags at {datetime.now().strftime('%H:%M:%S')}")
            self.status_label.setStyleSheet("color: green;")
            
        except Exception as e:
            self.status_label.setText(f"Error generating flags: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

    def update_flags_display(self, flags: List[TradingFlag]):
        """Update the flags table display"""
        self.flags_table.setRowCount(len(flags))
        
        for row, flag in enumerate(flags):
            # Agent
            agent_item = QTableWidgetItem(flag.agent_id.value.replace("_", "-").title())
            self.flags_table.setItem(row, 0, agent_item)
            
            # Flag type
            flag_type_item = QTableWidgetItem(flag.flag_type.value.replace("_", " ").title())
            self._set_flag_type_color(flag_type_item, flag.flag_type)
            self.flags_table.setItem(row, 1, flag_type_item)
            
            # Strength
            strength_item = QTableWidgetItem(flag.strength.value.replace("_", " ").title())
            self._set_strength_color(strength_item, flag.strength)
            self.flags_table.setItem(row, 2, strength_item)
            
            # Price target
            price_item = QTableWidgetItem(f"${flag.price_target:.2f}")
            self.flags_table.setItem(row, 3, price_item)
            
            # Confidence
            confidence_item = QTableWidgetItem(f"{flag.confidence:.1%}")
            self._set_confidence_color(confidence_item, flag.confidence)
            self.flags_table.setItem(row, 4, confidence_item)
            
            # Reasoning
            reasoning_item = QTableWidgetItem(flag.reasoning)
            self.flags_table.setItem(row, 5, reasoning_item)
            
            # Timestamp
            timestamp_item = QTableWidgetItem(flag.timestamp[:19])  # Remove microseconds
            self.flags_table.setItem(row, 6, timestamp_item)
            
            # Expires
            expires_item = QTableWidgetItem(flag.expires_at[:19])
            self.flags_table.setItem(row, 7, expires_item)
        
        # Resize columns to fit content
        self.flags_table.resizeColumnsToContents()

    def _set_flag_type_color(self, item: QTableWidgetItem, flag_type: FlagType):
        """Set color based on flag type"""
        if flag_type in [FlagType.BUY, FlagType.STRONG_BUY]:
            item.setBackground(QColor(144, 238, 144))  # Light green
        elif flag_type in [FlagType.SELL, FlagType.STRONG_SELL]:
            item.setBackground(QColor(255, 182, 193))  # Light red
        else:
            item.setBackground(QColor(255, 255, 224))  # Light yellow

    def _set_strength_color(self, item: QTableWidgetItem, strength):
        """Set color based on flag strength"""
        if strength.value == "very_strong":
            item.setBackground(QColor(255, 0, 0))  # Red
            item.setForeground(QColor(255, 255, 255))  # White text
        elif strength.value == "strong":
            item.setBackground(QColor(255, 165, 0))  # Orange
        elif strength.value == "moderate":
            item.setBackground(QColor(255, 255, 0))  # Yellow
        else:
            item.setBackground(QColor(192, 192, 192))  # Light gray

    def _set_confidence_color(self, item: QTableWidgetItem, confidence: float):
        """Set color based on confidence level"""
        if confidence >= 0.8:
            item.setBackground(QColor(144, 238, 144))  # Light green
        elif confidence >= 0.6:
            item.setBackground(QColor(255, 255, 224))  # Light yellow
        else:
            item.setBackground(QColor(255, 182, 193))  # Light red

    def show_consensus(self):
        """Show consensus analysis"""
        active_flags = self.flag_engine.get_active_flags()
        
        if not active_flags:
            self.consensus_label.setText("No flags available for consensus")
            self.consensus_details.clear()
            return
        
        # Generate consensus
        consensus_flag = self.flag_engine.get_consensus_flag(active_flags)
        
        if consensus_flag:
            # Update consensus label
            consensus_text = f"Consensus: {consensus_flag.flag_type.value.replace('_', ' ').title()} - {consensus_flag.confidence:.1%} Confidence"
            self.consensus_label.setText(consensus_text)
            
            # Update consensus details
            details = f"""
Consensus Analysis:
• Flag Type: {consensus_flag.flag_type.value.replace('_', ' ').title()}
• Strength: {consensus_flag.strength.value.replace('_', ' ').title()}
• Price Target: ${consensus_flag.price_target:.2f}
• Confidence: {consensus_flag.confidence:.1%}
• Participating Agents: {consensus_flag.metadata.get('participating_agents', 0)}

Reasoning: {consensus_flag.reasoning}

Flag Distribution:
"""
            
            # Add flag distribution
            flag_dist = consensus_flag.metadata.get('flag_distribution', {})
            for flag_type, count in flag_dist.items():
                details += f"• {flag_type.replace('_', ' ').title()}: {count} agents\n"
            
            self.consensus_details.setText(details)
            
            # Update status
            self.status_label.setText(f"Consensus generated at {datetime.now().strftime('%H:%M:%S')}")
            self.status_label.setStyleSheet("color: blue;")

    def refresh_flags(self):
        """Refresh flags display"""
        active_flags = self.flag_engine.get_active_flags()
        self.update_flags_display(active_flags)
        
        # Clean up expired flags
        self.flag_engine.expire_old_flags()
        
        self.status_label.setText(f"Refreshed {len(active_flags)} flags at {datetime.now().strftime('%H:%M:%S')}")
        self.status_label.setStyleSheet("color: green;")

    def save_flags(self):
        """Save flags to file"""
        try:
            filename = self.flag_engine.save_flags_to_file()
            self.status_label.setText(f"Flags saved to {filename}")
            self.status_label.setStyleSheet("color: green;")
        except Exception as e:
            self.status_label.setText(f"Error saving flags: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

    def filter_flags(self):
        """Filter flags based on selected criteria"""
        # This would implement filtering logic
        # For now, just refresh the display
        self.refresh_flags()

    def auto_refresh(self):
        """Auto-refresh flags"""
        # Clean up expired flags
        self.flag_engine.expire_old_flags()
        
        # Update display if there are active flags
        active_flags = self.flag_engine.get_active_flags()
        if active_flags:
            self.update_flags_display(active_flags)

    def update_stock_data(self, stock_data: Dict[str, Any]):
        """Update flags based on new stock data"""
        self.generate_flags(stock_data)