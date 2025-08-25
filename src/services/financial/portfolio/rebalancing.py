"""
Portfolio Rebalancing Module (Refactored)

Single Responsibility: Orchestrates portfolio rebalancing operations.
Follows V2 coding standards: Clean OOP design, SRP compliance, modular architecture.
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

from rebalancing_core import (
    RebalancingCore, RebalancingPlan, RebalancingSignal, 
    RebalancingFrequency, RebalancingTrigger
)
from portfolio_analysis import PortfolioAnalyzer
from rebalancing_executor import RebalancingExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortfolioRebalancing:
    """Portfolio rebalancing orchestrator - coordinates core, analysis, and execution"""
    
    def __init__(self, data_dir: str = "portfolio_rebalancing"):
        """Initialize portfolio rebalancing system"""
        self.core = RebalancingCore(data_dir)
        self.analyzer = PortfolioAnalyzer()
        self.executor = RebalancingExecutor()

    def generate_rebalancing_signals(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        current_prices: Dict[str, float] = None,
        market_data: Dict[str, Any] = None
    ) -> List[RebalancingSignal]:
        """Generate rebalancing signals using core module"""
        return self.core.generate_rebalancing_signals(
            current_weights, target_weights, current_prices, market_data
        )

    def create_rebalancing_plan(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        current_prices: Dict[str, float] = None,
        market_data: Dict[str, Any] = None
    ) -> RebalancingPlan:
        """Create rebalancing plan using core module"""
        return self.core.create_rebalancing_plan(
            current_weights, target_weights, current_prices, market_data
        )

    def execute_rebalancing_plan(
        self,
        plan: RebalancingPlan,
        execution_prices: Dict[str, float] = None
    ) -> bool:
        """Execute rebalancing plan using executor module"""
        return self.executor.execute_rebalancing_plan(plan, execution_prices)

    def check_rebalancing_needed(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        last_rebalance_date: datetime = None,
        frequency: RebalancingFrequency = RebalancingFrequency.MONTHLY
    ) -> Tuple[bool, str]:
        """Check if rebalancing is needed using analyzer module"""
        return self.analyzer.check_rebalancing_needed(
            current_weights, target_weights, last_rebalance_date, frequency
        )

    def analyze_portfolio_health(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float]
    ) -> Dict[str, Any]:
        """Analyze portfolio health using analyzer module"""
        return self.analyzer.analyze_portfolio_health(current_weights, target_weights)

    def get_rebalancing_recommendations(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        market_conditions: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Get rebalancing recommendations using analyzer module"""
        return self.analyzer.get_rebalancing_recommendations(
            current_weights, target_weights, market_conditions
        )

    def validate_plan_executability(self, plan: RebalancingPlan) -> Tuple[bool, List[str]]:
        """Validate plan executability using executor module"""
        return self.executor.validate_plan_executability(plan)

    def simulate_execution(self, plan: RebalancingPlan, market_conditions: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate plan execution using executor module"""
        return self.executor.simulate_execution(plan, market_conditions)

    def get_execution_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get execution history from executor module"""
        return self.executor.get_execution_history(limit)

    def get_execution_statistics(self) -> Dict[str, Any]:
        """Get execution statistics from executor module"""
        return self.executor.get_execution_statistics()

    def save_rebalancing_plan(self, plan: RebalancingPlan):
        """Save rebalancing plan using core module"""
        self.core.save_rebalancing_plan(plan)

    def load_rebalancing_history(self):
        """Load rebalancing history using core module"""
        self.core.load_rebalancing_history()

    # Convenience methods for backward compatibility
    @property
    def rebalancing_params(self):
        """Access rebalancing parameters from core module"""
        return self.core.rebalancing_params

    @property
    def rebalancing_history(self):
        """Access rebalancing history from core module"""
        return self.core.rebalancing_history

    @property
    def signals_history(self):
        """Access signals history from core module"""
        return self.core.signals_history


def main():
    """CLI interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Portfolio Rebalancing")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run basic functionality tests"""
    print("🧪 Running Portfolio Rebalancing smoke tests...")
    
    try:
        # Test initialization
        rebalancing = PortfolioRebalancing()
        print("✅ Initialization successful")
        
        # Test data structures
        signal = RebalancingSignal(
            symbol="AAPL",
            current_weight=0.08,
            target_weight=0.10,
            weight_difference=0.02,
            action="BUY",
            priority="MEDIUM",
            reason="Underweight position"
        )
        print("✅ Data structures working")
        
        # Test rebalancing frequency enum
        frequencies = list(RebalancingFrequency)
        print(f"✅ Rebalancing frequencies: {len(frequencies)} frequencies available")
        
        # Test signal generation
        current_weights = {"AAPL": 0.08, "MSFT": 0.12}
        target_weights = {"AAPL": 0.10, "MSFT": 0.10}
        signals = rebalancing.generate_rebalancing_signals(current_weights, target_weights)
        print(f"✅ Signal generation: {len(signals)} signals generated")
        
        # Test portfolio analysis
        health = rebalancing.analyze_portfolio_health(current_weights, target_weights)
        print(f"✅ Portfolio analysis: {health.get('rebalancing_score', 0):.1f} score")
        
        # Test recommendations
        recommendations = rebalancing.get_rebalancing_recommendations(current_weights, target_weights)
        print(f"✅ Recommendations: {len(recommendations)} recommendations generated")
        
        print("✅ All smoke tests passed!")
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")


if __name__ == "__main__":
    main()

