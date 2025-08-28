"""
Portfolio Risk Models Module

Single Responsibility: Portfolio risk modeling and risk metrics calculations.
Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from .common_algorithms import calculate_max_drawdown, calculate_beta, calculate_alpha

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskModelType(Enum):
    """Types of risk models"""
    HISTORICAL_SIMULATION = "HISTORICAL_SIMULATION"
    MONTE_CARLO = "MONTE_CARLO"
    PARAMETRIC = "PARAMETRIC"
    CONDITIONAL_VAR = "CONDITIONAL_VAR"
    STRESS_TEST = "STRESS_TEST"


@dataclass
class RiskMetrics:
    """Portfolio risk metrics"""
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    max_drawdown: float
    beta: float
    alpha: float
    sharpe_ratio: float
    sortino_ratio: float
    information_ratio: float
    tracking_error: float
    volatility: float
    correlation: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StressTestScenario:
    """Stress test scenario definition"""
    name: str
    description: str
    market_shock: float  # Percentage change in market
    volatility_shock: float  # Multiplier for volatility
    correlation_shock: float  # Change in correlations
    interest_rate_shock: float  # Change in risk-free rate
    sector_shocks: Dict[str, float] = None  # Sector-specific shocks


class PortfolioRiskModels:
    """Portfolio risk modeling and analysis"""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.confidence_levels = [0.95, 0.99]
        
        # Risk model parameters
        self.risk_params = {
            "var_lookback_days": 252,  # 1 year of trading days
            "monte_carlo_simulations": 10000,
            "stress_test_scenarios": 5,
            "correlation_threshold": 0.7,
            "volatility_threshold": 0.3,
            "beta_target": 1.0,
            "alpha_target": 0.02
        }

    def calculate_historical_var(
        self, 
        returns: pd.Series, 
        confidence_level: float = 0.95
    ) -> float:
        """Calculate historical Value at Risk"""
        try:
            if returns.empty:
                logger.warning("Empty returns series for VaR calculation")
                return 0.0
            
            # Sort returns and find percentile
            sorted_returns = returns.sort_values()
            var_percentile = (1 - confidence_level) * 100
            var_index = int(var_percentile / 100 * len(sorted_returns))
            
            if var_index >= len(sorted_returns):
                var_index = len(sorted_returns) - 1
            
            var = sorted_returns.iloc[var_index]
            return abs(var)
            
        except Exception as e:
            logger.error(f"Error calculating historical VaR: {e}")
            return 0.0

    def calculate_conditional_var(
        self, 
        returns: pd.Series, 
        confidence_level: float = 0.95
    ) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        try:
            if returns.empty:
                logger.warning("Empty returns series for CVaR calculation")
                return 0.0
            
            var = self.calculate_historical_var(returns, confidence_level)
            
            # Calculate average of returns below VaR
            tail_returns = returns[returns <= -var]
            
            if len(tail_returns) == 0:
                return var
            
            cvar = tail_returns.mean()
            return abs(cvar)
            
        except Exception as e:
            logger.error(f"Error calculating CVaR: {e}")
            return 0.0

    def calculate_portfolio_risk_metrics(
        self,
        weights: Dict[str, float],
        returns: pd.DataFrame,
        benchmark_returns: pd.Series = None
    ) -> RiskMetrics:
        """Calculate comprehensive portfolio risk metrics"""
        try:
            if not weights or returns.empty:
                logger.warning("Invalid inputs for risk metrics calculation")
                return None
            
            # Calculate portfolio returns
            portfolio_returns = self._calculate_portfolio_returns(weights, returns)
            
            # Basic risk metrics
            volatility = portfolio_returns.std() * np.sqrt(252)  # Annualized
            var_95 = self.calculate_historical_var(portfolio_returns, 0.95)
            var_99 = self.calculate_historical_var(portfolio_returns, 0.99)
            cvar_95 = self.calculate_conditional_var(portfolio_returns, 0.95)
            cvar_99 = self.calculate_conditional_var(portfolio_returns, 0.99)
            
            # Calculate max drawdown
            max_drawdown = calculate_max_drawdown(portfolio_returns)

            # Calculate Sharpe ratio
            sharpe_ratio = self._calculate_sharpe_ratio(portfolio_returns)
            
            # Calculate Sortino ratio
            sortino_ratio = self._calculate_sortino_ratio(portfolio_returns)
            
            # Calculate beta and alpha if benchmark provided
            beta = 1.0
            alpha = 0.0
            information_ratio = 0.0
            tracking_error = 0.0

            if benchmark_returns is not None:
                beta = calculate_beta(portfolio_returns, benchmark_returns)
                alpha = calculate_alpha(portfolio_returns, benchmark_returns, self.risk_free_rate)
                information_ratio = self._calculate_information_ratio(portfolio_returns, benchmark_returns)
                tracking_error = self._calculate_tracking_error(portfolio_returns, benchmark_returns)
            
            # Calculate correlation
            correlation = self._calculate_portfolio_correlation(weights, returns)
            
            return RiskMetrics(
                var_95=var_95,
                var_99=var_99,
                cvar_95=cvar_95,
                cvar_99=cvar_99,
                max_drawdown=max_drawdown,
                beta=beta,
                alpha=alpha,
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                information_ratio=information_ratio,
                tracking_error=tracking_error,
                volatility=volatility,
                correlation=correlation
            )
            
        except Exception as e:
            logger.error(f"Error calculating portfolio risk metrics: {e}")
            return None

    def run_stress_test(
        self,
        weights: Dict[str, float],
        returns: pd.DataFrame,
        scenarios: List[StressTestScenario] = None
    ) -> Dict[str, RiskMetrics]:
        """Run stress tests on portfolio"""
        try:
            if not scenarios:
                scenarios = self._generate_default_stress_scenarios()
            
            stress_results = {}
            
            for scenario in scenarios:
                # Apply stress scenario
                stressed_returns = self._apply_stress_scenario(
                    returns, weights, scenario
                )
                
                # Calculate stressed risk metrics
                stressed_metrics = self.calculate_portfolio_risk_metrics(
                    weights, stressed_returns
                )
                
                if stressed_metrics:
                    stress_results[scenario.name] = stressed_metrics
            
            return stress_results
            
        except Exception as e:
            logger.error(f"Error running stress test: {e}")
            return {}

    def calculate_risk_contribution(
        self,
        weights: Dict[str, float],
        returns: pd.DataFrame
    ) -> Dict[str, float]:
        """Calculate risk contribution of each asset"""
        try:
            if not weights or returns.empty:
                return {}
            
            # Calculate covariance matrix
            covariance_matrix = returns.cov()
            
            # Calculate portfolio volatility
            weights_array = np.array(list(weights.values()))
            portfolio_volatility = np.sqrt(
                np.dot(weights_array.T, np.dot(covariance_matrix, weights_array))
            )
            
            if portfolio_volatility == 0:
                return {symbol: 0.0 for symbol in weights.keys()}
            
            # Calculate marginal risk contribution
            risk_contributions = {}
            symbols = list(weights.keys())
            
            for i, symbol in enumerate(symbols):
                # Marginal contribution to risk
                marginal_contribution = np.dot(covariance_matrix[i], weights_array) / portfolio_volatility
                risk_contributions[symbol] = weights[symbol] * marginal_contribution
            
            return risk_contributions
            
        except Exception as e:
            logger.error(f"Error calculating risk contribution: {e}")
            return {}

    def _calculate_portfolio_returns(
        self, 
        weights: Dict[str, float], 
        returns: pd.DataFrame
    ) -> pd.Series:
        """Calculate portfolio returns from asset returns and weights"""
        try:
            portfolio_returns = pd.Series(0.0, index=returns.index)
            
            for symbol, weight in weights.items():
                if symbol in returns.columns:
                    portfolio_returns += weight * returns[symbol]
            
            return portfolio_returns.dropna()
            
        except Exception as e:
            logger.error(f"Error calculating portfolio returns: {e}")
            return pd.Series()

    def _calculate_sharpe_ratio(self, returns: pd.Series) -> float:
        """Calculate Sharpe ratio"""
        try:
            if returns.empty:
                return 0.0
            
            excess_returns = returns - self.risk_free_rate / 252  # Daily risk-free rate
            return excess_returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0

    def _calculate_sortino_ratio(self, returns: pd.Series) -> float:
        """Calculate Sortino ratio"""
        try:
            if returns.empty:
                return 0.0
            
            excess_returns = returns - self.risk_free_rate / 252  # Daily risk-free rate
            
            # Calculate downside deviation
            downside_returns = excess_returns[excess_returns < 0]
            if len(downside_returns) == 0:
                return 0.0
            
            downside_deviation = downside_returns.std()
            return excess_returns.mean() / downside_deviation * np.sqrt(252) if downside_deviation != 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating Sortino ratio: {e}")
            return 0.0

    def _calculate_information_ratio(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate information ratio"""
        try:
            if portfolio_returns.empty or benchmark_returns.empty:
                return 0.0
            
            # Calculate tracking error
            tracking_error = self._calculate_tracking_error(portfolio_returns, benchmark_returns)
            
            if tracking_error == 0:
                return 0.0
            
            # Calculate excess return
            excess_return = (portfolio_returns.mean() - benchmark_returns.mean()) * 252
            
            return excess_return / tracking_error
            
        except Exception as e:
            logger.error(f"Error calculating information ratio: {e}")
            return 0.0

    def _calculate_tracking_error(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate tracking error"""
        try:
            if portfolio_returns.empty or benchmark_returns.empty:
                return 0.0
            
            # Align returns
            aligned_returns = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
            
            if len(aligned_returns) < 2:
                return 0.0
            
            portfolio_ret = aligned_returns.iloc[:, 0]
            benchmark_ret = aligned_returns.iloc[:, 1]
            
            # Calculate tracking error
            tracking_diff = portfolio_ret - benchmark_ret
            tracking_error = tracking_diff.std() * np.sqrt(252)  # Annualized
            
            return tracking_error
            
        except Exception as e:
            logger.error(f"Error calculating tracking error: {e}")
            return 0.0

    def _calculate_portfolio_correlation(self, weights: Dict[str, float], returns: pd.DataFrame) -> float:
        """Calculate average portfolio correlation"""
        try:
            if not weights or returns.empty:
                return 0.0
            
            # Get correlation matrix
            correlation_matrix = returns.corr()
            
            # Calculate weighted average correlation
            total_correlation = 0.0
            total_weight = 0.0
            
            symbols = list(weights.keys())
            for i, symbol1 in enumerate(symbols):
                for j, symbol2 in enumerate(symbols):
                    if i < j and symbol1 in correlation_matrix.index and symbol2 in correlation_matrix.columns:
                        weight_product = weights[symbol1] * weights[symbol2]
                        correlation = correlation_matrix.loc[symbol1, symbol2]
                        if not pd.isna(correlation):
                            total_correlation += weight_product * correlation
                            total_weight += weight_product
            
            return total_correlation / total_weight if total_weight > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating portfolio correlation: {e}")
            return 0.0

    def _generate_default_stress_scenarios(self) -> List[StressTestScenario]:
        """Generate default stress test scenarios"""
        return [
            StressTestScenario(
                name="Market Crash",
                description="Severe market downturn scenario",
                market_shock=-0.20,
                volatility_shock=2.0,
                correlation_shock=0.3,
                interest_rate_shock=-0.02
            ),
            StressTestScenario(
                name="Volatility Spike",
                description="High volatility environment",
                market_shock=0.0,
                volatility_shock=3.0,
                correlation_shock=0.2,
                interest_rate_shock=0.01
            ),
            StressTestScenario(
                name="Interest Rate Hike",
                description="Rising interest rates",
                market_shock=-0.10,
                volatility_shock=1.5,
                correlation_shock=0.1,
                interest_rate_shock=0.03
            )
        ]

    def _apply_stress_scenario(
        self, 
        returns: pd.DataFrame, 
        weights: Dict[str, float], 
        scenario: StressTestScenario
    ) -> pd.DataFrame:
        """Apply stress scenario to returns"""
        try:
            stressed_returns = returns.copy()
            
            # Apply market shock
            if scenario.market_shock != 0:
                stressed_returns = stressed_returns * (1 + scenario.market_shock)
            
            # Apply volatility shock
            if scenario.volatility_shock != 1.0:
                stressed_returns = stressed_returns * scenario.volatility_shock
            
            # Apply interest rate shock (affects risk-free rate)
            if scenario.interest_rate_shock != 0:
                self.risk_free_rate += scenario.interest_rate_shock
            
            return stressed_returns
            
        except Exception as e:
            logger.error(f"Error applying stress scenario: {e}")
            return returns


def main():
    """CLI interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Portfolio Risk Models")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run basic functionality tests"""
    print("🧪 Running Portfolio Risk Models smoke tests...")
    
    try:
        # Test initialization
        risk_models = PortfolioRiskModels()
        print("✅ Initialization successful")
        
        # Test data structures
        risk_metrics = RiskMetrics(
            var_95=0.02, var_99=0.03, cvar_95=0.025, cvar_99=0.035,
            max_drawdown=0.15, beta=1.1, alpha=0.01, sharpe_ratio=1.2,
            sortino_ratio=1.5, information_ratio=0.8, tracking_error=0.05,
            volatility=0.18, correlation=0.6
        )
        print("✅ Data structures working")
        
        # Test risk model types enum
        model_types = list(RiskModelType)
        print(f"✅ Risk model types: {len(model_types)} types available")
        
        print("✅ All smoke tests passed!")
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")


if __name__ == "__main__":
    main()

