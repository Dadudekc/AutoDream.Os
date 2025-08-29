"""
AI/ML Automation Engine Module
Modularized from src/ai_ml/core.py

Contains the automation engine for AI/ML operations:
- AutomationEngine: Handles automation rules and task scheduling
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AutomationEngine:
    """AI/ML automation engine for rules and task scheduling"""

    def __init__(self, ai_manager, model_manager):
        """Initialize automation engine"""
        self.ai_manager = ai_manager
        self.model_manager = model_manager
        self.automation_rules: Dict[str, Dict[str, Any]] = {}
        self.scheduled_tasks: List[Dict[str, Any]] = []

    def add_automation_rule(
        self,
        rule_name: str,
        conditions: Dict[str, Any],
        actions: List[Dict[str, Any]],
        enabled: bool = True
    ) -> bool:
        """Add an automation rule"""
        try:
            self.automation_rules[rule_name] = {
                "conditions": conditions,
                "actions": actions,
                "enabled": enabled,
                "created_at": datetime.now().isoformat()
            }
            logger.info(f"Added automation rule: {rule_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add automation rule {rule_name}: {e}")
            return False

    def evaluate_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate automation rule conditions"""
        try:
            for condition_key, expected_value in conditions.items():
                if condition_key not in context:
                    return False
                if context[condition_key] != expected_value:
                    return False
            return True
        except Exception as e:
            logger.error(f"Error evaluating conditions: {e}")
            return False

    def execute_actions(
        self, actions: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        """Execute automation rule actions"""
        try:
            for action in actions:
                action_type = action.get("type")
                parameters = action.get("parameters", {})

                if action_type == "create_workflow":
                    self.ai_manager.create_workflow(
                        name=parameters.get("name"),
                        description=parameters.get("description", ""),
                    )
                elif action_type == "update_model_status":
                    self.model_manager.update_model_status(
                        model_id=parameters.get("model_id"),
                        status=parameters.get("status"),
                    )
                elif action_type == "execute_workflow":
                    self.ai_manager.execute_workflow(
                        workflow_name=parameters.get("workflow_name")
                    )

            return True
        except Exception as e:
            logger.error(f"Error executing actions: {e}")
            return False

    def process_automation_rules(self, context: Dict[str, Any]) -> int:
        """Process all automation rules against current context"""
        executed_count = 0

        for rule_name, rule in self.automation_rules.items():
            if not rule.get("enabled", True):
                continue

            if self.evaluate_conditions(rule["conditions"], context):
                if self.execute_actions(rule["actions"], context):
                    executed_count += 1
                    logger.info(f"Executed automation rule: {rule_name}")

        return executed_count

    def schedule_task(
        self, task_name: str, schedule: str, task_func: callable, **kwargs
    ) -> bool:
        """Schedule a task for execution"""
        try:
            scheduled_task = {
                "name": task_name,
                "schedule": schedule,
                "task_func": task_func,
                "kwargs": kwargs,
                "created_at": datetime.now().isoformat(),
                "next_run": self._calculate_next_run(schedule),
            }
            self.scheduled_tasks.append(scheduled_task)
            logger.info(f"Scheduled task: {task_name}")
            return True
        except Exception as e:
            logger.error(f"Error scheduling task {task_name}: {e}")
            return False

    def _calculate_next_run(self, schedule: str) -> datetime:
        """Calculate next run time based on schedule"""
        # Simple implementation - could be enhanced with cron-like parsing
        return datetime.now()

    def run_scheduled_tasks(self) -> int:
        """Run all scheduled tasks that are due"""
        executed_count = 0
        current_time = datetime.now()

        for task in self.scheduled_tasks[:]:  # Copy list to avoid modification during iteration
            if current_time >= task["next_run"]:
                try:
                    task["task_func"](**task.get("kwargs", {}))
                    executed_count += 1
                    task["next_run"] = self._calculate_next_run(task["schedule"])
                    logger.info(f"Executed scheduled task: {task['name']}")
                except Exception as e:
                    logger.error(f"Error executing scheduled task {task['name']}: {e}")

        return executed_count
