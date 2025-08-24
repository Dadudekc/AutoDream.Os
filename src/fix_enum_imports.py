#!/usr/bin/env python3
"""
Fix missing Enum imports across the codebase
"""

import os
import re

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path


def fix_enum_imports(file_path):
    """Fix missing Enum imports in a single file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if file uses Enum but doesn't import it
        if (
            "class" in content
            and "(Enum)" in content
            and "from enum import Enum" not in content
        ):
            # Find the first import line
            lines = content.split("\n")
            import_index = -1

            for i, line in enumerate(lines):
                if line.strip().startswith("import ") or line.strip().startswith(
                    "from "
                ):
                    import_index = i
                    break

            if import_index >= 0:
                # Insert Enum import after the last import
                lines.insert(import_index + 1, "from enum import Enum")
                content = "\n".join(lines)

                # Write back to file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"Fixed: {file_path}")
                return True

        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Fix Enum imports across the entire codebase"""
    src_dir = Path("src")
    fixed_count = 0

    # Find all Python files
    for py_file in src_dir.rglob("*.py"):
        if fix_enum_imports(py_file):
            fixed_count += 1

    print(f"\nFixed {fixed_count} files with missing Enum imports")


if __name__ == "__main__":
    main()
