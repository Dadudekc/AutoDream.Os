#!/usr/bin/env python3
"""
Coordination Validator Core Module - Agent Cellphone V2
====================================================

Coordination system validation functionality.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from typing import Dict, Any, List

from .validation_models import ValidationIssue, ValidationSeverity


class CoordinationValidatorCore:
    """Handles coordination system validation."""

    def validate_coordination_system(self, system_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate coordination system configuration."""
        issues = []

        # Check agent configuration
        if 'agents' in system_data:
            agent_data = system_data['agents']
            for agent_id, agent_info in agent_data.items():
                if not isinstance(agent_info, dict):
                    issues.append(ValidationIssue(
                        rule_id="coordination_structure",
                        rule_name="Coordination Structure",
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid agent configuration for {agent_id}",
                        details={"agent_id": agent_id, "agent_info": agent_info},
                        timestamp=datetime.now(),
                        component="coordination_system"
                    ))
                    continue

                # Check required agent fields
                required_agent_fields = ['description', 'coords']
                for field in required_agent_fields:
                    if field not in agent_info:
                        issues.append(ValidationIssue(
                            rule_id="agent_required_fields",
                            rule_name="Agent Required Fields",
                            severity=ValidationSeverity.ERROR,
                            message=f"Missing required field '{field}' for agent {agent_id}",
                            details={"agent_id": agent_id, "field": field},
                            timestamp=datetime.now(),
                            component="coordination_system"
                        ))

        return issues
