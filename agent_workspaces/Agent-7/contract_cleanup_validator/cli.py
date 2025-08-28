import sys
from pathlib import Path
from typing import List

from .validator import ContractCleanupValidator

class CleanupCLI:
    """CLI interface for cleanup validation"""

    def __init__(self):
        self.validator = ContractCleanupValidator()

    def show_help(self):
        """Show CLI help"""
        help_text = """
🧹 CONTRACT CLEANUP VALIDATOR CLI - Agent Cellphone V2

USAGE:
  python cleanup_validator.py [COMMAND] [OPTIONS]

COMMANDS:
  validate <contract_id>    - Validate contract cleanup and standards
  report <contract_id>      - Generate cleanup validation report
  checklist <contract_id>   - Show cleanup checklist
  auto-validate <contract_id> - Auto-validate contract cleanup
  help                     - Show this help message

EXAMPLES:
  python cleanup_validator.py validate TASK_1B
  python cleanup_validator.py report TASK_1B
  python cleanup_validator.py checklist TASK_1B
  python cleanup_validator.py auto-validate TASK_1B

PURPOSE:
  Ensure contracts are properly cleaned up and meet V2 standards
  before marking them as completed.
"""
        print(help_text)

    def validate_contract(self, contract_id: str):
        """Validate contract cleanup"""
        print(f"🔍 Validating cleanup for contract {contract_id}...")
        validation = self.validator.validate_cleanup_completion(contract_id)
        if validation.is_valid:
            print(f"✅ Contract {contract_id} cleanup is VALID (Score: {validation.overall_score:.2f})")
        else:
            print(f"❌ Contract {contract_id} cleanup is INVALID (Score: {validation.overall_score:.2f})")
        if validation.missing_cleanup:
            print("\n❌ Missing Cleanup:")
            for req in validation.missing_cleanup:
                print(f"  - {req}")
        if validation.validation_errors:
            print("\n🚨 Validation Errors:")
            for error in validation.validation_errors:
                print(f"  - {error}")
        if validation.warnings:
            print("\n⚠️  Warnings:")
            for warning in validation.warnings:
                print(f"  - {warning}")

    def generate_report(self, contract_id: str):
        """Generate cleanup report"""
        print(f"📊 Generating cleanup report for {contract_id}...")
        report = self.validator.generate_cleanup_report(contract_id)
        report_file = Path(f"logs/{contract_id}_cleanup_report.md")
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Report saved to: {report_file}")
        print("\n" + "=" * 80)
        print(report)
        print("=" * 80)

    def show_checklist(self, contract_id: str):
        """Show cleanup checklist"""
        print(f"📋 Cleanup Checklist for {contract_id}:")
        cleanup_requirements = self.validator.get_cleanup_requirements()
        standards_requirements = self.validator.get_v2_standards_requirements()
        print("\n🧹 CLEANUP REQUIREMENTS:")
        for req in cleanup_requirements:
            status = "✅" if req.completed else "❌"
            print(f"{status} {req.description}")
        print("\n🏗️ V2 STANDARDS REQUIREMENTS:")
        for std in standards_requirements:
            status = "✅" if std.compliant else "❌"
            print(f"{status} {std.description}")

    def auto_validate(self, contract_id: str):
        """Auto-validate contract"""
        print(f"🤖 Auto-validating contract {contract_id}...")
        validation = self.validator.auto_validate_contract(contract_id)
        if validation.is_valid:
            print(f"✅ Auto-validation complete: Contract is VALID (Score: {validation.overall_score:.2f})")
        else:
            print(f"❌ Auto-validation complete: Contract is INVALID (Score: {validation.overall_score:.2f})")
        print("\n📊 DETAILED RESULTS:")
        print(f"Cleanup Score: {validation.cleanup_score:.2f}/1.0")
        print(f"Standards Score: {validation.standards_score:.2f}/1.0")
        print(f"Overall Score: {validation.overall_score:.2f}/1.0")
        if validation.missing_cleanup:
            print("\n❌ MISSING CLEANUP:")
            for req in validation.missing_cleanup:
                print(f"  - {req}")

    def run(self, args: List[str]):
        """Run CLI with arguments"""
        if not args or args[0] in ["help", "--help", "-h"]:
            self.show_help()
            return
        command = args[0].lower()
        try:
            if command == "validate":
                if len(args) < 2:
                    print("❌ Usage: validate <contract_id>")
                    return
                self.validate_contract(args[1])
            elif command == "report":
                if len(args) < 2:
                    print("❌ Usage: report <contract_id>")
                    return
                self.generate_report(args[1])
            elif command == "checklist":
                if len(args) < 2:
                    print("❌ Usage: checklist <contract_id>")
                    return
                self.show_checklist(args[1])
            elif command == "auto-validate":
                if len(args) < 2:
                    print("❌ Usage: auto-validate <contract_id>")
                    return
                self.auto_validate(args[1])
            else:
                print(f"❌ Unknown command: {command}")
                self.show_help()
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            import logging
            logging.getLogger(__name__).error(f"CLI error: {e}")

def main():
    """Main CLI entry point"""
    cli = CleanupCLI()
    cli.run(sys.argv[1:])

__all__ = ["CleanupCLI", "main"]
