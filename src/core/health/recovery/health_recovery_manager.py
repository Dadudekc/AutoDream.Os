#!/usr/bin/env python3
"""
Health Recovery Manager - V2 Modular Architecture
================================================

Handles automated health recovery actions and remediation.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from threading import Lock

from ..types.health_types import HealthAlert, RecoveryAction


logger = logging.getLogger(__name__)


class HealthRecoveryManager:
    """
    Health Recovery Manager - Single responsibility: Execute recovery actions
    
    Handles all recovery operations including:
    - Automated recovery execution
    - Recovery action management
    - Recovery success tracking
    - Recovery strategy management
    """

    def __init__(self):
        """Initialize health recovery manager"""
        self.logger = logging.getLogger(f"{__name__}.HealthRecoveryManager")
        
        # Recovery actions
        self.recovery_actions: Dict[str, RecoveryAction] = {}
        self.recovery_strategies: Dict[str, Dict[str, Any]] = {}
        
        # Recovery configuration
        self.auto_recovery_enabled = True
        self.max_concurrent_recoveries = 5
        self.recovery_timeout = 300  # 5 minutes
        
        # Thread safety
        self._lock = Lock()
        
        # Setup default recovery strategies
        self._setup_default_recovery_strategies()
        
        self.logger.info("✅ Health Recovery Manager initialized successfully")

    def _setup_default_recovery_strategies(self):
        """Setup default recovery strategies"""
        try:
            # CPU overload recovery
            self.recovery_strategies["cpu_usage"] = {
                "threshold": 90.0,
                "actions": [
                    {
                        "name": "reduce_worker_threads",
                        "target": "cpu_usage < 80",
                        "execution_time": 30.0,
                        "success_rate": 0.8
                    },
                    {
                        "name": "enable_cpu_throttling",
                        "target": "cpu_usage < 80",
                        "execution_time": 15.0,
                        "success_rate": 0.9
                    }
                ]
            }
            
            # Memory pressure recovery
            self.recovery_strategies["memory_usage"] = {
                "threshold": 85.0,
                "actions": [
                    {
                        "name": "trigger_garbage_collection",
                        "target": "memory_usage < 80",
                        "execution_time": 45.0,
                        "success_rate": 0.7
                    },
                    {
                        "name": "clear_cache",
                        "target": "memory_usage < 80",
                        "execution_time": 20.0,
                        "success_rate": 0.8
                    }
                ]
            }
            
            # Disk space recovery
            self.recovery_strategies["disk_usage"] = {
                "threshold": 90.0,
                "actions": [
                    {
                        "name": "clean_temp_files",
                        "target": "disk_usage < 85",
                        "execution_time": 60.0,
                        "success_rate": 0.9
                    },
                    {
                        "name": "compress_log_files",
                        "target": "disk_usage < 85",
                        "execution_time": 120.0,
                        "success_rate": 0.8
                    }
                ]
            }
            
            # Response time recovery
            self.recovery_strategies["response_time"] = {
                "threshold": 5.0,
                "actions": [
                    {
                        "name": "enable_response_caching",
                        "target": "response_time < 2.0",
                        "execution_time": 30.0,
                        "success_rate": 0.8
                    },
                    {
                        "name": "optimize_database_queries",
                        "target": "response_time < 2.0",
                        "execution_time": 90.0,
                        "success_rate": 0.6
                    }
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to setup default recovery strategies: {e}")

    def execute_automated_recovery(self, alert: HealthAlert) -> Dict[str, Any]:
        """Execute automated recovery actions for health issues"""
        try:
            if not self.auto_recovery_enabled:
                return {"error": "Automated recovery is disabled"}
            
            if alert.metric_name not in self.recovery_strategies:
                return {"error": f"No recovery strategy for metric {alert.metric_name}"}
            
            strategy = self.recovery_strategies[alert.metric_name]
            recovery_actions = {
                "actions_executed": [],
                "success_rate": 0.0,
                "recovery_status": "pending",
                "total_execution_time": 0.0
            }
            
            # Execute recovery actions based on strategy
            for action_config in strategy["actions"]:
                action_result = self._execute_recovery_action(alert, action_config)
                if action_result:
                    recovery_actions["actions_executed"].append(action_result)
                    recovery_actions["total_execution_time"] += action_result.get("execution_time", 0.0)
            
            # Calculate success rate
            if recovery_actions["actions_executed"]:
                successful_actions = len([
                    a for a in recovery_actions["actions_executed"] 
                    if a.get("status") == "completed"
                ])
                recovery_actions["success_rate"] = successful_actions / len(recovery_actions["actions_executed"])
                
                if recovery_actions["success_rate"] > 0.5:
                    recovery_actions["recovery_status"] = "successful"
                else:
                    recovery_actions["recovery_status"] = "partial"
            
            self.logger.info(f"Automated recovery completed for alert {alert.id}")
            return recovery_actions
            
        except Exception as e:
            self.logger.error(f"Failed to execute automated recovery: {e}")
            return {"error": str(e)}

    def _execute_recovery_action(self, alert: HealthAlert, action_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a single recovery action"""
        try:
            action_name = action_config["name"]
            target = action_config["target"]
            expected_execution_time = action_config["execution_time"]
            expected_success_rate = action_config["success_rate"]
            
            # Create recovery action record
            action_id = f"recovery_{alert.id}_{action_name}_{int(time.time())}"
            recovery_action = RecoveryAction(
                action_id=action_id,
                action_name=action_name,
                target_metric=alert.metric_name,
                target_value=0.0,  # Will be updated based on target
                current_value=alert.metric_value,
                status="executing",
                execution_time=None,
                result=None,
                metadata={"alert_id": alert.id, "expected_success_rate": expected_success_rate}
            )
            
            # Store action
            with self._lock:
                self.recovery_actions[action_id] = recovery_action
            
            # Simulate action execution
            start_time = time.time()
            time.sleep(0.1)  # Simulate execution time
            execution_time = time.time() - start_time
            
            # Determine success based on expected success rate
            import random
            success = random.random() < expected_success_rate
            
            # Update action status
            recovery_action.execution_time = execution_time
            recovery_action.status = "completed" if success else "failed"
            recovery_action.result = f"Action {'succeeded' if success else 'failed'}"
            
            # Update target value based on success
            if success:
                recovery_action.target_value = alert.metric_value * 0.8  # Simulate improvement
            
            action_result = {
                "action": action_name,
                "target": target,
                "status": recovery_action.status,
                "execution_time": execution_time,
                "result": recovery_action.result,
                "success": success
            }
            
            self.logger.info(f"Recovery action {action_name} {'succeeded' if success else 'failed'}")
            return action_result
            
        except Exception as e:
            self.logger.error(f"Failed to execute recovery action {action_config.get('name', 'unknown')}: {e}")
            return None

    def add_recovery_strategy(self, metric_name: str, strategy: Dict[str, Any]) -> bool:
        """Add a new recovery strategy"""
        try:
            with self._lock:
                self.recovery_strategies[metric_name] = strategy
                self.logger.info(f"Added recovery strategy for {metric_name}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to add recovery strategy for {metric_name}: {e}")
            return False

    def update_recovery_strategy(self, metric_name: str, strategy: Dict[str, Any]) -> bool:
        """Update an existing recovery strategy"""
        try:
            with self._lock:
                if metric_name in self.recovery_strategies:
                    self.recovery_strategies[metric_name] = strategy
                    self.logger.info(f"Updated recovery strategy for {metric_name}")
                    return True
                else:
                    self.logger.warning(f"Recovery strategy not found for {metric_name}")
                    return False
        except Exception as e:
            self.logger.error(f"Failed to update recovery strategy for {metric_name}: {e}")
            return False

    def remove_recovery_strategy(self, metric_name: str) -> bool:
        """Remove a recovery strategy"""
        try:
            with self._lock:
                if metric_name in self.recovery_strategies:
                    del self.recovery_strategies[metric_name]
                    self.logger.info(f"Removed recovery strategy for {metric_name}")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"Failed to remove recovery strategy for {metric_name}: {e}")
            return False

    def get_recovery_strategy(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get a recovery strategy"""
        try:
            with self._lock:
                return self.recovery_strategies.get(metric_name)
        except Exception as e:
            self.logger.error(f"Failed to get recovery strategy for {metric_name}: {e}")
            return None

    def get_all_recovery_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Get all recovery strategies"""
        try:
            with self._lock:
                return self.recovery_strategies.copy()
        except Exception as e:
            self.logger.error(f"Failed to get all recovery strategies: {e}")
            return {}

    def get_recovery_action(self, action_id: str) -> Optional[RecoveryAction]:
        """Get a specific recovery action"""
        try:
            with self._lock:
                return self.recovery_actions.get(action_id)
        except Exception as e:
            self.logger.error(f"Failed to get recovery action {action_id}: {e}")
            return None

    def get_all_recovery_actions(self) -> List[RecoveryAction]:
        """Get all recovery actions"""
        try:
            with self._lock:
                return list(self.recovery_actions.values())
        except Exception as e:
            self.logger.error(f"Failed to get all recovery actions: {e}")
            return []

    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get recovery statistics"""
        try:
            with self._lock:
                total_actions = len(self.recovery_actions)
                completed_actions = len([a for a in self.recovery_actions.values() if a.status == "completed"])
                failed_actions = len([a for a in self.recovery_actions.values() if a.status == "failed"])
                pending_actions = len([a for a in self.recovery_actions.values() if a.status == "pending"])
                
                # Calculate success rate
                success_rate = completed_actions / total_actions if total_actions > 0 else 0.0
                
                # Calculate average execution time
                execution_times = [a.execution_time for a in self.recovery_actions.values() if a.execution_time]
                avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0.0
                
                return {
                    "total_actions": total_actions,
                    "completed_actions": completed_actions,
                    "failed_actions": failed_actions,
                    "pending_actions": pending_actions,
                    "success_rate": round(success_rate, 3),
                    "average_execution_time": round(avg_execution_time, 3),
                    "total_strategies": len(self.recovery_strategies),
                    "auto_recovery_enabled": self.auto_recovery_enabled,
                    "last_updated": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get recovery statistics: {e}")
            return {"error": str(e)}

    def enable_auto_recovery(self):
        """Enable automated recovery"""
        try:
            self.auto_recovery_enabled = True
            self.logger.info("✅ Automated recovery enabled")
        except Exception as e:
            self.logger.error(f"Failed to enable auto recovery: {e}")

    def disable_auto_recovery(self):
        """Disable automated recovery"""
        try:
            self.auto_recovery_enabled = False
            self.logger.info("⚠️ Automated recovery disabled")
        except Exception as e:
            self.logger.error(f"Failed to disable auto recovery: {e}")

    def clear_recovery_actions(self):
        """Clear all recovery actions"""
        try:
            with self._lock:
                self.recovery_actions.clear()
                self.logger.info("✅ All recovery actions cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear recovery actions: {e}")

    def test_recovery_strategy(self, metric_name: str) -> bool:
        """Test a recovery strategy"""
        try:
            strategy = self.get_recovery_strategy(metric_name)
            if not strategy:
                self.logger.error(f"Recovery strategy not found for {metric_name}")
                return False
            
            # Create a test alert
            test_alert = HealthAlert(
                id="test_recovery",
                type=None,  # Will be set by the manager
                level=None,  # Will be set by the manager
                component="test",
                message="Test recovery action",
                metric_name=metric_name,
                metric_value=95.0,  # High value to trigger recovery
                threshold=90.0,
                timestamp=datetime.now().isoformat(),
                acknowledged=False,
                acknowledged_by=None,
                acknowledged_at=None,
                resolved=False,
                resolved_at=None,
                metadata={"test": True}
            )
            
            # Execute test recovery
            result = self.execute_automated_recovery(test_alert)
            
            if "error" not in result:
                self.logger.info(f"✅ Test recovery strategy successful for {metric_name}")
                return True
            else:
                self.logger.error(f"❌ Test recovery strategy failed for {metric_name}: {result['error']}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to test recovery strategy for {metric_name}: {e}")
            return False

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.clear_recovery_actions()
            self.logger.info("✅ Health Recovery Manager cleanup completed")
        except Exception as e:
            self.logger.error(f"Health Recovery Manager cleanup failed: {e}")

