"""
Portfolio Optimization Algorithms Module

Single Responsibility: Portfolio optimization algorithms and mathematical calculations.
Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import logging
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy import stats
from enum import Enum

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


class PortfolioOptimizationAlgorithms:
    """Portfolio optimization algorithms implementation"""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.optimization_params = {
            "target_volatility": 0.15,
            "max_position_size": 0.1,
            "min_position_size": 0.01,
            "max_sector_weight": 0.3,
            "rebalancing_threshold": 0.05,
            "correlation_threshold": 0.7,
            "beta_target": 1.0,
            "alpha_target": 0.02,
        }

    def calculate_returns_and_covariance(
        self, 
        historical_data: Dict[str, pd.DataFrame]
    ) -> Tuple[pd.Series, pd.DataFrame]:
        """Calculate historical returns and covariance matrix"""
        try:
            if not historical_data:
                logger.error("No historical data available for optimization")
                return None, None

            # Calculate returns
            returns_data = {}
            for symbol, data in historical_data.items():
                if "Close" in data.columns:
                    returns_data[symbol] = data["Close"].pct_change().dropna()

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

    def optimize_portfolio_sharpe(
        self,
        symbols: List[str],
        mean_returns: pd.Series,
        covariance_matrix: pd.DataFrame,
        current_weights: Dict[str, float] = None,
        constraints: List[OptimizationConstraint] = None,
    ) -> OptimizationResult:
        """Optimize portfolio for maximum Sharpe ratio"""
        try:
            start_time = time.time()

            if mean_returns is None or covariance_matrix is None:
                return None

            n_assets = len(symbols)

            # Initial weights (equal weight if not provided)
            if current_weights is None:
                initial_weights = np.array([1.0 / n_assets] * n_assets)
            else:
                initial_weights = np.array(
                    [current_weights.get(symbol, 0.0) for symbol in symbols]
                )

            # Objective function: negative Sharpe ratio (minimize)
            def objective(weights):
                portfolio_return = np.sum(mean_returns * weights)
                portfolio_volatility = np.sqrt(
                    np.dot(weights.T, np.dot(covariance_matrix, weights))
                )

                if portfolio_volatility == 0:
                    return 0

                sharpe_ratio = (
                    portfolio_return - self.risk_free_rate
                ) / portfolio_volatility
                return -sharpe_ratio  # Negative because we minimize

            # Constraints
            constraints_list = []

            # Weight sum constraint
            constraints_list.append({"type": "eq", "fun": lambda x: np.sum(x) - 1})

            # Individual weight constraints
            for i in range(n_assets):
                constraints_list.append(
                    {
                        "type": "ineq",
                        "fun": lambda x, i=i: x[i] - self.optimization_params["min_position_size"],
                    }
                )
                constraints_list.append(
                    {
                        "type": "ineq",
                        "fun": lambda x, i=i: self.optimization_params["max_position_size"] - x[i],
                    }
                )

            # Sector constraints
            if constraints:
                for constraint in constraints:
                    if constraint.constraint_type == "SECTOR_LIMIT":
                        sector_symbols = [i for i, symbol in enumerate(symbols) 
                                        if symbol in self._get_sector_symbols(constraint.sector)]
                        if sector_symbols:
                            constraints_list.append({
                                "type": "ineq",
                                "fun": lambda x, sector_symbols=sector_symbols: 
                                    constraint.max_sector_weight - np.sum(x[sector_symbols])
                            })

            # Optimization
            result = minimize(
                objective,
                initial_weights,
                method="SLSQP",
                constraints=constraints_list,
                bounds=[(self.optimization_params["min_position_size"], 
                        self.optimization_params["max_position_size"])] * n_assets
            )

            if not result.success:
                logger.warning(f"Optimization failed: {result.message}")
                return None

            optimal_weights = result.x
            optimization_time = time.time() - start_time

            # Calculate portfolio metrics
            portfolio_return = np.sum(mean_returns * optimal_weights)
            portfolio_volatility = np.sqrt(
                np.dot(optimal_weights.T, np.dot(covariance_matrix, optimal_weights))
            )
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility

            # Create weights dictionary
            weights_dict = {symbol: weight for symbol, weight in zip(symbols, optimal_weights)}

            # Risk metrics
            risk_metrics = {
                "var_95": self._calculate_var(weights_dict, mean_returns, covariance_matrix, 0.95),
                "var_99": self._calculate_var(weights_dict, mean_returns, covariance_matrix, 0.99),
                "max_drawdown": self._calculate_max_drawdown(weights_dict, mean_returns, covariance_matrix),
                "beta": self._calculate_beta(weights_dict, mean_returns, covariance_matrix),
                "alpha": self._calculate_alpha(weights_dict, mean_returns, covariance_matrix)
            }

            return OptimizationResult(
                method=OptimizationMethod.SHARPE_RATIO,
                optimal_weights=weights_dict,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                risk_metrics=risk_metrics,
                constraints_satisfied=result.success,
                optimization_time=optimization_time
            )

        except Exception as e:
            logger.error(f"Error in Sharpe ratio optimization: {e}")
            return None

    def optimize_portfolio_minimum_variance(
        self,
        symbols: List[str],
        covariance_matrix: pd.DataFrame,
        current_weights: Dict[str, float] = None,
        constraints: List[OptimizationConstraint] = None,
    ) -> OptimizationResult:
        """Optimize portfolio for minimum variance"""
        try:
            start_time = time.time()

            if covariance_matrix is None:
                return None

            n_assets = len(symbols)

            # Initial weights (equal weight if not provided)
            if current_weights is None:
                initial_weights = np.array([1.0 / n_assets] * n_assets)
            else:
                initial_weights = np.array(
                    [current_weights.get(symbol, 0.0) for symbol in symbols]
                )

            # Objective function: portfolio variance
            def objective(weights):
                return np.dot(weights.T, np.dot(covariance_matrix, weights))

            # Constraints
            constraints_list = []

            # Weight sum constraint
            constraints_list.append({"type": "eq", "fun": lambda x: np.sum(x) - 1})

            # Individual weight constraints
            for i in range(n_assets):
                constraints_list.append(
                    {
                        "type": "ineq",
                        "fun": lambda x, i=i: x[i] - self.optimization_params["min_position_size"],
                    }
                )
                constraints_list.append(
                    {
                        "type": "ineq",
                        "fun": lambda x, i=i: self.optimization_params["max_position_size"] - x[i],
                    }
                )

            # Optimization
            result = minimize(
                objective,
                initial_weights,
                method="SLSQP",
                constraints=constraints_list,
                bounds=[(self.optimization_params["min_position_size"], 
                        self.optimization_params["max_position_size"])] * n_assets
            )

            if not result.success:
                logger.warning(f"Optimization failed: {result.message}")
                return None

            optimal_weights = result.x
            optimization_time = time.time() - start_time

            # Calculate portfolio metrics
            portfolio_volatility = np.sqrt(result.fun)
            
            # For minimum variance, we don't have expected returns, so we'll use 0
            portfolio_return = 0.0
            sharpe_ratio = 0.0

            # Create weights dictionary
            weights_dict = {symbol: weight for symbol, weight in zip(symbols, optimal_weights)}

            # Risk metrics
            risk_metrics = {
                "var_95": self._calculate_var(weights_dict, None, covariance_matrix, 0.95),
                "var_99": self._calculate_var(weights_dict, None, covariance_matrix, 0.99),
                "max_drawdown": self._calculate_max_drawdown(weights_dict, None, covariance_matrix),
                "beta": 0.0,  # No returns data for beta calculation
                "alpha": 0.0   # No returns data for alpha calculation
            }

            return OptimizationResult(
                method=OptimizationMethod.MINIMUM_VARIANCE,
                optimal_weights=weights_dict,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                risk_metrics=risk_metrics,
                constraints_satisfied=result.success,
                optimization_time=optimization_time
            )

        except Exception as e:
            logger.error(f"Error in minimum variance optimization: {e}")
            return None

    def _get_sector_symbols(self, sector: str) -> List[str]:
        """Get symbols for a given sector"""
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
        return sector_classifications.get(sector.upper(), [])

    def _calculate_var(self, weights: Dict[str, float], returns: pd.Series, 
                      covariance: pd.DataFrame, confidence_level: float) -> float:
        """Calculate Value at Risk"""
        try:
            if returns is None:
                return 0.0
            
            portfolio_return = np.sum(returns * np.array(list(weights.values())))
            portfolio_volatility = np.sqrt(
                np.dot(np.array(list(weights.values())).T, 
                      np.dot(covariance, np.array(list(weights.values())))))
            
            # Assuming normal distribution
            z_score = stats.norm.ppf(1 - confidence_level)
            var = portfolio_return - z_score * portfolio_volatility
            return var
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0

    def _calculate_max_drawdown(self, weights: Dict[str, float], returns: pd.Series, 
                               covariance: pd.DataFrame) -> float:
        """Calculate maximum drawdown"""
        try:
            if returns is None:
                return 0.0
            
            portfolio_return = np.sum(returns * np.array(list(weights.values())))
            portfolio_volatility = np.sqrt(
                np.dot(np.array(list(weights.values())).T, 
                      np.dot(covariance, np.array(list(weights.values())))))
            
            # Simplified max drawdown calculation
            max_drawdown = portfolio_volatility * 2.0  # Rough estimate
            return max_drawdown
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0

    def _calculate_beta(self, weights: Dict[str, float], returns: pd.Series, 
                       covariance: pd.DataFrame) -> float:
        """Calculate portfolio beta"""
        try:
            if returns is None:
                return 0.0
            
            # Simplified beta calculation
            portfolio_return = np.sum(returns * np.array(list(weights.values())))
            beta = portfolio_return / returns.mean() if returns.mean() != 0 else 1.0
            return beta
        except Exception as e:
            logger.error(f"Error calculating beta: {e}")
            return 1.0

    def _calculate_alpha(self, weights: Dict[str, float], returns: pd.Series, 
                        covariance: pd.DataFrame) -> float:
        """Calculate portfolio alpha"""
        try:
            if returns is None:
                return 0.0
            
            portfolio_return = np.sum(returns * np.array(list(weights.values())))
            alpha = portfolio_return - self.risk_free_rate
            return alpha
        except Exception as e:
            logger.error(f"Error calculating alpha: {e}")
            return 0.0


def main():
    """CLI interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Portfolio Optimization Algorithms")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run basic functionality tests"""
    print("🧪 Running Portfolio Optimization Algorithms smoke tests...")
    
    try:
        # Test initialization
        algo = PortfolioOptimizationAlgorithms()
        print("✅ Initialization successful")
        
        # Test data structures
        constraint = OptimizationConstraint("WEIGHT_LIMIT", "AAPL", 0.0, 0.1)
        print("✅ Data structures working")
        
        # Test optimization methods enum
        methods = list(OptimizationMethod)
        print(f"✅ Optimization methods: {len(methods)} methods available")
        
        print("✅ All smoke tests passed!")
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")


if __name__ == "__main__":
    main()
