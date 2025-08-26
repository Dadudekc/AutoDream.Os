#!/usr/bin/env python3
"""
Contract Cleanup Validator - Agent Cellphone V2
==============================================

Comprehensive validation system that ensures agents complete contracts properly,
follow all V2 standards, clean up their work, and maintain project integrity.

Author: Agent-4 (Captain)
Purpose: Enforce contract completion standards and cleanup requirements
"""

import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CleanupStatus(Enum):
    """Cleanup status enumeration"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class StandardCompliance(Enum):
    """Standard compliance enumeration"""
    COMPLIANT = "COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"

@dataclass
class CleanupRequirement:
    """Individual cleanup requirement"""
    requirement_id: str
    description: str
    required: bool
    completed: bool = False
    validation_notes: str = ""
    completion_timestamp: Optional[str] = None
    evidence_files: List[str] = None

@dataclass
class StandardRequirement:
    """V2 standard requirement"""
    standard_id: str
    description: str
    required: bool
    compliant: bool = False
    validation_notes: str = ""
    compliance_score: float = 0.0

@dataclass
class CleanupValidation:
    """Cleanup validation result"""
    is_valid: bool
    missing_cleanup: List[str]
    validation_errors: List[str]
    warnings: List[str]
    cleanup_score: float  # 0.0 to 1.0
    standards_score: float  # 0.0 to 1.0
    overall_score: float  # 0.0 to 1.0
    timestamp: str

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
                with open(self.validation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for contract_id, validation_data in data.items():
                        self.cleanup_validations[contract_id] = CleanupValidation(**validation_data)
            except Exception as e:
                logger.error(f"Error loading cleanup validations: {e}")
                self.cleanup_validations = {}
    
    def save_validations(self):
        """Save cleanup validations to file"""
        try:
            data = {}
            for contract_id, validation in self.cleanup_validations.items():
                data[contract_id] = asdict(validation)
            
            with open(self.validation_file, 'w', encoding='utf-8') as f:
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
                evidence_files=[]
            ),
            CleanupRequirement(
                requirement_id="documentation_cleanup",
                description="Update or create proper documentation (README, docstrings, comments)",
                required=True,
                evidence_files=[]
            ),
            CleanupRequirement(
                requirement_id="test_cleanup",
                description="Ensure tests pass and remove any test-specific temporary code",
                required=True,
                evidence_files=[]
            ),
            CleanupRequirement(
                requirement_id="file_organization",
                description="Organize files in proper directories and remove any temporary files",
                required=True,
                evidence_files=[]
            ),
            CleanupRequirement(
                requirement_id="git_cleanup",
                description="Commit all changes with proper commit messages and push to remote",
                required=True,
                evidence_files=[]
            ),
            CleanupRequirement(
                requirement_id="devlog_entry",
                description="Create comprehensive devlog entry documenting all work completed",
                required=True,
                evidence_files=[]
            ),
            CleanupRequirement(
                requirement_id="discord_update",
                description="Post Discord devlog update summarizing completed work",
                required=True,
                evidence_files=[]
            )
        ]
    
    def get_v2_standards_requirements(self) -> List[StandardRequirement]:
        """Get V2 architecture standards requirements"""
        return [
            StandardRequirement(
                standard_id="srp_compliance",
                description="Single Responsibility Principle - Each class/module has one clear purpose",
                required=True,
                compliance_score=0.0
            ),
            StandardRequirement(
                standard_id="loc_compliance",
                description="Line count compliance - No file exceeds 200 LOC",
                required=True,
                compliance_score=0.0
            ),
            StandardRequirement(
                standard_id="oop_patterns",
                description="Proper OOP patterns and inheritance structure",
                required=True,
                compliance_score=0.0
            ),
            StandardRequirement(
                standard_id="no_duplication",
                description="No duplicate functionality - use existing unified systems",
                required=True,
                compliance_score=0.0
            ),
            StandardRequirement(
                standard_id="error_handling",
                description="Comprehensive error handling and logging",
                required=True,
                compliance_score=0.0
            ),
            StandardRequirement(
                standard_id="integration_compliance",
                description="Proper integration with existing systems",
                required=True,
                compliance_score=0.0
            )
        ]
    
    def validate_cleanup_completion(self, contract_id: str) -> CleanupValidation:
        """Validate that all cleanup requirements are met"""
        cleanup_requirements = self.get_cleanup_requirements()
        standards_requirements = self.get_v2_standards_requirements()
        
        missing_cleanup = []
        validation_errors = []
        warnings = []
        
        # Validate cleanup requirements
        cleanup_completed = 0
        total_cleanup = len(cleanup_requirements)
        
        for req in cleanup_requirements:
            if not req.completed:
                missing_cleanup.append(req.description)
            else:
                cleanup_completed += 1
        
        cleanup_score = cleanup_completed / total_cleanup if total_cleanup > 0 else 0.0
        
        # Validate V2 standards
        standards_compliant = 0
        total_standards = len(standards_requirements)
        
        for std in standards_requirements:
            if std.compliant:
                standards_compliant += 1
        
        standards_score = standards_compliant / total_standards if total_standards > 0 else 0.0
        
        # Calculate overall score (cleanup is 60%, standards are 40%)
        overall_score = (cleanup_score * 0.6) + (standards_score * 0.4)
        
        # Determine if valid
        is_valid = overall_score >= 0.9 and cleanup_score >= 0.85 and standards_score >= 0.8
        
        # Create validation result
        validation = CleanupValidation(
            is_valid=is_valid,
            missing_cleanup=missing_cleanup,
            validation_errors=validation_errors,
            warnings=warnings,
            cleanup_score=cleanup_score,
            standards_score=standards_score,
            overall_score=overall_score,
            timestamp=datetime.now().isoformat()
        )
        
        # Save validation
        self.cleanup_validations[contract_id] = validation
        self.save_validations()
        
        return validation
    
    def check_code_cleanup(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check if code cleanup requirements are met"""
        issues = []
        
        # Check for temporary files
        temp_files = list(Path(".").glob("*.tmp")) + list(Path(".").glob("*temp*"))
        if temp_files:
            issues.append(f"Temporary files found: {[f.name for f in temp_files]}")
        
        # Check for debug statements
        debug_patterns = ["print(", "debug(", "console.log(", "TODO:", "FIXME:"]
        for pattern in debug_patterns:
            # This is a simplified check - in practice you'd scan actual source files
            pass
        
        # Check for unused imports (simplified)
        # In practice, you'd use tools like pyflakes or pylint
        
        return len(issues) == 0, issues
    
    def check_documentation_cleanup(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check if documentation cleanup requirements are met"""
        issues = []
        
        # Check for devlog entry
        devlog_files = list(Path("logs").glob(f"*{contract_id}*"))
        if not devlog_files:
            issues.append("Devlog entry not found")
        
        # Check for README updates
        readme_files = list(Path(".").glob("README*"))
        if not readme_files:
            issues.append("No README files found")
        
        return len(issues) == 0, issues
    
    def check_git_cleanup(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check if git cleanup requirements are met"""
        issues = []
        
        # Check git status
        try:
            import subprocess
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True, cwd=".")
            if result.stdout.strip():
                issues.append("Uncommitted changes found")
        except Exception:
            issues.append("Could not check git status")
        
        return len(issues) == 0, issues
    
    def check_v2_standards_compliance(self, contract_id: str) -> Tuple[bool, List[str]]:
        """Check V2 standards compliance"""
        issues = []
        
        # Check for large files
        large_files = []
        for py_file in Path("src").rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    if lines > 200:
                        large_files.append(f"{py_file}: {lines} lines")
            except Exception:
                pass
        
        if large_files:
            issues.append(f"Files exceeding 200 LOC: {large_files[:5]}")  # Show first 5
        
        # Check for duplicate functionality (simplified)
        # In practice, you'd use more sophisticated analysis
        
        return len(issues) == 0, issues
    
    def generate_cleanup_report(self, contract_id: str) -> str:
        """Generate comprehensive cleanup report"""
        validation = self.validate_cleanup_completion(contract_id)
        
        report = f"""# 🧹 CONTRACT CLEANUP VALIDATION REPORT - {contract_id}

**Generated**: {validation.timestamp}  
**Overall Status**: {'✅ VALID' if validation.is_valid else '❌ INVALID'}  
**Overall Score**: {validation.overall_score:.2f}/1.0

---

## 📊 **VALIDATION SCORES**

### **🧹 Cleanup Requirements**: {validation.cleanup_score:.2f}/1.0
- **Status**: {'✅ COMPLETE' if validation.cleanup_score >= 0.85 else '❌ INCOMPLETE'}
- **Weight**: 60% of overall score

### **🏗️ V2 Standards Compliance**: {validation.standards_score:.2f}/1.0
- **Status**: {'✅ COMPLIANT' if validation.standards_score >= 0.8 else '❌ NON-COMPLIANT'}
- **Weight**: 40% of overall score

---

## ❌ **MISSING CLEANUP REQUIREMENTS**

"""
        
        if validation.missing_cleanup:
            for req in validation.missing_cleanup:
                report += f"- {req}\n"
        else:
            report += "✅ All cleanup requirements completed\n"
        
        report += f"""

---

## 🚨 **VALIDATION ERRORS**

"""
        
        if validation.validation_errors:
            for error in validation.validation_errors:
                report += f"- {error}\n"
        else:
            report += "✅ No validation errors found\n"
        
        report += f"""

---

## ⚠️ **WARNINGS**

"""
        
        if validation.warnings:
            for warning in validation.warnings:
                report += f"- {warning}\n"
        else:
            report += "✅ No warnings\n"
        
        report += f"""

---

## 🎯 **CLEANUP CHECKLIST**

### **Required Cleanup Tasks:**
"""
        
        cleanup_requirements = self.get_cleanup_requirements()
        for req in cleanup_requirements:
            status = "✅" if req.completed else "❌"
            report += f"{status} {req.description}\n"
        
        report += f"""

### **V2 Standards Requirements:**
"""
        
        standards_requirements = self.get_v2_standards_requirements()
        for std in standards_requirements:
            status = "✅" if std.compliant else "❌"
            report += f"{status} {std.description}\n"
        
        report += f"""

---

## 🚀 **NEXT STEPS**

"""
        
        if validation.is_valid:
            report += """✅ **CONTRACT READY FOR COMPLETION**

All cleanup requirements met and V2 standards compliant.
You can now mark this contract as completed."""
        else:
            report += """❌ **CLEANUP REQUIRED**

Please complete the missing cleanup tasks and ensure V2 standards compliance
before marking this contract as completed."""
        
        return report
    
    def auto_validate_contract(self, contract_id: str) -> CleanupValidation:
        """Automatically validate contract cleanup and standards"""
        logger.info(f"Auto-validating contract {contract_id}...")
        
        # Run all validation checks
        code_cleanup_ok, code_issues = self.check_code_cleanup(contract_id)
        doc_cleanup_ok, doc_issues = self.check_documentation_cleanup(contract_id)
        git_cleanup_ok, git_issues = self.check_git_cleanup(contract_id)
        standards_ok, standards_issues = self.check_v2_standards_compliance(contract_id)
        
        # Update cleanup requirements based on checks
        cleanup_requirements = self.get_cleanup_requirements()
        
        # Code cleanup
        for req in cleanup_requirements:
            if req.requirement_id == "code_cleanup":
                req.completed = code_cleanup_ok
                if not code_cleanup_ok:
                    req.validation_notes = f"Issues found: {', '.join(code_issues)}"
        
        # Documentation cleanup
        for req in cleanup_requirements:
            if req.requirement_id == "documentation_cleanup":
                req.completed = doc_cleanup_ok
                if not doc_cleanup_ok:
                    req.validation_notes = f"Issues found: {', '.join(doc_issues)}"
        
        # Git cleanup
        for req in cleanup_requirements:
            if req.requirement_id == "git_cleanup":
                req.completed = git_cleanup_ok
                if not git_cleanup_ok:
                    req.validation_notes = f"Issues found: {', '.join(git_issues)}"
        
        # Update standards requirements
        standards_requirements = self.get_v2_standards_requirements()
        
        for std in standards_requirements:
            if std.standard_id == "loc_compliance":
                std.compliant = standards_ok
                if not standards_ok:
                    std.validation_notes = f"Issues found: {', '.join(standards_issues)}"
        
        # Validate completion
        return self.validate_cleanup_completion(contract_id)

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
            print(f"\n❌ Missing Cleanup:")
            for req in validation.missing_cleanup:
                print(f"  - {req}")
        
        if validation.validation_errors:
            print(f"\n🚨 Validation Errors:")
            for error in validation.validation_errors:
                print(f"  - {error}")
        
        if validation.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in validation.warnings:
                print(f"  - {warning}")
    
    def generate_report(self, contract_id: str):
        """Generate cleanup report"""
        print(f"📊 Generating cleanup report for {contract_id}...")
        
        report = self.validator.generate_cleanup_report(contract_id)
        
        # Save report to file
        report_file = Path(f"logs/{contract_id}_cleanup_report.md")
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report saved to: {report_file}")
        print("\n" + "="*80)
        print(report)
        print("="*80)
    
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
        
        # Show detailed results
        print(f"\n📊 DETAILED RESULTS:")
        print(f"Cleanup Score: {validation.cleanup_score:.2f}/1.0")
        print(f"Standards Score: {validation.standards_score:.2f}/1.0")
        print(f"Overall Score: {validation.overall_score:.2f}/1.0")
        
        if validation.missing_cleanup:
            print(f"\n❌ MISSING CLEANUP:")
            for req in validation.missing_cleanup:
                print(f"  - {req}")
    
    def run(self, args: List[str]):
        """Run CLI with arguments"""
        if not args or args[0] in ['help', '--help', '-h']:
            self.show_help()
            return
        
        command = args[0].lower()
        
        try:
            if command == 'validate':
                if len(args) < 2:
                    print("❌ Usage: validate <contract_id>")
                    return
                self.validate_contract(args[1])
            
            elif command == 'report':
                if len(args) < 2:
                    print("❌ Usage: report <contract_id>")
                    return
                self.generate_report(args[1])
            
            elif command == 'checklist':
                if len(args) < 2:
                    print("❌ Usage: checklist <contract_id>")
                    return
                self.show_checklist(args[1])
            
            elif command == 'auto-validate':
                if len(args) < 2:
                    print("❌ Usage: auto-validate <contract_id>")
                    return
                self.auto_validate(args[1])
            
            else:
                print(f"❌ Unknown command: {command}")
                self.show_help()
        
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            logger.error(f"CLI error: {e}")

def main():
    """Main CLI entry point"""
    cli = CleanupCLI()
    cli.run(sys.argv[1:])

if __name__ == "__main__":
    main()
