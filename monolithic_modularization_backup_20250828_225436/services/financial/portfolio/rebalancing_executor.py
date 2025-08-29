"""
Portfolio Rebalancing Executor Module

Single Responsibility: Plan execution and trade management.
Follows V2 coding standards: Clean OOP design, SRP compliance, focused functionality.
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from rebalancing_core import RebalancingPlan, RebalancingSignal

# Configure logging
logger = logging.getLogger(__name__)


class RebalancingExecutor:
    """Portfolio rebalancing plan execution and trade management"""
    
    def __init__(self):
        """Initialize rebalancing executor"""
        self.execution_history = []
        self.current_executions = {}

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
                
                # Record execution
                self._record_execution(plan, True)
            else:
                plan.status = "FAILED"
                logger.error(f"Rebalancing plan {plan.plan_id} failed")
                
                # Record execution
                self._record_execution(plan, False)
            
            return execution_success
            
        except Exception as e:
            logger.error(f"Error executing rebalancing plan: {e}")
            if plan:
                plan.status = "FAILED"
                self._record_execution(plan, False)
            return False

    def _execute_trades(self, plan: RebalancingPlan, execution_prices: Dict[str, float] = None) -> bool:
        """Execute trades for rebalancing plan (simulated)"""
        try:
            logger.info(f"Executing {len(plan.signals)} trades for plan {plan.plan_id}")
            
            # Simulate trade execution
            for signal in plan.signals:
                logger.info(f"Executing {signal.action} order for {signal.symbol}: "
                          f"{abs(signal.weight_difference):.4f} weight adjustment")
                
                # Simulate execution delay
                time.sleep(0.1)
            
            logger.info("All trades executed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error executing trades: {e}")
            return False

    def _record_execution(self, plan: RebalancingPlan, success: bool):
        """Record execution result in history"""
        try:
            execution_record = {
                "plan_id": plan.plan_id,
                "timestamp": datetime.now(),
                "success": success,
                "signals_count": len(plan.signals),
                "total_cost": plan.total_cost,
                "estimated_impact": plan.estimated_impact,
                "execution_time": None,
                "completion_time": None
            }
            
            if plan.execution_date and plan.completion_date:
                execution_record["execution_time"] = (plan.completion_date - plan.execution_date).total_seconds()
                execution_record["completion_time"] = plan.completion_date
            
            self.execution_history.append(execution_record)
            
            # Keep only last 100 executions
            if len(self.execution_history) > 100:
                self.execution_history = self.execution_history[-100:]
                
        except Exception as e:
            logger.error(f"Error recording execution: {e}")

    def get_execution_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get execution history"""
        try:
            return self.execution_history[-limit:] if limit > 0 else self.execution_history
        except Exception as e:
            logger.error(f"Error getting execution history: {e}")
            return []

    def get_execution_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        try:
            if not self.execution_history:
                return {}
            
            total_executions = len(self.execution_history)
            successful_executions = sum(1 for record in self.execution_history if record["success"])
            failed_executions = total_executions - successful_executions
            
            success_rate = (successful_executions / total_executions) * 100 if total_executions > 0 else 0
            
            # Calculate average execution time
            execution_times = [record["execution_time"] for record in self.execution_history 
                             if record["execution_time"] is not None]
            avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
            
            # Calculate total costs and impact
            total_costs = sum(record["total_cost"] for record in self.execution_history)
            total_impact = sum(record["estimated_impact"] for record in self.execution_history)
            
            return {
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "failed_executions": failed_executions,
                "success_rate": success_rate,
                "average_execution_time": avg_execution_time,
                "total_costs": total_costs,
                "total_impact": total_impact
            }
            
        except Exception as e:
            logger.error(f"Error calculating execution statistics: {e}")
            return {}

    def validate_plan_executability(self, plan: RebalancingPlan) -> Tuple[bool, List[str]]:
        """Validate if a plan can be executed"""
        try:
            issues = []
            
            # Check plan status
            if plan.status != "PENDING":
                issues.append(f"Plan status is {plan.status}, must be PENDING")
            
            # Check if plan has signals
            if not plan.signals:
                issues.append("Plan has no rebalancing signals")
            
            # Check signal validity
            for i, signal in enumerate(plan.signals):
                if not signal.symbol:
                    issues.append(f"Signal {i} has no symbol")
                if abs(signal.weight_difference) < 0.001:
                    issues.append(f"Signal {i} has negligible weight difference")
                if signal.action not in ["BUY", "SELL", "HOLD"]:
                    issues.append(f"Signal {i} has invalid action: {signal.action}")
            
            # Check cost thresholds
            if plan.total_cost > 10000:  # $10K threshold
                issues.append("Total cost exceeds maximum threshold")
            
            return len(issues) == 0, issues
            
        except Exception as e:
            logger.error(f"Error validating plan executability: {e}")
            return False, [f"Validation error: {e}"]

    def simulate_execution(self, plan: RebalancingPlan, market_conditions: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate plan execution without actually executing trades"""
        try:
            simulation = {
                "plan_id": plan.plan_id,
                "simulation_timestamp": datetime.now(),
                "estimated_execution_time": len(plan.signals) * 0.1,  # 0.1s per trade
                "estimated_success_rate": 0.95,  # 95% success rate assumption
                "market_impact_analysis": {},
                "cost_analysis": {},
                "risk_assessment": {}
            }
            
            # Analyze market impact
            for signal in plan.signals:
                simulation["market_impact_analysis"][signal.symbol] = {
                    "action": signal.action,
                    "weight_change": abs(signal.weight_difference),
                    "estimated_impact": signal.market_impact,
                    "priority": signal.priority
                }
            
            # Analyze costs
            simulation["cost_analysis"] = {
                "total_cost": plan.total_cost,
                "cost_per_trade": plan.total_cost / len(plan.signals) if plan.signals else 0,
                "cost_efficiency": "HIGH" if plan.total_cost < 1000 else "MEDIUM" if plan.total_cost < 5000 else "LOW"
            }
            
            # Risk assessment
            high_priority_signals = sum(1 for signal in plan.signals if signal.priority == "HIGH")
            simulation["risk_assessment"] = {
                "high_priority_signals": high_priority_signals,
                "risk_level": "HIGH" if high_priority_signals >= 3 else "MEDIUM" if high_priority_signals >= 1 else "LOW",
                "execution_complexity": "HIGH" if len(plan.signals) > 5 else "MEDIUM" if len(plan.signals) > 2 else "LOW"
            }
            
            return simulation
            
        except Exception as e:
            logger.error(f"Error simulating execution: {e}")
            return {}

    def cancel_execution(self, plan_id: str) -> bool:
        """Cancel an ongoing execution"""
        try:
            if plan_id in self.current_executions:
                logger.info(f"Cancelling execution of plan {plan_id}")
                # In a real implementation, this would cancel actual trades
                del self.current_executions[plan_id]
                return True
            else:
                logger.warning(f"No active execution found for plan {plan_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error cancelling execution: {e}")
            return False
