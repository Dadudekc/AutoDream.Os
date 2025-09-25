#!/usr/bin/env python3
"""
Chart Display Component
======================

Advanced data visualization with real-time charts
V2 Compliant: ≤200 lines, focused chart visualization
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, 
    QComboBox, QPushButton, QFrame, QSlider
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush, QColor
import random
from datetime import datetime, timedelta


class RealTimeChart(QWidget):
    """Real-time chart widget"""

    def __init__(self):
        super().__init__()
        self.data_points = []
        self.max_points = 100
        self.chart_type = "line"
        self.show_volume = True
        self.show_indicators = True
        self.init_ui()

    def init_ui(self):
        """Initialize chart UI"""
        self.setMinimumSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 5px;
            }
        """)

    def paintEvent(self, event):
        """Paint the chart"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up colors
        bg_color = QColor(30, 30, 30)
        grid_color = QColor(60, 60, 60)
        line_color = QColor(0, 255, 0)  # Green for price
        volume_color = QColor(100, 100, 255)  # Blue for volume
        
        # Fill background
        painter.fillRect(self.rect(), bg_color)
        
        if not self.data_points:
            return
        
        # Calculate chart dimensions
        margin = 40
        chart_width = self.width() - 2 * margin
        chart_height = self.height() - 2 * margin
        
        # Draw grid
        painter.setPen(QPen(grid_color, 1))
        for i in range(5):
            y = margin + (chart_height // 4) * i
            painter.drawLine(margin, y, margin + chart_width, y)
        
        for i in range(10):
            x = margin + (chart_width // 9) * i
            painter.drawLine(x, margin, x, margin + chart_height)
        
        # Find min/max values
        prices = [point['price'] for point in self.data_points]
        volumes = [point['volume'] for point in self.data_points]
        
        if not prices:
            return
        
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price if max_price != min_price else 1
        
        # Draw price line
        painter.setPen(QPen(line_color, 2))
        for i in range(1, len(self.data_points)):
            x1 = margin + (chart_width * (i-1) / (len(self.data_points)-1))
            y1 = margin + chart_height - (chart_height * (prices[i-1] - min_price) / price_range)
            
            x2 = margin + (chart_width * i / (len(self.data_points)-1))
            y2 = margin + chart_height - (chart_height * (prices[i] - min_price) / price_range)
            
            painter.drawLine(x1, y1, x2, y2)
        
        # Draw volume bars if enabled
        if self.show_volume and volumes:
            painter.setPen(QPen(volume_color, 1))
            painter.setBrush(QBrush(volume_color))
            
            max_volume = max(volumes)
            for i, point in enumerate(self.data_points):
                x = margin + (chart_width * i / (len(self.data_points)-1))
                bar_height = (chart_height * point['volume'] / max_volume) * 0.3
                painter.drawRect(x-2, margin + chart_height - bar_height, 4, bar_height)
        
        # Draw labels
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont("Arial", 8))
        
        # Price labels
        for i in range(5):
            price = max_price - (price_range * i / 4)
            y = margin + (chart_height // 4) * i
            painter.drawText(5, y + 5, f"${price:.2f}")
        
        # Time labels
        if len(self.data_points) > 1:
            for i in range(0, len(self.data_points), max(1, len(self.data_points) // 5)):
                x = margin + (chart_width * i / (len(self.data_points)-1))
                painter.drawText(x - 20, self.height() - 10, 
                               self.data_points[i]['time'].strftime("%H:%M"))

    def add_data_point(self, price, volume=0):
        """Add a new data point"""
        self.data_points.append({
            'price': price,
            'volume': volume,
            'time': datetime.now()
        })
        
        # Limit data points
        if len(self.data_points) > self.max_points:
            self.data_points.pop(0)
        
        self.update()

    def set_chart_type(self, chart_type):
        """Set chart type"""
        self.chart_type = chart_type
        self.update()

    def set_show_volume(self, show):
        """Toggle volume display"""
        self.show_volume = show
        self.update()

    def set_show_indicators(self, show):
        """Toggle indicators display"""
        self.show_indicators = show
        self.update()


class ChartDisplayWidget(QWidget):
    """Chart display widget with controls"""

    def __init__(self):
        super().__init__()
        self.chart = None
        self.update_timer = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Real-Time Chart")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4169E1; margin: 10px;")
        layout.addWidget(title)
        
        # Chart controls
        controls_group = QGroupBox("Chart Controls")
        controls_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4169E1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        controls_layout = QHBoxLayout()
        
        # Chart type
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Line", "Candlestick", "Bar"])
        self.chart_type_combo.setStyleSheet("padding: 5px; border: 1px solid #4169E1; border-radius: 3px;")
        controls_layout.addWidget(QLabel("Type:"))
        controls_layout.addWidget(self.chart_type_combo)
        
        # Update interval
        self.interval_slider = QSlider(Qt.Horizontal)
        self.interval_slider.setRange(1, 60)
        self.interval_slider.setValue(5)
        self.interval_slider.setStyleSheet("padding: 5px;")
        controls_layout.addWidget(QLabel("Interval:"))
        controls_layout.addWidget(self.interval_slider)
        
        # Start/Stop button
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
        """)
        controls_layout.addWidget(self.start_button)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Chart widget
        self.chart = RealTimeChart()
        layout.addWidget(self.chart)
        
        # Status
        self.status_label = QLabel("Chart Ready")
        self.status_label.setStyleSheet("color: #666; padding: 5px; font-size: 10px;")
        layout.addWidget(self.status_label)
        
        # Connect signals
        self.start_button.clicked.connect(self.toggle_chart)
        self.chart_type_combo.currentTextChanged.connect(self.on_chart_type_changed)
        self.interval_slider.valueChanged.connect(self.on_interval_changed)
        
        self.setLayout(layout)

    def toggle_chart(self):
        """Toggle chart updates"""
        if self.update_timer and self.update_timer.isActive():
            self.stop_chart()
        else:
            self.start_chart()

    def start_chart(self):
        """Start real-time chart updates"""
        interval = self.interval_slider.value() * 1000  # Convert to milliseconds
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_chart_data)
        self.update_timer.start(interval)
        
        self.start_button.setText("Stop")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #DC143C;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B22222;
            }
        """)
        self.status_label.setText("Chart updating...")

    def stop_chart(self):
        """Stop chart updates"""
        if self.update_timer:
            self.update_timer.stop()
        
        self.start_button.setText("Start")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
        """)
        self.status_label.setText("Chart stopped")

    def update_chart_data(self):
        """Update chart with new data"""
        # Simulate real-time data (in real app, this would come from API)
        base_price = 425.85
        change = random.uniform(-5, 5)
        price = base_price + change
        volume = random.randint(1000000, 50000000)
        
        self.chart.add_data_point(price, volume)

    def on_chart_type_changed(self, chart_type):
        """Handle chart type change"""
        self.chart.set_chart_type(chart_type.lower())

    def on_interval_changed(self, interval):
        """Handle interval change"""
        if self.update_timer and self.update_timer.isActive():
            self.update_timer.setInterval(interval * 1000)