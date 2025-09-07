"""Core validator orchestrating cleanup checks and reporting."""
from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Dict

from .shared import CleanupValidation
from . import rules, validation, reporting

logger = logging.getLogger(__name__)


class ContractCleanupValidator:
    """Main contract cleanup validation system."""

    def __init__(self, contracts_dir: str = "logs"):
        self.contracts_dir = Path(contracts_dir)
        self.contracts_dir.mkdir(exist_ok=True)
        self.validation_file = self.contracts_dir / "cleanup_validations.json"
        self.cleanup_validations: Dict[str, CleanupValidation] = {}
        self.load_validations()

    def load_validations(self) -> None:
        """Load existing cleanup validations from disk."""
        if self.validation_file.exists():
            try:
                with open(self.validation_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for contract_id, validation_data in data.items():
                        self.cleanup_validations[contract_id] = CleanupValidation(
                            **validation_data
                        )
            except Exception as exc:
                logger.error("Error loading cleanup validations: %s", exc)
                self.cleanup_validations = {}

    def save_validations(self) -> None:
        """Persist cleanup validations to disk."""
        try:
            data = {
                contract_id: asdict(validation)
                for contract_id, validation in self.cleanup_validations.items()
            }
            with open(self.validation_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as exc:
            logger.error("Error saving cleanup validations: %s", exc)

    def validate_cleanup_completion(self, contract_id: str) -> CleanupValidation:
        """Validate that all cleanup requirements are met."""
        cleanup_requirements = rules.get_cleanup_requirements()
        standards_requirements = rules.get_v2_standards_requirements()
        validation_result = validation.validate_cleanup_completion(
            contract_id, cleanup_requirements, standards_requirements
        )
        self.cleanup_validations[contract_id] = validation_result
        self.save_validations()
        return validation_result

    def generate_cleanup_report(self, contract_id: str) -> str:
        """Generate comprehensive cleanup report."""
        validation_result = self.validate_cleanup_completion(contract_id)
        cleanup_requirements = rules.get_cleanup_requirements()
        standards_requirements = rules.get_v2_standards_requirements()
        return reporting.generate_cleanup_report(
            contract_id, validation_result, cleanup_requirements, standards_requirements
        )

    def auto_validate_contract(self, contract_id: str) -> CleanupValidation:
        """Automatically validate contract cleanup and standards."""
        validation_result = validation.auto_validate_contract(contract_id)
        self.cleanup_validations[contract_id] = validation_result
        self.save_validations()
        return validation_result


__all__ = ["ContractCleanupValidator"]
