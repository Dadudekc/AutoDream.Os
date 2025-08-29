"""
Portfolio Analysis Module

Single Responsibility: Portfolio analysis and rebalancing trigger checking.
Follows V2 coding standards: Clean OOP design, SRP compliance, focused functionality.
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from rebalancing_core import RebalancingFrequency, RebalancingTrigger

# Configure logging
logger = logging.getLogger(__name__)


class PortfolioAnalyzer:
    """Portfolio analysis and trigger checking functionality"""
    
    def __init__(self):
        """Initialize portfolio analyzer"""
        pass

    def check_rebalancing_needed(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        last_rebalance_date: datetime = None,
        frequency: RebalancingFrequency = RebalancingFrequency.MONTHLY
    ) -> Tuple[bool, str]:
        """Check if rebalancing is needed based on various triggers"""
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
        target_weights: Dict[str, float],
        threshold: float = 0.05
    ) -> bool:
        """Check if weight threshold is breached"""
        try:
            for symbol in set(current_weights.keys()) | set(target_weights.keys()):
                current = current_weights.get(symbol, 0.0)
                target = target_weights.get(symbol, 0.0)
                
                if abs(target - current) > threshold:
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

    def analyze_portfolio_health(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float]
    ) -> Dict[str, Any]:
        """Analyze overall portfolio health and rebalancing needs"""
        try:
            analysis = {
                "total_positions": len(set(current_weights.keys()) | set(target_weights.keys())),
                "positions_needing_rebalancing": 0,
                "largest_deviation": 0.0,
                "average_deviation": 0.0,
                "rebalancing_score": 0.0
            }
            
            deviations = []
            for symbol in set(current_weights.keys()) | set(target_weights.keys()):
                current = current_weights.get(symbol, 0.0)
                target = target_weights.get(symbol, 0.0)
                deviation = abs(target - current)
                deviations.append(deviation)
                
                if deviation > 0.05:  # 5% threshold
                    analysis["positions_needing_rebalancing"] += 1
                
                if deviation > analysis["largest_deviation"]:
                    analysis["largest_deviation"] = deviation
            
            if deviations:
                analysis["average_deviation"] = sum(deviations) / len(deviations)
                # Calculate rebalancing score (0-100, higher = more rebalancing needed)
                analysis["rebalancing_score"] = min(100, analysis["average_deviation"] * 1000)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio health: {e}")
            return {}

    def get_rebalancing_recommendations(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        market_conditions: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Get specific rebalancing recommendations"""
        try:
            recommendations = []
            
            for symbol in set(current_weights.keys()) | set(target_weights.keys()):
                current = current_weights.get(symbol, 0.0)
                target = target_weights.get(symbol, 0.0)
                deviation = target - current
                
                if abs(deviation) > 0.05:  # 5% threshold
                    recommendation = {
                        "symbol": symbol,
                        "current_weight": current,
                        "target_weight": target,
                        "deviation": deviation,
                        "action": "BUY" if deviation > 0 else "SELL",
                        "priority": self._get_recommendation_priority(abs(deviation)),
                        "urgency": self._get_recommendation_urgency(abs(deviation)),
                        "estimated_impact": self._estimate_recommendation_impact(abs(deviation))
                    }
                    recommendations.append(recommendation)
            
            # Sort by priority and urgency
            recommendations.sort(
                key=lambda x: (self._priority_score(x["priority"]), x["urgency"]), 
                reverse=True
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting rebalancing recommendations: {e}")
            return []

    def _get_recommendation_priority(self, deviation: float) -> str:
        """Get recommendation priority based on deviation"""
        if abs(deviation) > 0.10:
            return "HIGH"
        elif abs(deviation) > 0.05:
            return "MEDIUM"
        else:
            return "LOW"

    def _get_recommendation_urgency(self, deviation: float) -> float:
        """Get recommendation urgency score (0-1)"""
        return min(1.0, abs(deviation) * 10)

    def _estimate_recommendation_impact(self, deviation: float) -> str:
        """Estimate the impact of following the recommendation"""
        if abs(deviation) > 0.15:
            return "SIGNIFICANT"
        elif abs(deviation) > 0.08:
            return "MODERATE"
        else:
            return "MINOR"

    def _priority_score(self, priority: str) -> int:
        """Convert priority to numeric score for sorting"""
        priority_scores = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }
        return priority_scores.get(priority, 1)
