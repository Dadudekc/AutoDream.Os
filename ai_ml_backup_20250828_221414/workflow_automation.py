"""
Workflow Automation Module
Extracted from core.py for modularization

Contains:
- WorkflowAutomation: Automated workflow execution and rule processing
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from .ai_manager import AIManager
from .model_manager import ModelManager

# Configure logging
logger = logging.getLogger(__name__)


class WorkflowAutomation:
    """Automated workflow execution and rule processing

    Handles automation rules and scheduled task execution
    """

    def __init__(self, ai_manager: AIManager, model_manager: ModelManager):
        """Initialize workflow automation"""
        self.ai_manager = ai_manager
        self.model_manager = model_manager
        self.automation_rules: Dict[str, Dict[str, Any]] = {}
        self.scheduled_tasks: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)

    def add_automation_rule(
        self, 
        rule_name: str, 
        conditions: Dict[str, Any], 
        actions: List[Dict[str, Any]],
        enabled: bool = True
    ) -> bool:
        """Add a new automation rule"""
        try:
            if rule_name in self.automation_rules:
                self.logger.warning(f"Automation rule {rule_name} already exists")
                return False

            self.automation_rules[rule_name] = {
                "conditions": conditions,
                "actions": actions,
                "enabled": enabled,
                "created_at": datetime.now().isoformat(),
                "execution_count": 0
            }

            self.logger.info(f"Added automation rule: {rule_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add automation rule: {e}")
            return False

    def remove_automation_rule(self, rule_name: str) -> bool:
        """Remove an automation rule"""
        try:
            if rule_name in self.automation_rules:
                del self.automation_rules[rule_name]
                self.logger.info(f"Removed automation rule: {rule_name}")
                return True
            else:
                self.logger.warning(f"Automation rule {rule_name} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to remove automation rule: {e}")
            return False

    def enable_automation_rule(self, rule_name: str) -> bool:
        """Enable an automation rule"""
        try:
            if rule_name in self.automation_rules:
                self.automation_rules[rule_name]["enabled"] = True
                self.logger.info(f"Enabled automation rule: {rule_name}")
                return True
            else:
                self.logger.warning(f"Automation rule {rule_name} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to enable automation rule: {e}")
            return False

    def disable_automation_rule(self, rule_name: str) -> bool:
        """Disable an automation rule"""
        try:
            if rule_name in self.automation_rules:
                self.automation_rules[rule_name]["enabled"] = False
                self.logger.info(f"Disabled automation rule: {rule_name}")
                return True
            else:
                self.logger.warning(f"Automation rule {rule_name} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to disable automation rule: {e}")
            return False

    def get_automation_rule(self, rule_name: str) -> Optional[Dict[str, Any]]:
        """Get an automation rule by name"""
        return self.automation_rules.get(rule_name)

    def list_automation_rules(self) -> List[str]:
        """List all automation rule names"""
        return list(self.automation_rules.keys())

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
            self.logger.error(f"Error evaluating conditions: {e}")
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
            self.logger.error(f"Error executing actions: {e}")
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
                    rule["execution_count"] += 1
                    self.logger.info(f"Executed automation rule: {rule_name}")

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
            self.logger.info(f"Scheduled task: {task_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error scheduling task {task_name}: {e}")
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
                    self.logger.info(f"Executed scheduled task: {task['name']}")
                except Exception as e:
                    self.logger.error(f"Error executing scheduled task {task['name']}: {e}")

        return executed_count

    def remove_scheduled_task(self, task_name: str) -> bool:
        """Remove a scheduled task"""
        try:
            for i, task in enumerate(self.scheduled_tasks):
                if task["name"] == task_name:
                    del self.scheduled_tasks[i]
                    self.logger.info(f"Removed scheduled task: {task_name}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove scheduled task: {e}")
            return False

    def list_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """List all scheduled tasks"""
        return self.scheduled_tasks.copy()

    def get_automation_statistics(self) -> Dict[str, Any]:
        """Get automation system statistics"""
        total_rules = len(self.automation_rules)
        enabled_rules = sum(1 for rule in self.automation_rules.values() if rule.get("enabled", True))
        total_executions = sum(rule.get("execution_count", 0) for rule in self.automation_rules.values())
        scheduled_tasks = len(self.scheduled_tasks)

        return {
            "total_automation_rules": total_rules,
            "enabled_rules": enabled_rules,
            "disabled_rules": total_rules - enabled_rules,
            "total_rule_executions": total_executions,
            "scheduled_tasks": scheduled_tasks
        }

    def validate_automation_rule(self, rule_name: str) -> Dict[str, Any]:
        """Validate an automation rule"""
        try:
            if rule_name not in self.automation_rules:
                return {"valid": False, "error": "Rule not found"}

            rule = self.automation_rules[rule_name]
            validation_result = {"valid": True, "warnings": []}

            # Check required fields
            if "conditions" not in rule:
                validation_result["valid"] = False
                validation_result["error"] = "Missing conditions"
                return validation_result

            if "actions" not in rule:
                validation_result["valid"] = False
                validation_result["error"] = "Missing actions"
                return validation_result

            # Validate conditions structure
            if not isinstance(rule["conditions"], dict):
                validation_result["warnings"].append("Conditions should be a dictionary")

            # Validate actions structure
            if not isinstance(rule["actions"], list):
                validation_result["warnings"].append("Actions should be a list")

            return validation_result

        except Exception as e:
            return {"valid": False, "error": str(e)}

    def export_automation_rules(self, file_path: str) -> bool:
        """Export automation rules to file"""
        try:
            import json
            with open(file_path, "w") as f:
                json.dump(self.automation_rules, f, indent=2)
            self.logger.info(f"Exported automation rules to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export automation rules: {e}")
            return False

    def import_automation_rules(self, file_path: str) -> bool:
        """Import automation rules from file"""
        try:
            with open(file_path, "r") as f:
                imported_rules = json.load(f)
            
            # Validate imported rules
            for rule_name, rule in imported_rules.items():
                if self.validate_automation_rule(rule_name)["valid"]:
                    self.automation_rules[rule_name] = rule
                else:
                    self.logger.warning(f"Skipping invalid rule: {rule_name}")

            self.logger.info(f"Imported automation rules from {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to import automation rules: {e}")
            return False
