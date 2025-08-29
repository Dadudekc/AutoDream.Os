"""Onboarding workflow validation functions."""
from typing import Any, Dict, List, Optional

from ..base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from . import rules


# --- Core validation helpers -------------------------------------------------

def validate_onboarding_structure(validator: BaseValidator, onboarding_data: Dict[str, Any]) -> List[ValidationResult]:
    """Validate onboarding data structure and format."""
    results: List[ValidationResult] = []
    if not isinstance(onboarding_data, dict):
        result = validator._create_result(
            rule_id="onboarding_type",
            rule_name="Onboarding Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Onboarding data must be a dictionary",
            actual_value=type(onboarding_data).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if len(onboarding_data) == 0:
        result = validator._create_result(
            rule_id="onboarding_empty",
            rule_name="Onboarding Empty Check",
            status=ValidationStatus.WARNING,
            severity=ValidationSeverity.WARNING,
            message="Onboarding data is empty",
            actual_value=onboarding_data,
            expected_value="non-empty onboarding data",
        )
        results.append(result)
    return results


def validate_onboarding_stage(validator: BaseValidator, stage: Any) -> Optional[ValidationResult]:
    """Validate onboarding stage value."""
    if not isinstance(stage, str):
        return validator._create_result(
            rule_id="stage_type",
            rule_name="Stage Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Onboarding stage must be a string",
            field_path="stage",
            actual_value=type(stage).__name__,
            expected_value="str",
        )
    if stage.lower() not in validator.onboarding_stages:
        return validator._create_result(
            rule_id="stage_invalid",
            rule_name="Stage Invalid Value",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message=f"Invalid onboarding stage: {stage}",
            field_path="stage",
            actual_value=stage,
            expected_value=f"one of {validator.onboarding_stages}",
        )
    return None


def validate_onboarding_flow(validator: BaseValidator, flow: Any) -> List[ValidationResult]:
    """Validate onboarding flow data."""
    results: List[ValidationResult] = []
    if not isinstance(flow, dict):
        result = validator._create_result(
            rule_id="flow_type",
            rule_name="Flow Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Onboarding flow must be a dictionary",
            field_path="flow",
            actual_value=type(flow).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "stages" in flow:
        stages = flow["stages"]
        if isinstance(stages, list):
            if len(stages) == 0:
                result = validator._create_result(
                    rule_id="flow_stages_empty",
                    rule_name="Flow Stages Empty Check",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Onboarding flow must have at least one stage",
                    field_path="flow.stages",
                    actual_value=stages,
                    expected_value="non-empty list of stages",
                )
                results.append(result)
            else:
                for i, stage in enumerate(stages):
                    if not isinstance(stage, dict):
                        result = validator._create_result(
                            rule_id=f"flow_stage_{i}_type",
                            rule_name=f"Flow Stage {i} Type Validation",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Flow stage {i} must be a dictionary",
                            field_path=f"flow.stages[{i}]",
                            actual_value=type(stage).__name__,
                            expected_value="dict",
                        )
                        results.append(result)
                        continue
                    stage_required_fields = ["name", "order", "required"]
                    stage_field_results = validator._validate_required_fields(stage, stage_required_fields)
                    for stage_result in stage_field_results:
                        stage_result.field_path = f"flow.stages[{i}].{stage_result.field_path}"
                    results.extend(stage_field_results)
                    if "order" in stage:
                        order = stage["order"]
                        if isinstance(order, int):
                            if order <= 0:
                                result = validator._create_result(
                                    rule_id=f"flow_stage_{i}_order",
                                    rule_name=f"Flow Stage {i} Order Validation",
                                    status=ValidationStatus.FAILED,
                                    severity=ValidationSeverity.ERROR,
                                    message=f"Flow stage {i} order must be greater than 0",
                                    field_path=f"flow.stages[{i}].order",
                                    actual_value=order,
                                    expected_value="> 0",
                                )
                                results.append(result)
    return results


def validate_verification(validator: BaseValidator, verification: Any) -> List[ValidationResult]:
    """Validate verification data."""
    results: List[ValidationResult] = []
    if not isinstance(verification, dict):
        result = validator._create_result(
            rule_id="verification_type",
            rule_name="Verification Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Verification data must be a dictionary",
            field_path="verification",
            actual_value=type(verification).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "method" in verification:
        method = verification["method"]
        if isinstance(method, str):
            if method.lower() not in validator.verification_methods:
                result = validator._create_result(
                    rule_id="verification_method_invalid",
                    rule_name="Verification Method Invalid Value",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid verification method: {method}",
                    field_path="verification.method",
                    actual_value=method,
                    expected_value=f"one of {validator.verification_methods}",
                )
                results.append(result)

    if "status" in verification:
        status = verification["status"]
        valid_statuses = [
            "pending",
            "in_progress",
            "completed",
            "failed",
            "expired",
        ]
        if isinstance(status, str):
            if status.lower() not in valid_statuses:
                result = validator._create_result(
                    rule_id="verification_status_invalid",
                    rule_name="Verification Status Invalid Value",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid verification status: {status}",
                    field_path="verification.status",
                    actual_value=status,
                    expected_value=f"one of {valid_statuses}",
                )
                results.append(result)

    if "attempts" in verification:
        attempts = verification["attempts"]
        if isinstance(attempts, int):
            if attempts < 0:
                result = validator._create_result(
                    rule_id="verification_attempts_invalid",
                    rule_name="Verification Attempts Invalid Value",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Verification attempts cannot be negative",
                    field_path="verification.attempts",
                    actual_value=attempts,
                    expected_value=">= 0",
                )
                results.append(result)
    return results


def validate_compliance(validator: BaseValidator, compliance: Any) -> List[ValidationResult]:
    """Validate compliance data."""
    results: List[ValidationResult] = []
    if not isinstance(compliance, dict):
        result = validator._create_result(
            rule_id="compliance_type",
            rule_name="Compliance Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Compliance data must be a dictionary",
            field_path="compliance",
            actual_value=type(compliance).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "required_fields" in compliance:
        required_fields = compliance["required_fields"]
        if isinstance(required_fields, list):
            if len(required_fields) == 0:
                result = validator._create_result(
                    rule_id="compliance_required_fields_empty",
                    rule_name="Compliance Required Fields Empty Check",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message="No required compliance fields specified",
                    field_path="compliance.required_fields",
                    actual_value=required_fields,
                    expected_value="non-empty list of required fields",
                )
                results.append(result)
            else:
                for i, field in enumerate(required_fields):
                    if not isinstance(field, str):
                        result = validator._create_result(
                            rule_id=f"compliance_field_{i}_type",
                            rule_name=f"Compliance Field {i} Type Validation",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Compliance field {i} must be a string",
                            field_path=f"compliance.required_fields[{i}]",
                            actual_value=type(field).__name__,
                            expected_value="str",
                        )
                        results.append(result)

    if "status" in compliance:
        status = compliance["status"]
        valid_statuses = [
            "pending",
            "in_review",
            "approved",
            "rejected",
            "requires_action",
        ]
        if isinstance(status, str):
            if status.lower() not in valid_statuses:
                result = validator._create_result(
                    rule_id="compliance_status_invalid",
                    rule_name="Compliance Status Invalid Value",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid compliance status: {status}",
                    field_path="compliance.status",
                    actual_value=status,
                    expected_value=f"one of {valid_statuses}",
                )
                results.append(result)
    return results


def validate_onboarding_progression(validator: BaseValidator, onboarding_data: Dict[str, Any]) -> List[ValidationResult]:
    """Validate onboarding progression logic."""
    results: List[ValidationResult] = []
    if "stage" in onboarding_data and "status" in onboarding_data:
        stage = onboarding_data["stage"]
        status = onboarding_data["status"]
        if isinstance(stage, str) and isinstance(status, str):
            stage_lower = stage.lower()
            status_lower = status.lower()
            if stage_lower == "completion" and status_lower != "completed":
                result = validator._create_result(
                    rule_id="stage_completion_mismatch",
                    rule_name="Stage Completion Mismatch",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message="Completion stage should have 'completed' status",
                    field_path="stage",
                    actual_value=f"stage: {stage}, status: {status}",
                    expected_value="status: completed for completion stage",
                )
                results.append(result)
            if stage_lower in validator.onboarding_stages:
                stage_index = validator.onboarding_stages.index(stage_lower)
                if stage_index > 0:
                    if "completed_stages" in onboarding_data:
                        completed_stages = onboarding_data["completed_stages"]
                        if isinstance(completed_stages, list):
                            for prev_stage in validator.onboarding_stages[:stage_index]:
                                if prev_stage not in completed_stages:
                                    result = validator._create_result(
                                        rule_id="stage_progression_invalid",
                                        rule_name="Stage Progression Invalid",
                                        status=ValidationStatus.WARNING,
                                        severity=ValidationSeverity.WARNING,
                                        message=f"Stage '{stage}' reached before completing '{prev_stage}'",
                                        field_path="stage",
                                        actual_value=f"current: {stage}, missing: {prev_stage}",
                                        expected_value=f"complete {prev_stage} before {stage}",
                                    )
                                    results.append(result)
    if "stage" in onboarding_data and "required_fields" in onboarding_data:
        stage = onboarding_data["stage"]
        required_fields = onboarding_data["required_fields"]
        if isinstance(required_fields, dict) and isinstance(stage, str):
            stage_requirements = required_fields.get(stage.lower(), [])
            if isinstance(stage_requirements, list) and len(stage_requirements) > 0:
                if "completed_fields" in onboarding_data:
                    completed_fields = onboarding_data["completed_fields"]
                    if isinstance(completed_fields, list):
                        missing_fields = [
                            field
                            for field in stage_requirements
                            if field not in completed_fields
                        ]
                        if missing_fields:
                            result = validator._create_result(
                                rule_id="required_fields_incomplete",
                                rule_name="Required Fields Incomplete",
                                status=ValidationStatus.WARNING,
                                severity=ValidationSeverity.WARNING,
                                message=f"Missing required fields for stage '{stage}': {missing_fields}",
                                field_path="required_fields",
                                actual_value=f"missing: {missing_fields}",
                                expected_value=f"complete all required fields for {stage}",
                            )
                            results.append(result)
    return results


# --- Extended workflow helpers ----------------------------------------------

def add_onboarding_stage(validator: BaseValidator, stage: str) -> bool:
    """Add a custom onboarding stage."""
    try:
        if stage not in validator.onboarding_stages:
            validator.onboarding_stages.append(stage)
            validator.logger.info(f"Onboarding stage added: {stage}")
        return True
    except Exception as e:  # pragma: no cover - defensive
        validator.logger.error(f"Failed to add onboarding stage: {e}")
        return False


def add_verification_method(validator: BaseValidator, method: str) -> bool:
    """Add a custom verification method."""
    try:
        if method not in validator.verification_methods:
            validator.verification_methods.append(method)
            validator.logger.info(f"Verification method added: {method}")
        return True
    except Exception as e:  # pragma: no cover - defensive
        validator.logger.error(f"Failed to add verification method: {e}")
        return False


def wait_for_phase_response(
    validator: BaseValidator,
    session: Dict[str, Any],
    phase: str,
    message_id: str,
    phase_timeout: float = 30.0,
) -> bool:
    """Wait for and validate phase response."""
    import time

    start = time.time()
    while time.time() - start < phase_timeout:
        time.sleep(0.1)
        return True
    validator.logger.warning(
        f"Timeout waiting for response for phase {phase} in session {session.get('session_id', 'unknown')}"
    )
    return False


def validate_onboarding_completion(
    validator: BaseValidator,
    session: Dict[str, Any],
    role_definitions: Optional[Dict[str, Any]] = None,
    fsm_core: Any = None,
) -> bool:
    """Validate that onboarding has been completed successfully."""
    try:
        if not role_definitions:
            role_definitions = {}
        agent_id = session.get("agent_id", "unknown")
        required_phases = role_definitions.get(agent_id, {}).get("onboarding_phases", [])
        if required_phases:
            completed_phases = session.get("completed_phases", [])
            if not all(phase in completed_phases for phase in required_phases):
                validator.logger.warning(
                    f"Not all required phases completed for {agent_id}"
                )
                return False
        if not validate_performance_metrics(validator, session):
            validator.logger.warning(f"Performance validation failed for {agent_id}")
            return False
        if fsm_core and hasattr(fsm_core, "create_task"):
            try:
                fsm_core.create_task(
                    title=f"Onboarding Completion - {agent_id}",
                    description=(
                        f"Agent {agent_id} has completed onboarding and is ready for active participation"
                    ),
                    assigned_agent=agent_id,
                )
            except Exception as e:  # pragma: no cover - defensive
                validator.logger.warning(f"Failed to create FSM task: {e}")
        return True
    except Exception as e:  # pragma: no cover - defensive
        validator.logger.error(f"Onboarding completion validation failed: {e}")
        return False


def validate_performance_metrics(validator: BaseValidator, session: Dict[str, Any]) -> bool:
    """Validate performance metrics for onboarding completion."""
    try:
        performance_data = session.get("performance_metrics", {})
        required_metrics = ["completion_time", "success_rate", "error_count"]
        for metric in required_metrics:
            if metric not in performance_data:
                validator.logger.warning(f"Missing performance metric: {metric}")
                return False
        completion_time = performance_data.get("completion_time", 0)
        if completion_time < 0:
            validator.logger.warning("Completion time cannot be negative")
            return False
        success_rate = performance_data.get("success_rate", 0)
        if not (0 <= success_rate <= 100):
            validator.logger.warning("Success rate must be between 0 and 100")
            return False
        error_count = performance_data.get("error_count", 0)
        if error_count < 0:
            validator.logger.warning("Error count cannot be negative")
            return False
        return True
    except Exception as e:  # pragma: no cover - defensive
        validator.logger.error(f"Performance metrics validation failed: {e}")
        return False
