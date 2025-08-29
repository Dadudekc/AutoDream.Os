#!/usr/bin/env python3
"""
Options Trading Package - Agent Cellphone V2
============================================

Modular options trading functionality extracted from the main service.
Follows V2 standards: ≤300 LOC per module, SRP, OOP principles.
"""

from .pricing import OptionsPricingEngine, OptionType, Greeks
from .risk import OptionsRiskManager, RiskMetrics
from .strategy import OptionsStrategyEngine, OptionsStrategy, OptionStrategy
from .market_data import OptionsMarketDataManager, OptionsChain, OptionContract

__all__ = [
    "OptionsPricingEngine",
    "OptionType", 
    "Greeks",
    "OptionsRiskManager",
    "RiskMetrics",
    "OptionsStrategyEngine",
    "OptionsStrategy",
    "OptionStrategy",
    "OptionsMarketDataManager",
    "OptionsChain",
    "OptionContract"
]

__version__ = "2.0.0"
__author__ = "Agent-3 (Integration & Testing Specialist)"
__status__ = "Production Ready"



