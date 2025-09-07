from datetime import datetime
from pathlib import Path
from typing import List

from .models import (
from .parser import parse_contract_requirements
from __future__ import annotations

"""Contract validation utilities."""



    ContractStatus,
    ContractValidation,
    TaskStatus,
    ValidationLevel,
)


def validate_contract(
    contract_status: ContractStatus,
    contracts_dir: Path,
    validation_level: ValidationLevel = ValidationLevel.STANDARD,
) -> ContractValidation:
    """Validate contract completion based on parsed requirements.

    Args:
        contract_status: Status information for the contract.
        contracts_dir: Root directory containing contracts.
        validation_level: Level of strictness for validation.

    Returns:
        The resulting :class:`ContractValidation` data.
    """
    contract_file = (
        contracts_dir
        / f"contracts_{contract_status.agent_id.lower().replace('-', '_')}"
        / f"{contract_status.contract_id.lower()}.md"
    )

    validation_errors: List[str] = []
    warnings: List[str] = []

    if not contract_file.exists():
        validation_errors.append(f"Contract file not found: {contract_file}")
        return ContractValidation(
            is_valid=False,
            missing_requirements=["Contract file missing"],
            validation_errors=validation_errors,
            warnings=warnings,
            score=0.0,
            timestamp=datetime.now().isoformat(),
        )

    requirements = parse_contract_requirements(contract_file)
    completed_count = sum(1 for req in requirements if req.completed)
    total_count = len(requirements)
    missing_requirements = [
        req.description for req in requirements if not req.completed
    ]
    score = completed_count / total_count if total_count else 0.0

    if validation_level == ValidationLevel.STRICT:
        devlog_dir = contracts_dir.parent / "logs"
        if not list(devlog_dir.glob(f"*{contract_status.contract_id}*")):
            validation_errors.append("Devlog entry not found")
            score = max(0.0, score - 0.2)
        if not any(req.completion_timestamp for req in requirements if req.completed):
            warnings.append("Some requirements lack completion timestamps")

    is_valid = score >= 0.8 and not validation_errors

    contract_status.progress_percentage = score * 100
    contract_status.requirements_completed = completed_count
    contract_status.total_requirements = total_count
    contract_status.current_status = (
        TaskStatus.COMPLETED
        if is_valid and score >= 0.95
        else TaskStatus.IN_PROGRESS
        if score >= 0.6
        else TaskStatus.BOUNCED_BACK
        if validation_errors
        else TaskStatus.REVIEW_NEEDED
    )
    contract_status.validation_result = ContractValidation(
        is_valid=is_valid,
        missing_requirements=missing_requirements,
        validation_errors=validation_errors,
        warnings=warnings,
        score=score,
        timestamp=datetime.now().isoformat(),
    )
    contract_status.update_timestamp()
    return contract_status.validation_result
