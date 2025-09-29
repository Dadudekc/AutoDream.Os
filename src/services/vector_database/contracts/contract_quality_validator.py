#!/usr/bin/env python3
"""
Contract Quality Validator
==========================

Validates contract execution quality and compliance.
V2 Compliance: ≤150 lines, focused responsibility, KISS principle.
"""

import logging
from datetime import UTC, datetime
from typing import Any

from .contract_models import ContractStatus, V3Contract

logger = logging.getLogger(__name__)


class ContractQualityValidator:
    """Validates contract execution quality."""

    def __init__(self, quality_assurance_framework=None):
        """Initialize quality validator."""
        self.quality_assurance = quality_assurance_framework
        self.quality_threshold = 85.0  # Minimum quality score

    def validate_contract_quality(self, contracts: list[V3Contract]) -> dict[str, Any]:
        """Validate contract execution quality."""
        try:
            quality_results = {
                "overall_quality_score": 0.0,
                "contract_quality_scores": {},
                "quality_violations": [],
                "compliance_status": "PASSED",
            }

            total_score = 0.0
            valid_contracts = 0

            for contract in contracts:
                contract_quality = self._validate_individual_contract(contract)
                quality_results["contract_quality_scores"][contract.contract_id] = contract_quality

                if contract_quality["score"] > 0:
                    total_score += contract_quality["score"]
                    valid_contracts += 1

                # Check for violations
                if contract_quality["score"] < self.quality_threshold:
                    quality_results["quality_violations"].append(
                        {
                            "contract_id": contract.contract_id,
                            "score": contract_quality["score"],
                            "threshold": self.quality_threshold,
                        }
                    )

            # Calculate overall quality score
            if valid_contracts > 0:
                quality_results["overall_quality_score"] = total_score / valid_contracts

            # Determine compliance status
            if quality_results["overall_quality_score"] < self.quality_threshold:
                quality_results["compliance_status"] = "FAILED"

            return quality_results

        except Exception as e:
            logger.error(f"Failed to validate contract quality: {e}")
            return {"overall_quality_score": 0.0, "error": str(e), "compliance_status": "FAILED"}

    def _validate_individual_contract(self, contract: V3Contract) -> dict[str, Any]:
        """Validate individual contract quality."""
        try:
            quality_score = 100.0  # Start with perfect score
            issues = []

            # Check contract structure
            if not contract.contract_id.startswith("V3-"):
                quality_score -= 20.0
                issues.append("Invalid contract ID format")

            if not contract.title or len(contract.title.strip()) < 5:
                quality_score -= 15.0
                issues.append("Insufficient contract title")

            if not contract.description or len(contract.description.strip()) < 10:
                quality_score -= 15.0
                issues.append("Insufficient contract description")

            # Check status consistency
            if contract.status == ContractStatus.COMPLETED and not contract.assigned_agent:
                quality_score -= 10.0
                issues.append("Completed contract without assigned agent")

            # Check timestamps
            if contract.updated_at < contract.created_at:
                quality_score -= 10.0
                issues.append("Invalid timestamp ordering")

            # Get quality assurance score if available
            if self.quality_assurance:
                try:
                    qa_status = self.quality_assurance.get_quality_assurance_status()
                    qa_score = qa_status.get("quality_score", 100.0)
                    quality_score = min(quality_score, qa_score)
                except Exception:
                    pass  # Use calculated score if QA framework unavailable

            return {
                "score": max(0.0, quality_score),
                "issues": issues,
                "status": "PASSED" if quality_score >= self.quality_threshold else "FAILED",
            }

        except Exception as e:
            logger.error(f"Failed to validate individual contract: {e}")
            return {"score": 0.0, "issues": [f"Validation error: {str(e)}"], "status": "FAILED"}

    def get_quality_metrics(self, contracts: list[V3Contract]) -> dict[str, Any]:
        """Get quality metrics for contracts."""
        try:
            total_contracts = len(contracts)
            completed_contracts = len(
                [c for c in contracts if c.status == ContractStatus.COMPLETED]
            )
            failed_contracts = len([c for c in contracts if c.status == ContractStatus.FAILED])

            success_rate = (
                (completed_contracts / total_contracts * 100) if total_contracts > 0 else 0
            )

            return {
                "total_contracts": total_contracts,
                "completed_contracts": completed_contracts,
                "failed_contracts": failed_contracts,
                "success_rate": success_rate,
                "quality_threshold": self.quality_threshold,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to get quality metrics: {e}")
            return {"error": str(e)}
