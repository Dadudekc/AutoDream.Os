#!/usr/bin/env python3
"""
🐝 Contract Creation Automation Tool
===================================

Automated contract generation from templates for the swarm system.
Creates standardized contracts with proper validation and formatting.

Usage:
    python create_contract.py --template security_enhancement --agent Agent-3 --priority high
    python create_contract.py --template ai_ml_integration --agent Agent-5 --deadline 2025-11-15

Author: Agent-2 - Contract System Enhancement
License: MIT
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any


class ContractGenerator:
    """Automated contract generation from templates."""

    def __init__(self):
        self.templates_dir = Path(__file__).parent
        self.contracts_dir = Path(__file__).parent

    def list_templates(self) -> list[str]:
        """List all available contract templates."""
        templates = []
        for file in self.templates_dir.glob("*_contract_template.json"):
            templates.append(file.stem.replace("_contract_template", ""))
        return sorted(templates)

    def load_template(self, template_name: str) -> Dict[str, Any]:
        """Load a contract template."""
        template_file = self.templates_dir / f"{template_name}_contract_template.json"
        if not template_file.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found")

        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def customize_contract(
        self,
        template: Dict[str, Any],
        agent_id: str,
        agent_name: str,
        priority: str = "MEDIUM",
        deadline_days: int = 30,
        **customizations
    ) -> Dict[str, Any]:
        """Customize a contract template with specific parameters."""

        # Generate contract ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        contract_type = template["contract_type"].replace("_", "").upper()
        contract_id = f"CONTRACT-{agent_id.upper()}-{contract_type}-{timestamp}"

        # Update basic contract information
        contract = template.copy()
        contract["contract_id"] = contract_id
        contract["agent_id"] = agent_id
        contract["agent_name"] = agent_name
        contract["priority"] = priority.upper()
        contract["status"] = "AVAILABLE"

        # Update deadline
        deadline = datetime.now() + timedelta(days=deadline_days)
        contract["contract_details"]["deadline"] = deadline.strftime("%Y-%m-%d")

        # Update metadata
        contract["contract_metadata"]["created_by"] = f"Automated - {agent_id}"
        contract["contract_metadata"]["created_at"] = datetime.now().isoformat()
        contract["contract_metadata"]["last_updated"] = datetime.now().isoformat()

        # Add contract history entry
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "AUTO_GENERATED",
            "actor": f"Contract Generator - {agent_id}",
            "details": f"Contract auto-generated from {template['contract_title']} template"
        }
        contract["contract_history"] = [history_entry]

        # Apply any customizations
        for key, value in customizations.items():
            if key in contract["contract_details"]:
                if isinstance(contract["contract_details"][key], list):
                    contract["contract_details"][key].append(value)
                else:
                    contract["contract_details"][key] = value

        return contract

    def save_contract(self, contract: Dict[str, Any], filename: str = None) -> str:
        """Save contract to file."""
        if filename is None:
            contract_id = contract["contract_id"].lower().replace("contract-", "").replace("-", "_")
            filename = f"{contract_id}.json"

        filepath = self.contracts_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(contract, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def validate_contract(self, contract: Dict[str, Any]) -> list[str]:
        """Validate contract structure and data."""
        errors = []

        required_fields = [
            "contract_id", "contract_title", "agent_id", "agent_name",
            "contract_type", "priority", "status", "contract_details",
            "contract_metadata", "contract_rewards"
        ]

        for field in required_fields:
            if field not in contract:
                errors.append(f"Missing required field: {field}")

        # Validate contract details
        if "contract_details" in contract:
            details = contract["contract_details"]
            required_details = ["description", "objectives", "deliverables", "success_criteria"]
            for detail in required_details:
                if detail not in details:
                    errors.append(f"Missing contract detail: {detail}")

        # Validate priority
        if contract.get("priority") not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
            errors.append("Invalid priority level")

        return errors


def main():
    """Main contract generation interface."""
    parser = argparse.ArgumentParser(
        description="🐝 Automated Contract Generation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🐝 SWARM CONTRACT GENERATION
============================

EXAMPLES:
--------
# Generate security contract for Agent-3
python create_contract.py --template security_enhancement --agent Agent-3 --priority high

# Generate AI/ML contract with custom deadline
python create_contract.py --template ai_ml_integration --agent Agent-5 --deadline 2025-11-15

# List all available templates
python create_contract.py --list-templates

# Generate DevOps contract with custom title
python create_contract.py --template devops_automation --agent Agent-2 --custom-title "Custom DevOps Contract"

🐝 WE ARE SWARM - AUTOMATED CONTRACT GENERATION!
        """
    )

    parser.add_argument(
        "--template", "-t",
        help="Contract template to use"
    )

    parser.add_argument(
        "--agent", "-a",
        help="Agent ID to assign contract to"
    )

    parser.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high", "critical"],
        default="medium",
        help="Contract priority (default: medium)"
    )

    parser.add_argument(
        "--deadline",
        type=int,
        default=30,
        help="Deadline in days from now (default: 30)"
    )

    parser.add_argument(
        "--list-templates", "-l",
        action="store_true",
        help="List all available contract templates"
    )

    parser.add_argument(
        "--custom-title",
        help="Custom contract title (optional)"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output filename (optional, auto-generated if not specified)"
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate the generated contract, don't save"
    )

    args = parser.parse_args()

    generator = ContractGenerator()

    if args.list_templates:
        templates = generator.list_templates()
        print("🐝 AVAILABLE CONTRACT TEMPLATES:")
        print("=" * 40)
        for template in templates:
            print(f"• {template}")
        print(f"\nTotal templates: {len(templates)}")
        return

    if not args.template or not args.agent:
        parser.print_help()
        return

    try:
        # Load and customize template
        template = generator.load_template(args.template)
        customizations = {}

        if args.custom_title:
            customizations["title"] = args.custom_title

        contract = generator.customize_contract(
            template=template,
            agent_id=args.agent,
            agent_name=f"Agent {args.agent.split('-')[1]}",
            priority=args.priority.upper(),
            deadline_days=args.deadline,
            **customizations
        )

        # Validate contract
        errors = generator.validate_contract(contract)
        if errors:
            print("❌ CONTRACT VALIDATION ERRORS:")
            for error in errors:
                print(f"  • {error}")
            return

        if args.validate_only:
            print("✅ CONTRACT VALIDATION SUCCESSFUL")
            print(f"Contract ID: {contract['contract_id']}")
            return

        # Save contract
        filepath = generator.save_contract(contract, args.output)
        print("✅ CONTRACT GENERATED SUCCESSFULLY!")
        print(f"📄 File: {filepath}")
        print(f"🆔 ID: {contract['contract_id']}")
        print(f"🤖 Agent: {contract['agent_id']}")
        print(f"🎯 Priority: {contract['priority']}")
        print(f"📅 Deadline: {contract['contract_details']['deadline']}")
        print(f"💰 XP Reward: {contract['contract_rewards']['experience_points']}")

        print("\n🐝 CONTRACT READY FOR SWARM ASSIGNMENT!")

    except Exception as e:
        print(f"❌ CONTRACT GENERATION FAILED: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
