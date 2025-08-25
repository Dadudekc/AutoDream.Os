"""
Portfolio Rebalancing Core Module

Single Responsibility: Core rebalancing data structures and fundamental logic.
Follows V2 coding standards: Clean OOP design, SRP compliance, focused functionality.
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import json

# Configure logging
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


class RebalancingCore:
    """Core rebalancing functionality and data management"""
    
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
