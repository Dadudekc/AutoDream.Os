"""
Core Service Manager - Phase-2 Manager Consolidation
===================================================

Consolidates ArchitecturalOnboardingManager, ErrorRecoveryManager, and ResultsManager.
Handles all service operations: onboarding, error recovery, and results processing.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
import json
import uuid
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from enum import Enum
from .contracts import ServiceManager, ManagerContext, ManagerResult
from src.core.constants import get_completion_signal


class OnboardingStatus(Enum):
    """Onboarding status levels."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RecoveryStrategy(Enum):
    """Error recovery strategies."""

    RETRY = "retry"
    FALLBACK = "fallback"
    ESCALATE = "escalate"
    IGNORE = "ignore"
    ROLLBACK = "rollback"


class ResultStatus(Enum):
    """Result processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class CoreServiceManager(ServiceManager):
    """Core service manager - consolidates onboarding, recovery, and results operations."""

    def __init__(self):
        """Initialize core service manager."""
        self.onboarding_sessions: Dict[str, Dict[str, Any]] = {}
        self.recovery_strategies: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Dict[str, Any]] = {}
        self.onboarding_templates: Dict[str, Dict[str, Any]] = {}
        self.recovery_callbacks: Dict[str, Callable] = {}
        self.result_callbacks: Dict[str, Callable] = {}
        self.onboarding_callbacks: Dict[str, Callable] = {}

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize service manager."""
        try:
            # Setup default onboarding templates
            self._setup_default_onboarding_templates()

            # Setup default recovery strategies
            self._setup_default_recovery_strategies()

            context.logger("Core Service Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize Core Service Manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute service operation."""
        try:
            if operation == "onboard_agent":
                agent_data = payload.get("agent_data", {})
                return self.onboard_agent(context, agent_data)
            elif operation == "recover_from_error":
                error_data = payload.get("error_data", {})
                return self.recover_from_error(context, error_data)
            elif operation == "process_results":
                results_data = payload.get("results_data", {})
                return self.process_results(context, results_data)
            elif operation == "start_onboarding":
                return self._start_onboarding(context, payload)
            elif operation == "complete_onboarding":
                return self._complete_onboarding(context, payload)
            elif operation == "register_recovery_strategy":
                return self._register_recovery_strategy(context, payload)
            elif operation == "get_onboarding_status":
                return self._get_onboarding_status(context, payload)
            elif operation == "get_recovery_strategies":
                return self._get_recovery_strategies(context, payload)
            elif operation == "get_results":
                return self._get_results(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def onboard_agent(
        self, context: ManagerContext, agent_data: Dict[str, Any]
    ) -> ManagerResult:
        """Onboard an agent."""
        try:
            agent_id = agent_data.get("agent_id", str(uuid.uuid4()))
            agent_name = agent_data.get("agent_name", f"Agent-{agent_id}")
            role = agent_data.get("role", "general")
            template = agent_data.get("template", "default")

            # Get onboarding template
            if template not in self.onboarding_templates:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Onboarding template not found: {template}",
                )

            template_data = self.onboarding_templates[template]

            # Create onboarding session
            session_id = str(uuid.uuid4())
            session = {
                "session_id": session_id,
                "agent_id": agent_id,
                "agent_name": agent_name,
                "role": role,
                "template": template,
                "status": OnboardingStatus.PENDING,
                "created_at": datetime.now().isoformat(),
                "steps": template_data.get("steps", []),
                "current_step": 0,
                "progress": 0.0,
                "metadata": agent_data.get("metadata", {}),
            }

            self.onboarding_sessions[session_id] = session

            # Execute onboarding callbacks
            for callback in self.onboarding_callbacks.values():
                try:
                    callback("onboarding_started", session)
                except Exception as e:
                    context.logger(f"Onboarding callback failed: {e}")

            return ManagerResult(
                success=True,
                data={"session_id": session_id, "session": session, "onboarded": True},
                metrics={"total_sessions": len(self.onboarding_sessions)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def recover_from_error(
        self, context: ManagerContext, error_data: Dict[str, Any]
    ) -> ManagerResult:
        """Recover from error."""
        try:
            error_type = error_data.get("error_type", "general")
            error_message = error_data.get("error_message", "")
            context_data = error_data.get("context", {})

            # Find appropriate recovery strategy
            strategy = self._find_recovery_strategy(
                error_type, error_message, context_data
            )

            if not strategy:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="No recovery strategy found for this error",
                )

            # Execute recovery strategy
            recovery_id = str(uuid.uuid4())
            recovery_result = self._execute_recovery_strategy(
                strategy, error_data, context
            )

            # Execute recovery callbacks
            for callback in self.recovery_callbacks.values():
                try:
                    callback(
                        "recovery_executed",
                        {
                            "recovery_id": recovery_id,
                            "strategy": strategy,
                            "error_data": error_data,
                            "result": recovery_result,
                        },
                    )
                except Exception as e:
                    context.logger(f"Recovery callback failed: {e}")

            return ManagerResult(
                success=recovery_result.get("success", False),
                data={
                    "recovery_id": recovery_id,
                    "strategy": strategy,
                    "result": recovery_result,
                },
                metrics={"recovery_attempts": 1},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def process_results(
        self, context: ManagerContext, results_data: Dict[str, Any]
    ) -> ManagerResult:
        """Process results."""
        try:
            result_id = results_data.get("result_id", str(uuid.uuid4()))
            result_type = results_data.get("result_type", "general")
            data = results_data.get("data", {})
            metadata = results_data.get("metadata", {})

            # Create result record
            result = {
                "result_id": result_id,
                "result_type": result_type,
                "data": data,
                "metadata": metadata,
                "status": ResultStatus.PENDING,
                "created_at": datetime.now().isoformat(),
                "processed_at": None,
                "processing_time": None,
            }

            # Process result based on type
            processing_result = self._process_result_by_type(result_type, data, context)

            # Update result
            result["status"] = (
                ResultStatus.COMPLETED
                if processing_result["success"]
                else ResultStatus.FAILED
            )
            result["processed_at"] = datetime.now().isoformat()
            result["processing_result"] = processing_result

            # Calculate processing time
            if result["processed_at"]:
                created_at = datetime.fromisoformat(result["created_at"])
                processed_at = datetime.fromisoformat(result["processed_at"])
                result["processing_time"] = (processed_at - created_at).total_seconds()

            self.results[result_id] = result

            # Execute result callbacks
            for callback in self.result_callbacks.values():
                try:
                    callback("result_processed", result)
                except Exception as e:
                    context.logger(f"Result callback failed: {e}")

            return ManagerResult(
                success=processing_result["success"],
                data={"result_id": result_id, "result": result, "processed": True},
                metrics={"total_results": len(self.results)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup service manager."""
        try:
            # Clear all data
            self.onboarding_sessions.clear()
            self.recovery_strategies.clear()
            self.results.clear()
            self.onboarding_templates.clear()
            self.recovery_callbacks.clear()
            self.result_callbacks.clear()
            self.onboarding_callbacks.clear()

            context.logger(
                f"Core Service Manager cleaned up {get_completion_signal()}"
            )
            return True
        except Exception as e:
            context.logger(f"Failed to cleanup Core Service Manager: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get service manager status."""
        pending_sessions = sum(
            1
            for s in self.onboarding_sessions.values()
            if s["status"] == OnboardingStatus.PENDING
        )
        in_progress_sessions = sum(
            1
            for s in self.onboarding_sessions.values()
            if s["status"] == OnboardingStatus.IN_PROGRESS
        )
        completed_sessions = sum(
            1
            for s in self.onboarding_sessions.values()
            if s["status"] == OnboardingStatus.COMPLETED
        )

        pending_results = sum(
            1 for r in self.results.values() if r["status"] == ResultStatus.PENDING
        )
        completed_results = sum(
            1 for r in self.results.values() if r["status"] == ResultStatus.COMPLETED
        )

        return {
            "total_onboarding_sessions": len(self.onboarding_sessions),
            "pending_sessions": pending_sessions,
            "in_progress_sessions": in_progress_sessions,
            "completed_sessions": completed_sessions,
            "total_recovery_strategies": len(self.recovery_strategies),
            "total_results": len(self.results),
            "pending_results": pending_results,
            "completed_results": completed_results,
            "total_templates": len(self.onboarding_templates),
        }

    def _start_onboarding(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Start onboarding process."""
        try:
            session_id = payload.get("session_id", "")

            if session_id not in self.onboarding_sessions:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Onboarding session not found: {session_id}",
                )

            session = self.onboarding_sessions[session_id]
            session["status"] = OnboardingStatus.IN_PROGRESS
            session["started_at"] = datetime.now().isoformat()

            return ManagerResult(
                success=True,
                data={"session_id": session_id, "status": "started"},
                metrics={},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _complete_onboarding(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Complete onboarding process."""
        try:
            session_id = payload.get("session_id", "")
            success = payload.get("success", True)
            notes = payload.get("notes", "")

            if session_id not in self.onboarding_sessions:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Onboarding session not found: {session_id}",
                )

            session = self.onboarding_sessions[session_id]
            session["status"] = (
                OnboardingStatus.COMPLETED if success else OnboardingStatus.FAILED
            )
            session["completed_at"] = datetime.now().isoformat()
            session["completion_notes"] = notes
            session["progress"] = 100.0

            return ManagerResult(
                success=True,
                data={
                    "session_id": session_id,
                    "status": "completed",
                    "success": success,
                },
                metrics={},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _register_recovery_strategy(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Register a recovery strategy."""
        try:
            strategy_name = payload.get("strategy_name", "")
            strategy_type = RecoveryStrategy(payload.get("strategy_type", "retry"))
            conditions = payload.get("conditions", {})
            actions = payload.get("actions", [])

            strategy = {
                "name": strategy_name,
                "type": strategy_type,
                "conditions": conditions,
                "actions": actions,
                "enabled": payload.get("enabled", True),
                "created_at": datetime.now().isoformat(),
            }

            self.recovery_strategies[strategy_name] = strategy

            return ManagerResult(
                success=True,
                data={
                    "strategy_name": strategy_name,
                    "strategy": strategy,
                    "registered": True,
                },
                metrics={"total_strategies": len(self.recovery_strategies)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _get_onboarding_status(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Get onboarding status."""
        try:
            session_id = payload.get("session_id", "")

            if session_id and session_id in self.onboarding_sessions:
                session = self.onboarding_sessions[session_id]
                return ManagerResult(
                    success=True, data={"session": session}, metrics={}
                )
            else:
                # Return all sessions
                return ManagerResult(
                    success=True,
                    data={"sessions": list(self.onboarding_sessions.values())},
                    metrics={"total_sessions": len(self.onboarding_sessions)},
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _get_recovery_strategies(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Get recovery strategies."""
        try:
            strategy_type_filter = payload.get("strategy_type_filter")

            filtered_strategies = []
            for strategy in self.recovery_strategies.values():
                if (
                    strategy_type_filter
                    and strategy["type"].value != strategy_type_filter
                ):
                    continue
                filtered_strategies.append(strategy)

            return ManagerResult(
                success=True,
                data={"strategies": filtered_strategies},
                metrics={"total_strategies": len(filtered_strategies)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _get_results(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Get results."""
        try:
            result_type_filter = payload.get("result_type_filter")
            status_filter = payload.get("status_filter")

            filtered_results = []
            for result in self.results.values():
                if result_type_filter and result["result_type"] != result_type_filter:
                    continue
                if status_filter and result["status"].value != status_filter:
                    continue
                filtered_results.append(result)

            return ManagerResult(
                success=True,
                data={"results": filtered_results},
                metrics={"total_results": len(filtered_results)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _find_recovery_strategy(
        self, error_type: str, error_message: str, context_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Find appropriate recovery strategy for error."""
        try:
            for strategy in self.recovery_strategies.values():
                if not strategy.get("enabled", True):
                    continue

                conditions = strategy.get("conditions", {})

                # Check error type match
                if (
                    "error_type" in conditions
                    and conditions["error_type"] != error_type
                ):
                    continue

                # Check error message pattern
                if "error_message_pattern" in conditions:
                    import re

                    if not re.search(
                        conditions["error_message_pattern"], error_message
                    ):
                        continue

                # Check context conditions
                context_match = True
                for key, value in conditions.get("context", {}).items():
                    if context_data.get(key) != value:
                        context_match = False
                        break

                if context_match:
                    return strategy

            return None
        except Exception:
            return None

    def _execute_recovery_strategy(
        self,
        strategy: Dict[str, Any],
        error_data: Dict[str, Any],
        context: ManagerContext,
    ) -> Dict[str, Any]:
        """Execute recovery strategy."""
        try:
            strategy_type = strategy["type"]
            actions = strategy.get("actions", [])

            if strategy_type == RecoveryStrategy.RETRY:
                return self._execute_retry_strategy(actions, error_data, context)
            elif strategy_type == RecoveryStrategy.FALLBACK:
                return self._execute_fallback_strategy(actions, error_data, context)
            elif strategy_type == RecoveryStrategy.ESCALATE:
                return self._execute_escalate_strategy(actions, error_data, context)
            elif strategy_type == RecoveryStrategy.IGNORE:
                return self._execute_ignore_strategy(actions, error_data, context)
            elif strategy_type == RecoveryStrategy.ROLLBACK:
                return self._execute_rollback_strategy(actions, error_data, context)
            else:
                return {
                    "success": False,
                    "error": f"Unknown strategy type: {strategy_type}",
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_retry_strategy(
        self,
        actions: List[Dict[str, Any]],
        error_data: Dict[str, Any],
        context: ManagerContext,
    ) -> Dict[str, Any]:
        """Execute retry strategy."""
        try:
            max_retries = actions[0].get("max_retries", 3) if actions else 3
            retry_delay = actions[0].get("retry_delay", 1) if actions else 1

            for attempt in range(max_retries):
                try:
                    # Simulate retry operation
                    context.logger(f"Retry attempt {attempt + 1}/{max_retries}")
                    return {"success": True, "attempts": attempt + 1}
                except Exception as e:
                    if attempt == max_retries - 1:
                        return {
                            "success": False,
                            "error": str(e),
                            "attempts": attempt + 1,
                        }
                    # Wait before next retry
                    import time

                    time.sleep(retry_delay)

            return {"success": False, "error": "Max retries exceeded"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_fallback_strategy(
        self,
        actions: List[Dict[str, Any]],
        error_data: Dict[str, Any],
        context: ManagerContext,
    ) -> Dict[str, Any]:
        """Execute fallback strategy."""
        try:
            fallback_action = actions[0] if actions else {}
            fallback_type = fallback_action.get("fallback_type", "default")

            context.logger(f"Executing fallback strategy: {fallback_type}")
            return {"success": True, "fallback_type": fallback_type}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_escalate_strategy(
        self,
        actions: List[Dict[str, Any]],
        error_data: Dict[str, Any],
        context: ManagerContext,
    ) -> Dict[str, Any]:
        """Execute escalate strategy."""
        try:
            escalation_level = (
                actions[0].get("escalation_level", "high") if actions else "high"
            )
            notify_targets = actions[0].get("notify_targets", []) if actions else []

            context.logger(f"Escalating error to level: {escalation_level}")
            return {
                "success": True,
                "escalation_level": escalation_level,
                "notified": notify_targets,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_ignore_strategy(
        self,
        actions: List[Dict[str, Any]],
        error_data: Dict[str, Any],
        context: ManagerContext,
    ) -> Dict[str, Any]:
        """Execute ignore strategy."""
        try:
            context.logger("Ignoring error as per strategy")
            return {"success": True, "ignored": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_rollback_strategy(
        self,
        actions: List[Dict[str, Any]],
        error_data: Dict[str, Any],
        context: ManagerContext,
    ) -> Dict[str, Any]:
        """Execute rollback strategy."""
        try:
            rollback_point = (
                actions[0].get("rollback_point", "last_known_good")
                if actions
                else "last_known_good"
            )

            context.logger(f"Rolling back to: {rollback_point}")
            return {"success": True, "rollback_point": rollback_point}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _process_result_by_type(
        self, result_type: str, data: Dict[str, Any], context: ManagerContext
    ) -> Dict[str, Any]:
        """Process result based on type."""
        try:
            if result_type == "validation":
                return self._process_validation_result(data, context)
            elif result_type == "analysis":
                return self._process_analysis_result(data, context)
            elif result_type == "integration":
                return self._process_integration_result(data, context)
            elif result_type == "performance":
                return self._process_performance_result(data, context)
            else:
                return self._process_general_result(data, context)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _process_validation_result(
        self, data: Dict[str, Any], context: ManagerContext
    ) -> Dict[str, Any]:
        """Process validation result."""
        try:
            validation_rules = data.get("rules", [])
            validation_data = data.get("data", {})

            passed_rules = 0
            failed_rules = 0

            for rule in validation_rules:
                if self._validate_rule(rule, validation_data):
                    passed_rules += 1
                else:
                    failed_rules += 1

            return {
                "success": failed_rules == 0,
                "passed_rules": passed_rules,
                "failed_rules": failed_rules,
                "total_rules": len(validation_rules),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _process_analysis_result(
        self, data: Dict[str, Any], context: ManagerContext
    ) -> Dict[str, Any]:
        """Process analysis result."""
        try:
            analysis_type = data.get("analysis_type", "general")
            analysis_data = data.get("data", [])

            # Simulate analysis processing
            if analysis_type == "statistical":
                return {
                    "success": True,
                    "analysis_type": analysis_type,
                    "data_points": len(analysis_data),
                    "summary": "Statistical analysis completed",
                }
            else:
                return {
                    "success": True,
                    "analysis_type": analysis_type,
                    "processed": True,
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _process_integration_result(
        self, data: Dict[str, Any], context: ManagerContext
    ) -> Dict[str, Any]:
        """Process integration result."""
        try:
            integration_type = data.get("integration_type", "general")
            integration_data = data.get("data", {})

            return {
                "success": True,
                "integration_type": integration_type,
                "integrated_components": len(integration_data),
                "status": "integrated",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _process_performance_result(
        self, data: Dict[str, Any], context: ManagerContext
    ) -> Dict[str, Any]:
        """Process performance result."""
        try:
            metrics = data.get("metrics", {})
            thresholds = data.get("thresholds", {})

            performance_score = 0
            total_metrics = 0

            for metric_name, value in metrics.items():
                total_metrics += 1
                threshold = thresholds.get(metric_name, 0)
                if value >= threshold:
                    performance_score += 1

            return {
                "success": True,
                "performance_score": performance_score,
                "total_metrics": total_metrics,
                "score_percentage": (
                    (performance_score / total_metrics * 100)
                    if total_metrics > 0
                    else 0
                ),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _process_general_result(
        self, data: Dict[str, Any], context: ManagerContext
    ) -> Dict[str, Any]:
        """Process general result."""
        try:
            return {"success": True, "processed": True, "data_size": len(str(data))}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _validate_rule(self, rule: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Validate a single rule."""
        try:
            rule_type = rule.get("type", "equals")
            field = rule.get("field", "")
            expected = rule.get("expected")

            if field not in data:
                return False

            actual = data[field]

            if rule_type == "equals":
                return actual == expected
            elif rule_type == "not_equals":
                return actual != expected
            elif rule_type == "greater_than":
                return actual > expected
            elif rule_type == "less_than":
                return actual < expected
            elif rule_type == "contains":
                return expected in str(actual)
            else:
                return True
        except Exception:
            return False

    def _setup_default_onboarding_templates(self) -> None:
        """Setup default onboarding templates."""
        self.onboarding_templates = {
            "default": {
                "name": "default",
                "steps": [
                    "initialize_agent",
                    "load_configuration",
                    "setup_logging",
                    "verify_dependencies",
                    "complete_onboarding",
                ],
                "estimated_duration": 300,  # 5 minutes
            },
            "developer": {
                "name": "developer",
                "steps": [
                    "initialize_agent",
                    "load_configuration",
                    "setup_logging",
                    "verify_dependencies",
                    "setup_development_environment",
                    "run_tests",
                    "complete_onboarding",
                ],
                "estimated_duration": 600,  # 10 minutes
            },
            "production": {
                "name": "production",
                "steps": [
                    "initialize_agent",
                    "load_configuration",
                    "setup_logging",
                    "verify_dependencies",
                    "security_validation",
                    "performance_check",
                    "complete_onboarding",
                ],
                "estimated_duration": 900,  # 15 minutes
            },
        }

    def _setup_default_recovery_strategies(self) -> None:
        """Setup default recovery strategies."""
        self.recovery_strategies = {
            "network_retry": {
                "name": "network_retry",
                "type": RecoveryStrategy.RETRY,
                "conditions": {
                    "error_type": "network",
                    "error_message_pattern": r"timeout|connection|network",
                },
                "actions": [{"max_retries": 3, "retry_delay": 2}],
                "enabled": True,
                "created_at": datetime.now().isoformat(),
            },
            "database_fallback": {
                "name": "database_fallback",
                "type": RecoveryStrategy.FALLBACK,
                "conditions": {
                    "error_type": "database",
                    "error_message_pattern": r"connection|timeout|unavailable",
                },
                "actions": [
                    {"fallback_type": "read_only", "fallback_database": "backup"}
                ],
                "enabled": True,
                "created_at": datetime.now().isoformat(),
            },
            "critical_escalation": {
                "name": "critical_escalation",
                "type": RecoveryStrategy.ESCALATE,
                "conditions": {
                    "error_type": "critical",
                    "context": {"severity": "high"},
                },
                "actions": [
                    {
                        "escalation_level": "critical",
                        "notify_targets": ["admin", "oncall"],
                    }
                ],
                "enabled": True,
                "created_at": datetime.now().isoformat(),
            },
        }
