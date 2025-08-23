#!/usr/bin/env python3
"""
Advanced Duplication Detector for Agent_Cellphone_V2_Repository
==============================================================

This tool detects various types of code duplication:
1. Exact code blocks (copy-paste)
2. Similar function/class structures
3. Duplicate imports and dependencies
4. Repeated patterns and boilerplate
5. Backup file detection

Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import ast
import hashlib
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import difflib
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class DuplicationIssue:
    """Represents a duplication issue found in the codebase"""

    issue_type: str
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    description: str
    files_involved: List[str]
    line_numbers: List[Tuple[str, int]]
    similarity_score: float
    suggested_action: str


@dataclass
class CodeBlock:
    """Represents a code block for analysis"""

    content: str
    hash: str
    file_path: str
    start_line: int
    end_line: int
    block_type: str  # 'function', 'class', 'import', 'block'
    length: int
    tokens: Set[str]


class DuplicationDetector:
    """Advanced duplication detection system"""

    def __init__(self, min_similarity: float = 0.8, min_block_size: int = 5):
        self.min_similarity = min_similarity
        self.min_block_size = min_block_size
        self.issues: List[DuplicationIssue] = []
        self.code_blocks: List[CodeBlock] = []
        self.file_hashes: Dict[str, str] = {}

    def analyze_codebase(self, root_path: str) -> List[DuplicationIssue]:
        """Analyze entire codebase for duplication issues"""
        logger.info(f"Analyzing codebase at: {root_path}")

        # Find all Python files
        python_files = list(Path(root_path).rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files")

        # Extract code blocks from all files
        for file_path in python_files:
            self._extract_code_blocks(file_path)

        # Detect various types of duplication
        self._detect_exact_duplicates()
        self._detect_similar_structures()
        self._detect_duplicate_imports()
        self._detect_backup_files()
        self._detect_repeated_patterns()
        self._detect_copy_paste_blocks()

        return self.issues

    def _extract_code_blocks(self, file_path: Path) -> None:
        """Extract code blocks from a Python file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse Python AST
            try:
                tree = ast.parse(content)
                self._extract_from_ast(tree, file_path, content)
            except SyntaxError:
                logger.warning(f"Syntax error in {file_path}, skipping AST analysis")
                self._extract_manual_blocks(file_path, content)

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    def _extract_from_ast(self, tree: ast.AST, file_path: Path, content: str) -> None:
        """Extract code blocks using AST analysis"""
        lines = content.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # Extract function/class block
                start_line = node.lineno - 1
                end_line = (
                    node.end_lineno if hasattr(node, "end_lineno") else start_line + 1
                )

                block_content = "\n".join(lines[start_line:end_line])
                block_hash = hashlib.md5(block_content.encode()).hexdigest()

                block_type = (
                    "function"
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    else "class"
                )
                tokens = set(re.findall(r"\w+", block_content))

                self.code_blocks.append(
                    CodeBlock(
                        content=block_content,
                        hash=block_hash,
                        file_path=str(file_path),
                        start_line=start_line + 1,
                        end_line=end_line,
                        block_type=block_type,
                        length=end_line - start_line,
                        tokens=tokens,
                    )
                )

    def _extract_manual_blocks(self, file_path: Path, content: str) -> None:
        """Extract code blocks manually when AST parsing fails"""
        lines = content.split("\n")

        # Extract import blocks
        import_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith(("import ", "from ")):
                import_lines.append((i, line))

        if import_lines:
            start_line = import_lines[0][0]
            end_line = import_lines[-1][0] + 1
            import_content = "\n".join(lines[start_line:end_line])
            tokens = set(re.findall(r"\w+", import_content))

            self.code_blocks.append(
                CodeBlock(
                    content=import_content,
                    hash=hashlib.md5(import_content.encode()).hexdigest(),
                    file_path=str(file_path),
                    start_line=start_line + 1,
                    end_line=end_line,
                    block_type="import",
                    length=end_line - start_line,
                    tokens=tokens,
                )
            )

    def _detect_exact_duplicates(self) -> None:
        """Detect exact duplicate code blocks"""
        hash_groups = defaultdict(list)

        for block in self.code_blocks:
            hash_groups[block.hash].append(block)

        for hash_val, blocks in hash_groups.items():
            if len(blocks) > 1:
                # Check if it's not just a common pattern (like simple getters)
                if len(blocks[0].content.strip()) > 50:  # Ignore very short blocks
                    files = [block.file_path for block in blocks]
                    line_numbers = [
                        (block.file_path, block.start_line) for block in blocks
                    ]

                    self.issues.append(
                        DuplicationIssue(
                            issue_type="EXACT_DUPLICATE",
                            severity="HIGH",
                            description=f"Exact duplicate code block found in {len(blocks)} files",
                            files_involved=files,
                            line_numbers=line_numbers,
                            similarity_score=1.0,
                            suggested_action="Extract to shared utility module",
                        )
                    )

    def _detect_similar_structures(self) -> None:
        """Detect similar function/class structures"""
        # Group by block type
        functions = [b for b in self.code_blocks if b.block_type == "function"]
        classes = [b for b in self.code_blocks if b.block_type == "class"]

        # Check for similar function structures
        self._check_similar_functions(functions)

        # Check for similar class structures
        self._check_similar_classes(classes)

    def _check_similar_functions(self, functions: List[CodeBlock]) -> None:
        """Check for similar function structures"""
        functions.sort(key=lambda b: b.length)
        for i, func1 in enumerate(functions):
            for func2 in functions[i + 1 :]:
                if func2.length - func1.length > max(func1.length, func2.length) * 0.3:
                    break
                if (
                    self._token_similarity(func1.tokens, func2.tokens)
                    < self.min_similarity
                ):
                    continue
                similarity = self._calculate_similarity(func1.content, func2.content)
                if similarity > self.min_similarity:
                    self.issues.append(
                        DuplicationIssue(
                            issue_type="SIMILAR_FUNCTION",
                            severity="MEDIUM",
                            description="Similar function structures detected",
                            files_involved=[func1.file_path, func2.file_path],
                            line_numbers=[
                                (func1.file_path, func1.start_line),
                                (func2.file_path, func2.start_line),
                            ],
                            similarity_score=similarity,
                            suggested_action="Consider creating a base function or using inheritance",
                        )
                    )

    def _check_similar_classes(self, classes: List[CodeBlock]) -> None:
        """Check for similar class structures"""
        classes.sort(key=lambda b: b.length)
        for i, class1 in enumerate(classes):
            for class2 in classes[i + 1 :]:
                if (
                    class2.length - class1.length
                    > max(class1.length, class2.length) * 0.3
                ):
                    break
                if (
                    self._token_similarity(class1.tokens, class2.tokens)
                    < self.min_similarity
                ):
                    continue
                similarity = self._calculate_similarity(class1.content, class2.content)
                if similarity > self.min_similarity:
                    self.issues.append(
                        DuplicationIssue(
                            issue_type="SIMILAR_CLASS",
                            severity="MEDIUM",
                            description="Similar class structures detected",
                            files_involved=[class1.file_path, class2.file_path],
                            line_numbers=[
                                (class1.file_path, class1.start_line),
                                (class2.file_path, class2.start_line),
                            ],
                            similarity_score=similarity,
                            suggested_action="Consider creating a base class or using composition",
                        )
                    )

    def _detect_duplicate_imports(self) -> None:
        """Detect duplicate import statements across files"""
        import_blocks = [b for b in self.code_blocks if b.block_type == "import"]

        # Extract import statements
        all_imports = []
        for block in import_blocks:
            imports = [
                line.strip()
                for line in block.content.split("\n")
                if line.strip().startswith(("import ", "from "))
            ]
            all_imports.extend(imports)

        # Find duplicates
        import_counter = Counter(all_imports)
        duplicates = {imp: count for imp, count in import_counter.items() if count > 1}

        if duplicates:
            self.issues.append(
                DuplicationIssue(
                    issue_type="DUPLICATE_IMPORTS",
                    severity="LOW",
                    description=f"Duplicate import statements found: {len(duplicates)} imports",
                    files_involved=list(
                        set(block.file_path for block in import_blocks)
                    ),
                    line_numbers=[
                        (block.file_path, block.start_line) for block in import_blocks
                    ],
                    similarity_score=1.0,
                    suggested_action="Consolidate imports in shared modules",
                )
            )

    def _detect_backup_files(self) -> None:
        """Detect backup files in the codebase"""
        backup_patterns = [".backup", ".bak", ".old", ".orig", ".tmp"]

        for pattern in backup_patterns:
            backup_files = list(Path(".").rglob(f"*{pattern}*"))
            if backup_files:
                self.issues.append(
                    DuplicationIssue(
                        issue_type="BACKUP_FILES",
                        severity="CRITICAL",
                        description=f"Backup files detected with pattern: {pattern}",
                        files_involved=[str(f) for f in backup_files],
                        line_numbers=[(str(f), 0) for f in backup_files],
                        similarity_score=1.0,
                        suggested_action="Remove backup files from repository",
                    )
                )

    def _detect_repeated_patterns(self) -> None:
        """Detect repeated code patterns within files"""
        for block in self.code_blocks:
            if block.length > self.min_block_size:
                lines = block.content.split("\n")
                max_size = min(10, len(lines) // 2)
                for pattern_size in range(3, max_size):
                    counts = defaultdict(int)
                    found = False
                    for i in range(len(lines) - pattern_size + 1):
                        pattern = "\n".join(lines[i : i + pattern_size])
                        pattern_hash = hashlib.md5(pattern.encode()).hexdigest()
                        counts[pattern_hash] += 1
                        if counts[pattern_hash] == 3:
                            self.issues.append(
                                DuplicationIssue(
                                    issue_type="REPEATED_PATTERN",
                                    severity="MEDIUM",
                                    description=f"Repeated code pattern ({pattern_size} lines) found 3 times or more",
                                    files_involved=[block.file_path],
                                    line_numbers=[
                                        (block.file_path, block.start_line + i)
                                    ],
                                    similarity_score=1.0,
                                    suggested_action="Extract repeated pattern to function or constant",
                                )
                            )
                            found = True
                            break
                    if found:
                        break

    def _detect_copy_paste_blocks(self) -> None:
        """Detect potential copy-paste blocks using similarity analysis"""
        blocks = sorted(self.code_blocks, key=lambda b: b.length)
        for i, block1 in enumerate(blocks):
            if block1.length <= 10:
                continue
            for block2 in blocks[i + 1 :]:
                if (
                    block2.length - block1.length
                    > max(block1.length, block2.length) * 0.3
                ):
                    break
                if block1.file_path == block2.file_path:
                    continue
                if self._token_similarity(block1.tokens, block2.tokens) < 0.5:
                    continue
                similarity = self._calculate_similarity(block1.content, block2.content)
                if similarity > 0.9:
                    self.issues.append(
                        DuplicationIssue(
                            issue_type="COPY_PASTE",
                            severity="HIGH",
                            description=f"Potential copy-paste detected (similarity: {similarity:.2f})",
                            files_involved=[block1.file_path, block2.file_path],
                            line_numbers=[
                                (block1.file_path, block1.start_line),
                                (block2.file_path, block2.start_line),
                            ],
                            similarity_score=similarity,
                            suggested_action="Refactor to eliminate duplication",
                        )
                    )

    def _token_similarity(self, tokens1: Set[str], tokens2: Set[str]) -> float:
        """Quick token-based similarity check"""
        if not tokens1 or not tokens2:
            return 0.0
        return len(tokens1 & tokens2) / len(tokens1 | tokens2)

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text blocks"""
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    def generate_report(self) -> str:
        """Generate a comprehensive duplication report"""
        if not self.issues:
            return "✅ No duplication issues found!"

        # Group issues by severity
        issues_by_severity = defaultdict(list)
        for issue in self.issues:
            issues_by_severity[issue.severity].append(issue)

        report = []
        report.append("🚨 DUPLICATION DETECTION REPORT")
        report.append("=" * 50)
        report.append(f"Total Issues Found: {len(self.issues)}")
        report.append("")

        # Report by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if severity in issues_by_severity:
                issues = issues_by_severity[severity]
                report.append(f"{severity} Issues ({len(issues)}):")
                report.append("-" * 30)

                for issue in issues:
                    report.append(f"• {issue.issue_type}: {issue.description}")
                    report.append(f"  Files: {', '.join(issue.files_involved)}")
                    report.append(f"  Action: {issue.suggested_action}")
                    report.append("")

        return "\n".join(report)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Advanced Duplication Detector for Agent_Cellphone_V2_Repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python tools/duplication_detector.py                    # Analyze current directory
    python tools/duplication_detector.py --path src/        # Analyze specific directory
    python tools/duplication_detector.py --min-similarity 0.9  # Higher similarity threshold
    python tools/duplication_detector.py --export report.txt  # Export report to file
        """,
    )

    parser.add_argument(
        "--path", default=".", help="Path to analyze (default: current directory)"
    )
    parser.add_argument(
        "--min-similarity",
        type=float,
        default=0.8,
        help="Minimum similarity threshold (default: 0.8)",
    )
    parser.add_argument(
        "--min-block-size",
        type=int,
        default=5,
        help="Minimum block size to analyze (default: 5 lines)",
    )
    parser.add_argument("--export", type=str, help="Export report to file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize detector
    detector = DuplicationDetector(
        min_similarity=args.min_similarity, min_block_size=args.min_block_size
    )

    # Analyze codebase
    print(f"🔍 Analyzing codebase at: {args.path}")
    issues = detector.analyze_codebase(args.path)

    # Generate report
    report = detector.generate_report()

    # Output report
    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"📄 Report exported to: {args.export}")
    else:
        print(report)

    # Exit with appropriate code
    critical_issues = len([i for i in issues if i.severity == "CRITICAL"])
    high_issues = len([i for i in issues if i.severity == "HIGH"])

    if critical_issues > 0:
        print(
            f"\n❌ {critical_issues} critical issues found - immediate action required!"
        )
        sys.exit(1)
    elif high_issues > 0:
        print(f"\n⚠️ {high_issues} high-severity issues found - address soon!")
        sys.exit(1)
    else:
        print(f"\n✅ Analysis complete - {len(issues)} issues found")
        sys.exit(0)


if __name__ == "__main__":
    main()

