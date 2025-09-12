#!/usr/bin/env python3
"""
Duplication Analysis Tool
========================

Advanced duplication detection and analysis system for safe consolidation.
Distinguishes between true duplicates, similar-but-different, and false duplicates.

Usage:
    python tools/duplication_analyzer.py --scan
    python tools/duplication_analyzer.py --analyze-function <function_name>
    python tools/duplication_analyzer.py --find-true-duplicates
    python tools/duplication_analyzer.py --generate-consolidation-plan
"""

import ast
import difflib
import hashlib
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class DuplicationAnalyzer:
    """Advanced duplication detection and analysis system."""

    def __init__(self):
        self.project_root = project_root
        self.exclude_patterns = [
            "__pycache__",
            ".git",
            "node_modules",
            "*.pyc",
            ".pytest_cache",
            "build",
            "dist",
            "venv",
        ]

    def scan_codebase(self) -> dict[str, Any]:

EXAMPLE USAGE:
==============

# Basic usage example
from tools.duplication_analyzer import Duplication_Analyzer

# Initialize and use
instance = Duplication_Analyzer()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Duplication_Analyzer(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

        """Scan entire codebase for potential duplications."""
        print("🔍 Scanning codebase for duplications...")

        functions = defaultdict(list)
        classes = defaultdict(list)
        imports = defaultdict(list)

        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    content = py_file.read_text(encoding="utf-8")
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_hash = self._get_function_hash(node, content)
                            functions[func_hash].append(
                                {
                                    "file": str(py_file.relative_to(self.project_root)),
                                    "name": node.name,
                                    "line": node.lineno,
                                    "content": self._get_node_content(node, content),
                                }
                            )

                        elif isinstance(node, ast.ClassDef):
                            class_hash = self._get_class_hash(node, content)
                            classes[class_hash].append(
                                {
                                    "file": str(py_file.relative_to(self.project_root)),
                                    "name": node.name,
                                    "line": node.lineno,
                                    "content": self._get_node_content(node, content),
                                }
                            )

                except Exception as e:
                    print(f"Warning: Could not process {py_file}: {e}")

        return {
            "functions": dict(functions),
            "classes": dict(classes),
            "imports": dict(imports),
            "summary": {
                "total_files": len(list(self.project_root.rglob("*.py"))),
                "processed_files": len(
                    [f for f in self.project_root.rglob("*.py") if self._should_include_file(f)]
                ),
                "function_groups": len(functions),
                "class_groups": len(classes),
                "potential_duplicates": sum(len(v) > 1 for v in functions.values())
                + sum(len(v) > 1 for v in classes.values()),
            },
        }

    def _should_include_file(self, file_path: Path) -> bool:
        """Determine if file should be included in analysis."""
        file_str = str(file_path)
        for pattern in self.exclude_patterns:
            if pattern in file_str:
                return False
        return file_path.suffix == ".py"

    def _get_function_hash(self, node: ast.FunctionDef, content: str) -> str:
        """Generate hash for function content."""
        func_content = self._get_node_content(node, content)
        # Remove docstrings and comments for better matching
        clean_content = self._clean_code_content(func_content)
        return hashlib.md5(clean_content.encode()).hexdigest()

    def _get_class_hash(self, node: ast.ClassDef, content: str) -> str:
        """Generate hash for class content."""
        class_content = self._get_node_content(node, content)
        clean_content = self._clean_code_content(class_content)
        return hashlib.md5(clean_content.encode()).hexdigest()

    def _get_node_content(self, node: ast.AST, content: str) -> str:
        """Extract source code for AST node."""
        if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
            lines = content.split("\n")
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
        return ""

    def _clean_code_content(self, content: str) -> str:
        """Clean code content for better duplicate detection."""
        lines = []
        for line in content.split("\n"):
            # Remove comments
            line = line.split("#")[0]
            # Remove leading/trailing whitespace
            line = line.strip()
            # Skip empty lines
            if line:
                lines.append(line)
        return "\n".join(lines)

    def analyze_duplicates(self, scan_results: dict[str, Any]) -> dict[str, Any]:
        """Analyze scan results to categorize duplications."""
        print("🔍 Analyzing duplication patterns...")

        analysis = {
            "true_duplicates": [],
            "similar_functions": [],
            "false_duplicates": [],
            "consolidation_candidates": [],
            "risk_assessment": {},
        }

        # Analyze functions
        for hash_key, instances in scan_results["functions"].items():
            if len(instances) > 1:
                category = self._categorize_function_duplicates(instances)
                analysis[category].append(
                    {
                        "hash": hash_key,
                        "instances": instances,
                        "similarity_score": self._calculate_similarity(instances),
                    }
                )

        # Analyze classes
        for hash_key, instances in scan_results["classes"].items():
            if len(instances) > 1:
                category = self._categorize_class_duplicates(instances)
                analysis[category].append(
                    {
                        "hash": hash_key,
                        "instances": instances,
                        "similarity_score": self._calculate_similarity(instances),
                    }
                )

        # Generate consolidation plan
        analysis["consolidation_plan"] = self._generate_consolidation_plan(analysis)

        return analysis

    def _categorize_function_duplicates(self, instances: list[dict]) -> str:
        """Categorize function duplicates."""
        if len(instances) < 2:
            return "false_duplicates"

        # Check if functions have different purposes (false duplicates)
        names = [inst["name"] for inst in instances]
        files = [inst["file"] for inst in instances]

        # Same name in different modules might be different functions
        if len(set(names)) == 1 and len(set(files)) > 1:
            # Check if they're in different domains
            domains = [self._get_file_domain(f) for f in files]
            if len(set(domains)) > 1:
                return "false_duplicates"

        # Check content similarity
        contents = [inst["content"] for inst in instances]
        if self._are_contents_identical(contents):
            return "true_duplicates"
        elif self._are_contents_similar(contents):
            return "similar_functions"
        else:
            return "false_duplicates"

    def _categorize_class_duplicates(self, instances: list[dict]) -> str:
        """Categorize class duplicates."""
        if len(instances) < 2:
            return "false_duplicates"

        # Check if classes serve different purposes
        names = [inst["name"] for inst in instances]
        if len(set(names)) == 1:
            files = [inst["file"] for inst in instances]
            domains = [self._get_file_domain(f) for f in files]
            if len(set(domains)) > 1:
                return "false_duplicates"

        return "true_duplicates"  # Classes are usually more distinct

    def _get_file_domain(self, file_path: str) -> str:
        """Get the domain/module category of a file."""
        path_parts = file_path.split("/")
        if len(path_parts) >= 2:
            return path_parts[1]  # e.g., 'services', 'core', 'web'
        return "unknown"

    def _are_contents_identical(self, contents: list[str]) -> bool:
        """Check if contents are identical."""
        if not contents:
            return False
        first = contents[0]
        return all(content == first for content in contents)

    def _are_contents_similar(self, contents: list[str]) -> bool:
        """Check if contents are similar (but not identical)."""
        if len(contents) < 2:
            return False

        # Use sequence matcher for similarity
        for i in range(len(contents)):
            for j in range(i + 1, len(contents)):
                similarity = difflib.SequenceMatcher(None, contents[i], contents[j]).ratio()
                if similarity > 0.8:  # 80% similar
                    return True
        return False

    def _calculate_similarity(self, instances: list[dict]) -> float:
        """Calculate average similarity between instances."""
        if len(instances) < 2:
            return 1.0

        contents = [inst["content"] for inst in instances]
        similarities = []

        for i in range(len(contents)):
            for j in range(i + 1, len(contents)):
                similarity = difflib.SequenceMatcher(None, contents[i], contents[j]).ratio()
                similarities.append(similarity)

        return sum(similarities) / len(similarities) if similarities else 1.0

    def _generate_consolidation_plan(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Generate detailed consolidation plan."""
        plan = {
            "safe_consolidations": [],
            "risky_consolidations": [],
            "manual_review_required": [],
            "estimated_effort": {},
            "risk_assessment": {},
        }

        # Process true duplicates (safest)
        for duplicate in analysis["true_duplicates"]:
            instances = duplicate["instances"]
            if len(instances) >= 2:
                consolidation = {
                    "type": "exact_duplicate",
                    "target_file": self._choose_target_file(instances),
                    "source_files": [inst["file"] for inst in instances],
                    "function_class": instances[0]["name"],
                    "risk_level": "LOW",
                    "effort": "SMALL",
                }
                plan["safe_consolidations"].append(consolidation)

        # Process similar functions (medium risk)
        for similar in analysis["similar_functions"]:
            instances = similar["instances"]
            if len(instances) >= 2:
                consolidation = {
                    "type": "similar_function",
                    "target_file": self._choose_target_file(instances),
                    "source_files": [inst["file"] for inst in instances],
                    "function_class": instances[0]["name"],
                    "similarity_score": similar["similarity_score"],
                    "risk_level": "MEDIUM",
                    "effort": "MEDIUM",
                }
                plan["risky_consolidations"].append(consolidation)

        # Process false duplicates (manual review)
        for false_dup in analysis["false_duplicates"]:
            instances = false_dup["instances"]
            if len(instances) >= 2:
                review_item = {
                    "type": "potential_false_duplicate",
                    "files": [inst["file"] for inst in instances],
                    "function_class": instances[0]["name"],
                    "domains": list({self._get_file_domain(inst["file"]) for inst in instances}),
                    "reason": "Different domains or purposes despite similar code",
                }
                plan["manual_review_required"].append(review_item)

        return plan

    def _choose_target_file(self, instances: list[dict]) -> str:
        """Choose the best target file for consolidation."""
        # Prefer files in core modules, then services, etc.
        priority_order = ["core", "services", "utils", "web", "tests"]

        for domain in priority_order:
            for instance in instances:
                if domain in instance["file"]:
                    return instance["file"]

        # Default to first instance
        return instances[0]["file"]

    def generate_report(self, scan_results: dict[str, Any], analysis: dict[str, Any]) -> str:
        """Generate comprehensive duplication analysis report."""
        report = []
        report.append("# 🔍 DUPLICATION ANALYSIS REPORT")
        report.append(f"**Generated:** {__import__('datetime').datetime.now().isoformat()}")
        report.append("")

        # Summary
        summary = scan_results["summary"]
        report.append("## 📊 SCAN SUMMARY")
        report.append(f"- Total Python files: {summary['total_files']}")
        report.append(f"- Files processed: {summary['processed_files']}")
        report.append(f"- Function groups found: {summary['function_groups']}")
        report.append(f"- Class groups found: {summary['class_groups']}")
        report.append(f"- Potential duplicates: {summary['potential_duplicates']}")
        report.append("")

        # Detailed Analysis
        report.append("## 🔍 DETAILED ANALYSIS")
        report.append(
            f"- **True Duplicates:** {len(analysis['true_duplicates'])} (SAFE to consolidate)"
        )
        report.append(
            f"- **Similar Functions:** {len(analysis['similar_functions'])} (REVIEW required)"
        )
        report.append(f"- **False Duplicates:** {len(analysis['false_duplicates'])} (DO NOT touch)")
        report.append("")

        # Consolidation Plan
        plan = analysis["consolidation_plan"]
        report.append("## 🎯 CONSOLIDATION PLAN")
        report.append(f"- **Safe Consolidations:** {len(plan['safe_consolidations'])}")
        report.append(f"- **Risky Consolidations:** {len(plan['risky_consolidations'])}")
        report.append(f"- **Manual Review Required:** {len(plan['manual_review_required'])}")
        report.append("")

        # Safe Consolidations
        if plan["safe_consolidations"]:
            report.append("### ✅ SAFE CONSOLIDATIONS (LOW RISK)")
            for i, consolidation in enumerate(plan["safe_consolidations"][:10], 1):  # Show first 10
                report.append(f"{i}. **{consolidation['function_class']}**")
                report.append(f"   - Target: `{consolidation['target_file']}`")
                report.append(f"   - Sources: {len(consolidation['source_files'])} files")
                report.append(f"   - Risk: {consolidation['risk_level']}")
                report.append("")

        # Risky Consolidations
        if plan["risky_consolidations"]:
            report.append("### ⚠️ RISKY CONSOLIDATIONS (REVIEW REQUIRED)")
            for i, consolidation in enumerate(plan["risky_consolidations"][:5], 1):  # Show first 5
                report.append(f"{i}. **{consolidation['function_class']}**")
                report.append(f"   - Similarity: {consolidation['similarity_score']:.1%}")
                report.append(f"   - Files: {len(consolidation['source_files'])}")
                report.append(f"   - Risk: {consolidation['risk_level']}")
                report.append("")

        # Manual Review Items
        if plan["manual_review_required"]:
            report.append("### 🤔 MANUAL REVIEW REQUIRED")
            for i, item in enumerate(plan["manual_review_required"][:5], 1):  # Show first 5
                report.append(f"{i}. **{item['function_class']}**")
                report.append(f"   - Domains: {', '.join(item['domains'])}")
                report.append(f"   - Reason: {item['reason']}")
                report.append("")

        # Recommendations
        report.append("## 🎯 RECOMMENDATIONS")
        report.append("1. **Start with Safe Consolidations** - Low risk, immediate benefits")
        report.append("2. **Review Risky Consolidations Carefully** - Manual verification required")
        report.append(
            "3. **Leave False Duplicates Alone** - Different purposes despite similar code"
        )
        report.append("4. **Test After Each Consolidation** - Use verification tools")
        report.append("5. **Maintain Rollback Capability** - Keep consolidation-safety-net branch")

        return "\n".join(report)


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Duplication Analysis Tool")
    parser.add_argument("--scan", action="store_true", help="Scan codebase for duplications")
    parser.add_argument("--analyze-function", help="Analyze specific function")
    parser.add_argument("--find-true-duplicates", action="store_true", help="Find exact duplicates")
    parser.add_argument(
        "--generate-consolidation-plan", action="store_true", help="Generate consolidation plan"
    )
    parser.add_argument("--comprehensive", action="store_true", help="Run comprehensive analysis")

    args = parser.parse_args()

    analyzer = DuplicationAnalyzer()

    if args.scan:
        results = analyzer.scan_codebase()
        print(
            f"✅ Scan complete: {results['summary']['potential_duplicates']} potential duplicates found"
        )

    elif args.comprehensive:
        print("🔍 Running comprehensive duplication analysis...")
        scan_results = analyzer.scan_codebase()
        analysis = analyzer.analyze_duplicates(scan_results)

        # Generate report
        report = analyzer.generate_report(scan_results, analysis)

        # Save report
        report_file = project_root / "duplication_analysis_report.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        print("✅ Comprehensive analysis complete")
        print(f"📄 Report saved to: {report_file}")

        # Print summary
        plan = analysis["consolidation_plan"]
        print("\n📊 SUMMARY:")
        print(f"   Safe consolidations: {len(plan['safe_consolidations'])}")
        print(f"   Risky consolidations: {len(plan['risky_consolidations'])}")
        print(f"   Manual reviews needed: {len(plan['manual_review_required'])}")

    else:
        print("Usage:")
        print("  python tools/duplication_analyzer.py --scan")
        print("  python tools/duplication_analyzer.py --comprehensive")


if __name__ == "__main__":
    main()
