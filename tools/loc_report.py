#!/usr/bin/env python3
"""
File/LOC Metrics Tracker
========================

Tracks file count and lines of code to monitor consolidation progress
toward ~500 file target.

V2 Compliance: ≤400 lines, focused metrics tool
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

from pathlib import Path


def count_files_and_loc(root_dir: str = ".") -> tuple[int, int, dict[str, int]]:
    """
    Count Python files and lines of code, excluding backup directories.

    Args:
        root_dir: Root directory to scan

    Returns:
        Tuple of (file_count, total_loc, file_type_counts)
    """
    root = Path(root_dir).resolve()
    files = 0
    loc = 0
    file_types = {}

    # Exclude backup directories and common non-source directories
    exclude_dirs = {
        "runtime/consolidation/backups",
        "__pycache__",
        ".git",
        "node_modules",
        ".pytest_cache",
        "venv",
        "env",
        ".venv",
    }

    for py_file in root.rglob("*.py"):
        # Skip if in excluded directory
        if any(excluded in str(py_file) for excluded in exclude_dirs):
            continue

        files += 1

        try:
            with open(py_file, encoding="utf-8", errors="ignore") as f:
                file_loc = sum(1 for _ in f)
                loc += file_loc

                # Track by directory type
                rel_path = py_file.relative_to(root)
                if "src/" in str(rel_path):
                    file_types["src"] = file_types.get("src", 0) + 1
                elif "tools/" in str(rel_path):
                    file_types["tools"] = file_types.get("tools", 0) + 1
                elif "tests/" in str(rel_path):
                    file_types["tests"] = file_types.get("tests", 0) + 1
                else:
                    file_types["root"] = file_types.get("root", 0) + 1

        except Exception as e:
            print(f"Warning: Could not read {py_file}: {e}")

    return files, loc, file_types


def count_markdown_files(root_dir: str = ".") -> int:
    """Count markdown documentation files."""
    root = Path(root_dir).resolve()
    md_files = 0

    exclude_dirs = {"runtime/consolidation/backups", ".git", "node_modules"}

    for md_file in root.rglob("*.md"):
        if any(excluded in str(md_file) for excluded in exclude_dirs):
            continue
        md_files += 1

    return md_files


def print_metrics_report(files: int, loc: int, file_types: dict[str, int], md_files: int) -> None:
    """Print formatted metrics report."""
    print("=" * 60)
    print("CONSOLIDATION METRICS REPORT")
    print("=" * 60)
    print(f"Python Files: {files}")
    print(f"Total LOC: {loc:,}")
    print(f"Markdown Files: {md_files}")
    print(f"Total Files: {files + md_files}")
    print()
    print("File Distribution:")
    for file_type, count in sorted(file_types.items()):
        print(f"  {file_type}/: {count}")
    print()

    # Progress toward target
    target_files = 500
    current_total = files + md_files
    reduction_needed = current_total - target_files
    reduction_percent = (reduction_needed / current_total) * 100 if current_total > 0 else 0

    print(f"Target: ~{target_files} files")
    print(f"Current: {current_total} files")
    print(f"Reduction needed: {reduction_needed} files ({reduction_percent:.1f}%)")
    print("=" * 60)


def main() -> None:
    """Main entry point for metrics reporting."""
    import argparse

    parser = argparse.ArgumentParser(description="File and LOC metrics tracker")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    # Count Python files and LOC
    py_files, loc, file_types = count_files_and_loc(args.root)

    # Count markdown files
    md_files = count_markdown_files(args.root)

    if args.json:
        import json

        metrics = {
            "python_files": py_files,
            "markdown_files": md_files,
            "total_files": py_files + md_files,
            "total_loc": loc,
            "file_distribution": file_types,
            "target_files": 500,
            "reduction_needed": (py_files + md_files) - 500,
        }
        print(json.dumps(metrics, indent=2))
    else:
        print_metrics_report(py_files, loc, file_types, md_files)


if __name__ == "__main__":
    main()
