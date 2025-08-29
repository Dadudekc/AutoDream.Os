"""
Portfolio Management Package

This package provides portfolio rebalancing functionality with a modular architecture
following Single Responsibility Principle and V2 coding standards.
"""

from .rebalancing_core import (
    RebalancingCore,
    RebalancingPlan,
    RebalancingSignal,
    RebalancingFrequency,
    RebalancingTrigger,
)
from .portfolio_analysis import PortfolioAnalyzer
from .rebalancing_executor import RebalancingExecutor
from .rebalancing import PortfolioRebalancing
from .rebalancing_engine import RebalancingEngine, WeightSnapshot

__all__ = [
    "RebalancingCore",
    "RebalancingPlan",
    "RebalancingSignal",
    "RebalancingFrequency",
    "RebalancingTrigger",
    "PortfolioAnalyzer",
    "RebalancingExecutor",
    "PortfolioRebalancing",
    "RebalancingEngine",
    "WeightSnapshot",
]

__version__ = "2.0.0"
__author__ = "Agent Cellphone V2 Team"
__description__ = "Modular portfolio rebalancing system following SRP principles"
