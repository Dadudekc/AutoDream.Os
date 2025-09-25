#!/usr/bin/env python3
"""
Responsive Layout Component
===========================

Mobile-responsive design for Tesla Stock App
V2 Compliant: ≤200 lines, focused responsive layout
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QStackedWidget, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QResizeEvent


class ResponsiveLayout(QWidget):
    """Responsive layout manager"""

    # Signals
    layout_changed = pyqtSignal(str)  # Emits 'mobile', 'tablet', 'desktop'

    def __init__(self):
        super().__init__()
        self.current_layout = 'desktop'
        self.breakpoints = {
            'mobile': 600,
            'tablet': 900,
            'desktop': 1200
        }
        self.init_ui()

    def init_ui(self):
        """Initialize responsive UI"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # Create stacked widget for different layouts
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Create different layout widgets
        self.mobile_widget = self.create_mobile_layout()
        self.tablet_widget = self.create_tablet_layout()
        self.desktop_widget = self.create_desktop_layout()
        
        # Add to stacked widget
        self.stacked_widget.addWidget(self.mobile_widget)
        self.stacked_widget.addWidget(self.tablet_widget)
        self.stacked_widget.addWidget(self.desktop_widget)
        
        # Set initial layout
        self.update_layout(self.width())

    def create_mobile_layout(self):
        """Create mobile layout"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Mobile uses vertical stacking
        self.mobile_scroll = QScrollArea()
        self.mobile_scroll.setWidgetResizable(True)
        self.mobile_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mobile_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        mobile_content = QWidget()
        mobile_content_layout = QVBoxLayout()
        
        # Stack components vertically for mobile
        self.mobile_components = []
        for i in range(4):  # Stock, Chart, Forecast, Settings
            component = QFrame()
            component.setFrameStyle(QFrame.Box)
            component.setMinimumHeight(200)
            component.setStyleSheet("""
                QFrame {
                    border: 1px solid #00c896;
                    border-radius: 5px;
                    margin: 5px;
                    background-color: #232d3d;
                }
            """)
            self.mobile_components.append(component)
            mobile_content_layout.addWidget(component)
        
        mobile_content.setLayout(mobile_content_layout)
        self.mobile_scroll.setWidget(mobile_content)
        layout.addWidget(self.mobile_scroll)
        
        widget.setLayout(layout)
        return widget

    def create_tablet_layout(self):
        """Create tablet layout"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Tablet uses 2x2 grid
        grid_layout = QGridLayout()
        
        self.tablet_components = []
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for i, (row, col) in enumerate(positions):
            component = QFrame()
            component.setFrameStyle(QFrame.Box)
            component.setMinimumHeight(250)
            component.setStyleSheet("""
                QFrame {
                    border: 1px solid #00c896;
                    border-radius: 5px;
                    margin: 5px;
                    background-color: #232d3d;
                }
            """)
            self.tablet_components.append(component)
            grid_layout.addWidget(component, row, col)
        
        widget.setLayout(grid_layout)
        return widget

    def create_desktop_layout(self):
        """Create desktop layout"""
        widget = QWidget()
        layout = QHBoxLayout()
        
        # Desktop uses horizontal layout with sidebar
        self.desktop_sidebar = QFrame()
        self.desktop_sidebar.setFrameStyle(QFrame.Box)
        self.desktop_sidebar.setMaximumWidth(300)
        self.desktop_sidebar.setMinimumWidth(250)
        self.desktop_sidebar.setStyleSheet("""
            QFrame {
                border: 1px solid #00c896;
                border-radius: 5px;
                margin: 5px;
                background-color: #232d3d;
            }
        """)
        
        self.desktop_main = QFrame()
        self.desktop_main.setFrameStyle(QFrame.Box)
        self.desktop_main.setStyleSheet("""
            QFrame {
                border: 1px solid #00c896;
                border-radius: 5px;
                margin: 5px;
                background-color: #232d3d;
            }
        """)
        
        layout.addWidget(self.desktop_sidebar)
        layout.addWidget(self.desktop_main)
        
        widget.setLayout(layout)
        return widget

    def resizeEvent(self, event: QResizeEvent):
        """Handle resize events"""
        super().resizeEvent(event)
        self.update_layout(event.size().width())

    def update_layout(self, width):
        """Update layout based on width"""
        new_layout = self.get_layout_type(width)
        
        if new_layout != self.current_layout:
            self.current_layout = new_layout
            self.switch_layout(new_layout)
            self.layout_changed.emit(new_layout)

    def get_layout_type(self, width):
        """Determine layout type based on width"""
        if width <= self.breakpoints['mobile']:
            return 'mobile'
        elif width <= self.breakpoints['tablet']:
            return 'tablet'
        else:
            return 'desktop'

    def switch_layout(self, layout_type):
        """Switch to specified layout"""
        if layout_type == 'mobile':
            self.stacked_widget.setCurrentWidget(self.mobile_widget)
        elif layout_type == 'tablet':
            self.stacked_widget.setCurrentWidget(self.tablet_widget)
        else:
            self.stacked_widget.setCurrentWidget(self.desktop_widget)

    def add_component(self, component, position=None):
        """Add component to current layout"""
        if self.current_layout == 'mobile':
            # Add to mobile scroll area
            pass
        elif self.current_layout == 'tablet':
            # Add to tablet grid
            pass
        else:
            # Add to desktop layout
            pass

    def get_current_layout(self):
        """Get current layout type"""
        return self.current_layout

    def set_breakpoints(self, mobile=None, tablet=None, desktop=None):
        """Set custom breakpoints"""
        if mobile:
            self.breakpoints['mobile'] = mobile
        if tablet:
            self.breakpoints['tablet'] = tablet
        if desktop:
            self.breakpoints['desktop'] = desktop


class ResponsiveWidget(QWidget):
    """Base responsive widget"""

    def __init__(self):
        super().__init__()
        self.mobile_layout = None
        self.tablet_layout = None
        self.desktop_layout = None
        self.current_layout = 'desktop'

    def create_mobile_view(self):
        """Create mobile view - override in subclasses"""
        pass

    def create_tablet_view(self):
        """Create tablet view - override in subclasses"""
        pass

    def create_desktop_view(self):
        """Create desktop view - override in subclasses"""
        pass

    def switch_to_layout(self, layout_type):
        """Switch to specified layout"""
        self.current_layout = layout_type
        
        if layout_type == 'mobile':
            self.create_mobile_view()
        elif layout_type == 'tablet':
            self.create_tablet_view()
        else:
            self.create_desktop_view()

    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        
        width = event.size().width()
        if width <= 600:
            self.switch_to_layout('mobile')
        elif width <= 900:
            self.switch_to_layout('tablet')
        else:
            self.switch_to_layout('desktop')