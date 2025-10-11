#!/usr/bin/env python3
"""
Trading Strategies Module - V2 Compliant
========================================

Trading strategies module following V2 compliance principles.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

from .base_strategy import TradingStrategy
from .moving_average_strategy import MovingAverageStrategy
from .rsi_strategy import RSIMeanReversionStrategy
from .bollinger_bands_strategy import BollingerBandsStrategy

__all__ = [
    'TradingStrategy',
    'MovingAverageStrategy', 
    'RSIMeanReversionStrategy',
    'BollingerBandsStrategy'
]