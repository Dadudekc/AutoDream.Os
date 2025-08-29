"""Process flow orchestration for handoff validation."""
from __future__ import annotations

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..base_manager import BaseManager
from .input_checks import VALIDATION_ENGINES
from .reporting import update_validation_metrics, validation_status, system_status
from .rules import (
    DEFAULT_RULES,
    ValidationResult,
    ValidationRule,
    ValidationSession,
    ValidationSeverity,
    ValidationStatus,
)


class HandoffValidationSystem(BaseManager):
    """Quality assurance system for handoff procedures."""

    def __init__(self, project_root: str = ".") -> None:
        super().__init__("HandoffValidationSystem")
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
        self.validation_rules: Dict[str, ValidationRule] = {
            rule.rule_id: rule for rule in DEFAULT_RULES
        }
        self.active_sessions: Dict[str, ValidationSession] = {}
        self.validation_history: List[ValidationSession] = []
        self.validation_metrics: Dict[str, Any] = {
            "total_sessions": 0,
            "successful_sessions": 0,
            "failed_sessions": 0,
            "average_duration": 0.0,
            "total_duration": 0.0,
            "rule_success_rates": {},
            "severity_distribution": {},
        }
        self.validation_engines = VALIDATION_ENGINES

    # ------------------------------------------------------------------
    # Session management
    def start_validation_session(
        self, handoff_id: str, procedure_id: str, rule_ids: Optional[List[str]] = None
    ) -> str:
        """Start asynchronous validation for a handoff."""
        session_id = f"validation_{int(time.time())}_{handoff_id}"
        rules = (
            [
                self.validation_rules[rid]
                for rid in rule_ids
                if rid in self.validation_rules
            ]
            if rule_ids
            else list(self.validation_rules.values())
        )
        session = ValidationSession(
            session_id=session_id,
            handoff_id=handoff_id,
            procedure_id=procedure_id,
            start_time=time.time(),
            rules=rules,
        )
        self.active_sessions[session_id] = session
        asyncio.create_task(self._execute_validation_session(session))
        self.logger.info(
            "🚀 Starting validation session %s for %s", session_id, handoff_id
        )
        return session_id

    async def _execute_validation_session(self, session: ValidationSession) -> None:
        """Run each validation rule in ``session`` sequentially."""
        session.overall_status = ValidationStatus.IN_PROGRESS
        for rule in session.rules:
            result = await self._execute_validation_rule(rule, session)
            session.results.append(result)
            if result.status == ValidationStatus.FAILED:
                if rule.severity == ValidationSeverity.CRITICAL:
                    session.critical_failures += 1
                elif rule.severity == ValidationSeverity.HIGH:
                    session.high_failures += 1
                elif rule.severity == ValidationSeverity.MEDIUM:
                    session.medium_failures += 1
                else:
                    session.low_failures += 1

        session.end_time = time.time()
        session.duration = session.end_time - session.start_time
        if session.critical_failures > 0:
            session.overall_status = ValidationStatus.FAILED
        elif (
            session.high_failures > 0
            or session.medium_failures > 0
            or session.low_failures > 0
        ):
            session.overall_status = ValidationStatus.WARNING
        else:
            session.overall_status = ValidationStatus.PASSED
        passed = sum(1 for r in session.results if r.status == ValidationStatus.PASSED)
        session.validation_score = passed / len(session.rules) if session.rules else 0.0
        update_validation_metrics(self.validation_metrics, session)
        self.validation_history.append(session)
        self.active_sessions.pop(session.session_id, None)

    async def _execute_validation_rule(
        self, rule: ValidationRule, session: ValidationSession
    ) -> ValidationResult:
        """Execute ``rule`` and return a :class:`ValidationResult`."""
        start = time.time()
        engine = self.validation_engines.get(rule.condition)
        if engine is None:
            end = time.time()
            return ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                status=ValidationStatus.ERROR,
                start_time=start,
                end_time=end,
                duration=end - start,
                error_details=f"Unknown validation condition: {rule.condition}",
                severity=rule.severity,
            )
        validation_success = False
        error_details = None
        for attempt in range(rule.retry_count + 1):
            try:
                if await asyncio.wait_for(engine(rule, session), timeout=rule.timeout):
                    validation_success = True
                    break
            except asyncio.TimeoutError:
                error_details = f"Validation timed out after {rule.timeout}s (attempt {attempt + 1})"
            except Exception as exc:  # pragma: no cover - defensive
                error_details = f"Validation error (attempt {attempt + 1}): {exc}"
        end = time.time()
        duration = end - start
        status = (
            ValidationStatus.PASSED
            if validation_success
            else (
                ValidationStatus.FAILED
                if rule.severity == ValidationSeverity.CRITICAL
                else ValidationStatus.WARNING
            )
        )
        return ValidationResult(
            rule_id=rule.rule_id,
            rule_name=rule.name,
            status=status,
            start_time=start,
            end_time=end,
            duration=duration,
            error_details=error_details,
            severity=rule.severity,
        )

    # ------------------------------------------------------------------
    # Reporting interfaces
    def get_validation_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Return status details for ``session_id``."""
        return validation_status(
            session_id, self.active_sessions, self.validation_history
        )

    def get_system_status(self) -> Dict[str, Any]:
        """Return overall system metrics."""
        return system_status(
            self.validation_metrics,
            self.active_sessions,
            list(self.validation_rules.keys()),
        )

    # ------------------------------------------------------------------
    # Rule management
    def add_validation_rule(self, rule: ValidationRule) -> bool:
        """Add ``rule`` to the registry."""
        self.validation_rules[rule.rule_id] = rule
        return True

    def remove_validation_rule(self, rule_id: str) -> bool:
        """Remove ``rule_id`` if not currently in use."""
        for session in self.active_sessions.values():
            if any(r.rule_id == rule_id for r in session.rules):
                return False
        return self.validation_rules.pop(rule_id, None) is not None


_handoff_validation_system = HandoffValidationSystem()


def get_handoff_validation_system() -> HandoffValidationSystem:
    """Return a global :class:`HandoffValidationSystem` instance."""
    return _handoff_validation_system
