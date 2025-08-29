"""Core models and analysis logic for the Intelligent Reviewer."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import ast
import re

from .intelligent_review_config import SECURITY_PATTERNS, QUALITY_PATTERNS


@dataclass
class ReviewIssue:
    """A code review issue."""

    severity: str
    category: str
    title: str
    description: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None
    cwe_id: Optional[str] = None
    fix_priority: str = "medium"


@dataclass
class CodeReview:
    """Complete code review results."""

    file_path: str
    review_date: datetime
    overall_score: float
    issues: List[ReviewIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    ai_insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SecurityVulnerability:
    """Security vulnerability information."""

    vulnerability_type: str
    description: str
    severity: str
    cwe_id: str
    affected_code: str
    remediation: str
    references: List[str] = field(default_factory=list)


class ReviewCore:
    """Core analysis engine for the Intelligent Reviewer."""

    def __init__(self) -> None:
        self.security_patterns = SECURITY_PATTERNS
        self.quality_patterns = QUALITY_PATTERNS

    # Security -----------------------------------------------------------------
    def security_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code for security vulnerabilities."""
        issues: List[ReviewIssue] = []
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            for vuln_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(
                            ReviewIssue(
                                severity="high"
                                if vuln_type in ["sql_injection", "command_injection"]
                                else "medium",
                                category="security",
                                title=f"Potential {vuln_type.replace('_', ' ').title()}",
                                description=f"Detected potential {vuln_type} vulnerability",
                                line_number=line_num,
                                code_snippet=line.strip(),
                                suggestion=f"Use parameterized queries or input validation to prevent {vuln_type}",
                                cwe_id=self.get_cwe_id(vuln_type),
                                fix_priority="high",
                            )
                        )

        if "import os" in content and "os.system" in content:
            issues.append(
                ReviewIssue(
                    severity="high",
                    category="security",
                    title="Command Execution Risk",
                    description="Direct command execution can lead to command injection",
                    suggestion="Use subprocess with proper argument handling",
                    cwe_id="CWE-78",
                    fix_priority="high",
                )
            )

        if "eval(" in content:
            issues.append(
                ReviewIssue(
                    severity="critical",
                    category="security",
                    title="Eval Usage",
                    description="eval() can execute arbitrary code",
                    suggestion="Avoid eval(), use safer alternatives like ast.literal_eval()",
                    cwe_id="CWE-95",
                    fix_priority="critical",
                )
            )

        return issues

    # Quality ------------------------------------------------------------------
    def quality_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code quality."""
        issues: List[ReviewIssue] = []
        lines = content.split("\n")

        if file_path.suffix.lower() == ".py":
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if len(node.body) > 20:
                            issues.append(
                                ReviewIssue(
                                    severity="medium",
                                    category="maintainability",
                                    title="Long Function",
                                    description=f"Function '{node.name}' is {len(node.body)} lines long",
                                    suggestion="Consider breaking into smaller functions",
                                    fix_priority="medium",
                                )
                            )
                        if len(node.args.args) > 5:
                            issues.append(
                                ReviewIssue(
                                    severity="low",
                                    category="maintainability",
                                    title="Too Many Parameters",
                                    description=f"Function '{node.name}' has {len(node.args.args)} parameters",
                                    suggestion="Consider using a configuration object or data class",
                                    fix_priority="low",
                                )
                            )
            except SyntaxError:
                pass

        for line_num, line in enumerate(lines, 1):
            magic_numbers = re.findall(r"\b\d{3,}\b", line)
            for number in magic_numbers:
                if int(number) > 999:
                    issues.append(
                        ReviewIssue(
                            severity="low",
                            category="style",
                            title="Magic Number",
                            description=f"Large magic number: {number}",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            suggestion="Define as a named constant",
                            fix_priority="low",
                        )
                    )

        for line_num, line in enumerate(lines, 1):
            if len(line.strip()) > 100:
                issues.append(
                    ReviewIssue(
                        severity="low",
                        category="style",
                        title="Long Line",
                        description="Line exceeds recommended length",
                        line_number=line_num,
                        code_snippet=line.strip()[:50] + "...",
                        suggestion="Break into multiple lines or extract to variable",
                        fix_priority="low",
                    )
                )

        return issues

    # Style --------------------------------------------------------------------
    def style_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code style and formatting."""
        issues: List[ReviewIssue] = []
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            if line.strip() and not line.startswith("#"):
                if "\t" in line and " " in line[: len(line) - len(line.lstrip())]:
                    issues.append(
                        ReviewIssue(
                            severity="low",
                            category="style",
                            title="Mixed Indentation",
                            description="Mixed tabs and spaces in indentation",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            suggestion="Use consistent indentation (spaces recommended)",
                            fix_priority="low",
                        )
                    )

        for line_num, line in enumerate(lines, 1):
            if line.rstrip() != line:
                issues.append(
                    ReviewIssue(
                        severity="low",
                        category="style",
                        title="Trailing Whitespace",
                        description="Line has trailing whitespace",
                        line_number=line_num,
                        code_snippet=line.strip(),
                        suggestion="Remove trailing whitespace",
                        fix_priority="low",
                    )
                )

        for line_num, line in enumerate(lines, 1):
            if re.search(r"[a-zA-Z0-9_]\s*[+\-*/=<>!]\s*[a-zA-Z0-9_]", line):
                if not re.search(r"[a-zA-Z0-9_]\s+[+\-*/=<>!]\s+[a-zA-Z0-9_]", line):
                    issues.append(
                        ReviewIssue(
                            severity="low",
                            category="style",
                            title="Operator Spacing",
                            description="Inconsistent spacing around operators",
                            line_number=line_num,
                            code_snippet=line.strip(),
                            suggestion="Add consistent spacing around operators",
                            fix_priority="low",
                        )
                    )

        return issues

    # Maintainability ---------------------------------------------------------
    def maintainability_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code maintainability."""
        issues: List[ReviewIssue] = []

        if file_path.suffix.lower() == ".py":
            try:
                tree = ast.parse(content)
                complexity = self.calculate_cyclomatic_complexity(tree)
                if complexity > 10:
                    issues.append(
                        ReviewIssue(
                            severity="medium",
                            category="maintainability",
                            title="High Cyclomatic Complexity",
                            description=f"Cyclomatic complexity is {complexity} (recommended < 10)",
                            suggestion="Consider breaking complex logic into smaller functions",
                            fix_priority="medium",
                        )
                    )

                max_depth = self.calculate_max_nesting_depth(tree)
                if max_depth > 4:
                    issues.append(
                        ReviewIssue(
                            severity="medium",
                            category="maintainability",
                            title="Deep Nesting",
                            description=f"Maximum nesting depth is {max_depth} (recommended < 4)",
                            suggestion="Extract nested logic into separate functions",
                            fix_priority="medium",
                        )
                    )

                duplicate_patterns = self.find_duplicate_patterns(content)
                if duplicate_patterns:
                    issues.append(
                        ReviewIssue(
                            severity="low",
                            category="maintainability",
                            title="Potential Code Duplication",
                            description=f"Found {len(duplicate_patterns)} potential duplicate patterns",
                            suggestion="Consider extracting common functionality",
                            fix_priority="low",
                        )
                    )
            except SyntaxError:
                pass

        return issues

    # Documentation ------------------------------------------------------------
    def documentation_analysis(self, content: str, file_path: Path) -> List[ReviewIssue]:
        """Analyze code documentation."""
        issues: List[ReviewIssue] = []

        if file_path.suffix.lower() == ".py":
            try:
                tree = ast.parse(content)
                functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

                documented_functions = [f for f in functions if ast.get_docstring(f)]
                documented_classes = [c for c in classes if ast.get_docstring(c)]

                if functions and len(documented_functions) / len(functions) < 0.8:
                    issues.append(
                        ReviewIssue(
                            severity="low",
                            category="documentation",
                            title="Missing Function Documentation",
                            description=f"Only {len(documented_functions)}/{len(functions)} functions have docstrings",
                            suggestion="Add docstrings to all public functions",
                            fix_priority="low",
                        )
                    )

                if classes and len(documented_classes) / len(classes) < 0.8:
                    issues.append(
                        ReviewIssue(
                            severity="low",
                            category="documentation",
                            title="Missing Class Documentation",
                            description=f"Only {len(documented_classes)}/{len(classes)} classes have docstrings",
                            suggestion="Add docstrings to all classes",
                            fix_priority="low",
                        )
                    )
            except SyntaxError:
                pass

        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            match = re.search(r"\b(TODO|FIXME|XXX|HACK)\b", line, re.IGNORECASE)
            if match:
                issues.append(
                    ReviewIssue(
                        severity="medium",
                        category="documentation",
                        title="Development Note",
                        description=f"Found {match.group(1)} comment",
                        line_number=line_num,
                        code_snippet=line.strip(),
                        suggestion="Address the TODO/FIXME or remove if resolved",
                        fix_priority="medium",
                    )
                )

        return issues

    # Metrics ------------------------------------------------------------------
    def calculate_metrics(self, content: str, issues: List[ReviewIssue]) -> Dict[str, Any]:
        """Calculate code quality metrics."""
        lines = content.split("\n")
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith("#")])
        comment_lines = len([line for line in lines if line.strip().startswith("#")])

        issue_counts: Dict[str, int] = {}
        for issue in issues:
            issue_counts[issue.severity] = issue_counts.get(issue.severity, 0) + 1
            key = f"{issue.category}_total"
            issue_counts[key] = issue_counts.get(key, 0) + 1

        complexity_score = 0
        if content.strip():
            try:
                tree = ast.parse(content)
                complexity_score = self.calculate_cyclomatic_complexity(tree)
            except SyntaxError:
                complexity_score = 999

        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "comment_ratio": comment_lines / max(code_lines, 1),
            "complexity_score": complexity_score,
            "issue_counts": issue_counts,
            "security_issues": len([i for i in issues if i.category == "security"]),
            "quality_issues": len([i for i in issues if i.category in ["maintainability", "style"]]),
            "documentation_issues": len([i for i in issues if i.category == "documentation"]),
        }

    # Helpers ------------------------------------------------------------------
    def calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for Python AST."""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.Assert):
                complexity += 1
            elif isinstance(node, ast.Return):
                complexity += 1
        return complexity

    def calculate_max_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0

        def visit(node: ast.AST, depth: int) -> None:
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                    visit(child, depth + 1)
                else:
                    visit(child, depth)

        visit(tree, 0)
        return max_depth

    def find_duplicate_patterns(self, content: str) -> List[str]:
        """Find potential duplicate code patterns."""
        lines = content.split("\n")
        patterns: List[str] = []
        for i in range(len(lines) - 3):
            pattern = "\n".join(lines[i : i + 3])
            if len(pattern.strip()) > 20 and content.count(pattern) > 1:
                patterns.append(pattern[:100] + "...")
        return patterns[:5]

    def get_cwe_id(self, vulnerability_type: str) -> str:
        """Get CWE ID for vulnerability type."""
        cwe_mapping = {
            "sql_injection": "CWE-89",
            "xss": "CWE-79",
            "path_traversal": "CWE-22",
            "command_injection": "CWE-78",
        }
        return cwe_mapping.get(vulnerability_type, "CWE-000")


__all__ = [
    "ReviewIssue",
    "CodeReview",
    "SecurityVulnerability",
    "ReviewCore",
]
