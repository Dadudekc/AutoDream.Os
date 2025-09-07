#!/usr/bin/env python3
"""Contract Management System - Agent Cellphone V2.

Command-line interface for managing contract lifecycle, parsing, and validation.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from typing import List, Optional

from .lifecycle import ContractManager
from .models import ContractValidation, TaskStatus

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ContractCLI:
    """CLI interface for contract management operations."""

    def __init__(self) -> None:
        self.manager = ContractManager()
        self.manager.auto_discover_contracts()

    def show_help(self) -> None:
        """Show CLI help."""
        help_text = """
🎯 CONTRACT MANAGEMENT CLI - Agent Cellphone V2

USAGE:
  python contract_cli.py [COMMAND] [OPTIONS]

COMMANDS:
  list [agent_id]           - List all contracts or contracts for specific agent
  status <contract_id>      - Show detailed status of specific contract
  update <contract_id> <requirement_id> <completed> [notes] - Update requirement status
  validate <contract_id>    - Validate contract completion
  complete <contract_id>    - Mark contract as completed
  progress <contract_id>    - Show progress of specific contract
  bounce <contract_id>      - Bounce contract back for review
  help                     - Show this help message

REQUIREMENT IDs:
  - task_completion: Complete the specific task
  - progress_documentation: Document progress and completion
  - integration_verification: Verify system integration

STATUS VALUES:
  - true/false: For requirement completion
  - 1/0: Alternative for requirement completion
"""
        print(help_text)

    def list_contracts(self, agent_id: Optional[str] = None) -> None:
        """List contracts."""
        if agent_id:
            contracts = self.manager.get_agent_contracts(agent_id.upper())
            print(f"\n📋 CONTRACTS FOR {agent_id.upper()}:")
        else:
            contracts = list(self.manager.contract_statuses.values())
            print(f"\n📋 ALL CONTRACTS ({len(contracts)} total):")

        if not contracts:
            print("No contracts found.")
            return

        status_emoji = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.REVIEW_NEEDED: "🔍",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.FAILED: "❌",
            TaskStatus.BOUNCED_BACK: "🚨",
        }
        for contract in contracts:
            emoji = status_emoji.get(contract.current_status, "❓")
            print(f"{emoji} {contract.contract_id}: {contract.current_status.value}")
            print(
                f"   Progress: {contract.progress_percentage:.1f}%"
                f" ({contract.requirements_completed}/{contract.total_requirements})"
            )
            print(f"   Agent: {contract.agent_id}")
            print(f"   Last Updated: {contract.last_updated}")
            if contract.validation_result:
                valid = (
                    "✅ Valid" if contract.validation_result.is_valid else "❌ Invalid"
                )
                print(
                    f"   Validation: {valid} (Score: {contract.validation_result.score:.2f})"
                )
            print()

    def show_status(self, contract_id: str) -> None:
        """Show detailed contract status."""
        status = self.manager.contract_statuses.get(contract_id)
        if not status:
            print(f"❌ Contract {contract_id} not found")
            return

        print(f"\n🎯 CONTRACT STATUS: {contract_id}")
        print(f"Agent: {status.agent_id}")
        print(f"Status: {status.current_status.value}")
        print(
            f"Progress: {status.progress_percentage:.1f}%"
            f" ({status.requirements_completed}/{status.total_requirements})"
        )
        print(f"Last Updated: {status.last_updated}")

        if status.validation_result:
            print(f"\n📊 VALIDATION RESULTS:")
            print(f"Valid: {'✅ Yes' if status.validation_result.is_valid else '❌ No'}")
            print(f"Score: {status.validation_result.score:.2f}")
            if status.validation_result.missing_requirements:
                print(f"\n❌ MISSING REQUIREMENTS:")
                for req in status.validation_result.missing_requirements:
                    print(f"  - {req}")
            if status.validation_result.validation_errors:
                print(f"\n🚨 VALIDATION ERRORS:")
                for error in status.validation_result.validation_errors:
                    print(f"  - {error}")
            if status.validation_result.warnings:
                print(f"\n⚠️  WARNINGS:")
                for warning in status.validation_result.warnings:
                    print(f"  - {warning}")

    def update_requirement(
        self, contract_id: str, requirement_id: str, completed: str, notes: str = ""
    ) -> None:
        """Update requirement status."""
        if completed.lower() in ["true", "1", "yes", "y"]:
            completed_bool = True
        elif completed.lower() in ["false", "0", "no", "n"]:
            completed_bool = False
        else:
            print(
                f"❌ Invalid completion value: {completed}. Use true/false, 1/0, yes/no, or y/n"
            )
            return

        if self.manager.update_requirement_status(
            contract_id, requirement_id, completed_bool, notes
        ):
            print(
                f"✅ Updated {requirement_id} in {contract_id} to "
                f"{'completed' if completed_bool else 'not completed'}"
            )
            if notes:
                print(f"Notes: {notes}")
            self.manager.validate_contract_completion(contract_id)
            self.show_status(contract_id)
        else:
            print(f"❌ Failed to update requirement {requirement_id} in {contract_id}")

    def validate_contract(self, contract_id: str) -> None:
        """Validate contract completion."""
        if contract_id not in self.manager.contract_statuses:
            print(f"❌ Contract {contract_id} not found")
            return
        print(f"🔍 Validating contract {contract_id}...")
        validation = self.manager.validate_contract_completion(contract_id)
        if validation.is_valid:
            print(f"✅ Contract {contract_id} is VALID (Score: {validation.score:.2f})")
        else:
            print(
                f"❌ Contract {contract_id} is INVALID (Score: {validation.score:.2f})"
            )
        if validation.missing_requirements:
            print("\n❌ Missing Requirements:")
            for req in validation.missing_requirements:
                print(f"  - {req}")
        if validation.validation_errors:
            print("\n🚨 Validation Errors:")
            for error in validation.validation_errors:
                print(f"  - {error}")
        if validation.warnings:
            print("\n⚠️  Warnings:")
            for warning in validation.warnings:
                print(f"  - {warning}")

    def complete_contract(self, contract_id: str) -> None:
        """Mark contract as completed."""
        if contract_id not in self.manager.contract_statuses:
            print(f"❌ Contract {contract_id} not found")
            return
        status = self.manager.contract_statuses[contract_id]
        contract_file = (
            self.manager.contracts_dir
            / f"contracts_{status.agent_id.lower().replace('-', '_')}"
            / f"{contract_id.lower()}.md"
        )
        if contract_file.exists():
            requirements = self.manager.get_contract_requirements(contract_file)
            for req in requirements:
                self.manager.update_requirement_status(
                    contract_id, req.requirement_id, True, "Auto-completed by CLI"
                )
        validation = self.manager.validate_contract_completion(contract_id)
        if validation.is_valid:
            print(f"✅ Contract {contract_id} marked as completed successfully!")
        else:
            print(f"⚠️  Contract {contract_id} completed but validation shows issues:")
            for error in validation.validation_errors:
                print(f"  - {error}")

    def show_progress(self, contract_id: str) -> None:
        """Show contract progress."""
        status = self.manager.contract_statuses.get(contract_id)
        if not status:
            print(f"❌ Contract {contract_id} not found")
            return
        print(f"\n📊 PROGRESS REPORT: {contract_id}")
        print(f"Overall Progress: {status.progress_percentage:.1f}%")
        print(
            f"Requirements: {status.requirements_completed}/{status.total_requirements}"
        )
        bar_length = 30
        filled_length = int(bar_length * status.progress_percentage / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        print(f"Progress Bar: [{bar}] {status.progress_percentage:.1f}%")
        status_emoji = {
            TaskStatus.PENDING: "⏳ PENDING",
            TaskStatus.IN_PROGRESS: "🔄 IN PROGRESS",
            TaskStatus.REVIEW_NEEDED: "🔍 REVIEW NEEDED",
            TaskStatus.COMPLETED: "✅ COMPLETED",
            TaskStatus.FAILED: "❌ FAILED",
            TaskStatus.BOUNCED_BACK: "🚨 BOUNCED BACK",
        }
        print(f"Status: {status_emoji.get(status.current_status, '❓ UNKNOWN')}")
        print(f"Last Updated: {status.last_updated}")

    def bounce_contract(self, contract_id: str) -> None:
        """Bounce contract back for review."""
        status = self.manager.contract_statuses.get(contract_id)
        if not status:
            print(f"❌ Contract {contract_id} not found")
            return
        status.current_status = TaskStatus.BOUNCED_BACK
        status.last_updated = datetime.now().isoformat()
        if status.validation_result:
            status.validation_result.validation_errors.append(
                "Contract bounced back for review by agent"
            )
        else:
            status.validation_result = ContractValidation(
                is_valid=False,
                missing_requirements=[],
                validation_errors=["Contract bounced back for review by agent"],
                warnings=[],
                score=0.0,
                timestamp=datetime.now().isoformat(),
            )
        self.manager.save_statuses()
        print(f"🚨 Contract {contract_id} has been bounced back for review")
        print(f"Agent {status.agent_id} will need to address issues and resubmit")

    def run(self, args: List[str]) -> None:
        """Run CLI with arguments."""
        if not args or args[0] in ["help", "--help", "-h"]:
            self.show_help()
            return
        command = args[0].lower()
        try:
            if command == "list":
                agent_id = args[1] if len(args) > 1 else None
                self.list_contracts(agent_id)
            elif command == "status":
                if len(args) < 2:
                    print("❌ Usage: status <contract_id>")
                    return
                self.show_status(args[1])
            elif command == "update":
                if len(args) < 4:
                    print(
                        "❌ Usage: update <contract_id> <requirement_id> <completed> [notes]"
                    )
                    return
                notes = args[4] if len(args) > 4 else ""
                self.update_requirement(args[1], args[2], args[3], notes)
            elif command == "validate":
                if len(args) < 2:
                    print("❌ Usage: validate <contract_id>")
                    return
                self.validate_contract(args[1])
            elif command == "complete":
                if len(args) < 2:
                    print("❌ Usage: complete <contract_id>")
                    return
                self.complete_contract(args[1])
            elif command == "progress":
                if len(args) < 2:
                    print("❌ Usage: progress <contract_id>")
                    return
                self.show_progress(args[1])
            elif command == "bounce":
                if len(args) < 2:
                    print("❌ Usage: bounce <contract_id>")
                    return
                self.bounce_contract(args[1])
            else:
                print(f"❌ Unknown command: {command}")
                self.show_help()
        except Exception as exc:  # pragma: no cover - catch CLI errors
            print(f"❌ Error executing command: {exc}")
            logger.error("CLI error: %s", exc)


def main() -> None:
    """Main CLI entry point."""
    cli = ContractCLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()
