"""Contract deliverables validation orchestrator."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

from .contract_parser import parse_contract
from .validation_rules import ValidationRule, default_validation_rules
from .deliverable_report import RuleResult, create_report, DeliverableReport

logger = logging.getLogger(__name__)


DEFAULT_CONTRACT = (
    Path(__file__).resolve().parents[2] / "contracts" / "MASTER_CONTRACT_INDEX.json"
)


class ContractDeliverablesValidator:
    """Coordinate contract parsing, rule execution, and reporting."""

    def __init__(self, contract_path: Optional[Path] = None):
        self.contract_path = Path(contract_path) if contract_path else DEFAULT_CONTRACT
        self.rules: List[ValidationRule] = default_validation_rules()

    async def validate_contract_deliverables(self) -> DeliverableReport:
        """Parse the contract, execute validation rules, and build report."""
        logger.info("Validating contract deliverables from %s", self.contract_path)
        contract_data = parse_contract(self.contract_path)
        results: List[RuleResult] = []
        for rule in self.rules:
            try:
                passed = rule.validate(contract_data)
            except Exception as exc:  # defensive: rule may raise
                logger.error("Rule %s failed: %s", rule.rule_id, exc)
                passed = False
            results.append(RuleResult(rule.rule_id, rule.description, passed))
        contract_id = contract_data.get(
            "master_contract_index", str(self.contract_path)
        )
        return create_report(contract_id, results)
