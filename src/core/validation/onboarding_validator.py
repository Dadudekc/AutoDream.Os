"""Onboarding Validator - Unified Validation Framework.

This module now acts as a slim coordinator that orchestrates onboarding
validation by delegating to modular workflow, rule, and reporting helpers.
"""
from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from .onboarding import reporting, rules, workflows


class OnboardingValidator(BaseValidator):
    """Validates onboarding data using modular workflow components."""

    def __init__(self) -> None:
        super().__init__("OnboardingValidator")
        self.onboarding_stages = list(rules.ONBOARDING_STAGES)
        self.verification_methods = list(rules.VERIFICATION_METHODS)

    def validate(self, onboarding_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        """Validate onboarding data and return validation results."""
        results: List[ValidationResult] = []
        try:
            results.extend(workflows.validate_onboarding_structure(self, onboarding_data))
            required_fields = ["user_id", "stage", "start_date", "status"]
            results.extend(self._validate_required_fields(onboarding_data, required_fields))
            if "stage" in onboarding_data:
                stage_result = workflows.validate_onboarding_stage(self, onboarding_data["stage"])
                if stage_result:
                    results.append(stage_result)
            if "flow" in onboarding_data:
                results.extend(workflows.validate_onboarding_flow(self, onboarding_data["flow"]))
            if "verification" in onboarding_data:
                results.extend(workflows.validate_verification(self, onboarding_data["verification"]))
            if "compliance" in onboarding_data:
                results.extend(workflows.validate_compliance(self, onboarding_data["compliance"]))
            results.extend(workflows.validate_onboarding_progression(self, onboarding_data))
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                results.append(reporting.generate_success_result(self, len(results)))
        except Exception as e:  # pragma: no cover - defensive
            results.append(reporting.generate_error_result(self, e))
        return results

    # Exposed workflow helpers -------------------------------------------------
    def add_onboarding_stage(self, stage: str) -> bool:
        return workflows.add_onboarding_stage(self, stage)

    def add_verification_method(self, method: str) -> bool:
        return workflows.add_verification_method(self, method)

    def _wait_for_phase_response(
        self,
        session: Dict[str, Any],
        phase: str,
        message_id: str,
        phase_timeout: float = 30.0,
    ) -> bool:
        return workflows.wait_for_phase_response(self, session, phase, message_id, phase_timeout)

    def _validate_onboarding_completion(
        self,
        session: Dict[str, Any],
        role_definitions: Dict[str, Any] = None,
        fsm_core: Any = None,
    ) -> bool:
        return workflows.validate_onboarding_completion(self, session, role_definitions, fsm_core)

    def _validate_performance_metrics(self, session: Dict[str, Any]) -> bool:
        return workflows.validate_performance_metrics(self, session)
