#!/usr/bin/env python3
"""
Trading BI Analytics Orchestrator
=================================

Main orchestrator for trading business intelligence analytics system.
Coordinates risk analysis, performance metrics, and market trend analysis.
V2 COMPLIANT: Focused orchestration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ORCHESTRATOR
@license MIT
"""

from datetime import datetime
from typing import Any

from ...repositories.trading_repository import TradingRepositoryInterface
from .market_trend_engine import create_market_trend_engine
from .performance_metrics_engine import create_performance_metrics_engine
from .risk_analysis_engine import create_risk_analysis_engine
from .trading_bi_models import (
    MarketTrend,
    PerformanceConfig,
    PerformanceMetrics,
    RiskAssessmentConfig,
    RiskMetrics,
    TrendAnalysisConfig,
)


class TradingBiAnalyticsOrchestrator:
    """Main orchestrator for trading BI analytics system."""

    def __init__(
        self,
        repository: TradingRepositoryInterface | None = None,
        risk_config: RiskAssessmentConfig | None = None,
        performance_config: PerformanceConfig | None = None,
        trend_config: TrendAnalysisConfig | None = None,
    ):
        """Initialize orchestrator with dependency injection."""
        self.repository = repository
        self.risk_engine = create_risk_analysis_engine(risk_config)
        self.performance_engine = create_performance_metrics_engine(performance_config)
        self.trend_engine = create_market_trend_engine(trend_config)

    async def calculate_real_time_pnl(self, symbol: str | None = None) -> dict[str, Any]:
        """Calculate real-time P&L for portfolio or specific symbol."""
        try:
            if symbol:
                return await self._calculate_symbol_pnl(symbol)
            else:
                return await self._calculate_portfolio_pnl()
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now()}

    async def _calculate_symbol_pnl(self, symbol: str) -> dict[str, Any]:
        """Calculate P&L for specific symbol."""
        if not self.repository:
            return {"error": "Repository not available", "timestamp": datetime.now()}

        position = await self.repository.get_position(symbol.upper())

        if not position:
            return {
                "symbol": symbol,
                "pnl": 0.0,
                "pnl_percentage": 0.0,
                "position_value": 0.0,
                "timestamp": datetime.now(),
            }

        # Calculate unrealized P&L
        unrealized_pnl = position.pnl
        position_value = position.quantity * position.current_price
        pnl_percentage = (unrealized_pnl / (position.quantity * position.average_price)) * 100

        return {
            "symbol": symbol,
            "pnl": unrealized_pnl,
            "pnl_percentage": pnl_percentage,
            "position_value": position_value,
            "timestamp": datetime.now(),
        }

    async def _calculate_portfolio_pnl(self) -> dict[str, Any]:
        """Calculate P&L for entire portfolio."""
        if not self.repository:
            return {"error": "Repository not available", "timestamp": datetime.now()}

        positions = await self.repository.get_all_positions()

        total_pnl = sum(position.pnl for position in positions)
        total_value = sum(position.quantity * position.current_price for position in positions)
        total_cost = sum(position.quantity * position.average_price for position in positions)

        pnl_percentage = (total_pnl / total_cost * 100) if total_cost > 0 else 0.0

        return {
            "total_pnl": total_pnl,
            "pnl_percentage": pnl_percentage,
            "total_value": total_value,
            "total_cost": total_cost,
            "position_count": len(positions),
            "timestamp": datetime.now(),
        }

    async def assess_portfolio_risk(self, portfolio_value: float) -> RiskMetrics:
        """Assess portfolio risk using risk analysis engine."""
        try:
            if not self.repository:
                return self.risk_engine._create_default_risk_metrics(portfolio_value)

            trades = await self.repository.get_all_trades(1000)
            return self.risk_engine.calculate_risk_metrics(trades, portfolio_value)

        except Exception:
            return self.risk_engine._create_default_risk_metrics(portfolio_value)

    async def generate_performance_report(self) -> PerformanceMetrics:
        """Generate comprehensive performance metrics report."""
        try:
            if not self.repository:
                return self.performance_engine._create_default_performance_metrics()

            trades = await self.repository.get_all_trades(1000)
            return self.performance_engine.calculate_performance_metrics(trades)

        except Exception:
            return self.performance_engine._create_default_performance_metrics()

    async def analyze_market_trends(self, symbol: str, timeframe: str = "medium") -> MarketTrend:
        """Analyze market trends using trend analysis engine."""
        try:
            if not self.repository:
                return self.trend_engine._create_default_trend(symbol, timeframe)

            trades = await self.repository.get_trades_by_symbol(symbol, 100)
            return self.trend_engine.analyze_market_trend(trades, symbol, timeframe)

        except Exception:
            return self.trend_engine._create_default_trend(symbol, timeframe)

    async def generate_comprehensive_report(
        self, symbols: list[str], portfolio_value: float
    ) -> dict[str, Any]:
        """Generate comprehensive analytics report."""
        try:
            # Generate all analytics in parallel
            performance_metrics = await self.generate_performance_report()
            risk_metrics = await self.assess_portfolio_risk(portfolio_value)

            # Analyze trends for each symbol
            trends = []
            for symbol in symbols:
                trend = await self.analyze_market_trends(symbol)
                trends.append(trend)

            # Get trend summary
            trend_summary = self.trend_engine.get_trend_summary(trends)

            return {
                "performance_metrics": performance_metrics,
                "risk_metrics": risk_metrics,
                "market_trends": trends,
                "trend_summary": trend_summary,
                "report_timestamp": datetime.now(),
                "symbols_analyzed": symbols,
            }

        except Exception as e:
            return {
                "error": str(e),
                "report_timestamp": datetime.now(),
                "symbols_analyzed": symbols,
            }

    def get_engine_status(self) -> dict[str, Any]:
        """Get status of all analytics engines."""
        return {
            "risk_engine": "active",
            "performance_engine": "active",
            "trend_engine": "active",
            "repository_available": self.repository is not None,
            "timestamp": datetime.now(),
        }


# Factory function for dependency injection
def create_trading_bi_analytics_orchestrator(
    repository: TradingRepositoryInterface | None = None,
    risk_config: RiskAssessmentConfig | None = None,
    performance_config: PerformanceConfig | None = None,
    trend_config: TrendAnalysisConfig | None = None,
) -> TradingBiAnalyticsOrchestrator:
    """Factory function to create trading BI analytics orchestrator with dependency
    injection."""
    return TradingBiAnalyticsOrchestrator(repository, risk_config, performance_config, trend_config)


# Export for DI
__all__ = ["TradingBiAnalyticsOrchestrator", "create_trading_bi_analytics_orchestrator"]
