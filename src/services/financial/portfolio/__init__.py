"""
Portfolio Optimization Package

This package contains modules for portfolio optimization, risk management,
rebalancing, and performance tracking.

Modules:
- algorithms: Portfolio optimization algorithms (Sharpe ratio, minimum variance, etc.)
- risk_models: Risk modeling and risk metrics calculations
- rebalancing: Portfolio rebalancing logic and signal generation
- tracking: Portfolio performance tracking and analytics

Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

from .algorithms import (
    PortfolioOptimizationAlgorithms,
    OptimizationMethod,
    OptimizationConstraint,
    OptimizationResult
)

from .risk_models import (
    PortfolioRiskModels,
    RiskModelType,
    RiskMetrics,
    StressTestScenario
)

from .rebalancing import (
    PortfolioRebalancing,
    RebalancingFrequency,
    RebalancingTrigger,
    RebalancingSignal,
    RebalancingPlan
)

from .tracking import (
    PortfolioPerformanceTracker,
    PerformanceMetric,
    PortfolioAllocation,
    PerformanceSnapshot,
    PerformanceReport
)

__all__ = [
    # Algorithms
    "PortfolioOptimizationAlgorithms",
    "OptimizationMethod",
    "OptimizationConstraint",
    "OptimizationResult",
    
    # Risk Models
    "PortfolioRiskModels",
    "RiskModelType",
    "RiskMetrics",
    "StressTestScenario",
    
    # Rebalancing
    "PortfolioRebalancing",
    "RebalancingFrequency",
    "RebalancingTrigger",
    "RebalancingSignal",
    "RebalancingPlan",
    
    # Tracking
    "PortfolioPerformanceTracker",
    "PerformanceMetric",
    "PortfolioAllocation",
    "PerformanceSnapshot",
    "PerformanceReport"
]

__version__ = "1.0.0"
__author__ = "Agent-5 (Business Intelligence & Trading Specialist)"
__description__ = "Portfolio optimization and management system"

