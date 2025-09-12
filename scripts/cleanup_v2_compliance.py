import logging

logger = logging.getLogger(__name__)
"""
V2 Compliance Cleanup Script - Agent Cellphone V2
================================================

Automated script to identify and report V2 compliance issues.
Helps maintain code quality standards across the project.

Author: Agent-2 (Architecture & Design)
License: MIT
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


class V2ComplianceChecker:
    """V2 compliance checker for code quality standards."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues = []
        self.stats = {
            "total_files": 0,
            "python_files": 0,
            "large_files": 0,
            "critical_files": 0,
            "major_files": 0,
        }

    def analyze_file_sizes(self) -> list[dict[str, Any]]:

EXAMPLE USAGE:
==============

# Run the script directly
python cleanup_v2_compliance.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.cleanup_v2_compliance import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.cleanup_v2_compliance import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

        """Analyze file sizes for V2 compliance."""
        large_files = []
        src_dir = self.project_root / "src"
        for py_file in src_dir.rglob("*.py"):
            try:
                if py_file.stat().st_size == 0:
                    continue
                with open(py_file, encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    line_count = len(lines)
                self.stats["python_files"] += 1
                file_info = {
                    "path": str(py_file.relative_to(self.project_root)),
                    "lines": line_count,
                    "size_kb": py_file.stat().st_size / 1024,
                }
                if line_count >= 600:
                    file_info["severity"] = "CRITICAL"
                    file_info["recommendation"] = "Immediate refactoring required"
                    self.stats["critical_files"] += 1
                    large_files.append(file_info)
                elif line_count >= 400:
                    file_info["severity"] = "MAJOR"
                    file_info["recommendation"] = "Strategic refactoring target"
                    self.stats["major_files"] += 1
                    large_files.append(file_info)
                elif line_count >= 300:
                    file_info["severity"] = "MINOR"
                    file_info["recommendation"] = "Consider refactoring if complex"
                    large_files.append(file_info)
            except Exception as e:
                self.issues.append(f"Error reading {py_file}: {e}")
                continue
        large_files.sort(key=lambda x: x["lines"], reverse=True)
        return large_files

    def analyze_code_structure(self) -> dict[str, Any]:
        """Analyze code structure for compliance."""
        structure_issues = {
            "missing_init_files": [],
            "empty_directories": [],
            "duplicate_files": [],
        }
        src_dir = self.project_root / "src"
        for dir_path in src_dir.rglob("*"):
            try:
                if dir_path.is_dir():
                    init_file = dir_path / "__init__.py"
                    if not init_file.exists():
                        has_py_files = list(dir_path.glob("*.py"))
                        if has_py_files:
                            structure_issues["missing_init_files"].append(
                                str(dir_path.relative_to(self.project_root))
                            )
            except Exception:
                continue
        for dir_path in src_dir.rglob("*"):
            try:
                if dir_path.is_dir():
                    contents = list(dir_path.iterdir())
                    if not contents:
                        structure_issues["empty_directories"].append(
                            str(dir_path.relative_to(self.project_root))
                        )
            except Exception:
                continue
        return structure_issues

    def generate_report(self) -> str:
        """Generate comprehensive V2 compliance report."""
        large_files = self.analyze_file_sizes()
        structure_issues = self.analyze_code_structure()
        report = []
        report.append("🔍 Agent Cellphone V2 Compliance Report")
        report.append("=" * 50)
        report.append(f"📊 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("📈 File Statistics:")
        report.append(f"   • Total Python files: {self.stats['python_files']}")
        report.append(f"   • Files ≥300 lines: {len(large_files)}")
        report.append(f"   • Critical files (≥600 lines): {self.stats['critical_files']}")
        report.append(f"   • Major files (400-600 lines): {self.stats['major_files']}")
        report.append("")
        if large_files:
            report.append("📏 File Size Compliance Issues:")
            report.append("-" * 30)
            for file_info in large_files[:10]:
                severity_icon = {"CRITICAL": "🚨", "MAJOR": "⚠️", "MINOR": "ℹ️"}.get(
                    file_info["severity"], "❓"
                )
                report.append(f"   {severity_icon} {file_info['severity']}: {file_info['path']}")
                report.append(
                    f"      Lines: {file_info['lines']}, Size: {file_info['size_kb']:.1f} KB"
                )
                report.append(f"      Recommendation: {file_info['recommendation']}")
                report.append("")
        if structure_issues["missing_init_files"]:
            report.append("📁 Missing __init__.py Files:")
            report.append("-" * 30)
            for missing_init in structure_issues["missing_init_files"][:5]:
                report.append(f"   • {missing_init}")
            if len(structure_issues["missing_init_files"]) > 5:
                report.append(f"   ... and {len(structure_issues['missing_init_files']) - 5} more")
            report.append("")
        if structure_issues["empty_directories"]:
            report.append("📂 Empty Directories:")
            report.append("-" * 30)
            for empty_dir in structure_issues["empty_directories"][:5]:
                report.append(f"   • {empty_dir}")
            if len(structure_issues["empty_directories"]) > 5:
                report.append(f"   ... and {len(structure_issues['empty_directories']) - 5} more")
            report.append("")
        report.append("🎯 V2 Compliance Summary:")
        report.append("-" * 30)
        compliance_score = 100
        deductions = []
        if self.stats["critical_files"] > 0:
            deduction = min(self.stats["critical_files"] * 20, 50)
            compliance_score -= deduction
            deductions.append(f"Critical files: -{deduction} points")
        if self.stats["major_files"] > 0:
            deduction = min(self.stats["major_files"] * 10, 30)
            compliance_score -= deduction
            deductions.append(f"Major files: -{deduction} points")
        if structure_issues["missing_init_files"]:
            deduction = min(len(structure_issues["missing_init_files"]) * 2, 20)
            compliance_score -= deduction
            deductions.append(f"Missing __init__.py: -{deduction} points")
        compliance_score = max(0, compliance_score)
        report.append(f"   📊 Overall Compliance Score: {compliance_score}%")
        if deductions:
            report.append("   📝 Deductions:")
            for deduction in deductions:
                report.append(f"      • {deduction}")
        else:
            report.append("   ✅ No compliance deductions!")
        report.append("")
        report.append("💡 Recommendations:")
        report.append("-" * 30)
        if self.stats["critical_files"] > 0:
            report.append("   🚨 Address critical files (≥600 lines) immediately")
            report.append("      • Break down into smaller, focused modules")
            report.append("      • Extract utility functions into separate files")
            report.append("      • Consider class-based decomposition")
        if self.stats["major_files"] > 0:
            report.append("   ⚠️ Plan refactoring for major files (400-600 lines)")
            report.append("      • Identify logical separation points")
            report.append("      • Create feature-specific modules")
            report.append("      • Maintain single responsibility principle")
        if structure_issues["missing_init_files"]:
            report.append("   📁 Add missing __init__.py files")
            report.append("      • Essential for proper Python package structure")
            report.append("      • Enables relative imports")
            report.append("      • Improves code organization")
        if compliance_score >= 85:
            report.append("   🎉 Excellent compliance! Maintain current standards.")
        elif compliance_score >= 70:
            report.append("   👍 Good compliance. Focus on critical issues.")
        else:
            report.append("   ⚠️ Needs improvement. Prioritize refactoring efforts.")
        return "\n".join(report)

    def save_report(self, report: str, output_file: str = None):
        """Save compliance report to file."""
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(report)
            logger.info(f"\n💾 Report saved to: {output_file}")


def create_argument_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Agent Cellphone V2 Compliance Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cleanup_v2_compliance.py                    # Check compliance and display report
  python cleanup_v2_compliance.py -o report.md      # Save report to file
  python cleanup_v2_compliance.py --help            # Show this help
        """,
    )
    parser.add_argument("-o", "--output", type=str, help="Save compliance report to specified file")
    parser.add_argument(
        "--project-root",
        type=str,
        default=".",
        help="Project root directory (default: current directory)",
    )
    return parser


def main():
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        logger.info(f"❌ Project root directory does not exist: {project_root}")
        sys.exit(1)
    checker = V2ComplianceChecker(project_root)
    report = checker.generate_report()
    logger.info(report)
    if args.output:
        checker.save_report(report, args.output)


if __name__ == "__main__":
    main()
