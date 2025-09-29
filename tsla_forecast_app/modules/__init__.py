#!/usr/bin/env python3
"""
Tesla Stock App Modules Package
===============================

Tesla Stock Forecast App Modules Package
V2 Compliant: Modular design with focused components
"""

from .data_worker import StockDataWorker
from .flag_display import TradingFlagsDisplay
from .main_app import TeslaStockApp, create_app, main
from .trading_flags import (
    AgentFlag,
    FlagStrength,
    FlagType,
    MarketAnalysis,
    TradingFlag,
    TradingFlagEngine,
)
from .ui_components import (
    ChartDisplayWidget,
    ForecastDisplayWidget,
    LogDisplayWidget,
    ProfessionalTheme,
    ResponsiveLayout,
    ResponsiveWidget,
    SettingsDisplayWidget,
    StockDisplayWidget,
)

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
    "TradingFlagsDisplay",
]
