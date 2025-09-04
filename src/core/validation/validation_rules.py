#!/usr/bin/env python3
"""
Validation Rules Module - Agent Cellphone V2
==========================================

Rule loading functionality for validation system.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""




class ValidationRules:
    """Handles loading and management of validation rules."""

    def __init__(self, rules_dir: str = "src/core/validation/rules"):
        """Initialize validation rules manager."""
        self.rules_dir = rules_dir
        self.rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules from YAML files."""
        rules = {}

        try:
            # Load message validation rules
            message_rules_path = get_unified_utility().path.join(self.rules_dir, "message.yaml")
            if get_unified_utility().path.exists(message_rules_path):
                with open(message_rules_path, "r") as f:
                    rules["message"] = yaml.safe_load(f)

            # Load quality validation rules
            quality_rules_path = get_unified_utility().path.join(self.rules_dir, "quality.yaml")
            if get_unified_utility().path.exists(quality_rules_path):
                with open(quality_rules_path, "r") as f:
                    rules["quality"] = yaml.safe_load(f)

            # Load security validation rules
            security_rules_path = get_unified_utility().path.join(self.rules_dir, "security.yaml")
            if get_unified_utility().path.exists(security_rules_path):
                with open(security_rules_path, "r") as f:
                    rules["security"] = yaml.safe_load(f)

        except Exception as e:
            get_logger(__name__).info(f"⚠️ Warning: Could not load validation rules: {e}")
            rules = {}

        return rules

    def get_rules(self) -> Dict[str, Any]:
        """Get loaded validation rules."""
        return self.rules

    def has_rules(self, rule_type: str) -> bool:
        """Check if rules exist for a specific type."""
        return rule_type in self.rules
