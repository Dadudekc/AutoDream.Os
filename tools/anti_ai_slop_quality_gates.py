#!/usr/bin/env python3
"""
Anti-AI-Slop Quality Gates - V2 Compliance
==========================================

Quality gates specifically designed to prevent AI slop patterns
that degrade system quality and create unnecessary bloat.

V2 Compliance: ≤400 lines, focused AI slop prevention
Author: Agent-6 (Quality Assurance Specialist)
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class AntiAISlopDetector:
    """Detects AI slop patterns in the system."""

    def __init__(self, project_root: str = "."):
        """Initialize AI slop detector."""
        self.project_root = Path(project_root)
        self.ai_slop_patterns = {
            "repetitive_files": r".*_\d+\.md$|.*_cycle_\d+\.md$|.*_continuation_\d+\.md$",
            "captain_logs": r"captain_log.*\.md$",
            "autonomous_logs": r"autonomous.*log.*\.json$",
            "self_prompting": r".*self.*prompt.*\.py$",
            "analysis_bloat": r".*analysis.*\.md$|.*test.*results.*\.md$"
        }
        self.thresholds = {
            "max_files_per_cycle": 3,
            "max_file_size_kb": 5,
            "min_content_uniqueness": 0.8,
            "max_similar_files": 2
        }

    def detect_ai_slop_files(self) -> List[Dict[str, Any]]:
        """Detect files that match AI slop patterns."""
        violations = []
        
        for pattern_name, pattern in self.ai_slop_patterns.items():
            matches = list(self.project_root.rglob("*"))
            for file_path in matches:
                if file_path.is_file() and re.match(pattern, file_path.name):
                    violations.append({
                        "file": str(file_path),
                        "pattern": pattern_name,
                        "severity": "HIGH" if pattern_name in ["repetitive_files", "captain_logs"] else "MEDIUM"
                    })
        
        return violations

    def check_file_count_violations(self) -> List[Dict[str, Any]]:
        """Check for excessive file creation patterns."""
        violations = []
        
        # Check for numbered file sequences
        file_groups = {}
        for file_path in self.project_root.rglob("*.md"):
            base_name = re.sub(r'_\d+\.md$', '', file_path.name)
            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(file_path)
        
        for base_name, files in file_groups.items():
            if len(files) > self.thresholds["max_similar_files"]:
                violations.append({
                    "pattern": "excessive_similar_files",
                    "base_name": base_name,
                    "count": len(files),
                    "files": [str(f) for f in files],
                    "severity": "CRITICAL"
                })
        
        return violations

    def check_content_uniqueness(self, file_path: Path) -> float:
        """Check content uniqueness of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple uniqueness check based on unique words
            words = content.split()
            unique_words = set(words)
            return len(unique_words) / len(words) if words else 0.0
        except Exception:
            return 0.0

    def check_file_size_violations(self) -> List[Dict[str, Any]]:
        """Check for files exceeding size thresholds."""
        violations = []
        max_size_bytes = self.thresholds["max_file_size_kb"] * 1024
        
        for file_path in self.project_root.rglob("*.md"):
            if file_path.stat().st_size > max_size_bytes:
                violations.append({
                    "file": str(file_path),
                    "size_kb": file_path.stat().st_size / 1024,
                    "threshold_kb": self.thresholds["max_file_size_kb"],
                    "severity": "MEDIUM"
                })
        
        return violations

    def generate_ai_slop_report(self) -> Dict[str, Any]:
        """Generate comprehensive AI slop detection report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "ai_slop_files": self.detect_ai_slop_files(),
            "file_count_violations": self.check_file_count_violations(),
            "file_size_violations": self.check_file_size_violations(),
            "summary": {
                "total_violations": 0,
                "critical_violations": 0,
                "high_violations": 0,
                "medium_violations": 0
            }
        }
        
        # Calculate summary
        all_violations = (
            report["ai_slop_files"] + 
            report["file_count_violations"] + 
            report["file_size_violations"]
        )
        
        report["summary"]["total_violations"] = len(all_violations)
        for violation in all_violations:
            severity = violation.get("severity", "MEDIUM")
            if severity == "CRITICAL":
                report["summary"]["critical_violations"] += 1
            elif severity == "HIGH":
                report["summary"]["high_violations"] += 1
            else:
                report["summary"]["medium_violations"] += 1
        
        return report


class AntiAISlopPrevention:
    """Prevention mechanisms for AI slop."""

    def __init__(self, project_root: str = "."):
        """Initialize AI slop prevention."""
        self.project_root = Path(project_root)
        self.detector = AntiAISlopDetector(project_root)

    def validate_file_creation(self, proposed_files: List[str]) -> Tuple[bool, List[str]]:
        """Validate proposed file creation against AI slop prevention rules."""
        violations = []
        
        # Check file count
        if len(proposed_files) > self.detector.thresholds["max_files_per_cycle"]:
            violations.append(f"Too many files proposed: {len(proposed_files)} > {self.detector.thresholds['max_files_per_cycle']}")
        
        # Check for AI slop patterns
        for file_path in proposed_files:
            for pattern_name, pattern in self.detector.ai_slop_patterns.items():
                if re.match(pattern, Path(file_path).name):
                    violations.append(f"File matches AI slop pattern '{pattern_name}': {file_path}")
        
        return len(violations) == 0, violations

    def suggest_consolidation(self, files: List[str]) -> List[str]:
        """Suggest file consolidation to prevent AI slop."""
        suggestions = []
        
        # Group similar files
        file_groups = {}
        for file_path in files:
            base_name = re.sub(r'_\d+\.md$', '', Path(file_path).name)
            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(file_path)
        
        for base_name, group_files in file_groups.items():
            if len(group_files) > 1:
                suggestions.append(f"Consolidate {len(group_files)} files with base name '{base_name}': {', '.join(group_files)}")
        
        return suggestions

    def cleanup_ai_slop(self, dry_run: bool = True) -> Dict[str, Any]:
        """Clean up detected AI slop files."""
        report = self.detector.generate_ai_slop_report()
        cleanup_actions = []
        
        if dry_run:
            print("🔍 DRY RUN - No files will be deleted")
        
        for violation in report["ai_slop_files"]:
            file_path = Path(violation["file"])
            if file_path.exists():
                cleanup_actions.append({
                    "action": "delete" if not dry_run else "would_delete",
                    "file": str(file_path),
                    "reason": f"AI slop pattern: {violation['pattern']}"
                })
                
                if not dry_run:
                    try:
                        file_path.unlink()
                    except Exception as e:
                        cleanup_actions[-1]["error"] = str(e)
        
        return {
            "cleanup_actions": cleanup_actions,
            "dry_run": dry_run,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main function for Anti-AI-Slop Quality Gates."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Anti-AI-Slop Quality Gates")
    parser.add_argument("--check", action="store_true", help="Check for AI slop patterns")
    parser.add_argument("--cleanup", action="store_true", help="Clean up AI slop files")
    parser.add_argument("--dry-run", action="store_true", help="Dry run cleanup (no actual deletion)")
    parser.add_argument("--report", action="store_true", help="Generate AI slop report")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    detector = AntiAISlopDetector(args.project_root)
    prevention = AntiAISlopPrevention(args.project_root)
    
    if args.check:
        violations = detector.detect_ai_slop_files()
        if violations:
            print("🚨 AI SLOP DETECTED:")
            for violation in violations:
                print(f"  {violation['severity']}: {violation['file']} ({violation['pattern']})")
        else:
            print("✅ No AI slop patterns detected")
    
    if args.report:
        report = detector.generate_ai_slop_report()
        print(f"📊 AI Slop Report:")
        print(f"  Total Violations: {report['summary']['total_violations']}")
        print(f"  Critical: {report['summary']['critical_violations']}")
        print(f"  High: {report['summary']['high_violations']}")
        print(f"  Medium: {report['summary']['medium_violations']}")
    
    if args.cleanup:
        cleanup_result = prevention.cleanup_ai_slop(dry_run=args.dry_run)
        print(f"🧹 Cleanup {'Dry Run' if args.dry_run else 'Executed'}:")
        for action in cleanup_result["cleanup_actions"]:
            print(f"  {action['action']}: {action['file']} - {action['reason']}")


if __name__ == "__main__":
    main()
