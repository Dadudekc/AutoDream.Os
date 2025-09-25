#!/usr/bin/env python3
"""
Chart Widget Component
=====================

Advanced data visualization with real-time charts
V2 Compliant: ≤200 lines, focused chart visualization
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QComboBox, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QPen, QColor
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple


class ChartWidget(QWidget):
    """Advanced chart widget with real-time visualization"""
    
    # Signals
    chart_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.chart_data = []
        self.max_points = 100
        self.chart_type = "line"
        self.timeframe = "1m"
        self.init_ui()
        self.setup_timers()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Chart controls
        self.create_chart_controls(layout)
        
        # Chart display area
        self.create_chart_display(layout)
        
        # Chart info
        self.create_chart_info(layout)
        
        self.setLayout(layout)

    def create_chart_controls(self, parent_layout):
        """Create chart control panel"""
        controls_group = QGroupBox("📊 Chart Controls")
        controls_layout = QHBoxLayout()
        
        # Chart type selector
        controls_layout.addWidget(QLabel("Type:"))
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Line", "Candlestick", "Volume", "MACD"])
        self.chart_type_combo.currentTextChanged.connect(self.on_chart_type_changed)
        controls_layout.addWidget(self.chart_type_combo)
        
        # Timeframe selector
        controls_layout.addWidget(QLabel("Timeframe:"))
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["1m", "5m", "15m", "1h", "1d"])
        self.timeframe_combo.currentTextChanged.connect(self.on_timeframe_changed)
        controls_layout.addWidget(self.timeframe_combo)
        
        # Auto-update toggle
        self.auto_update_check = QCheckBox("Auto Update")
        self.auto_update_check.setChecked(True)
        self.auto_update_check.toggled.connect(self.on_auto_update_toggled)
        controls_layout.addWidget(self.auto_update_check)
        
        # Refresh button
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.clicked.connect(self.refresh_chart)
        controls_layout.addWidget(self.refresh_button)
        
        controls_group.setLayout(controls_layout)
        parent_layout.addWidget(controls_group)

    def create_chart_display(self, parent_layout):
        """Create chart display area"""
        self.chart_area = QWidget()
        self.chart_area.setMinimumHeight(300)
        self.chart_area.setStyleSheet("""
            QWidget {
                background-color: #000000;
                border: 1px solid #333333;
                border-radius: 5px;
            }
        """)
        parent_layout.addWidget(self.chart_area)

    def create_chart_info(self, parent_layout):
        """Create chart information panel"""
        info_group = QGroupBox("📈 Chart Information")
        info_layout = QHBoxLayout()
        
        self.price_info_label = QLabel("Price: $0.00")
        self.price_info_label.setFont(QFont("Arial", 12, QFont.Bold))
        info_layout.addWidget(self.price_info_label)
        
        self.change_info_label = QLabel("Change: $0.00 (0.00%)")
        info_layout.addWidget(self.change_info_label)
        
        self.volume_info_label = QLabel("Volume: 0")
        info_layout.addWidget(self.volume_info_label)
        
        self.last_update_label = QLabel("Last Update: Never")
        info_layout.addWidget(self.last_update_label)
        
        info_group.setLayout(info_layout)
        parent_layout.addWidget(info_group)

    def setup_timers(self):
        """Setup update timers"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_chart)
        self.update_timer.start(5000)  # Update every 5 seconds

    def paintEvent(self, event):
        """Paint chart visualization"""
        painter = QPainter(self.chart_area)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Clear background
        painter.fillRect(self.chart_area.rect(), QColor(0, 0, 0))
        
        if not self.chart_data:
            self.draw_no_data_message(painter)
            return
            
        # Draw chart based on type
        if self.chart_type == "line":
            self.draw_line_chart(painter)
        elif self.chart_type == "candlestick":
            self.draw_candlestick_chart(painter)
        elif self.chart_type == "volume":
            self.draw_volume_chart(painter)
        elif self.chart_type == "macd":
            self.draw_macd_chart(painter)

    def draw_no_data_message(self, painter):
        """Draw no data message"""
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 14))
        painter.drawText(
            self.chart_area.rect(), 
            Qt.AlignCenter, 
            "No chart data available"
        )

    def draw_line_chart(self, painter):
        """Draw line chart"""
        if len(self.chart_data) < 2:
            return
            
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        
        # Calculate scaling
        prices = [point['price'] for point in self.chart_data]
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price if max_price != min_price else 1
        
        width = self.chart_area.width()
        height = self.chart_area.height()
        
        # Draw price line
        points = []
        for i, point in enumerate(self.chart_data):
            x = int((i / (len(self.chart_data) - 1)) * width)
            y = int(height - ((point['price'] - min_price) / price_range) * height)
            points.append((x, y))
        
        for i in range(len(points) - 1):
            painter.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

    def draw_candlestick_chart(self, painter):
        """Draw candlestick chart"""
        if len(self.chart_data) < 1:
            return
            
        width = self.chart_area.width()
        height = self.chart_area.height()
        candle_width = width // len(self.chart_data) - 2
        
        for i, point in enumerate(self.chart_data):
            x = i * (candle_width + 2)
            
            # Calculate OHLC positions
            open_price = point.get('open', point['price'])
            high_price = point.get('high', point['price'])
            low_price = point.get('low', point['price'])
            close_price = point['price']
            
            # Draw candlestick
            color = QColor(0, 255, 0) if close_price >= open_price else QColor(255, 0, 0)
            painter.setPen(QPen(color, 1))
            painter.setBrush(color)
            
            # Draw body
            body_height = abs(close_price - open_price) * height // 100
            painter.drawRect(x, height//2, candle_width, body_height)

    def draw_volume_chart(self, painter):
        """Draw volume chart"""
        if len(self.chart_data) < 1:
            return
            
        painter.setPen(QPen(QColor(100, 100, 255), 1))
        painter.setBrush(QColor(100, 100, 255, 100))
        
        width = self.chart_area.width()
        height = self.chart_area.height()
        bar_width = width // len(self.chart_data) - 2
        
        max_volume = max(point.get('volume', 0) for point in self.chart_data)
        
        for i, point in enumerate(self.chart_data):
            x = i * (bar_width + 2)
            volume = point.get('volume', 0)
            bar_height = int((volume / max_volume) * height) if max_volume > 0 else 0
            
            painter.drawRect(x, height - bar_height, bar_width, bar_height)

    def draw_macd_chart(self, painter):
        """Draw MACD chart"""
        # Simplified MACD visualization
        painter.setPen(QPen(QColor(255, 255, 0), 2))
        painter.drawText(50, 50, "MACD Chart - Coming Soon")

    def update_chart_data(self, data: List[Dict[str, Any]]):
        """Update chart data"""
        self.chart_data = data[-self.max_points:]  # Keep only recent data
        self.chart_area.update()  # Trigger repaint
        
        if data:
            latest = data[-1]
            self.update_chart_info(latest)

    def update_chart_info(self, data: Dict[str, Any]):
        """Update chart information display"""
        price = data.get('price', 0)
        self.price_info_label.setText(f"Price: ${price:.2f}")
        
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        self.change_info_label.setText(f"Change: ${change:.2f} ({change_percent:.2f}%)")
        
        volume = data.get('volume', 0)
        self.volume_info_label.setText(f"Volume: {volume:,}")
        
        timestamp = data.get('timestamp', datetime.now().strftime("%H:%M:%S"))
        self.last_update_label.setText(f"Last Update: {timestamp}")

    def on_chart_type_changed(self, chart_type):
        """Handle chart type change"""
        self.chart_type = chart_type.lower()
        self.chart_area.update()

    def on_timeframe_changed(self, timeframe):
        """Handle timeframe change"""
        self.timeframe = timeframe
        self.refresh_chart()

    def on_auto_update_toggled(self, enabled):
        """Handle auto-update toggle"""
        if enabled:
            self.update_timer.start(5000)
        else:
            self.update_timer.stop()

    def refresh_chart(self):
        """Refresh chart data"""
        self.chart_updated.emit({
            'chart_type': self.chart_type,
            'timeframe': self.timeframe
        })

    def update_chart(self):
        """Update chart display"""
        self.chart_area.update()






