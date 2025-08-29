"""Duplication detection algorithms."""
from __future__ import annotations

import difflib
import hashlib
import logging
import os
import re
from pathlib import Path
from typing import List, Optional

from ..models import (
    DuplicationGroup,
    DuplicationInstance,
    DuplicationSeverity,
    DuplicationType,
)
from .parser import CodeParser


class DuplicationDetector:
    """Advanced duplication detection using multiple strategies."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.DuplicationDetector")
        self.parser = CodeParser()
        self.min_similarity = 0.8
        self.min_lines = 3

    def detect_duplications(self, codebase_path: str) -> List[DuplicationGroup]:
        """Detect all types of duplications in a codebase."""
        try:
            base_path = Path(codebase_path)
            if not base_path.exists():
                raise ValueError(f"Codebase path does not exist: {codebase_path}")

            source_files = self._collect_source_files(base_path)
            self.logger.info("Analyzing %d source files", len(source_files))

            duplications: List[DuplicationGroup] = []

            exact_dups = self._detect_exact_duplications(source_files)
            if exact_dups:
                duplications.append(exact_dups)

            func_dups = self._detect_function_duplications(source_files)
            if func_dups:
                duplications.append(func_dups)

            class_dups = self._detect_class_duplications(source_files)
            if class_dups:
                duplications.append(class_dups)

            pattern_dups = self._detect_pattern_duplications(source_files)
            if pattern_dups:
                duplications.append(pattern_dups)

            near_dups = self._detect_near_duplications(source_files)
            if near_dups:
                duplications.append(near_dups)

            self.logger.info("Detected %d duplication groups", len(duplications))
            return duplications
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Duplication detection failed: %s", exc)
            return []

    def _collect_source_files(self, codebase_path: Path) -> List[Path]:
        """Collect all source files under a path."""
        source_files: List[Path] = []
        try:
            for root, dirs, files in os.walk(codebase_path):
                dirs[:] = [
                    d
                    for d in dirs
                    if not d.startswith(".")
                    and d not in {"__pycache__", "node_modules", "venv", "env"}
                ]
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix in self.parser.supported_extensions:
                        source_files.append(file_path)
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to collect source files: %s", exc)
        return source_files

    def _detect_exact_duplications(
        self, source_files: List[Path]
    ) -> Optional[DuplicationGroup]:
        """Detect exact line duplications."""
        try:
            code_hashes = {}
            exact_dups: List[DuplicationInstance] = []
            for file_path in source_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        lines = content.split("\n")
                        for i, line in enumerate(lines):
                            if line.strip():
                                line_hash = hashlib.md5(line.encode()).hexdigest()
                                if line_hash in code_hashes:
                                    existing = code_hashes[line_hash]
                                    exact_dups.append(
                                        DuplicationInstance(
                                            id=f"exact_{len(exact_dups)}",
                                            duplication_type=DuplicationType.EXACT_MATCH,
                                            severity=DuplicationSeverity.LOW,
                                            similarity_score=1.0,
                                            lines_count=1,
                                            locations=[
                                                {
                                                    "file": str(existing["file"]),
                                                    "line": existing["line"],
                                                },
                                                {"file": str(file_path), "line": i + 1},
                                            ],
                                            code_snippet=line,
                                            hash_value=line_hash,
                                            metadata={"duplication_type": "exact_line"},
                                        )
                                    )
                                else:
                                    code_hashes[line_hash] = {
                                        "file": file_path,
                                        "line": i + 1,
                                    }
                except Exception as exc:  # pragma: no cover - logging
                    self.logger.warning("Failed to process %s: %s", file_path, exc)
                    continue

            if exact_dups:
                return DuplicationGroup(
                    id="exact_duplications",
                    duplication_type=DuplicationType.EXACT_MATCH,
                    instances=exact_dups,
                    total_duplication=len(exact_dups),
                    consolidation_priority=DuplicationSeverity.MEDIUM,
                    suggested_consolidation="Extract common lines into utility functions or constants",
                    estimated_effort="Low",
                    metadata={"detection_method": "hash_based"},
                )
            return None
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Exact duplication detection failed: %s", exc)
            return None

    def _detect_function_duplications(
        self, source_files: List[Path]
    ) -> Optional[DuplicationGroup]:
        """Detect duplicate function signatures."""
        try:
            function_signatures = {}
            func_dups: List[DuplicationInstance] = []
            for file_path in source_files:
                if file_path.suffix != ".py":
                    continue
                try:
                    ast_tree = self.parser.parse_file(file_path)
                    if not ast_tree:
                        continue
                    functions = self.parser.extract_functions(ast_tree)
                    for func in functions:
                        signature = (
                            f"{func['name']}_{len(func['args'])}_{func['body_lines']}"
                        )
                        sig_hash = hashlib.md5(signature.encode()).hexdigest()
                        if sig_hash in function_signatures:
                            existing = function_signatures[sig_hash]
                            func_dups.append(
                                DuplicationInstance(
                                    id=f"func_{len(func_dups)}",
                                    duplication_type=DuplicationType.FUNCTION_DUPLICATE,
                                    severity=DuplicationSeverity.HIGH,
                                    similarity_score=0.9,
                                    lines_count=func["body_lines"],
                                    locations=[
                                        {
                                            "file": str(existing["file"]),
                                            "function": existing["name"],
                                        },
                                        {
                                            "file": str(file_path),
                                            "function": func["name"],
                                        },
                                    ],
                                    code_snippet=f"Function: {func['name']}",
                                    hash_value=sig_hash,
                                    metadata={
                                        "duplication_type": "function_signature",
                                        "args_count": len(func["args"]),
                                        "body_lines": func["body_lines"],
                                    },
                                )
                            )
                        else:
                            function_signatures[sig_hash] = {
                                "file": file_path,
                                "name": func["name"],
                                "args": func["args"],
                                "body_lines": func["body_lines"],
                            }
                except Exception as exc:  # pragma: no cover - logging
                    self.logger.warning("Failed to analyze %s: %s", file_path, exc)
                    continue
            if func_dups:
                return DuplicationGroup(
                    id="function_duplications",
                    duplication_type=DuplicationType.FUNCTION_DUPLICATE,
                    instances=func_dups,
                    total_duplication=len(func_dups),
                    consolidation_priority=DuplicationSeverity.HIGH,
                    suggested_consolidation="Consolidate duplicate functions into shared utility modules",
                    estimated_effort="Medium",
                    metadata={"detection_method": "ast_analysis"},
                )
            return None
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Function duplication detection failed: %s", exc)
            return None

    def _detect_class_duplications(
        self, source_files: List[Path]
    ) -> Optional[DuplicationGroup]:
        """Detect duplicate class structures."""
        try:
            class_signatures = {}
            class_dups: List[DuplicationInstance] = []
            for file_path in source_files:
                if file_path.suffix != ".py":
                    continue
                try:
                    ast_tree = self.parser.parse_file(file_path)
                    if not ast_tree:
                        continue
                    classes = self.parser.extract_classes(ast_tree)
                    for cls in classes:
                        signature = (
                            f"{cls['name']}_{len(cls['bases'])}_{cls['methods']}"
                        )
                        sig_hash = hashlib.md5(signature.encode()).hexdigest()
                        if sig_hash in class_signatures:
                            existing = class_signatures[sig_hash]
                            class_dups.append(
                                DuplicationInstance(
                                    id=f"class_{len(class_dups)}",
                                    duplication_type=DuplicationType.CLASS_DUPLICATE,
                                    severity=DuplicationSeverity.CRITICAL,
                                    similarity_score=0.9,
                                    lines_count=cls.get("end_lineno", 0)
                                    - cls["lineno"],
                                    locations=[
                                        {
                                            "file": str(existing["file"]),
                                            "class": existing["name"],
                                        },
                                        {"file": str(file_path), "class": cls["name"]},
                                    ],
                                    code_snippet=f"Class: {cls['name']}",
                                    hash_value=sig_hash,
                                    metadata={
                                        "duplication_type": "class_structure",
                                        "bases_count": len(cls["bases"]),
                                        "methods_count": cls["methods"],
                                    },
                                )
                            )
                        else:
                            class_signatures[sig_hash] = {
                                "file": file_path,
                                "name": cls["name"],
                                "bases": cls["bases"],
                                "methods": cls["methods"],
                            }
                except Exception as exc:  # pragma: no cover - logging
                    self.logger.warning("Failed to analyze %s: %s", file_path, exc)
                    continue
            if class_dups:
                return DuplicationGroup(
                    id="class_duplications",
                    duplication_type=DuplicationType.CLASS_DUPLICATE,
                    instances=class_dups,
                    total_duplication=len(class_dups),
                    consolidation_priority=DuplicationSeverity.CRITICAL,
                    suggested_consolidation="Refactor duplicate classes using inheritance or composition",
                    estimated_effort="High",
                    metadata={"detection_method": "ast_analysis"},
                )
            return None
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Class duplication detection failed: %s", exc)
            return None

    def _detect_pattern_duplications(
        self, source_files: List[Path]
    ) -> Optional[DuplicationGroup]:
        """Detect common code patterns."""
        try:
            patterns = {}
            pattern_dups: List[DuplicationInstance] = []
            common_patterns = [
                r'def\s+\w+\s*\([^)]*\):\s*\n\s*"""[^"]*"""\s*\n\s*pass',
                r"class\s+\w+:\s*\n\s*pass",
                r"try:\s*\n\s*[^\n]*\n\sexcept\s+\w+:\s*\n\s*pass",
                r'if\s+__name__\s*==\s*["\']__main__["\']:',
                r"logging\.(basicConfig|getLogger)",
                r"@dataclass",
                r"@property",
                r"def\s+main\(\):",
                r'if\s+__name__\s*==\s*["\']__main__["\']:\s*\n\s*main\(\)',
            ]
            for file_path in source_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        for pattern in common_patterns:
                            matches = re.finditer(pattern, content, re.MULTILINE)
                            for match in matches:
                                pattern_hash = hashlib.md5(
                                    match.group().encode()
                                ).hexdigest()
                                if pattern_hash in patterns:
                                    existing = patterns[pattern_hash]
                                    pattern_dups.append(
                                        DuplicationInstance(
                                            id=f"pattern_{len(pattern_dups)}",
                                            duplication_type=DuplicationType.PATTERN_DUPLICATE,
                                            severity=DuplicationSeverity.MEDIUM,
                                            similarity_score=1.0,
                                            lines_count=len(match.group().split("\n")),
                                            locations=[
                                                {
                                                    "file": str(existing["file"]),
                                                    "line": existing["line"],
                                                },
                                                {
                                                    "file": str(file_path),
                                                    "line": content[
                                                        : match.start()
                                                    ].count("\n")
                                                    + 1,
                                                },
                                            ],
                                            code_snippet=match.group()[:100] + "...",
                                            hash_value=pattern_hash,
                                            metadata={
                                                "duplication_type": "code_pattern",
                                                "pattern": pattern,
                                            },
                                        )
                                    )
                                else:
                                    patterns[pattern_hash] = {
                                        "file": file_path,
                                        "line": content[: match.start()].count("\n")
                                        + 1,
                                        "pattern": pattern,
                                    }
                except Exception as exc:  # pragma: no cover - logging
                    self.logger.warning("Failed to process %s: %s", file_path, exc)
                    continue
            if pattern_dups:
                return DuplicationGroup(
                    id="pattern_duplications",
                    duplication_type=DuplicationType.PATTERN_DUPLICATE,
                    instances=pattern_dups,
                    total_duplication=len(pattern_dups),
                    consolidation_priority=DuplicationSeverity.MEDIUM,
                    suggested_consolidation="Extract common patterns into utility functions or decorators",
                    estimated_effort="Medium",
                    metadata={"detection_method": "regex_patterns"},
                )
            return None
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Pattern duplication detection failed: %s", exc)
            return None

    def _detect_near_duplications(
        self, source_files: List[Path]
    ) -> Optional[DuplicationGroup]:
        """Detect near-duplicate files by similarity."""
        try:
            near_dups: List[DuplicationInstance] = []
            for i, file1 in enumerate(source_files):
                for j, file2 in enumerate(source_files[i + 1 :], i + 1):
                    try:
                        similarity = self._calculate_file_similarity(file1, file2)
                        if similarity >= self.min_similarity:
                            near_dups.append(
                                DuplicationInstance(
                                    id=f"near_{len(near_dups)}",
                                    duplication_type=DuplicationType.NEAR_DUPLICATE,
                                    severity=DuplicationSeverity.HIGH,
                                    similarity_score=similarity,
                                    lines_count=self._count_file_lines(file1),
                                    locations=[
                                        {"file": str(file1)},
                                        {"file": str(file2)},
                                    ],
                                    code_snippet=f"Similarity: {similarity:.2f}",
                                    hash_value=f"near_{i}_{j}",
                                    metadata={
                                        "duplication_type": "file_similarity",
                                        "similarity_score": similarity,
                                    },
                                )
                            )
                    except Exception as exc:  # pragma: no cover - logging
                        self.logger.warning(
                            "Failed to compare %s and %s: %s", file1, file2, exc
                        )
                        continue
            if near_dups:
                return DuplicationGroup(
                    id="near_duplications",
                    duplication_type=DuplicationType.NEAR_DUPLICATE,
                    instances=near_dups,
                    total_duplication=len(near_dups),
                    consolidation_priority=DuplicationSeverity.HIGH,
                    suggested_consolidation="Refactor similar files to share common code",
                    estimated_effort="High",
                    metadata={"detection_method": "similarity_analysis"},
                )
            return None
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Near duplication detection failed: %s", exc)
            return None

    def _calculate_file_similarity(self, file1: Path, file2: Path) -> float:
        try:
            with open(file1, "r", encoding="utf-8") as f1, open(
                file2, "r", encoding="utf-8"
            ) as f2:
                content1 = f1.read()
                content2 = f2.read()
                return difflib.SequenceMatcher(None, content1, content2).ratio()
        except Exception:
            return 0.0

    def _count_file_lines(self, file_path: Path) -> int:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return len(file.readlines())
        except Exception:
            return 0
