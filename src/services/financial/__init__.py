"""
Financial Services Module - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

This module provides comprehensive financial automation, trading intelligence,
and market data analysis capabilities for the Agent_Cellphone_V2_Repository.
"""

__version__ = "1.0.0"
__author__ = "Business Intelligence Agent"
__status__ = "ACTIVE"

# Import services
from .portfolio_management_service import (
    PortfolioManager,
    PortfolioPosition,
    PortfolioMetrics,
)
from .risk_management_service import (
    RiskManager,
    RiskMetric,
    RiskAlert,
    PortfolioRiskProfile,
    RiskLevel,
    RiskType,
)
from .market_data_service import (
    MarketDataService,
    MarketData,
    HistoricalData,
    MarketSentiment,
)
from .trading_intelligence_service import (
    TradingIntelligenceService,
    TradingSignal,
    StrategyType,
    SignalType,
    SignalStrength,
    StrategyPerformance,
    MarketCondition,
)
from .options_trading_service import (
    OptionsTradingService,
    OptionContract,
    OptionsChain,
    OptionsStrategy,
    OptionType,
    OptionStrategy,
    Greeks,
)
from .financial_analytics_service import (
    FinancialAnalyticsService,
    BacktestResult,
    PerformanceMetrics,
    RiskAnalysis,
)
from .market_sentiment_service import (
    MarketSentimentService,
    SentimentData,
    SentimentAggregate,
    NewsArticle,
    MarketPsychology,
    SentimentSource,
    SentimentType,
)
from .portfolio_optimization_service import (
    PortfolioOptimizationService,
    OptimizationResult,
    RebalancingSignal,
    PortfolioAllocation,
    OptimizationMethod,
    RebalancingFrequency,
    OptimizationConstraint,
)

# Export main classes
__all__ = [
    # Portfolio Management
    "PortfolioManager",
    "PortfolioPosition",
    "PortfolioMetrics",
    # Risk Management
    "RiskManager",
    "RiskMetric",
    "RiskAlert",
    "PortfolioRiskProfile",
    "RiskLevel",
    "RiskType",
    # Market Data
    "MarketDataService",
    "MarketData",
    "HistoricalData",
    "MarketSentiment",
    # Trading Intelligence
    "TradingIntelligenceService",
    "TradingSignal",
    "StrategyType",
    "SignalType",
    "SignalStrength",
    "StrategyPerformance",
    "MarketCondition",
    # Options Trading
    "OptionsTradingService",
    "OptionContract",
    "OptionsChain",
    "OptionsStrategy",
    "OptionType",
    "Greeks",
    # Financial Analytics
    "FinancialAnalyticsService",
    "BacktestResult",
    "PerformanceMetrics",
    "RiskAnalysis",
    # Market Sentiment Analysis
    "MarketSentimentService",
    "SentimentData",
    "SentimentAggregate",
    "NewsArticle",
    "MarketPsychology",
    "SentimentSource",
    "SentimentType",
    # Portfolio Optimization
    "PortfolioOptimizationService",
    "OptimizationResult",
    "RebalancingSignal",
    "PortfolioAllocation",
    "OptimizationMethod",
    "RebalancingFrequency",
    "OptimizationConstraint",
]

# Version info
__version_info__ = (1, 0, 0)
