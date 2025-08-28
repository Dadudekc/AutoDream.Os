"""Validation pipeline assembly module."""
from __future__ import annotations

from typing import Any, Dict

from .validation_rules import ValidationRuleManager
from .validation_executor import ValidationExecutor
from .validation_reporter import ValidationReporter
from .constants import RESULTS_KEY, SUMMARY_KEY


class ValidationPipeline:
    """Assemble and run the validation pipeline."""

    def __init__(self, rule_manager: ValidationRuleManager | None = None) -> None:
        self.rule_manager = rule_manager or ValidationRuleManager()
        self.executor = ValidationExecutor(self.rule_manager)
        self.reporter = ValidationReporter()

    def run(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute validation and return results with summary."""
        results = self.executor.execute(contract_data)
        summary = self.reporter.summarize(results)
        return {RESULTS_KEY: results, SUMMARY_KEY: summary}
