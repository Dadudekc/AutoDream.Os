"""
Portfolio Rebalancing Module

Single Responsibility: Portfolio rebalancing logic and signal generation.
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RebalancingFrequency(Enum):
    """Portfolio rebalancing frequencies"""
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    ANNUALLY = "ANNUALLY"
    ON_SIGNAL = "ON_SIGNAL"


class RebalancingTrigger(Enum):
    """Rebalancing trigger types"""
    THRESHOLD_BREACH = "THRESHOLD_BREACH"
    TIME_BASED = "TIME_BASED"
    VOLATILITY_BREACH = "VOLATILITY_BREACH"
    CORRELATION_BREACH = "CORRELATION_BREACH"
    PERFORMANCE_BREACH = "PERFORMANCE_BREACH"
    MANUAL = "MANUAL"


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
    estimated_cost: float = 0.0
    market_impact: float = 0.0

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class RebalancingPlan:
    """Portfolio rebalancing plan"""
    plan_id: str
    timestamp: datetime
    current_weights: Dict[str, float]
    target_weights: Dict[str, float]
    signals: List[RebalancingSignal]
    total_cost: float
    estimated_impact: float
    priority: str
    status: str = "PENDING"  # PENDING, EXECUTING, COMPLETED, FAILED
    execution_date: datetime = None
    completion_date: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class PortfolioRebalancing:
    """Portfolio rebalancing management"""
    
    def __init__(self, data_dir: str = "portfolio_rebalancing"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Rebalancing parameters
        self.rebalancing_params = {
            "threshold": 0.05,  # 5% weight difference threshold
            "max_trades_per_rebalance": 10,
            "min_trade_size": 0.01,  # 1% minimum trade size
            "max_single_trade": 0.05,  # 5% maximum single trade
            "cost_threshold": 0.001,  # 0.1% cost threshold
            "volatility_threshold": 0.25,
            "correlation_threshold": 0.8,
            "performance_threshold": -0.05  # -5% performance threshold
        }
        
        # Rebalancing history
        self.rebalancing_history: List[RebalancingPlan] = []
        self.signals_history: List[RebalancingSignal] = []
        
        # Load historical data
        self.load_rebalancing_history()

    def generate_rebalancing_signals(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        current_prices: Dict[str, float] = None,
        market_data: Dict[str, Any] = None
    ) -> List[RebalancingSignal]:
        """Generate rebalancing signals based on weight differences"""
        try:
            if not current_weights or not target_weights:
                logger.warning("Invalid weights for rebalancing signal generation")
                return []
            
            signals = []
            all_symbols = set(current_weights.keys()) | set(target_weights.keys())
            
            for symbol in all_symbols:
                current_weight = current_weights.get(symbol, 0.0)
                target_weight = target_weights.get(symbol, 0.0)
                weight_difference = target_weight - current_weight
                
                # Check if rebalancing is needed
                if abs(weight_difference) > self.rebalancing_params["threshold"]:
                    # Determine action
                    if weight_difference > 0:
                        action = "BUY"
                    else:
                        action = "SELL"
                    
                    # Determine priority
                    priority = self._determine_priority(abs(weight_difference), symbol, market_data)
                    
                    # Determine reason
                    reason = self._determine_rebalancing_reason(weight_difference, symbol, market_data)
                    
                    # Estimate costs and market impact
                    estimated_cost = self._estimate_trading_cost(symbol, abs(weight_difference), current_prices)
                    market_impact = self._estimate_market_impact(symbol, abs(weight_difference), market_data)
                    
                    signal = RebalancingSignal(
                        symbol=symbol,
                        current_weight=current_weight,
                        target_weight=target_weight,
                        weight_difference=weight_difference,
                        action=action,
                        priority=priority,
                        reason=reason,
                        estimated_cost=estimated_cost,
                        market_impact=market_impact
                    )
                    
                    signals.append(signal)
            
            # Sort signals by priority and weight difference
            signals.sort(key=lambda x: (self._priority_score(x.priority), abs(x.weight_difference)), reverse=True)
            
            # Limit number of signals
            max_signals = self.rebalancing_params["max_trades_per_rebalance"]
            if len(signals) > max_signals:
                signals = signals[:max_signals]
                logger.info(f"Limited rebalancing signals to {max_signals}")
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating rebalancing signals: {e}")
            return []

    def create_rebalancing_plan(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        current_prices: Dict[str, float] = None,
        market_data: Dict[str, Any] = None
    ) -> RebalancingPlan:
        """Create a comprehensive rebalancing plan"""
        try:
            # Generate signals
            signals = self.generate_rebalancing_signals(
                current_weights, target_weights, current_prices, market_data
            )
            
            if not signals:
                logger.info("No rebalancing signals generated")
                return None
            
            # Calculate total costs and impact
            total_cost = sum(signal.estimated_cost for signal in signals)
            estimated_impact = sum(signal.market_impact for signal in signals)
            
            # Determine overall priority
            overall_priority = self._determine_overall_priority(signals)
            
            # Create plan
            plan = RebalancingPlan(
                plan_id=f"REBAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                timestamp=datetime.now(),
                current_weights=current_weights.copy(),
                target_weights=target_weights.copy(),
                signals=signals,
                total_cost=total_cost,
                estimated_impact=estimated_impact,
                priority=overall_priority
            )
            
            # Save plan
            self.save_rebalancing_plan(plan)
            
            return plan
            
        except Exception as e:
            logger.error(f"Error creating rebalancing plan: {e}")
            return None

    def execute_rebalancing_plan(
        self,
        plan: RebalancingPlan,
        execution_prices: Dict[str, float] = None
    ) -> bool:
        """Execute a rebalancing plan"""
        try:
            if not plan:
                logger.error("No rebalancing plan provided")
                return False
            
            if plan.status != "PENDING":
                logger.warning(f"Plan {plan.plan_id} is not in PENDING status: {plan.status}")
                return False
            
            # Update plan status
            plan.status = "EXECUTING"
            plan.execution_date = datetime.now()
            
            logger.info(f"Executing rebalancing plan {plan.plan_id}")
            
            # Execute trades (simulated)
            execution_success = self._execute_trades(plan, execution_prices)
            
            if execution_success:
                plan.status = "COMPLETED"
                plan.completion_date = datetime.now()
                logger.info(f"Rebalancing plan {plan.plan_id} completed successfully")
            else:
                plan.status = "FAILED"
                logger.error(f"Rebalancing plan {plan.plan_id} failed")
            
            # Update plan
            self.save_rebalancing_plan(plan)
            
            return execution_success
            
        except Exception as e:
            logger.error(f"Error executing rebalancing plan: {e}")
            if plan:
                plan.status = "FAILED"
                self.save_rebalancing_plan(plan)
            return False

    def check_rebalancing_needed(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        last_rebalance_date: datetime = None,
        frequency: RebalancingFrequency = RebalancingFrequency.MONTHLY
    ) -> Tuple[bool, str]:
        """Check if rebalancing is needed"""
        try:
            # Check time-based triggers
            if self._check_time_based_trigger(last_rebalance_date, frequency):
                return True, "Time-based rebalancing due"
            
            # Check threshold-based triggers
            if self._check_threshold_trigger(current_weights, target_weights):
                return True, "Weight threshold breached"
            
            # Check volatility triggers
            if self._check_volatility_trigger(current_weights, target_weights):
                return True, "Volatility threshold breached"
            
            # Check correlation triggers
            if self._check_correlation_trigger(current_weights, target_weights):
                return True, "Correlation threshold breached"
            
            return False, "No rebalancing needed"
            
        except Exception as e:
            logger.error(f"Error checking rebalancing needs: {e}")
            return False, f"Error: {e}"

    def _determine_priority(
        self, 
        weight_difference: float, 
        symbol: str, 
        market_data: Dict[str, Any] = None
    ) -> str:
        """Determine signal priority"""
        try:
            # High priority for large weight differences
            if abs(weight_difference) > 0.10:  # 10%
                return "HIGH"
            
            # Medium priority for moderate differences
            if abs(weight_difference) > 0.05:  # 5%
                return "MEDIUM"
            
            # Low priority for small differences
            return "LOW"
            
        except Exception as e:
            logger.error(f"Error determining priority: {e}")
            return "MEDIUM"

    def _determine_rebalancing_reason(
        self, 
        weight_difference: float, 
        symbol: str, 
        market_data: Dict[str, Any] = None
    ) -> str:
        """Determine reason for rebalancing"""
        try:
            if weight_difference > 0:
                return f"Underweight position - need to increase {symbol} allocation"
            else:
                return f"Overweight position - need to reduce {symbol} allocation"
                
        except Exception as e:
            logger.error(f"Error determining rebalancing reason: {e}")
            return "Weight adjustment needed"

    def _priority_score(self, priority: str) -> int:
        """Convert priority to numeric score for sorting"""
        priority_scores = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }
        return priority_scores.get(priority, 1)

    def _determine_overall_priority(self, signals: List[RebalancingSignal]) -> str:
        """Determine overall plan priority"""
        try:
            if not signals:
                return "LOW"
            
            # Count high priority signals
            high_priority_count = sum(1 for signal in signals if signal.priority == "HIGH")
            
            if high_priority_count >= 3:
                return "HIGH"
            elif high_priority_count >= 1:
                return "MEDIUM"
            else:
                return "LOW"
                
        except Exception as e:
            logger.error(f"Error determining overall priority: {e}")
            return "MEDIUM"

    def _estimate_trading_cost(
        self, 
        symbol: str, 
        weight_difference: float, 
        current_prices: Dict[str, float] = None
    ) -> float:
        """Estimate trading cost for rebalancing"""
        try:
            # Base trading cost (0.1% of trade value)
            base_cost_rate = 0.001
            
            # Estimate trade value (simplified)
            trade_value = abs(weight_difference) * 1000000  # Assume $1M portfolio
            
            estimated_cost = trade_value * base_cost_rate
            
            return estimated_cost
            
        except Exception as e:
            logger.error(f"Error estimating trading cost: {e}")
            return 0.0

    def _estimate_market_impact(
        self, 
        symbol: str, 
        weight_difference: float, 
        market_data: Dict[str, Any] = None
    ) -> float:
        """Estimate market impact of rebalancing trade"""
        try:
            # Simplified market impact estimation
            # Larger trades have higher market impact
            impact_rate = min(0.001 * abs(weight_difference) * 100, 0.01)  # Max 1%
            
            return impact_rate
            
        except Exception as e:
            logger.error(f"Error estimating market impact: {e}")
            return 0.0

    def _execute_trades(self, plan: RebalancingPlan, execution_prices: Dict[str, float] = None) -> bool:
        """Execute trades for rebalancing plan (simulated)"""
        try:
            logger.info(f"Executing {len(plan.signals)} trades for plan {plan.plan_id}")
            
            # Simulate trade execution
            for signal in plan.signals:
                logger.info(f"Executing {signal.action} order for {signal.symbol}: "
                          f"{abs(signal.weight_difference):.4f} weight adjustment")
                
                # Simulate execution delay
                import time
                time.sleep(0.1)
            
            logger.info("All trades executed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error executing trades: {e}")
            return False

    def _check_time_based_trigger(
        self, 
        last_rebalance_date: datetime, 
        frequency: RebalancingFrequency
    ) -> bool:
        """Check if time-based rebalancing is due"""
        try:
            if not last_rebalance_date:
                return True
            
            now = datetime.now()
            time_since_rebalance = now - last_rebalance_date
            
            frequency_days = {
                RebalancingFrequency.DAILY: 1,
                RebalancingFrequency.WEEKLY: 7,
                RebalancingFrequency.MONTHLY: 30,
                RebalancingFrequency.QUARTERLY: 90,
                RebalancingFrequency.SEMI_ANNUALLY: 180,
                RebalancingFrequency.ANNUALLY: 365
            }
            
            required_days = frequency_days.get(frequency, 30)
            
            return time_since_rebalance.days >= required_days
            
        except Exception as e:
            logger.error(f"Error checking time-based trigger: {e}")
            return False

    def _check_threshold_trigger(
        self, 
        current_weights: Dict[str, float], 
        target_weights: Dict[str, float]
    ) -> bool:
        """Check if weight threshold is breached"""
        try:
            for symbol in set(current_weights.keys()) | set(target_weights.keys()):
                current = current_weights.get(symbol, 0.0)
                target = target_weights.get(symbol, 0.0)
                
                if abs(target - current) > self.rebalancing_params["threshold"]:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking threshold trigger: {e}")
            return False

    def _check_volatility_trigger(
        self, 
        current_weights: Dict[str, float], 
        target_weights: Dict[str, float]
    ) -> bool:
        """Check if volatility threshold is breached"""
        try:
            # Simplified volatility check
            # In a real implementation, this would use actual volatility data
            return False
            
        except Exception as e:
            logger.error(f"Error checking volatility trigger: {e}")
            return False

    def _check_correlation_trigger(
        self, 
        current_weights: Dict[str, float], 
        target_weights: Dict[str, float]
    ) -> bool:
        """Check if correlation threshold is breached"""
        try:
            # Simplified correlation check
            # In a real implementation, this would use actual correlation data
            return False
            
        except Exception as e:
            logger.error(f"Error checking correlation trigger: {e}")
            return False

    def save_rebalancing_plan(self, plan: RebalancingPlan):
        """Save rebalancing plan to file"""
        try:
            plan_file = self.data_dir / f"{plan.plan_id}.json"
            
            # Convert plan to dictionary
            plan_dict = {
                "plan_id": plan.plan_id,
                "timestamp": plan.timestamp.isoformat(),
                "current_weights": plan.current_weights,
                "target_weights": plan.target_weights,
                "signals": [
                    {
                        "symbol": signal.symbol,
                        "current_weight": signal.current_weight,
                        "target_weight": signal.target_weight,
                        "weight_difference": signal.weight_difference,
                        "action": signal.action,
                        "priority": signal.priority,
                        "reason": signal.reason,
                        "timestamp": signal.timestamp.isoformat(),
                        "estimated_cost": signal.estimated_cost,
                        "market_impact": signal.market_impact
                    }
                    for signal in plan.signals
                ],
                "total_cost": plan.total_cost,
                "estimated_impact": plan.estimated_impact,
                "priority": plan.priority,
                "status": plan.status,
                "execution_date": plan.execution_date.isoformat() if plan.execution_date else None,
                "completion_date": plan.completion_date.isoformat() if plan.completion_date else None
            }
            
            with open(plan_file, 'w') as f:
                json.dump(plan_dict, f, indent=2)
            
            logger.info(f"Saved rebalancing plan {plan.plan_id}")
            
        except Exception as e:
            logger.error(f"Error saving rebalancing plan: {e}")

    def load_rebalancing_history(self):
        """Load rebalancing history from files"""
        try:
            for plan_file in self.data_dir.glob("*.json"):
                try:
                    with open(plan_file, 'r') as f:
                        plan_data = json.load(f)
                    
                    # Convert back to RebalancingPlan object
                    # This is a simplified version - in practice, you'd want more robust parsing
                    logger.info(f"Loaded rebalancing plan {plan_data.get('plan_id', 'unknown')}")
                    
                except Exception as e:
                    logger.error(f"Error loading plan file {plan_file}: {e}")
                    
        except Exception as e:
            logger.error(f"Error loading rebalancing history: {e}")


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
        
        print("✅ All smoke tests passed!")
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")


if __name__ == "__main__":
    main()

