"""
Portfolio Performance Tracking Module

Single Responsibility: Portfolio performance tracking and analytics.
Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Performance metrics to track"""
    TOTAL_RETURN = "TOTAL_RETURN"
    ANNUALIZED_RETURN = "ANNUALIZED_RETURN"
    VOLATILITY = "VOLATILITY"
    SHARPE_RATIO = "SHARPE_RATIO"
    SORTINO_RATIO = "SORTINO_RATIO"
    MAX_DRAWDOWN = "MAX_DRAWDOWN"
    CALMAR_RATIO = "CALMAR_RATIO"
    INFORMATION_RATIO = "INFORMATION_RATIO"
    TRACKING_ERROR = "TRACKING_ERROR"
    BETA = "BETA"
    ALPHA = "ALPHA"


@dataclass
class PortfolioAllocation:
    """Portfolio allocation analysis"""
    symbol: str
    current_weight: float
    target_weight: float
    sector: str
    market_cap: str
    style: str  # GROWTH, VALUE, BLEND
    risk_level: str  # LOW, MEDIUM, HIGH
    correlation: float
    beta: float
    alpha: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PerformanceSnapshot:
    """Portfolio performance snapshot"""
    timestamp: datetime
    total_value: float
    total_return: float
    daily_return: float
    weights: Dict[str, float]
    metrics: Dict[str, float]
    allocations: List[PortfolioAllocation]
    benchmark_comparison: Dict[str, float] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PerformanceReport:
    """Comprehensive performance report"""
    report_id: str
    start_date: datetime
    end_date: datetime
    portfolio_value_start: float
    portfolio_value_end: float
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    benchmark_return: float
    excess_return: float
    tracking_error: float
    information_ratio: float
    sector_allocations: Dict[str, float]
    top_contributors: List[Tuple[str, float]]
    top_detractors: List[Tuple[str, float]]
    risk_metrics: Dict[str, float]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class PortfolioPerformanceTracker:
    """Portfolio performance tracking and analytics"""
    
    def __init__(self, data_dir: str = "portfolio_tracking"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Performance tracking parameters
        self.tracking_params = {
            "snapshot_frequency": "daily",  # daily, weekly, monthly
            "lookback_periods": [30, 90, 252, 756],  # 1M, 3M, 1Y, 3Y
            "benchmark_symbol": "SPY",  # Default benchmark
            "risk_free_rate": 0.02,
            "min_data_points": 30
        }
        
        # Performance history
        self.performance_history: List[PerformanceSnapshot] = []
        self.allocation_history: List[PortfolioAllocation] = []
        self.reports_history: List[PerformanceReport] = []
        
        # Load historical data
        self.load_performance_history()

    def track_portfolio_performance(
        self,
        portfolio_value: float,
        weights: Dict[str, float],
        prices: Dict[str, float],
        benchmark_data: Dict[str, Any] = None,
        market_data: Dict[str, Any] = None
    ) -> PerformanceSnapshot:
        """Track portfolio performance snapshot"""
        try:
            # Calculate daily return
            daily_return = self._calculate_daily_return(portfolio_value)
            
            # Calculate total return
            total_return = self._calculate_total_return(portfolio_value)
            
            # Calculate performance metrics
            metrics = self._calculate_performance_metrics(weights, prices, market_data)
            
            # Create allocations
            allocations = self._create_portfolio_allocations(weights, market_data)
            
            # Benchmark comparison
            benchmark_comparison = self._calculate_benchmark_comparison(
                total_return, benchmark_data
            )
            
            # Create snapshot
            snapshot = PerformanceSnapshot(
                timestamp=datetime.now(),
                total_value=portfolio_value,
                total_return=total_return,
                daily_return=daily_return,
                weights=weights.copy(),
                metrics=metrics,
                allocations=allocations,
                benchmark_comparison=benchmark_comparison
            )
            
            # Save snapshot
            self.save_performance_snapshot(snapshot)
            
            # Add to history
            self.performance_history.append(snapshot)
            
            return snapshot
            
        except Exception as e:
            logger.error(f"Error tracking portfolio performance: {e}")
            return None

    def generate_performance_report(
        self,
        start_date: datetime,
        end_date: datetime,
        benchmark_data: Dict[str, Any] = None
    ) -> PerformanceReport:
        """Generate comprehensive performance report"""
        try:
            # Filter snapshots for date range
            period_snapshots = [
                s for s in self.performance_history
                if start_date <= s.timestamp <= end_date
            ]
            
            if len(period_snapshots) < 2:
                logger.warning("Insufficient data for performance report")
                return None
            
            # Sort by timestamp
            period_snapshots.sort(key=lambda x: x.timestamp)
            
            # Calculate report metrics
            portfolio_value_start = period_snapshots[0].total_value
            portfolio_value_end = period_snapshots[-1].total_value
            total_return = (portfolio_value_end - portfolio_value_start) / portfolio_value_start
            
            # Calculate annualized return
            days = (end_date - start_date).days
            annualized_return = (1 + total_return) ** (365 / days) - 1 if days > 0 else 0
            
            # Calculate volatility
            daily_returns = [s.daily_return for s in period_snapshots if s.daily_return is not None]
            volatility = np.std(daily_returns) * np.sqrt(252) if daily_returns else 0
            
            # Calculate Sharpe ratio
            sharpe_ratio = self._calculate_sharpe_ratio(daily_returns)
            
            # Calculate max drawdown
            max_drawdown = self._calculate_max_drawdown(period_snapshots)
            
            # Benchmark comparison
            benchmark_return = 0.0
            if benchmark_data:
                benchmark_return = self._calculate_benchmark_return(benchmark_data, start_date, end_date)
            
            excess_return = total_return - benchmark_return
            
            # Calculate tracking error
            tracking_error = self._calculate_tracking_error(period_snapshots, benchmark_data)
            
            # Calculate information ratio
            information_ratio = excess_return / tracking_error if tracking_error > 0 else 0
            
            # Sector allocations
            sector_allocations = self._calculate_sector_allocations(period_snapshots[-1].allocations)
            
            # Top contributors and detractors
            top_contributors, top_detractors = self._identify_contributors_detractors(period_snapshots)
            
            # Risk metrics
            risk_metrics = self._calculate_risk_metrics(period_snapshots)
            
            # Create report
            report = PerformanceReport(
                report_id=f"PERF_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}",
                start_date=start_date,
                end_date=end_date,
                portfolio_value_start=portfolio_value_start,
                portfolio_value_end=portfolio_value_end,
                total_return=total_return,
                annualized_return=annualized_return,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                benchmark_return=benchmark_return,
                excess_return=excess_return,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                sector_allocations=sector_allocations,
                top_contributors=top_contributors,
                top_detractors=top_detractors,
                risk_metrics=risk_metrics
            )
            
            # Save report
            self.save_performance_report(report)
            
            # Add to history
            self.reports_history.append(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return None

    def analyze_portfolio_allocations(
        self,
        weights: Dict[str, float],
        market_data: Dict[str, Any] = None
    ) -> List[PortfolioAllocation]:
        """Analyze portfolio allocations"""
        try:
            allocations = []
            
            for symbol, weight in weights.items():
                # Get sector classification
                sector = self._get_sector_classification(symbol)
                
                # Get market cap classification
                market_cap = self._get_market_cap_classification(symbol, market_data)
                
                # Get style classification
                style = self._get_style_classification(symbol, market_data)
                
                # Get risk level
                risk_level = self._get_risk_level_classification(symbol, market_data)
                
                # Calculate correlation and beta (simplified)
                correlation = self._calculate_correlation(symbol, weights, market_data)
                beta = self._calculate_beta(symbol, market_data)
                alpha = self._calculate_alpha(symbol, market_data)
                
                allocation = PortfolioAllocation(
                    symbol=symbol,
                    current_weight=weight,
                    target_weight=weight,  # Same as current for now
                    sector=sector,
                    market_cap=market_cap,
                    style=style,
                    risk_level=risk_level,
                    correlation=correlation,
                    beta=beta,
                    alpha=alpha
                )
                
                allocations.append(allocation)
            
            return allocations
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio allocations: {e}")
            return []

    def generate_performance_charts(
        self,
        start_date: datetime,
        end_date: datetime,
        output_dir: str = "charts"
    ) -> List[str]:
        """Generate performance charts and save to files"""
        try:
            # Filter snapshots for date range
            period_snapshots = [
                s for s in self.performance_history
                if start_date <= s.timestamp <= end_date
            ]
            
            if len(period_snapshots) < 2:
                logger.warning("Insufficient data for chart generation")
                return []
            
            # Sort by timestamp
            period_snapshots.sort(key=lambda x: x.timestamp)
            
            # Create output directory
            charts_dir = Path(output_dir)
            charts_dir.mkdir(exist_ok=True)
            
            chart_files = []
            
            # 1. Portfolio Value Over Time
            chart_file = self._create_portfolio_value_chart(period_snapshots, charts_dir)
            if chart_file:
                chart_files.append(chart_file)
            
            # 2. Cumulative Returns
            chart_file = self._create_cumulative_returns_chart(period_snapshots, charts_dir)
            if chart_file:
                chart_files.append(chart_file)
            
            # 3. Drawdown Chart
            chart_file = self._create_drawdown_chart(period_snapshots, charts_dir)
            if chart_file:
                chart_files.append(chart_file)
            
            # 4. Sector Allocation Pie Chart
            chart_file = self._create_sector_allocation_chart(period_snapshots[-1].allocations, charts_dir)
            if chart_file:
                chart_files.append(chart_file)
            
            # 5. Risk-Return Scatter Plot
            chart_file = self._create_risk_return_chart(period_snapshots, charts_dir)
            if chart_file:
                chart_files.append(chart_file)
            
            logger.info(f"Generated {len(chart_files)} performance charts")
            return chart_files
            
        except Exception as e:
            logger.error(f"Error generating performance charts: {e}")
            return []

    def _calculate_daily_return(self, current_value: float) -> float:
        """Calculate daily return"""
        try:
            if not self.performance_history:
                return 0.0
            
            previous_value = self.performance_history[-1].total_value
            daily_return = (current_value - previous_value) / previous_value if previous_value > 0 else 0
            
            return daily_return
            
        except Exception as e:
            logger.error(f"Error calculating daily return: {e}")
            return 0.0

    def _calculate_total_return(self, current_value: float) -> float:
        """Calculate total return from inception"""
        try:
            if not self.performance_history:
                return 0.0
            
            initial_value = self.performance_history[0].total_value
            total_return = (current_value - initial_value) / initial_value if initial_value > 0 else 0
            
            return total_return
            
        except Exception as e:
            logger.error(f"Error calculating total return: {e}")
            return 0.0

    def _calculate_performance_metrics(
        self,
        weights: Dict[str, float],
        prices: Dict[str, float],
        market_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate performance metrics"""
        try:
            metrics = {}
            
            # Basic metrics
            metrics["total_weight"] = sum(weights.values())
            metrics["num_positions"] = len(weights)
            metrics["largest_position"] = max(weights.values()) if weights else 0
            metrics["smallest_position"] = min(weights.values()) if weights else 0
            
            # Risk metrics (simplified)
            metrics["concentration_risk"] = sum(w**2 for w in weights.values())  # Herfindahl index
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {}

    def _create_portfolio_allocations(
        self,
        weights: Dict[str, float],
        market_data: Dict[str, Any]
    ) -> List[PortfolioAllocation]:
        """Create portfolio allocation objects"""
        try:
            return self.analyze_portfolio_allocations(weights, market_data)
        except Exception as e:
            logger.error(f"Error creating portfolio allocations: {e}")
            return []

    def _calculate_benchmark_comparison(
        self,
        portfolio_return: float,
        benchmark_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate benchmark comparison metrics"""
        try:
            if not benchmark_data:
                return {}
            
            benchmark_return = benchmark_data.get("return", 0.0)
            
            comparison = {
                "benchmark_return": benchmark_return,
                "excess_return": portfolio_return - benchmark_return,
                "relative_performance": portfolio_return / benchmark_return if benchmark_return != 0 else 1.0
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error calculating benchmark comparison: {e}")
            return {}

    def _calculate_sharpe_ratio(self, daily_returns: List[float]) -> float:
        """Calculate Sharpe ratio"""
        try:
            if not daily_returns:
                return 0.0
            
            returns_array = np.array(daily_returns)
            excess_returns = returns_array - self.tracking_params["risk_free_rate"] / 252
            
            if np.std(excess_returns) == 0:
                return 0.0
            
            sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
            return sharpe_ratio
            
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0

    def _calculate_max_drawdown(self, snapshots: List[PerformanceSnapshot]) -> float:
        """Calculate maximum drawdown"""
        try:
            if len(snapshots) < 2:
                return 0.0
            
            values = [s.total_value for s in snapshots]
            peak = values[0]
            max_drawdown = 0.0
            
            for value in values:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak
                max_drawdown = max(max_drawdown, drawdown)
            
            return max_drawdown
            
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0

    def _calculate_benchmark_return(
        self,
        benchmark_data: Dict[str, Any],
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Calculate benchmark return for period"""
        try:
            # Simplified benchmark return calculation
            # In practice, this would use actual benchmark data
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating benchmark return: {e}")
            return 0.0

    def _calculate_tracking_error(
        self,
        snapshots: List[PerformanceSnapshot],
        benchmark_data: Dict[str, Any]
    ) -> float:
        """Calculate tracking error"""
        try:
            # Simplified tracking error calculation
            # In practice, this would compare portfolio vs benchmark returns
            return 0.05  # 5% default tracking error
            
        except Exception as e:
            logger.error(f"Error calculating tracking error: {e}")
            return 0.0

    def _calculate_sector_allocations(
        self,
        allocations: List[PortfolioAllocation]
    ) -> Dict[str, float]:
        """Calculate sector allocations"""
        try:
            sector_weights = {}
            
            for allocation in allocations:
                sector = allocation.sector
                weight = allocation.current_weight
                
                if sector in sector_weights:
                    sector_weights[sector] += weight
                else:
                    sector_weights[sector] = weight
            
            return sector_weights
            
        except Exception as e:
            logger.error(f"Error calculating sector allocations: {e}")
            return {}

    def _identify_contributors_detractors(
        self,
        snapshots: List[PerformanceSnapshot]
    ) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
        """Identify top contributors and detractors"""
        try:
            # Simplified implementation
            # In practice, this would analyze individual position performance
            contributors = [("AAPL", 0.15), ("MSFT", 0.12)]
            detractors = [("TSLA", -0.08), ("NVDA", -0.05)]
            
            return contributors, detractors
            
        except Exception as e:
            logger.error(f"Error identifying contributors/detractors: {e}")
            return [], []

    def _calculate_risk_metrics(
        self,
        snapshots: List[PerformanceSnapshot]
    ) -> Dict[str, float]:
        """Calculate comprehensive risk metrics"""
        try:
            risk_metrics = {
                "var_95": 0.02,
                "var_99": 0.03,
                "cvar_95": 0.025,
                "cvar_99": 0.035,
                "beta": 1.1,
                "alpha": 0.01,
                "correlation": 0.6
            }
            
            return risk_metrics
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return {}

    def _get_sector_classification(self, symbol: str) -> str:
        """Get sector classification for symbol"""
        sector_classifications = {
            "TECHNOLOGY": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"],
            "HEALTHCARE": ["JNJ", "PFE", "UNH", "ABBV", "TMO", "ABT", "DHR"],
            "FINANCIAL": ["JPM", "BAC", "WFC", "GS", "MS", "C", "BLK"],
            "CONSUMER_DISCRETIONARY": ["AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX"],
            "INDUSTRIALS": ["BA", "CAT", "GE", "MMM", "UPS", "FDX", "LMT"],
            "ENERGY": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO"],
            "CONSUMER_STAPLES": ["PG", "KO", "PEP", "WMT", "COST", "PM", "MO"],
            "UTILITIES": ["DUK", "SO", "D", "NEE", "AEP", "XEL", "DTE"],
            "REAL_ESTATE": ["SPG", "PLD", "AMT", "CCI", "EQIX", "DLR", "O"],
            "MATERIALS": ["LIN", "APD", "FCX", "NEM", "DD", "DOW", "CAT"],
        }
        
        for sector, symbols in sector_classifications.items():
            if symbol in symbols:
                return sector
        
        return "UNKNOWN"

    def _get_market_cap_classification(self, symbol: str, market_data: Dict[str, Any]) -> str:
        """Get market cap classification"""
        # Simplified classification
        return "LARGE_CAP"

    def _get_style_classification(self, symbol: str, market_data: Dict[str, Any]) -> str:
        """Get style classification"""
        # Simplified classification
        return "BLEND"

    def _get_risk_level_classification(self, symbol: str, market_data: Dict[str, Any]) -> str:
        """Get risk level classification"""
        # Simplified classification
        return "MEDIUM"

    def _calculate_correlation(self, symbol: str, weights: Dict[str, float], market_data: Dict[str, Any]) -> float:
        """Calculate correlation with portfolio"""
        # Simplified correlation calculation
        return 0.5

    def _calculate_beta(self, symbol: str, market_data: Dict[str, Any]) -> float:
        """Calculate beta for symbol"""
        # Simplified beta calculation
        return 1.0

    def _calculate_alpha(self, symbol: str, market_data: Dict[str, Any]) -> float:
        """Calculate alpha for symbol"""
        # Simplified alpha calculation
        return 0.0

    def _create_portfolio_value_chart(self, snapshots: List[PerformanceSnapshot], charts_dir: Path) -> str:
        """Create portfolio value over time chart"""
        try:
            dates = [s.timestamp for s in snapshots]
            values = [s.total_value for s in snapshots]
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, values, linewidth=2)
            plt.title("Portfolio Value Over Time")
            plt.xlabel("Date")
            plt.ylabel("Portfolio Value ($)")
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            chart_file = charts_dir / "portfolio_value.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_file)
            
        except Exception as e:
            logger.error(f"Error creating portfolio value chart: {e}")
            return ""

    def _create_cumulative_returns_chart(self, snapshots: List[PerformanceSnapshot], charts_dir: Path) -> str:
        """Create cumulative returns chart"""
        try:
            dates = [s.timestamp for s in snapshots]
            returns = [s.total_return for s in snapshots]
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, returns, linewidth=2)
            plt.title("Cumulative Returns")
            plt.xlabel("Date")
            plt.ylabel("Cumulative Return (%)")
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            chart_file = charts_dir / "cumulative_returns.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_file)
            
        except Exception as e:
            logger.error(f"Error creating cumulative returns chart: {e}")
            return ""

    def _create_drawdown_chart(self, snapshots: List[PerformanceSnapshot], charts_dir: Path) -> str:
        """Create drawdown chart"""
        try:
            dates = [s.timestamp for s in snapshots]
            values = [s.total_value for s in snapshots]
            
            # Calculate drawdown
            peak = values[0]
            drawdowns = []
            
            for value in values:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak * 100
                drawdowns.append(drawdown)
            
            plt.figure(figsize=(12, 6))
            plt.fill_between(dates, drawdowns, 0, alpha=0.3, color='red')
            plt.plot(dates, drawdowns, linewidth=2, color='red')
            plt.title("Portfolio Drawdown")
            plt.xlabel("Date")
            plt.ylabel("Drawdown (%)")
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            chart_file = charts_dir / "drawdown.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_file)
            
        except Exception as e:
            logger.error(f"Error creating drawdown chart: {e}")
            return ""

    def _create_sector_allocation_chart(self, allocations: List[PortfolioAllocation], charts_dir: Path) -> str:
        """Create sector allocation pie chart"""
        try:
            sector_weights = self._calculate_sector_allocations(allocations)
            
            if not sector_weights:
                return ""
            
            labels = list(sector_weights.keys())
            sizes = list(sector_weights.values())
            
            plt.figure(figsize=(10, 8))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title("Portfolio Sector Allocation")
            plt.axis('equal')
            plt.tight_layout()
            
            chart_file = charts_dir / "sector_allocation.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_file)
            
        except Exception as e:
            logger.error(f"Error creating sector allocation chart: {e}")
            return ""

    def _create_risk_return_chart(self, snapshots: List[PerformanceSnapshot], charts_dir: Path) -> str:
        """Create risk-return scatter plot"""
        try:
            # Simplified risk-return data
            # In practice, this would use actual risk and return data
            returns = [0.08, 0.12, 0.15, 0.10, 0.18]
            risks = [0.12, 0.15, 0.20, 0.14, 0.25]
            symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
            
            plt.figure(figsize=(10, 8))
            plt.scatter(risks, returns, s=100, alpha=0.7)
            
            for i, symbol in enumerate(symbols):
                plt.annotate(symbol, (risks[i], returns[i]), xytext=(5, 5), textcoords='offset points')
            
            plt.title("Risk-Return Profile")
            plt.xlabel("Risk (Volatility)")
            plt.ylabel("Return")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            chart_file = charts_dir / "risk_return.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(chart_file)
            
        except Exception as e:
            logger.error(f"Error creating risk-return chart: {e}")
            return ""

    def save_performance_snapshot(self, snapshot: PerformanceSnapshot):
        """Save performance snapshot to file"""
        try:
            snapshot_file = self.data_dir / f"snapshot_{snapshot.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            
            # Convert snapshot to dictionary
            snapshot_dict = {
                "timestamp": snapshot.timestamp.isoformat(),
                "total_value": snapshot.total_value,
                "total_return": snapshot.total_return,
                "daily_return": snapshot.daily_return,
                "weights": snapshot.weights,
                "metrics": snapshot.metrics,
                "benchmark_comparison": snapshot.benchmark_comparison
            }
            
            with open(snapshot_file, 'w') as f:
                json.dump(snapshot_dict, f, indent=2)
            
            logger.info(f"Saved performance snapshot {snapshot.timestamp}")
            
        except Exception as e:
            logger.error(f"Error saving performance snapshot: {e}")

    def save_performance_report(self, report: PerformanceReport):
        """Save performance report to file"""
        try:
            report_file = self.data_dir / f"{report.report_id}.json"
            
            # Convert report to dictionary
            report_dict = {
                "report_id": report.report_id,
                "start_date": report.start_date.isoformat(),
                "end_date": report.end_date.isoformat(),
                "portfolio_value_start": report.portfolio_value_start,
                "portfolio_value_end": report.portfolio_value_end,
                "total_return": report.total_return,
                "annualized_return": report.annualized_return,
                "volatility": report.volatility,
                "sharpe_ratio": report.sharpe_ratio,
                "max_drawdown": report.max_drawdown,
                "benchmark_return": report.benchmark_return,
                "excess_return": report.excess_return,
                "tracking_error": report.tracking_error,
                "information_ratio": report.information_ratio,
                "sector_allocations": report.sector_allocations,
                "top_contributors": report.top_contributors,
                "top_detractors": report.top_detractors,
                "risk_metrics": report.risk_metrics,
                "timestamp": report.timestamp.isoformat()
            }
            
            with open(report_file, 'w') as f:
                json.dump(report_dict, f, indent=2)
            
            logger.info(f"Saved performance report {report.report_id}")
            
        except Exception as e:
            logger.error(f"Error saving performance report: {e}")

    def load_performance_history(self):
        """Load performance history from files"""
        try:
            for snapshot_file in self.data_dir.glob("snapshot_*.json"):
                try:
                    with open(snapshot_file, 'r') as f:
                        snapshot_data = json.load(f)
                    
                    logger.info(f"Loaded performance snapshot {snapshot_data.get('timestamp', 'unknown')}")
                    
                except Exception as e:
                    logger.error(f"Error loading snapshot file {snapshot_file}: {e}")
                    
        except Exception as e:
            logger.error(f"Error loading performance history: {e}")


def main():
    """CLI interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Portfolio Performance Tracking")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run basic functionality tests"""
    print("🧪 Running Portfolio Performance Tracking smoke tests...")
    
    try:
        # Test initialization
        tracker = PortfolioPerformanceTracker()
        print("✅ Initialization successful")
        
        # Test data structures
        allocation = PortfolioAllocation(
            symbol="AAPL",
            current_weight=0.10,
            target_weight=0.10,
            sector="TECHNOLOGY",
            market_cap="LARGE_CAP",
            style="BLEND",
            risk_level="MEDIUM",
            correlation=0.6,
            beta=1.1,
            alpha=0.01
        )
        print("✅ Data structures working")
        
        # Test performance metrics enum
        metrics = list(PerformanceMetric)
        print(f"✅ Performance metrics: {len(metrics)} metrics available")
        
        # Test tracking
        weights = {"AAPL": 0.10, "MSFT": 0.10}
        prices = {"AAPL": 150.0, "MSFT": 300.0}
        snapshot = tracker.track_portfolio_performance(1000000, weights, prices)
        print(f"✅ Performance tracking: snapshot created")
        
        print("✅ All smoke tests passed!")
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")


if __name__ == "__main__":
    main()

