#!/usr/bin/env python3
"""
LOC Report Tool
===============
Generate lines of code metrics for the repository.
"""

import os
from collections import defaultdict
from pathlib import Path


def count_lines_in_file(file_path):
    """Count lines in a single file."""
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            return len(f.readlines())
    except:
        return 0


def get_file_size(file_path):
    """Get file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except:
        return 0


def scan_directory(directory):
    """Scan directory for Python files and generate metrics."""
    stats = {
        "total_files": 0,
        "total_lines": 0,
        "total_size": 0,
        "by_directory": defaultdict(lambda: {"files": 0, "lines": 0, "size": 0}),
        "by_file_type": defaultdict(lambda: {"files": 0, "lines": 0, "size": 0}),
        "largest_files": [],
        "file_list": [],
    }

    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [
            d for d in dirs if d not in [".git", "__pycache__", "node_modules", ".venv", "venv"]
        ]

        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                relative_path = file_path.relative_to(directory)

                lines = count_lines_in_file(file_path)
                size = get_file_size(file_path)

                stats["total_files"] += 1
                stats["total_lines"] += lines
                stats["total_size"] += size

                # Directory stats
                dir_name = (
                    str(relative_path.parent) if relative_path.parent != Path(".") else "root"
                )
                stats["by_directory"][dir_name]["files"] += 1
                stats["by_directory"][dir_name]["lines"] += lines
                stats["by_directory"][dir_name]["size"] += size

                # File type stats (by directory pattern)
                if "src/v3" in str(relative_path):
                    file_type = "v3"
                elif "src/services" in str(relative_path):
                    file_type = "services"
                elif "src/core" in str(relative_path):
                    file_type = "core"
                elif "tools" in str(relative_path):
                    file_type = "tools"
                elif "tests" in str(relative_path):
                    file_type = "tests"
                else:
                    file_type = "other"

                stats["by_file_type"][file_type]["files"] += 1
                stats["by_file_type"][file_type]["lines"] += lines
                stats["by_file_type"][file_type]["size"] += size

                # Track largest files
                stats["largest_files"].append((str(relative_path), lines, size))
                stats["file_list"].append((str(relative_path), lines, size))

    # Sort largest files
    stats["largest_files"].sort(key=lambda x: x[1], reverse=True)

    return stats


def print_report(stats):
    """Print formatted report."""
    print("=" * 60)
    print("LINES OF CODE REPORT")
    print("=" * 60)
    print(f"Total Python files: {stats['total_files']}")
    print(f"Total lines of code: {stats['total_lines']:,}")
    print(f"Total size: {stats['total_size'] / (1024*1024):.2f} MB")
    print()

    print("BY FILE TYPE:")
    print("-" * 30)
    for file_type, data in sorted(stats["by_file_type"].items()):
        pct_files = (data["files"] / stats["total_files"]) * 100
        pct_lines = (data["lines"] / stats["total_lines"]) * 100
        print(
            f"{file_type:10} | {data['files']:3} files ({pct_files:4.1f}%) | {data['lines']:6,} lines ({pct_lines:4.1f}%)"
        )
    print()

    print("BY DIRECTORY (top 15):")
    print("-" * 50)
    sorted_dirs = sorted(stats["by_directory"].items(), key=lambda x: x[1]["lines"], reverse=True)
    for dir_name, data in sorted_dirs[:15]:
        pct_lines = (data["lines"] / stats["total_lines"]) * 100
        print(f"{dir_name:40} | {data['lines']:6,} lines ({pct_lines:4.1f}%)")
    print()

    print("LARGEST FILES (top 10):")
    print("-" * 50)
    for file_path, lines, size in stats["largest_files"][:10]:
        print(f"{file_path:45} | {lines:6,} lines | {size/1024:.1f} KB")
    print()


def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    stats = scan_directory(project_root)
    print_report(stats)

    # Also write to file for comparison
    import json

    output_file = project_root / "runtime" / "consolidation" / "loc_report.json"
    with open(output_file, "w") as f:
        json.dump({"timestamp": str(Path().cwd()), "stats": dict(stats)}, f, indent=2, default=str)

    print(f"Detailed report saved to: {output_file}")


if __name__ == "__main__":
    main()
