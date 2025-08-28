import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import asdict

from .models import (
    CleanupRequirement,
    StandardRequirement,
    CleanupValidation,
)

logger = logging.getLogger(__name__)

class ContractCleanupValidator:
    """Main contract cleanup validation system"""

    def __init__(self, contracts_dir: str = "logs"):
        self.contracts_dir = Path(contracts_dir)
        self.contracts_dir.mkdir(exist_ok=True)
        self.validation_file = self.contracts_dir / "cleanup_validations.json"
        self.cleanup_validations: Dict[str, CleanupValidation] = {}
        self.load_validations()

    def load_validations(self):
        """Load existing cleanup validations"""
        if self.validation_file.exists():
            try:
                with open(self.validation_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for contract_id, validation_data in data.items():
                        self.cleanup_validations[contract_id] = CleanupValidation(**validation_data)
            except Exception as e:
                logger.error(f"Error loading cleanup validations: {e}")
                self.cleanup_validations = {}

    def save_validations(self):
        """Save cleanup validations to file"""
        try:
            data = {contract_id: asdict(validation) for contract_id, validation in self.cleanup_validations.items()}
            with open(self.validation_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving cleanup validations: {e}")

    def get_cleanup_requirements(self) -> List[CleanupRequirement]:
        """Get standard cleanup requirements for all contracts"""
        return [
            CleanupRequirement(
                requirement_id="code_cleanup",
                description="Clean up any temporary code, debug statements, or unused imports",
                required=True,
                evidence_files=[],
            ),
            CleanupRequirement(
                requirement_id="documentation_cleanup",
                description="Update or create proper documentation (README, docstrings, comments)",
                required=True,
                evidence_files=[],
            ),
            CleanupRequirement(
                requirement_id="test_cleanup",
                description="Ensure tests pass and remove any test-specific temporary code",
                required=True,
                evidence_files=[],
            ),
            CleanupRequirement(
                requirement_id="file_organization",
                description="Organize files in proper directories and remove any temporary files",
                required=True,
                evidence_files=[],
            ),
            CleanupRequirement(
                requirement_id="git_cleanup",
                description="Commit all changes with proper commit messages and push to remote",
                required=True,
                evidence_files=[],
            ),
            CleanupRequirement(
                requirement_id="devlog_entry",
                description="Create comprehensive devlog entry documenting all work completed",
                required=True,
                evidence_files=[],
            ),
            CleanupRequirement(
                requirement_id="discord_update",
                description="Post Discord devlog update summarizing completed work",
                required=True,
                evidence_files=[],
            ),
        ]

    def get_v2_standards_requirements(self) -> List[StandardRequirement]:
        """Get V2 architecture standards requirements"""
        return [
            StandardRequirement(
                standard_id="srp_compliance",
                description="Single Responsibility Principle - Each class/module has one clear purpose",
                required=True,
                compliance_score=0.0,
            ),
            StandardRequirement(
                standard_id="loc_compliance",
                description="Line count compliance - No file exceeds 200 LOC",
                required=True,
                compliance_score=0.0,
            ),
            StandardRequirement(
                standard_id="oop_patterns",
                description="Proper OOP patterns and inheritance structure",
                required=True,
                compliance_score=0.0,
            ),
            StandardRequirement(
                standard_id="no_duplication",
                description="No duplicate functionality - use existing unified systems",
                required=True,
                compliance_score=0.0,
            ),
            StandardRequirement(
                standard_id="error_handling",
                description="Comprehensive error handling and logging",
                required=True,
                compliance_score=0.0,
            ),
            StandardRequirement(
                standard_id="integration_compliance",
                description="Proper integration with existing systems",
                required=True,
                compliance_score=0.0,
            ),
        ]

    def validate_cleanup_completion(self, contract_id: str) -> CleanupValidation:
        """Validate that all cleanup requirements are met"""
        cleanup_requirements = self.get_cleanup_requirements()
        standards_requirements = self.get_v2_standards_requirements()

        missing_cleanup: List[str] = []
        validation_errors: List[str] = []
        warnings: List[str] = []

        cleanup_completed = sum(req.completed for req in cleanup_requirements)
        total_cleanup = len(cleanup_requirements)
        for req in cleanup_requirements:
            if not req.completed:
                missing_cleanup.append(req.description)

        cleanup_score = cleanup_completed / total_cleanup if total_cleanup > 0 else 0.0

        standards_compliant = sum(std.compliant for std in standards_requirements)
        total_standards = len(standards_requirements)
        standards_score = standards_compliant / total_standards if total_standards > 0 else 0.0

        overall_score = (cleanup_score * 0.6) + (standards_score * 0.4)
        is_valid = overall_score >= 0.9 and cleanup_score >= 0.85 and standards_score >= 0.8

        validation = CleanupValidation(
            is_valid=is_valid,
            missing_cleanup=missing_cleanup,
            validation_errors=validation_errors,
            warnings=warnings,
            cleanup_score=cleanup_score,
            standards_score=standards_score,
            overall_score=overall_score,
            timestamp=datetime.now().isoformat(),
        )

        self.cleanup_validations[contract_id] = validation
        self.save_validations()
        return validation

    def check_code_cleanup(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check if code cleanup requirements are met"""
        issues: List[str] = []
        temp_files = list(Path(".").glob("*.tmp")) + list(Path(".").glob("*temp*"))
        if temp_files:
            issues.append(f"Temporary files found: {[f.name for f in temp_files]}")
        debug_patterns = ["print(", "debug(", "console.log(", "TODO:", "FIXME:"]
        for _ in debug_patterns:
            pass
        return len(issues) == 0, issues

    def check_documentation_cleanup(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check if documentation cleanup requirements are met"""
        issues: List[str] = []
        devlog_files = list(Path("logs").glob(f"*{contract_id}*"))
        if not devlog_files:
            issues.append("Devlog entry not found")
        readme_files = list(Path(".").glob("README*"))
        if not readme_files:
            issues.append("No README files found")
        return len(issues) == 0, issues

    def check_git_cleanup(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check if git cleanup requirements are met"""
        issues: List[str] = []
        try:
            import subprocess
            result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=".")
            if result.stdout.strip():
                issues.append("Uncommitted changes found")
        except Exception:
            issues.append("Could not check git status")
        return len(issues) == 0, issues

    def check_v2_standards_compliance(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check V2 standards compliance"""
        issues: List[str] = []
        large_files = []
        for py_file in Path("src").rglob("*.py"):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    lines = len(f.readlines())
                    if lines > 200:
                        large_files.append(f"{py_file}: {lines} lines")
            except Exception:
                pass
        if large_files:
            issues.append(f"Files exceeding 200 LOC: {large_files[:5]}")
        return len(issues) == 0, issues

    def generate_cleanup_report(self, contract_id: str) -> str:
        """Generate comprehensive cleanup report"""
        validation = self.validate_cleanup_completion(contract_id)
        report = f"""# 🧹 CONTRACT CLEANUP VALIDATION REPORT - {contract_id}\n\n**Generated**: {validation.timestamp}\n**Overall Status**: {'✅ VALID' if validation.is_valid else '❌ INVALID'}\n**Overall Score**: {validation.overall_score:.2f}/1.0\n\n---\n\n## 📊 **VALIDATION SCORES**\n\n### **🧹 Cleanup Requirements**: {validation.cleanup_score:.2f}/1.0\n- **Status**: {'✅ COMPLETE' if validation.cleanup_score >= 0.85 else '❌ INCOMPLETE'}\n- **Weight**: 60% of overall score\n\n### **🏗️ V2 Standards Compliance**: {validation.standards_score:.2f}/1.0\n- **Status**: {'✅ COMPLIANT' if validation.standards_score >= 0.8 else '❌ NON-COMPLIANT'}\n- **Weight**: 40% of overall score\n\n---\n\n## ❌ **MISSING CLEANUP REQUIREMENTS**\n"""
        if validation.missing_cleanup:
            for req in validation.missing_cleanup:
                report += f"- {req}\n"
        else:
            report += "✅ All cleanup requirements completed\n"
        report += f"""\n---\n\n## 🚨 **VALIDATION ERRORS**\n"""
        if validation.validation_errors:
            for error in validation.validation_errors:
                report += f"- {error}\n"
        else:
            report += "✅ No validation errors found\n"
        report += f"""\n---\n\n## ⚠️ **WARNINGS**\n"""
        if validation.warnings:
            for warning in validation.warnings:
                report += f"- {warning}\n"
        else:
            report += "✅ No warnings\n"
        report += f"""\n---\n\n## 🎯 **CLEANUP CHECKLIST**\n\n### **Required Cleanup Tasks:**\n"""
        cleanup_requirements = self.get_cleanup_requirements()
        for req in cleanup_requirements:
            status = "✅" if req.completed else "❌"
            report += f"{status} {req.description}\n"
        report += f"""\n### **V2 Standards Requirements:**\n"""
        standards_requirements = self.get_v2_standards_requirements()
        for std in standards_requirements:
            status = "✅" if std.compliant else "❌"
            report += f"{status} {std.description}\n"
        report += f"""\n---\n\n## 🚀 **NEXT STEPS**\n"""
        if validation.is_valid:
            report += """✅ **CONTRACT READY FOR COMPLETION**\n\nAll cleanup requirements met and V2 standards compliant.\nYou can now mark this contract as completed."""
        else:
            report += """❌ **CLEANUP REQUIRED**\n\nPlease complete the missing cleanup tasks and ensure V2 standards compliance\nbefore marking this contract as completed."""
        return report

    def auto_validate_contract(self, contract_id: str) -> CleanupValidation:
        """Automatically validate contract cleanup and standards"""
        logger.info(f"Auto-validating contract {contract_id}...")
        code_cleanup_ok, code_issues = self.check_code_cleanup(contract_id)
        doc_cleanup_ok, doc_issues = self.check_documentation_cleanup(contract_id)
        git_cleanup_ok, git_issues = self.check_git_cleanup(contract_id)
        standards_ok, standards_issues = self.check_v2_standards_compliance(contract_id)

        cleanup_requirements = self.get_cleanup_requirements()
        for req in cleanup_requirements:
            if req.requirement_id == "code_cleanup":
                req.completed = code_cleanup_ok
                if not code_cleanup_ok:
                    req.validation_notes = f"Issues found: {', '.join(code_issues)}"
        for req in cleanup_requirements:
            if req.requirement_id == "documentation_cleanup":
                req.completed = doc_cleanup_ok
                if not doc_cleanup_ok:
                    req.validation_notes = f"Issues found: {', '.join(doc_issues)}"
        for req in cleanup_requirements:
            if req.requirement_id == "git_cleanup":
                req.completed = git_cleanup_ok
                if not git_cleanup_ok:
                    req.validation_notes = f"Issues found: {', '.join(git_issues)}"

        standards_requirements = self.get_v2_standards_requirements()
        for std in standards_requirements:
            if std.standard_id == "loc_compliance":
                std.compliant = standards_ok
                if not standards_ok:
                    std.validation_notes = f"Issues found: {', '.join(standards_issues)}"
        return self.validate_cleanup_completion(contract_id)

__all__ = ["ContractCleanupValidator"]
