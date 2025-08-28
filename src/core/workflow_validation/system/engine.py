"""Execution engine for the workflow validation system."""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from ...managers.base_manager import BaseManager
except Exception:  # pragma: no cover - fallback if unavailable
    class BaseManager:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:  # pragma: no cover - simple stub
            pass

        def _setup_logging(self) -> None:  # pragma: no cover - simple stub
            logging.basicConfig(level=logging.INFO)

from .rules import (
    ValidationLevel,
    ValidationResult,
    ValidationRule,
    RuleResult,
    initialize_validation_rules,
)
from .reporting import (
    WorkflowValidationReport,
    calculate_validation_scores,
    generate_recommendations,
    export_validation_report,
    get_reliability_trends,
)

logger = logging.getLogger(__name__)


class WorkflowValidationSystem(BaseManager):
    """Coordinate validation rules, execution and reporting."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config or {})
        self.validation_rules: Dict[str, ValidationRule] = initialize_validation_rules()
        self.validation_reports: Dict[str, WorkflowValidationReport] = {}
        self.performance_benchmarks: Dict[str, float] = {}
        self.reliability_history: List[float] = []

        self._setup_logging()

    # ------------------------------------------------------------------
    # Rule management
    # ------------------------------------------------------------------

    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule to the system."""

        self.validation_rules[rule.rule_id] = rule
        logger.info("Added validation rule: %s", rule.name)

    # ------------------------------------------------------------------
    # Validation execution
    # ------------------------------------------------------------------

    async def validate_workflow(
        self,
        workflow_id: str,
        validation_level: ValidationLevel = ValidationLevel.STANDARD,
        target_files: Optional[List[str]] = None,
        workflow_data: Optional[Dict[str, Any]] = None,
    ) -> WorkflowValidationReport:
        """Perform comprehensive workflow validation."""

        logger.info(
            "Starting workflow validation for %s at %s level",
            workflow_id,
            validation_level.value,
        )

        report = WorkflowValidationReport(
            workflow_id=workflow_id,
            validation_level=validation_level,
            start_time=datetime.now(),
        )

        applicable_rules = self._get_applicable_rules(validation_level)
        report.total_rules = len(applicable_rules)
        logger.info("Executing %s validation rules", len(applicable_rules))

        for rule in applicable_rules:
            try:
                result = await self._execute_validation_rule(
                    rule, workflow_id, target_files, workflow_data
                )
                report.rule_results.append(result)

                if result.result == ValidationResult.PASSED:
                    report.passed_rules += 1
                elif result.result == ValidationResult.FAILED:
                    report.failed_rules += 1
                elif result.result == ValidationResult.WARNING:
                    report.warning_rules += 1
                elif result.result == ValidationResult.ERROR:
                    report.error_rules += 1
                else:
                    report.skipped_rules += 1

            except Exception as exc:  # pragma: no cover - defensive
                logger.error(
                    "Validation rule %s failed with error: %s", rule.rule_id, str(exc)
                )
                error_result = RuleResult(
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    result=ValidationResult.ERROR,
                    error_message=str(exc),
                    timestamp=datetime.now(),
                )
                report.rule_results.append(error_result)
                report.error_rules += 1

        report = calculate_validation_scores(report, self.validation_rules)
        report.recommendations = generate_recommendations(report)
        report.end_time = datetime.now()

        self.validation_reports[workflow_id] = report
        self.reliability_history.append(report.reliability_score)

        logger.info(
            "Workflow validation completed for %s", workflow_id
        )
        logger.info(
            "Overall score: %.2f%%, Reliability: %.2f%%",
            report.overall_score,
            report.reliability_score,
        )

        return report

    def _get_applicable_rules(
        self, validation_level: ValidationLevel
    ) -> List[ValidationRule]:
        """Get validation rules applicable to the specified level."""

        level_priorities = {
            ValidationLevel.BASIC: 1,
            ValidationLevel.STANDARD: 2,
            ValidationLevel.COMPREHENSIVE: 3,
            ValidationLevel.EXPERT: 4,
        }

        target_priority = level_priorities[validation_level]
        applicable_rules = []

        for rule in self.validation_rules.values():
            rule_priority = level_priorities[rule.level]
            if rule_priority <= target_priority:
                applicable_rules.append(rule)

        applicable_rules.sort(key=lambda r: r.weight, reverse=True)
        return applicable_rules

    async def _execute_validation_rule(
        self,
        rule: ValidationRule,
        workflow_id: str,
        target_files: Optional[List[str]],
        workflow_data: Optional[Dict[str, Any]],
    ) -> RuleResult:
        """Execute a single validation rule."""

        start_time = time.time()

        try:
            if asyncio.iscoroutinefunction(rule.validation_func):
                result = await asyncio.wait_for(
                    rule.validation_func(workflow_id, target_files, workflow_data),
                    timeout=rule.timeout,
                )
            else:
                result = rule.validation_func(workflow_id, target_files, workflow_data)

            execution_time = time.time() - start_time
            return RuleResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                result=result.get("status", ValidationResult.PASSED),
                score=result.get("score", 100.0),
                details=result.get("details", {}),
                execution_time=execution_time,
                timestamp=datetime.now(),
            )

        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            return RuleResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                result=ValidationResult.ERROR,
                error_message="Validation rule execution timed out",
                execution_time=execution_time,
                timestamp=datetime.now(),
            )
        except Exception as exc:  # pragma: no cover - defensive
            execution_time = time.time() - start_time
            return RuleResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                result=ValidationResult.ERROR,
                error_message=str(exc),
                execution_time=execution_time,
                timestamp=datetime.now(),
            )

    # ------------------------------------------------------------------
    # Reporting helpers
    # ------------------------------------------------------------------

    def get_validation_report(
        self, workflow_id: str
    ) -> Optional[WorkflowValidationReport]:
        """Get a validation report by workflow ID."""

        return self.validation_reports.get(workflow_id)

    def list_validation_reports(self) -> List[Dict[str, Any]]:
        """List all validation reports with summary information."""

        report_list: List[Dict[str, Any]] = []
        for workflow_id, report in self.validation_reports.items():
            report_info = {
                "workflow_id": workflow_id,
                "validation_level": report.validation_level.value,
                "overall_score": report.overall_score,
                "reliability_score": report.reliability_score,
                "quality_score": report.quality_score,
                "performance_score": report.performance_score,
                "total_rules": report.total_rules,
                "passed_rules": report.passed_rules,
                "failed_rules": report.failed_rules,
                "start_time": report.start_time.isoformat(),
                "end_time": report.end_time.isoformat() if report.end_time else None,
            }
            report_list.append(report_info)
        return report_list

    def get_reliability_trends(self) -> Dict[str, Any]:
        """Get reliability trends and statistics."""

        return get_reliability_trends(self.reliability_history)

    def export_validation_report(self, workflow_id: str, output_path: str) -> bool:
        """Export a validation report to JSON."""

        report = self.get_validation_report(workflow_id)
        if not report:
            return False
        return export_validation_report(report, output_path)


__all__ = ["WorkflowValidationSystem"]

