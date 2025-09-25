#!/usr/bin/env python3
"""
Tesla Stock App Modules Package
===============================

Tesla Stock Forecast App Modules Package
V2 Compliant: Modular design with focused components
"""

from .main_app import TeslaStockApp, create_app, main
from .data_worker import StockDataWorker
from .ui_components import (
    StockDisplayWidget,
    ForecastDisplayWidget,
    LogDisplayWidget,
    SettingsDisplayWidget,
    ChartDisplayWidget,
    ProfessionalTheme,
    ResponsiveLayout,
    ResponsiveWidget
)
from .trading_flags import (
    TradingFlagEngine,
    TradingFlag,
    FlagType,
    FlagStrength,
    AgentFlag,
    MarketAnalysis
)
from .flag_display import TradingFlagsDisplay

__all__ = [
    # Main application
    "TeslaStockApp",
    "create_app",
    "main",
    
    # Data worker
    "StockDataWorker",
    
    # UI components
    "StockDisplayWidget",
    "ForecastDisplayWidget",
    "LogDisplayWidget",
    "SettingsDisplayWidget",
    "ChartDisplayWidget",
    "ProfessionalTheme",
    "ResponsiveLayout",
    "ResponsiveWidget",
    
    # Trading flags
    "TradingFlagEngine",
    "TradingFlag",
    "FlagType",
    "FlagStrength",
    "AgentFlag",
    "MarketAnalysis",
    "TradingFlagsDisplay"
]