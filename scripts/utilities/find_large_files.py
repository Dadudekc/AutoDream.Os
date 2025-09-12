#!/usr/bin/env python3
"""Find Python files exceeding line limits."""


def find_large_python_files(directory="src", min_lines=400):

EXAMPLE USAGE:
==============

# Run the script directly
python find_large_files.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.utilities.find_large_files import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.utilities.find_large_files import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

    """Find Python files exceeding the specified line count."""
    large_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = get_unified_utility().path.join(root, file)
                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        line_count = sum(1 for line in f)
                        if line_count > min_lines:
                            large_files.append((file_path, line_count))
                except Exception as e:
                    get_logger(__name__).info(f"Error reading {file_path}: {e}")

    return sorted(large_files, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    get_logger(__name__).info("Python files over 400 lines:")
    large_files = find_large_python_files()

    for file_path, line_count in large_files[:15]:
        get_logger(__name__).info(f"{file_path}: {line_count} lines")

    get_logger(__name__).info(f"\nTotal files over 400 lines: {len(large_files)}")
