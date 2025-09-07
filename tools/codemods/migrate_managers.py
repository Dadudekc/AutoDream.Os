#!/usr/bin/env python3
"""
Manager Migration Codemod - Phase-2 Manager Consolidation
=========================================================

Zero-dep codemod to migrate legacy manager imports/usages.
- Dry-run by default; print unified diffs
- --write to apply in-place
- Uses simple token/line replace (safe subset) — review diff before commit

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
import argparse
import os
import sys
import difflib
import json


def load_map(path: str) -> dict:
    """Load migration mapping from JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[codemod] Error loading mapping file {path}: {e}")
        return {}


def transform(text: str, mapping: dict) -> str:
    """Transform text using mapping rules."""
    result = text
    for old_pattern, new_pattern in mapping.items():
        result = result.replace(old_pattern, new_pattern)
    return result


def iter_python_files(root: str):
    """Iterate over Python files in directory tree."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip certain directories
        if any(
            part
            in {".git", "venv", ".venv", "node_modules", "dist", "build", "__pycache__"}
            for part in dirpath.split(os.sep)
        ):
            continue

        for filename in filenames:
            if filename.endswith(".py"):
                yield os.path.join(dirpath, filename)


def main():
    """Main codemod function."""
    parser = argparse.ArgumentParser(
        description="Migrate legacy managers to core managers"
    )
    parser.add_argument("--root", default=".", help="Root directory to process")
    parser.add_argument(
        "--map",
        default="runtime/migrations/manager-map.json",
        help="Path to migration mapping file",
    )
    parser.add_argument(
        "--write", action="store_true", help="Apply changes (default is dry-run)"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Load migration mapping
    mapping = load_map(args.map)
    if not mapping:
        print(f"[codemod] No mapping rules found in {args.map}")
        return 1

    if args.verbose:
        print(f"[codemod] Loaded {len(mapping)} mapping rules")

    # Process files
    modified_files = 0
    total_files = 0

    for file_path in iter_python_files(args.root):
        total_files += 1

        try:
            # Read original file
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            # Apply transformations
            transformed_content = transform(original_content, mapping)

            # Check if file was modified
            if original_content != transformed_content:
                modified_files += 1

                if args.write:
                    # Write transformed content
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(transformed_content)
                    print(f"[codemod] Updated: {file_path}")
                else:
                    # Show diff
                    print(f"[codemod] Would modify: {file_path}")
                    diff = difflib.unified_diff(
                        original_content.splitlines(True),
                        transformed_content.splitlines(True),
                        fromfile=file_path,
                        tofile=file_path,
                    )
                    sys.stdout.writelines(diff)
                    print()

        except Exception as e:
            print(f"[codemod] Error processing {file_path}: {e}")
            continue

    # Summary
    if args.write:
        print(
            f"[codemod] Migration complete: {modified_files}/{total_files} files updated"
        )
        return 0
    else:
        print(
            f"[codemod] Dry run complete: {modified_files}/{total_files} files would be modified"
        )
        if modified_files > 0:
            print("[codemod] Run with --write to apply changes")
            return 2
        else:
            return 0


if __name__ == "__main__":
    sys.exit(main())
