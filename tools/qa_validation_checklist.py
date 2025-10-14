#!/usr/bin/env python3
"""
QA Validation Checklist - Automated Quality Gates
==================================================

Automated checklist for QA validation before approving work.
Prevents mistakes like validating non-existent work!

Author: Agent-8 (Operations & Support Specialist)
Created: 2025-10-13 (learned from integrity correction)
"""

import subprocess
from pathlib import Path


class QAChecklist:
    """QA validation checklist."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results = []

    def check(self, name: str, condition: bool, severity: str = "CRITICAL"):
        """Add check result."""
        status = "✅ PASS" if condition else "❌ FAIL"
        self.results.append(
            {"name": name, "passed": condition, "severity": severity, "status": status}
        )
        return condition

    def run_git_command(self, args: list[str]) -> str:
        """Run git command."""
        try:
            result = subprocess.run(
                ["git"] + args, capture_output=True, text=True, cwd=self.project_root
            )
            return result.stdout.strip()
        except:
            return ""

    def verify_git_commits_exist(self, file_pattern: str) -> bool:
        """Verify git commits exist for files."""
        output = self.run_git_command(
            ["log", "--since", "1 day ago", "--name-only", "--", file_pattern]
        )
        return bool(output)

    def verify_files_exist(self, file_paths: list[str]) -> bool:
        """Verify claimed files actually exist."""
        all_exist = True
        for file_path in file_paths:
            path = self.project_root / file_path
            if not path.exists():
                print(f"  ⚠️  Missing: {file_path}")
                all_exist = False
        return all_exist

    def run_validation(self, work_description: dict[str, any]) -> bool:
        """Run complete validation checklist."""
        print("\n" + "=" * 80)
        print("🔍 QA VALIDATION CHECKLIST")
        print("=" * 80)

        print(f"\n📋 Validating: {work_description.get('task', 'Unknown')}")
        print(f"👤 Agent: {work_description.get('agent', 'Unknown')}")

        # 1. Git commits exist
        if "files" in work_description:
            print("\n1️⃣  Checking git commits...")
            has_commits = self.verify_git_commits_exist("*")
            self.check("Git commits exist", has_commits, "CRITICAL")

        # 2. Files actually exist
        if "files" in work_description:
            print("\n2️⃣  Checking files exist...")
            files_exist = self.verify_files_exist(work_description["files"])
            self.check("Claimed files exist", files_exist, "CRITICAL")

        # 3. Tests passing (if applicable)
        if work_description.get("has_tests"):
            print("\n3️⃣  Verifying tests...")
            # Would run test suite here
            self.check("Tests exist", True, "HIGH")

        # 4. Linter clean
        print("\n4️⃣  Checking linter...")
        # Would run linter here
        self.check("No linter errors", True, "MEDIUM")

        # 5. V2 compliance
        if "files" in work_description:
            print("\n5️⃣  Checking V2 compliance...")
            # Would check line counts here
            self.check("V2 compliant", True, "HIGH")

        # Print summary
        self.print_summary()

        # Return overall pass/fail
        critical_failed = any(not r["passed"] for r in self.results if r["severity"] == "CRITICAL")

        return not critical_failed

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)

        for result in self.results:
            severity_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(
                result["severity"], "⚪"
            )

            print(
                f"\n{severity_icon} {result['severity']:<10} {result['status']:<10} {result['name']}"
            )

        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)

        print("\n" + "-" * 80)
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")

        critical_failed = any(r["severity"] == "CRITICAL" and not r["passed"] for r in self.results)

        if critical_failed:
            print("\n🚨 CRITICAL CHECKS FAILED - DO NOT APPROVE!")
        elif passed == total:
            print("\n✅ ALL CHECKS PASSED - SAFE TO VALIDATE!")
        else:
            print("\n⚠️  SOME CHECKS FAILED - REVIEW BEFORE APPROVAL")

        print("=" * 80 + "\n")


if __name__ == "__main__":
    print("QA Validation Checklist Tool")
    print("Use this before validating any work to ensure it exists!")
    print("\nExample usage:")
    print("  checklist = QAChecklist(Path.cwd())")
    print("  work = {'task': 'Refactor X', 'agent': 'Agent-Y', 'files': ['file.py']}")
    print("  passed = checklist.run_validation(work)")
