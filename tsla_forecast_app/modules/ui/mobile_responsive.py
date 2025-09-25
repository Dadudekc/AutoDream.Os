#!/usr/bin/env python3
"""
Mobile Responsive Component
==========================

Mobile-responsive design utilities and adaptive layouts
V2 Compliant: ≤200 lines, focused responsive design
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QGridLayout, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from typing import Dict, Any, List


class ResponsiveLayout(QVBoxLayout):
    """Responsive layout that adapts to screen size"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen_size = "desktop"
        self.setup_responsive_styles()

    def setup_responsive_styles(self):
        """Setup responsive styling based on screen size"""
        if self.screen_size == "mobile":
            self.setSpacing(5)
            self.setContentsMargins(5, 5, 5, 5)
        elif self.screen_size == "tablet":
            self.setSpacing(10)
            self.setContentsMargins(10, 10, 10, 10)
        else:  # desktop
            self.setSpacing(15)
            self.setContentsMargins(15, 15, 15, 15)

    def update_screen_size(self, size: str):
        """Update screen size and adjust layout"""
        self.screen_size = size
        self.setup_responsive_styles()


class MobileResponsiveWidget(QWidget):
    """Base widget with mobile-responsive capabilities"""
    
    # Signals
    screen_size_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.screen_size = "desktop"
        self.responsive_elements = []
        self.init_responsive_ui()

    def init_responsive_ui(self):
        """Initialize responsive UI"""
        self.main_layout = ResponsiveLayout(self)
        self.setLayout(self.main_layout)
        self.setup_responsive_styles()

    def setup_responsive_styles(self):
        """Setup responsive styles based on screen size"""
        if self.screen_size == "mobile":
            self.setStyleSheet("""
                QWidget {
                    font-size: 14px;
                    padding: 5px;
                }
                QGroupBox {
                    font-size: 12px;
                    margin: 5px;
                }
                QPushButton {
                    min-height: 40px;
                    font-size: 14px;
                    padding: 8px;
                }
                QLabel {
                    font-size: 12px;
                }
            """)
        elif self.screen_size == "tablet":
            self.setStyleSheet("""
                QWidget {
                    font-size: 16px;
                    padding: 10px;
                }
                QGroupBox {
                    font-size: 14px;
                    margin: 10px;
                }
                QPushButton {
                    min-height: 45px;
                    font-size: 16px;
                    padding: 10px;
                }
                QLabel {
                    font-size: 14px;
                }
            """)
        else:  # desktop
            self.setStyleSheet("""
                QWidget {
                    font-size: 18px;
                    padding: 15px;
                }
                QGroupBox {
                    font-size: 16px;
                    margin: 15px;
                }
                QPushButton {
                    min-height: 50px;
                    font-size: 18px;
                    padding: 12px;
                }
                QLabel {
                    font-size: 16px;
                }
            """)

    def add_responsive_element(self, element):
        """Add element to responsive tracking"""
        self.responsive_elements.append(element)

    def update_screen_size(self, size: str):
        """Update screen size and refresh UI"""
        self.screen_size = size
        self.setup_responsive_styles()
        self.screen_size_changed.emit(size)
        
        # Update responsive elements
        for element in self.responsive_elements:
            if hasattr(element, 'update_screen_size'):
                element.update_screen_size(size)

    def get_responsive_font_size(self, base_size: int) -> int:
        """Get responsive font size based on screen size"""
        if self.screen_size == "mobile":
            return max(base_size - 4, 10)
        elif self.screen_size == "tablet":
            return base_size - 2
        else:  # desktop
            return base_size

    def get_responsive_spacing(self, base_spacing: int) -> int:
        """Get responsive spacing based on screen size"""
        if self.screen_size == "mobile":
            return max(base_spacing // 2, 2)
        elif self.screen_size == "tablet":
            return int(base_spacing * 0.75)
        else:  # desktop
            return base_spacing


class MobileTradingCard(QWidget):
    """Mobile-optimized trading information card"""
    
    def __init__(self, title: str = "Trading Info"):
        super().__init__()
        self.title = title
        self.init_ui()

    def init_ui(self):
        """Initialize mobile trading card UI"""
        layout = QVBoxLayout()
        
        # Card header
        header_frame = QFrame()
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel(self.title)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
        # Card content
        self.content_group = QGroupBox()
        content_layout = QGridLayout()
        
        # Price display
        self.price_label = QLabel("$0.00")
        self.price_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.price_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.price_label, 0, 0, 1, 2)
        
        # Change display
        self.change_label = QLabel("$0.00 (0.00%)")
        self.change_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.change_label, 1, 0, 1, 2)
        
        # Volume display
        self.volume_label = QLabel("Volume: 0")
        content_layout.addWidget(self.volume_label, 2, 0)
        
        # Time display
        self.time_label = QLabel("Last Update: Never")
        content_layout.addWidget(self.time_label, 2, 1)
        
        self.content_group.setLayout(content_layout)
        layout.addWidget(self.content_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.buy_button = QPushButton("🟢 BUY")
        self.buy_button.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
        """)
        button_layout.addWidget(self.buy_button)
        
        self.sell_button = QPushButton("🔴 SELL")
        self.sell_button.setStyleSheet("""
            QPushButton {
                background-color: #aa0000;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
        """)
        button_layout.addWidget(self.sell_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_data(self, data: Dict[str, Any]):
        """Update card data"""
        if not data:
            return
            
        # Update price
        price = data.get('price', 0)
        self.price_label.setText(f"${price:.2f}")
        
        # Update change
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        change_color = "green" if change >= 0 else "red"
        self.change_label.setText(f"${change:.2f} ({change_percent:.2f}%)")
        self.change_label.setStyleSheet(f"color: {change_color}")
        
        # Update volume
        volume = data.get('volume', 0)
        self.volume_label.setText(f"Volume: {volume:,}")
        
        # Update timestamp
        timestamp = data.get('timestamp', 'Unknown')
        self.time_label.setText(f"Last Update: {timestamp}")


class ResponsiveScrollArea(QScrollArea):
    """Responsive scroll area for mobile devices"""
    
    def __init__(self):
        super().__init__()
        self.setup_responsive_scroll()

    def setup_responsive_scroll(self):
        """Setup responsive scrolling behavior"""
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Mobile-friendly scrolling
        self.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background-color: #f0f0f0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)

    def add_responsive_widget(self, widget: QWidget):
        """Add responsive widget to scroll area"""
        self.setWidget(widget)






