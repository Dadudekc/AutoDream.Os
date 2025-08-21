"""
Portfolio Optimization Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides advanced portfolio optimization, rebalancing, and risk-adjusted returns.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy import stats
import warnings
import time
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizationMethod(Enum):
    """Portfolio optimization methods"""
    SHARPE_RATIO = "SHARPE_RATIO"
    MINIMUM_VARIANCE = "MINIMUM_VARIANCE"
    MAXIMUM_RETURN = "MAXIMUM_RETURN"
    BLACK_LITTERMAN = "BLACK_LITTERMAN"
    RISK_PARITY = "RISK_PARITY"
    MEAN_VARIANCE = "MEAN_VARIANCE"

class RebalancingFrequency(Enum):
    """Portfolio rebalancing frequencies"""
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    ANNUALLY = "ANNUALLY"
    ON_SIGNAL = "ON_SIGNAL"

@dataclass
class OptimizationConstraint:
    """Portfolio optimization constraint"""
    constraint_type: str  # WEIGHT_LIMIT, SECTOR_LIMIT, CONCENTRATION_LIMIT
    symbol: str = ""
    min_weight: float = 0.0
    max_weight: float = 1.0
    sector: str = ""
    max_sector_weight: float = 0.3
    max_concentration: float = 0.1

@dataclass
class OptimizationResult:
    """Portfolio optimization result"""
    method: OptimizationMethod
    optimal_weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    risk_metrics: Dict[str, float]
    constraints_satisfied: bool
    optimization_time: float
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class RebalancingSignal:
    """Portfolio rebalancing signal"""
    symbol: str
    current_weight: float
    target_weight: float
    weight_difference: float
    action: str  # BUY, SELL, HOLD
    priority: str  # HIGH, MEDIUM, LOW
    reason: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

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

class PortfolioOptimizationService:
    """Advanced portfolio optimization and rebalancing service"""
    
    def __init__(self, portfolio_manager=None, market_data_service=None, 
                 risk_manager=None, data_dir: str = "portfolio_optimization"):
        self.portfolio_manager = portfolio_manager
        self.market_data_service = market_data_service
        self.risk_manager = risk_manager
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.optimization_results: Dict[str, OptimizationResult] = {}
        self.rebalancing_signals: List[RebalancingSignal] = []
        self.portfolio_allocations: Dict[str, PortfolioAllocation] = {}
        
        self.optimization_file = self.data_dir / "optimization_results.json"
        self.signals_file = self.data_dir / "rebalancing_signals.json"
        self.allocations_file = self.data_dir / "portfolio_allocations.json"
        
        # Optimization parameters
        self.optimization_params = {
            "risk_free_rate": 0.02,
            "target_volatility": 0.15,
            "max_position_size": 0.1,
            "min_position_size": 0.01,
            "max_sector_weight": 0.3,
            "rebalancing_threshold": 0.05,
            "correlation_threshold": 0.7,
            "beta_target": 1.0,
            "alpha_target": 0.02
        }
        
        # Sector classifications
        self.sector_classifications = {
            "TECHNOLOGY": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"],
            "HEALTHCARE": ["JNJ", "PFE", "UNH", "ABBV", "TMO", "ABT", "DHR"],
            "FINANCIAL": ["JPM", "BAC", "WFC", "GS", "MS", "C", "BLK"],
            "CONSUMER_DISCRETIONARY": ["AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX"],
            "INDUSTRIALS": ["BA", "CAT", "GE", "MMM", "UPS", "FDX", "LMT"],
            "ENERGY": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO"],
            "CONSUMER_STAPLES": ["PG", "KO", "PEP", "WMT", "COST", "PM", "MO"],
            "UTILITIES": ["DUK", "SO", "D", "NEE", "AEP", "XEL", "DTE"],
            "REAL_ESTATE": ["SPG", "PLD", "AMT", "CCI", "EQIX", "DLR", "O"],
            "MATERIALS": ["LIN", "APD", "FCX", "NEM", "DD", "DOW", "CAT"]
        }
        
        # Market cap classifications
        self.market_cap_classifications = {
            "LARGE_CAP": 10000000000,  # $10B+
            "MID_CAP": 2000000000,     # $2B-$10B
            "SMALL_CAP": 300000000,    # $300M-$2B
            "MICRO_CAP": 50000000      # $50M-$300M
        }
        
        self.load_data()
    
    def calculate_returns_and_covariance(self, symbols: List[str], 
                                       period: str = "1y", 
                                       interval: str = "1d") -> Tuple[pd.Series, pd.DataFrame]:
        """Calculate historical returns and covariance matrix"""
        try:
            if not self.market_data_service:
                logger.warning("Market data service not available")
                return None, None
            
            # Get historical data for all symbols
            all_data = {}
            for symbol in symbols:
                historical_data = self.market_data_service.get_historical_data(symbol, period, interval)
                if historical_data and historical_data.data is not None:
                    all_data[symbol] = historical_data.data
            
            if not all_data:
                logger.error("No historical data available for optimization")
                return None, None
            
            # Calculate returns
            returns_data = {}
            for symbol, data in all_data.items():
                if 'Close' in data.columns:
                    returns_data[symbol] = data['Close'].pct_change().dropna()
            
            if not returns_data:
                logger.error("Could not calculate returns from historical data")
                return None, None
            
            # Create returns DataFrame
            returns_df = pd.DataFrame(returns_data)
            returns_df = returns_df.dropna()
            
            # Calculate mean returns
            mean_returns = returns_df.mean()
            
            # Calculate covariance matrix
            covariance_matrix = returns_df.cov()
            
            return mean_returns, covariance_matrix
            
        except Exception as e:
            logger.error(f"Error calculating returns and covariance: {e}")
            return None, None
    
    def optimize_portfolio_sharpe(self, symbols: List[str], 
                                 current_weights: Dict[str, float] = None,
                                 constraints: List[OptimizationConstraint] = None) -> OptimizationResult:
        """Optimize portfolio for maximum Sharpe ratio"""
        try:
            start_time = time.time()
            
            # Get returns and covariance
            mean_returns, covariance_matrix = self.calculate_returns_and_covariance(symbols)
            if mean_returns is None or covariance_matrix is None:
                return None
            
            n_assets = len(symbols)
            
            # Initial weights (equal weight if not provided)
            if current_weights is None:
                initial_weights = np.array([1.0 / n_assets] * n_assets)
            else:
                initial_weights = np.array([current_weights.get(symbol, 0.0) for symbol in symbols])
            
            # Objective function: negative Sharpe ratio (minimize)
            def objective(weights):
                portfolio_return = np.sum(mean_returns * weights)
                portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
                
                if portfolio_volatility == 0:
                    return 0
                
                sharpe_ratio = (portfolio_return - self.optimization_params["risk_free_rate"]) / portfolio_volatility
                return -sharpe_ratio  # Negative because we minimize
            
            # Constraints
            constraints_list = []
            
            # Weight sum constraint
            constraints_list.append({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            
            # Individual weight constraints
            for i in range(n_assets):
                constraints_list.append({'type': 'ineq', 'fun': lambda x, i=i: x[i] - self.optimization_params["min_position_size"]})
                constraints_list.append({'type': 'ineq', 'fun': lambda x, i=i: self.optimization_params["max_position_size"] - x[i]})
            
            # Sector constraints
            if constraints:
                for constraint in constraints:
                    if constraint.constraint_type == "SECTOR_LIMIT":
                        sector_symbols = [i for i, symbol in enumerate(symbols) 
                                        if symbol in self.sector_classifications.get(constraint.sector, [])]
                        if sector_symbols:
                            constraints_list.append({
                                'type': 'ineq', 
                                'fun': lambda x, sector_symbols=sector_symbols: constraint.max_sector_weight - np.sum(x[sector_symbols])
                            })
            
            # Bounds
            bounds = [(self.optimization_params["min_position_size"], self.optimization_params["max_position_size"])] * n_assets
            
            # Optimization
            result = minimize(
                objective, 
                initial_weights, 
                method='SLSQP',
                bounds=bounds,
                constraints=constraints_list,
                options={'maxiter': 1000}
            )
            
            if not result.success:
                logger.warning(f"Optimization failed: {result.message}")
                return None
            
            optimal_weights = result.x
            optimal_weights_dict = {symbol: weight for symbol, weight in zip(symbols, optimal_weights)}
            
            # Calculate portfolio metrics
            portfolio_return = np.sum(mean_returns * optimal_weights)
            portfolio_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(covariance_matrix, optimal_weights)))
            sharpe_ratio = (portfolio_return - self.optimization_params["risk_free_rate"]) / portfolio_volatility if portfolio_volatility > 0 else 0
            
            # Calculate risk metrics
            risk_metrics = {
                "var_95": self.calculate_value_at_risk(optimal_weights, mean_returns, covariance_matrix, 0.95),
                "cvar_95": self.calculate_conditional_var(optimal_weights, mean_returns, covariance_matrix, 0.95),
                "max_drawdown": self.calculate_max_drawdown(optimal_weights, mean_returns, covariance_matrix),
                "beta": self.calculate_portfolio_beta(optimal_weights, symbols),
                "correlation": self.calculate_portfolio_correlation(optimal_weights, covariance_matrix)
            }
            
            optimization_time = time.time() - start_time
            
            result_obj = OptimizationResult(
                method=OptimizationMethod.SHARPE_RATIO,
                optimal_weights=optimal_weights_dict,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                risk_metrics=risk_metrics,
                constraints_satisfied=result.success,
                optimization_time=optimization_time
            )
            
            # Store result
            self.optimization_results[f"sharpe_{datetime.now().strftime('%Y%m%d_%H%M%S')}"] = result_obj
            
            return result_obj
            
        except Exception as e:
            logger.error(f"Error optimizing portfolio for Sharpe ratio: {e}")
            return None
    
    def optimize_portfolio_minimum_variance(self, symbols: List[str],
                                         constraints: List[OptimizationConstraint] = None) -> OptimizationResult:
        """Optimize portfolio for minimum variance"""
        try:
            start_time = time.time()
            
            # Get returns and covariance
            mean_returns, covariance_matrix = self.calculate_returns_and_covariance(symbols)
            if mean_returns is None or covariance_matrix is None:
                return None
            
            n_assets = len(symbols)
            
            # Initial weights (equal weight)
            initial_weights = np.array([1.0 / n_assets] * n_assets)
            
            # Objective function: portfolio variance
            def objective(weights):
                return np.dot(weights.T, np.dot(covariance_matrix, weights))
            
            # Constraints
            constraints_list = []
            constraints_list.append({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            
            # Individual weight constraints
            for i in range(n_assets):
                constraints_list.append({'type': 'ineq', 'fun': lambda x, i=i: x[i] - self.optimization_params["min_position_size"]})
                constraints_list.append({'type': 'ineq', 'fun': lambda x, i=i: self.optimization_params["max_position_size"] - x[i]})
            
            # Bounds
            bounds = [(self.optimization_params["min_position_size"], self.optimization_params["max_position_size"])] * n_assets
            
            # Optimization
            result = minimize(
                objective,
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints_list,
                options={'maxiter': 1000}
            )
            
            if not result.success:
                logger.warning(f"Minimum variance optimization failed: {result.message}")
                return None
            
            optimal_weights = result.x
            optimal_weights_dict = {symbol: weight for symbol, weight in zip(symbols, optimal_weights)}
            
            # Calculate portfolio metrics
            portfolio_return = np.sum(mean_returns * optimal_weights)
            portfolio_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(covariance_matrix, optimal_weights)))
            sharpe_ratio = (portfolio_return - self.optimization_params["risk_free_rate"]) / portfolio_volatility if portfolio_volatility > 0 else 0
            
            # Calculate risk metrics
            risk_metrics = {
                "var_95": self.calculate_value_at_risk(optimal_weights, mean_returns, covariance_matrix, 0.95),
                "cvar_95": self.calculate_conditional_var(optimal_weights, mean_returns, covariance_matrix, 0.95),
                "max_drawdown": self.calculate_max_drawdown(optimal_weights, mean_returns, covariance_matrix),
                "beta": self.calculate_portfolio_beta(optimal_weights, symbols),
                "correlation": self.calculate_portfolio_correlation(optimal_weights, covariance_matrix)
            }
            
            optimization_time = time.time() - start_time
            
            result_obj = OptimizationResult(
                method=OptimizationMethod.MINIMUM_VARIANCE,
                optimal_weights=optimal_weights_dict,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                risk_metrics=risk_metrics,
                constraints_satisfied=result.success,
                optimization_time=optimization_time
            )
            
            # Store result
            self.optimization_results[f"minvar_{datetime.now().strftime('%Y%m%d_%H%M%S')}"] = result_obj
            
            return result_obj
            
        except Exception as e:
            logger.error(f"Error optimizing portfolio for minimum variance: {e}")
            return None
    
    def calculate_value_at_risk(self, weights: np.ndarray, mean_returns: pd.Series, 
                               covariance_matrix: pd.DataFrame, confidence_level: float) -> float:
        """Calculate Value at Risk"""
        try:
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
            
            # Assuming normal distribution
            z_score = stats.norm.ppf(1 - confidence_level)
            var = portfolio_return - (z_score * portfolio_volatility)
            
            return var
            
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0
    
    def calculate_conditional_var(self, weights: np.ndarray, mean_returns: pd.Series,
                                covariance_matrix: pd.DataFrame, confidence_level: float) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        try:
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
            
            # Assuming normal distribution
            z_score = stats.norm.ppf(1 - confidence_level)
            cvar = portfolio_return - (portfolio_volatility * stats.norm.pdf(z_score) / (1 - confidence_level))
            
            return cvar
            
        except Exception as e:
            logger.error(f"Error calculating CVaR: {e}")
            return 0.0
    
    def calculate_max_drawdown(self, weights: np.ndarray, mean_returns: pd.Series,
                              covariance_matrix: pd.DataFrame) -> float:
        """Calculate maximum drawdown estimate"""
        try:
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
            
            # Simple estimate based on volatility
            max_drawdown = portfolio_volatility * 2.5  # Conservative estimate
            
            return max_drawdown
            
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def calculate_portfolio_beta(self, weights: np.ndarray, symbols: List[str]) -> float:
        """Calculate portfolio beta"""
        try:
            if not self.market_data_service:
                return 1.0
            
            # Get market data (using SPY as proxy)
            market_data = self.market_data_service.get_historical_data("SPY", "1y", "1d")
            if not market_data or market_data.data is None:
                return 1.0
            
            market_returns = market_data.data['Close'].pct_change().dropna()
            
            # Calculate individual betas
            betas = []
            for i, symbol in enumerate(symbols):
                symbol_data = self.market_data_service.get_historical_data(symbol, "1y", "1d")
                if symbol_data and symbol_data.data is not None:
                    symbol_returns = symbol_data.data['Close'].pct_change().dropna()
                    
                    # Align returns
                    aligned_returns = pd.concat([symbol_returns, market_returns], axis=1).dropna()
                    if len(aligned_returns) > 30:
                        symbol_returns_aligned = aligned_returns.iloc[:, 0]
                        market_returns_aligned = aligned_returns.iloc[:, 1]
                        
                        # Calculate beta
                        covariance = np.cov(symbol_returns_aligned, market_returns_aligned)[0, 1]
                        market_variance = np.var(market_returns_aligned)
                        
                        if market_variance > 0:
                            beta = covariance / market_variance
                            betas.append(beta)
            
            if betas:
                # Weighted average beta
                portfolio_beta = np.sum(np.array(betas) * weights[:len(betas)])
                return portfolio_beta
            
            return 1.0
            
        except Exception as e:
            logger.error(f"Error calculating portfolio beta: {e}")
            return 1.0
    
    def calculate_portfolio_correlation(self, weights: np.ndarray, 
                                     covariance_matrix: pd.DataFrame) -> float:
        """Calculate average portfolio correlation"""
        try:
            n_assets = len(weights)
            if n_assets < 2:
                return 0.0
            
            # Calculate correlation matrix
            std_devs = np.sqrt(np.diag(covariance_matrix))
            correlation_matrix = covariance_matrix / np.outer(std_devs, std_devs)
            
            # Calculate average correlation (excluding diagonal)
            total_correlation = 0
            count = 0
            
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    if not np.isnan(correlation_matrix.iloc[i, j]):
                        total_correlation += correlation_matrix.iloc[i, j]
                        count += 1
            
            avg_correlation = total_correlation / count if count > 0 else 0.0
            return avg_correlation
            
        except Exception as e:
            logger.error(f"Error calculating portfolio correlation: {e}")
            return 0.0
    
    def generate_rebalancing_signals(self, current_portfolio: Dict[str, float],
                                   target_weights: Dict[str, float]) -> List[RebalancingSignal]:
        """Generate rebalancing signals based on current vs target weights"""
        try:
            signals = []
            threshold = self.optimization_params["rebalancing_threshold"]
            
            all_symbols = set(current_portfolio.keys()) | set(target_weights.keys())
            
            for symbol in all_symbols:
                current_weight = current_portfolio.get(symbol, 0.0)
                target_weight = target_weights.get(symbol, 0.0)
                weight_difference = target_weight - current_weight
                
                # Check if rebalancing is needed
                if abs(weight_difference) > threshold:
                    if weight_difference > 0:
                        action = "BUY"
                        priority = "HIGH" if weight_difference > threshold * 2 else "MEDIUM"
                    else:
                        action = "SELL"
                        priority = "HIGH" if abs(weight_difference) > threshold * 2 else "MEDIUM"
                    
                    # Determine reason
                    if abs(weight_difference) > threshold * 3:
                        reason = "SIGNIFICANT_DRIFT"
                    elif abs(weight_difference) > threshold * 2:
                        reason = "MODERATE_DRIFT"
                    else:
                        reason = "MINOR_DRIFT"
                    
                    signal = RebalancingSignal(
                        symbol=symbol,
                        current_weight=current_weight,
                        target_weight=target_weight,
                        weight_difference=weight_difference,
                        action=action,
                        priority=priority,
                        reason=reason
                    )
                    
                    signals.append(signal)
            
            # Sort by priority and weight difference
            signals.sort(key=lambda x: (x.priority == "HIGH", abs(x.weight_difference)), reverse=True)
            
            # Store signals
            self.rebalancing_signals.extend(signals)
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating rebalancing signals: {e}")
            return []
    
    def analyze_portfolio_allocation(self, portfolio_positions: List[Dict[str, Any]],
                                   target_weights: Dict[str, float]) -> Dict[str, PortfolioAllocation]:
        """Analyze portfolio allocation characteristics"""
        try:
            allocations = {}
            
            for position in portfolio_positions:
                symbol = position.get("symbol", "")
                if not symbol:
                    continue
                
                current_weight = position.get("weight", 0.0)
                target_weight = target_weights.get(symbol, 0.0)
                
                # Determine sector
                sector = "UNKNOWN"
                for sec, symbols_list in self.sector_classifications.items():
                    if symbol in symbols_list:
                        sector = sec
                        break
                
                # Determine market cap
                market_cap = "UNKNOWN"
                if self.market_data_service:
                    market_data = self.market_data_service.get_real_time_data([symbol])
                    if symbol in market_data:
                        price = market_data[symbol].price
                        shares_outstanding = market_data[symbol].volume * 100  # Rough estimate
                        market_cap_value = price * shares_outstanding
                        
                        for cap_type, threshold in self.market_cap_classifications.items():
                            if market_cap_value >= threshold:
                                market_cap = cap_type
                                break
                
                # Determine style (simplified)
                style = "BLEND"  # Would need fundamental data for accurate classification
                
                # Determine risk level
                if current_weight > 0.05:
                    risk_level = "HIGH"
                elif current_weight > 0.02:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
                
                # Calculate correlation and beta (simplified)
                correlation = 0.5  # Would need historical data for accurate calculation
                beta = 1.0  # Would need market data for accurate calculation
                alpha = 0.0  # Would need benchmark data for accurate calculation
                
                allocation = PortfolioAllocation(
                    symbol=symbol,
                    current_weight=current_weight,
                    target_weight=target_weight,
                    sector=sector,
                    market_cap=market_cap,
                    style=style,
                    risk_level=risk_level,
                    correlation=correlation,
                    beta=beta,
                    alpha=alpha
                )
                
                allocations[symbol] = allocation
            
            # Store allocations
            self.portfolio_allocations = allocations
            
            return allocations
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio allocation: {e}")
            return {}
    
    def get_optimization_recommendations(self, optimization_result: OptimizationResult) -> List[str]:
        """Get recommendations based on optimization results"""
        try:
            recommendations = []
            
            # Risk analysis recommendations
            if optimization_result.expected_volatility > 0.25:
                recommendations.append("HIGH_VOLATILITY - Consider reducing risk through diversification")
            
            if optimization_result.risk_metrics.get("var_95", 0) < -0.1:
                recommendations.append("HIGH_DOWNSIDE_RISK - Consider defensive positioning")
            
            if optimization_result.risk_metrics.get("beta", 1.0) > 1.2:
                recommendations.append("HIGH_BETA - Portfolio may be too aggressive for current market")
            
            if optimization_result.risk_metrics.get("correlation", 0) > 0.6:
                recommendations.append("HIGH_CORRELATION - Consider adding uncorrelated assets")
            
            # Return analysis recommendations
            if optimization_result.sharpe_ratio < 0.5:
                recommendations.append("LOW_SHARPE_RATIO - Risk-adjusted returns need improvement")
            
            if optimization_result.expected_return < 0.05:
                recommendations.append("LOW_EXPECTED_RETURN - Consider higher-yielding assets")
            
            # Weight analysis recommendations
            max_weight = max(optimization_result.optimal_weights.values())
            if max_weight > 0.15:
                recommendations.append("CONCENTRATED_POSITIONS - Consider reducing largest positions")
            
            # Sector analysis recommendations
            sector_weights = {}
            for symbol, weight in optimization_result.optimal_weights.items():
                for sector, symbols in self.sector_classifications.items():
                    if symbol in symbols:
                        sector_weights[sector] = sector_weights.get(sector, 0) + weight
                        break
            
            for sector, weight in sector_weights.items():
                if weight > 0.4:
                    recommendations.append(f"SECTOR_OVERWEIGHT - {sector} sector concentration too high")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting optimization recommendations: {e}")
            return []
    
    def save_data(self):
        """Save optimization data"""
        try:
            # Save optimization results
            results_data = {}
            for key, result in self.optimization_results.items():
                results_data[key] = asdict(result)
            
            with open(self.optimization_file, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            # Save rebalancing signals
            signals_data = [asdict(signal) for signal in self.rebalancing_signals]
            with open(self.signals_file, 'w') as f:
                json.dump(signals_data, f, indent=2, default=str)
            
            # Save portfolio allocations
            allocations_data = {symbol: asdict(allocation) 
                              for symbol, allocation in self.portfolio_allocations.items()}
            with open(self.allocations_file, 'w') as f:
                json.dump(allocations_data, f, indent=2, default=str)
            
            logger.info("Portfolio optimization data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving portfolio optimization data: {e}")
    
    def load_data(self):
        """Load optimization data"""
        try:
            # Load optimization results
            if self.optimization_file.exists():
                with open(self.optimization_file, 'r') as f:
                    results_data = json.load(f)
                
                for key, result_dict in results_data.items():
                    if "timestamp" in result_dict:
                        result_dict["timestamp"] = datetime.fromisoformat(result_dict["timestamp"])
                    
                    result_obj = OptimizationResult(**result_dict)
                    self.optimization_results[key] = result_obj
                
                logger.info(f"Loaded {len(results_data)} optimization results")
            
            # Load rebalancing signals
            if self.signals_file.exists():
                with open(self.signals_file, 'r') as f:
                    signals_data = json.load(f)
                
                for signal_dict in signals_data:
                    if "timestamp" in signal_dict:
                        signal_dict["timestamp"] = datetime.fromisoformat(signal_dict["timestamp"])
                    
                    signal_obj = RebalancingSignal(**signal_dict)
                    self.rebalancing_signals.append(signal_obj)
                
                logger.info(f"Loaded {len(signals_data)} rebalancing signals")
            
            # Load portfolio allocations
            if self.allocations_file.exists():
                with open(self.allocations_file, 'r') as f:
                    allocations_data = json.load(f)
                
                for symbol, allocation_dict in allocations_data.items():
                    allocation_obj = PortfolioAllocation(**allocation_dict)
                    self.portfolio_allocations[symbol] = allocation_obj
                
                logger.info(f"Loaded {len(allocations_data)} portfolio allocations")
            
        except Exception as e:
            logger.error(f"Error loading portfolio optimization data: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Create portfolio optimization service
    pos = PortfolioOptimizationService()
    
    # Test optimization with sample data
    test_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    
    print("Portfolio Optimization Service initialized successfully")
    print(f"Available optimization methods: {[method.value for method in OptimizationMethod]}")
    print(f"Default rebalancing threshold: {pos.optimization_params['rebalancing_threshold']}")
