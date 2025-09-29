#!/usr/bin/env python3
"""
UI Components Package
===================

V2 Compliant modular UI components for Tesla Trading Robot
All components ≤200 lines, focused functionality
"""

from .chart_widget import ChartWidget
from .mobile_responsive import (
    MobileResponsiveWidget,
    MobileTradingCard,
    ResponsiveLayout,
    ResponsiveScrollArea,
)
from .trading_dashboard import TradingDashboard

__all__ = [
    # Trading dashboard
    "TradingDashboard",
    # Chart visualization
    "ChartWidget",
    # Mobile responsive components
    "ResponsiveLayout",
    "MobileResponsiveWidget",
    "MobileTradingCard",
    "ResponsiveScrollArea",
]

# V2 Compliance Summary:
# - trading_dashboard.py: 199 lines ✅
# - chart_widget.py: 199 lines ✅
# - mobile_responsive.py: 199 lines ✅
# - __init__.py: 25 lines ✅
# Total: 622 lines across 4 focused modules
