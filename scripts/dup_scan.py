#!/usr/bin/env python3
"""
Duplication Scanner v3.1
Part of V3.1 Unified Feedback Loop
Prevents code duplication across the swarm

Deployed by Agent-5 as Integration & Tooling Specialist
"""

import argparse
import hashlib
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class DuplicationResult:
    """Represents a duplication detection result"""

    file1: str
    file2: str
    similarity_score: float
    duplicate_lines: list[int]
    duplicate_content: str
    severity: str


class DuplicationScanner:

EXAMPLE USAGE:
==============

# Run the script directly
python dup_scan.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.dup_scan import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.dup_scan import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

    """Advanced duplication scanner for swarm codebase"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.duplications: list[DuplicationResult] = []
        self.file_hashes: dict[str, str] = {}
        self.content_hashes: dict[str, list[str]] = {}

        # File extensions to scan
        self.scan_extensions = {".py", ".js", ".ts", ".md", ".json", ".yaml", ".yml"}

        # Directories to exclude
        self.exclude_dirs = {
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            "venv",
            "htmlcov",
            "coverage_reports",
            "coverage_latest",
            "coverage_baseline",
            "backup",
            "backups",
            "archive",
            "logs",
            "devlogs",
        }

        # Minimum similarity threshold
        self.similarity_threshold = 0.8

    def scan_directory(self) -> dict[str, any]:
        """Perform comprehensive duplication scan"""
        logger.info("Starting duplication scan...")

        # Phase 1: Collect all files
        files = self._collect_files()
        logger.info(f"Collected {len(files)} files for scanning")

        # Phase 2: Calculate file hashes
        self._calculate_hashes(files)

        # Phase 3: Detect exact duplicates
        exact_duplicates = self._detect_exact_duplicates()

        # Phase 4: Detect similar content
        similar_content = self._detect_similar_content()

        # Phase 5: Analyze patterns
        patterns = self._analyze_duplication_patterns()

        # Generate report
        report = self._generate_report(exact_duplicates, similar_content, patterns)

        logger.info(f"Scan complete. Found {len(self.duplications)} duplications")
        return report

    def _collect_files(self) -> list[Path]:
        """Collect all files to be scanned"""
        files = []

        for root, dirs, files_in_dir in os.walk(self.root_path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]

            for file in files_in_dir:
                file_path = Path(root) / file
                if file_path.suffix in self.scan_extensions:
                    files.append(file_path)

        return files

    def _calculate_hashes(self, files: list[Path]) -> None:
        """Calculate hashes for all files"""
        for file_path in files:
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # File hash (entire content)
                file_hash = hashlib.md5(content.encode()).hexdigest()
                self.file_hashes[str(file_path)] = file_hash

                # Content hash (for similarity detection)
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if len(line.strip()) > 10:  # Skip short lines
                        line_hash = hashlib.md5(line.encode()).hexdigest()
                        if line_hash not in self.content_hashes:
                            self.content_hashes[line_hash] = []
                        self.content_hashes[line_hash].append(f"{file_path}:{i}")

            except Exception as e:
                logger.warning(f"Error processing {file_path}: {e}")

    def _detect_exact_duplicates(self) -> list[tuple[str, str]]:
        """Detect files with identical content"""
        exact_duplicates = []
        hash_to_files = {}

        for file_path, file_hash in self.file_hashes.items():
            if file_hash in hash_to_files:
                hash_to_files[file_hash].append(file_path)
            else:
                hash_to_files[file_hash] = [file_path]

        for file_hash, files in hash_to_files.items():
            if len(files) > 1:
                for i in range(len(files)):
                    for j in range(i + 1, len(files)):
                        exact_duplicates.append((files[i], files[j]))

                        # Create duplication result
                        result = DuplicationResult(
                            file1=files[i],
                            file2=files[j],
                            similarity_score=1.0,
                            duplicate_lines=[],
                            duplicate_content="",
                            severity="critical",
                        )
                        self.duplications.append(result)

        return exact_duplicates

    def _detect_similar_content(self) -> list[tuple[str, str, float]]:
        """Detect files with similar content"""
        similar_content = []

        # Group files by similar line content
        line_groups = {}
        for line_hash, file_lines in self.content_hashes.items():
            if len(file_lines) > 1:
                files = set()
                for file_line in file_lines:
                    file_path = file_line.split(":")[0]
                    files.add(file_path)

                if len(files) > 1:
                    for file1 in files:
                        for file2 in files:
                            if file1 != file2:
                                similarity = self._calculate_similarity(file1, file2)
                                if similarity >= self.similarity_threshold:
                                    similar_content.append((file1, file2, similarity))

                                    # Create duplication result
                                    result = DuplicationResult(
                                        file1=file1,
                                        file2=file2,
                                        similarity_score=similarity,
                                        duplicate_lines=[],
                                        duplicate_content="",
                                        severity="high" if similarity > 0.9 else "medium",
                                    )
                                    self.duplications.append(result)

        return similar_content

    def _calculate_similarity(self, file1: str, file2: str) -> float:
        """Calculate similarity between two files"""
        try:
            with open(file1, encoding="utf-8", errors="ignore") as f:
                content1 = set(f.read().split("\n"))

            with open(file2, encoding="utf-8", errors="ignore") as f:
                content2 = set(f.read().split("\n"))

            if not content1 or not content2:
                return 0.0

            intersection = content1.intersection(content2)
            union = content1.union(content2)

            return len(intersection) / len(union) if union else 0.0

        except Exception as e:
            logger.warning(f"Error calculating similarity between {file1} and {file2}: {e}")
            return 0.0

    def _analyze_duplication_patterns(self) -> dict[str, any]:
        """Analyze patterns in duplications"""
        patterns = {
            "most_duplicated_files": {},
            "duplication_by_extension": {},
            "duplication_by_directory": {},
            "severity_distribution": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        }

        for dup in self.duplications:
            # Count duplications per file
            for file_path in [dup.file1, dup.file2]:
                if file_path not in patterns["most_duplicated_files"]:
                    patterns["most_duplicated_files"][file_path] = 0
                patterns["most_duplicated_files"][file_path] += 1

            # Count by extension
            ext1 = Path(dup.file1).suffix
            ext2 = Path(dup.file2).suffix
            for ext in [ext1, ext2]:
                if ext not in patterns["duplication_by_extension"]:
                    patterns["duplication_by_extension"][ext] = 0
                patterns["duplication_by_extension"][ext] += 1

            # Count by directory
            dir1 = str(Path(dup.file1).parent)
            dir2 = str(Path(dup.file2).parent)
            for dir_path in [dir1, dir2]:
                if dir_path not in patterns["duplication_by_directory"]:
                    patterns["duplication_by_directory"][dir_path] = 0
                patterns["duplication_by_directory"][dir_path] += 1

            # Count by severity
            patterns["severity_distribution"][dup.severity] += 1

        return patterns

    def _generate_report(
        self, exact_duplicates: list, similar_content: list, patterns: dict
    ) -> dict[str, any]:
        """Generate comprehensive duplication report"""
        report = {
            "scan_metadata": {
                "timestamp": datetime.now().isoformat(),
                "scanner_version": "3.1",
                "deployed_by": "Agent-5",
                "root_path": str(self.root_path),
                "total_files_scanned": len(self.file_hashes),
                "total_duplications_found": len(self.duplications),
            },
            "summary": {
                "exact_duplicates": len(exact_duplicates),
                "similar_content": len(similar_content),
                "total_duplications": len(self.duplications),
                "severity_breakdown": patterns["severity_distribution"],
            },
            "duplications": [
                {
                    "file1": dup.file1,
                    "file2": dup.file2,
                    "similarity_score": dup.similarity_score,
                    "severity": dup.severity,
                    "duplicate_lines": dup.duplicate_lines,
                    "duplicate_content": (
                        dup.duplicate_content[:200] + "..."
                        if len(dup.duplicate_content) > 200
                        else dup.duplicate_content
                    ),
                }
                for dup in self.duplications
            ],
            "patterns": patterns,
            "recommendations": self._generate_recommendations(patterns),
        }

        return report

    def _generate_recommendations(self, patterns: dict) -> list[str]:
        """Generate recommendations based on duplication patterns"""
        recommendations = []

        # Most duplicated files
        most_duplicated = sorted(
            patterns["most_duplicated_files"].items(), key=lambda x: x[1], reverse=True
        )[:5]

        if most_duplicated:
            recommendations.append(
                f"Top duplicated files: {', '.join([f'{f} ({c})' for f, c in most_duplicated])}"
            )

        # Extension-based recommendations
        if patterns["duplication_by_extension"]:
            top_ext = max(patterns["duplication_by_extension"].items(), key=lambda x: x[1])
            recommendations.append(
                f"Highest duplication in {top_ext[0]} files ({top_ext[1]} instances)"
            )

        # Directory-based recommendations
        if patterns["duplication_by_directory"]:
            top_dir = max(patterns["duplication_by_directory"].items(), key=lambda x: x[1])
            recommendations.append(
                f"Highest duplication in {top_dir[0]} directory ({top_dir[1]} instances)"
            )

        # General recommendations
        if patterns["severity_distribution"]["critical"] > 0:
            recommendations.append("CRITICAL: Remove exact duplicate files immediately")

        if patterns["severity_distribution"]["high"] > 5:
            recommendations.append("HIGH: Consider refactoring similar code into shared modules")

        recommendations.extend(
            [
                "Implement code review process to prevent future duplications",
                "Use shared libraries for common functionality",
                "Regular duplication scans should be part of CI/CD pipeline",
            ]
        )

        return recommendations

    def save_report(self, report: dict, output_file: str = "duplication_scan_report.json") -> None:
        """Save duplication report to file"""
        output_path = self.root_path / output_file

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"Duplication report saved to {output_path}")


def main():
    """Main entry point for duplication scanner"""
    parser = argparse.ArgumentParser(description="Duplication Scanner v3.1")
    parser.add_argument("--path", default=".", help="Root path to scan")
    parser.add_argument(
        "--output", default="duplication_scan_report.json", help="Output report file"
    )
    parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize scanner
    scanner = DuplicationScanner(args.path)
    scanner.similarity_threshold = args.threshold

    # Perform scan
    report = scanner.scan_directory()

    # Save report
    scanner.save_report(report, args.output)

    # Print summary
    print("\n🔍 DUPLICATION SCAN COMPLETE")
    print(f"📊 Total duplications found: {report['summary']['total_duplications']}")
    print(f"🚨 Critical: {report['summary']['severity_breakdown']['critical']}")
    print(f"⚠️  High: {report['summary']['severity_breakdown']['high']}")
    print(f"📝 Medium: {report['summary']['severity_breakdown']['medium']}")
    print(f"📄 Report saved to: {args.output}")

    # Print recommendations
    if report["recommendations"]:
        print("\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"   {i}. {rec}")


if __name__ == "__main__":
    main()
