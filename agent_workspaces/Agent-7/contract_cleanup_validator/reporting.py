"""Result reporting utilities for cleanup validation."""
from __future__ import annotations

from typing import List

from .shared import CleanupRequirement, CleanupValidation, StandardRequirement


def generate_cleanup_report(
    contract_id: str,
    validation: CleanupValidation,
    cleanup_requirements: List[CleanupRequirement],
    standards_requirements: List[StandardRequirement],
) -> str:
    """Generate a comprehensive cleanup report."""
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
    report += (
        f"""\n---\n\n## 🎯 **CLEANUP CHECKLIST**\n\n### **Required Cleanup Tasks:**\n"""
    )
    for req in cleanup_requirements:
        status = "✅" if req.completed else "❌"
        report += f"{status} {req.description}\n"
    report += f"""\n### **V2 Standards Requirements:**\n"""
    for std in standards_requirements:
        status = "✅" if std.compliant else "❌"
        report += f"{status} {std.description}\n"
    report += f"""\n---\n\n## 🚀 **NEXT STEPS**\n"""
    if validation.is_valid:
        report += "✅ **CONTRACT READY FOR COMPLETION**\n\nAll cleanup requirements met and V2 standards compliant.\nYou can now mark this contract as completed."
    else:
        report += "❌ **CLEANUP REQUIRED**\n\nPlease complete the missing cleanup tasks and ensure V2 standards compliance before marking this contract as completed."
    return report


__all__ = ["generate_cleanup_report"]
