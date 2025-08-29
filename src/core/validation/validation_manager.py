"""Thin orchestration layer for the validation system."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from .base_validator import BaseValidator
from .rule_registry import RuleRegistry
from .executor import ValidationExecutor
from .reporting import ValidationReporter


class ValidationManager:
    """Coordinate validator registration, execution and reporting."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.ValidationManager")
        self.registry = RuleRegistry()
        self.executor = ValidationExecutor(self.registry)
        self.reporter = ValidationReporter(self.executor)
        # Expose underlying mapping for legacy compatibility
        self.validators = self.registry._validators
        self._initialize_default_validators()

    # ------------------------------------------------------------------
    def _initialize_default_validators(self) -> None:
        """Load built‑in validators into the registry."""
        try:
            from .contract_validator import ContractValidator
            from .config_validator import ConfigValidator
            from ..workflow.validation.workflow_validator import WorkflowValidator
            from .message_validator import MessageValidator
            from .quality_validator import QualityValidator
            from .security_validator import SecurityValidator
            from .storage_validator import StorageValidator
            from .onboarding_validator import OnboardingValidator
            from .task_validator import TaskValidator
            from .code_validator import CodeValidator

            self.registry.register("contract", ContractValidator())
            self.registry.register("config", ConfigValidator())
            self.registry.register("workflow", WorkflowValidator())
            self.registry.register("message", MessageValidator())
            self.registry.register("quality", QualityValidator())
            self.registry.register("security", SecurityValidator())
            self.registry.register("storage", StorageValidator())
            self.registry.register("onboarding", OnboardingValidator())
            self.registry.register("task", TaskValidator())
            self.registry.register("code", CodeValidator())
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error(f"Failed to initialize default validators: {exc}")

    # ------------------------------------------------------------------
    # Registry proxy methods
    # ------------------------------------------------------------------
    def register_validator(self, name: str, validator: BaseValidator) -> None:
        self.registry.register(name, validator)

    def unregister_validator(self, name: str) -> None:
        self.registry.unregister(name)

    def get_validator(self, name: str) -> BaseValidator | None:
        return self.registry.get(name)

    def list_validators(self) -> List[str]:
        return self.registry.list()

    # ------------------------------------------------------------------
    # Execution proxy methods
    # ------------------------------------------------------------------
    def validate_with_validator(self, name: str, data: Any, **kwargs):
        return self.executor.validate_with_validator(name, data, **kwargs)

    def validate_all(self, data: Dict[str, Any], **kwargs):
        return self.executor.validate_all(data, **kwargs)

    # ------------------------------------------------------------------
    # Reporting proxy methods
    # ------------------------------------------------------------------
    def get_validation_summary(self) -> Dict[str, Any]:
        return self.reporter.get_validation_summary()

    def export_validation_report(self) -> List[Dict[str, Any]]:
        return self.reporter.export_validation_report()
