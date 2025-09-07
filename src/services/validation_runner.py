"""Configuration-driven validation runner."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .contract_validation_engine import ContractValidationEngine


class ValidationRunner:
    """Run contract validation based on configuration data."""

    def __init__(self, engine: Optional[ContractValidationEngine] = None) -> None:
        self.engine = engine or ContractValidationEngine()

    @classmethod
    def from_file(
        cls, config_path: str | Path, engine: Optional[ContractValidationEngine] = None
    ) -> "ValidationRunner":
        """Create a runner using configuration loaded from a JSON file."""
        path = Path(config_path)
        config = json.loads(path.read_text())
        runner = cls(engine)
        runner.config = config
        return runner

    def run(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute validation using provided or pre-loaded configuration."""
        cfg = config or getattr(self, "config", {})
        rules_cfg = cfg.get("rules", {})
        for rule_id in rules_cfg.get("enable", []):
            self.engine.rule_manager.enable_rule(rule_id)
        for rule_id in rules_cfg.get("disable", []):
            self.engine.rule_manager.disable_rule(rule_id)

        contract_data = cfg.get("contract", {})
        results = self.engine.validate_contract(contract_data)
        violations = [self.engine.create_violation(r) for r in results if not r.passed]
        return {"results": results, "violations": violations}
