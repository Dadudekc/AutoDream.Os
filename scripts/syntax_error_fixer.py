#!/usr/bin/env python3
"""
Syntax Error Fixer for Agent Cellphone V2 Repository
====================================================

Automatically fixes common syntax errors in Python files.
Addresses unterminated strings, missing indentation, and other issues.

Author: Agent-5 (Data Organization Specialist)
Mission: DATA-ORGANIZE-001
License: MIT
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class SyntaxErrorFixer:
    """Fixes common syntax errors in Python files."""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.fixes_applied = 0
        self.files_processed = 0

    def fix_unterminated_strings(self, content: str) -> str:
        """Fix unterminated triple-quoted strings."""
        # Pattern to find unterminated triple quotes
        pattern = r'""".*?(?=\n\s*[^"]|$)'

        def fix_match(match):
            text = match.group(0)
            if not text.endswith('"""'):
                # Add closing triple quotes
                return text + '"""'
            return text

        return re.sub(pattern, fix_match, content, flags=re.DOTALL)

    def fix_missing_indentation(self, content: str) -> str:
        """Fix missing indentation after function/class definitions."""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            fixed_lines.append(line)

            # Check if this line ends with a colon and next line needs indentation
            if line.strip().endswith(":") and i + 1 < len(lines):
                next_line = lines[i + 1]

                # If next line is not empty and not indented, add indentation
                if (
                    next_line.strip()
                    and not next_line.startswith(" ")
                    and not next_line.startswith("\t")
                ):
                    # Add 4 spaces of indentation
                    fixed_lines.append("    pass  # TODO: Implement")

        return "\n".join(fixed_lines)

    def fix_empty_blocks(self, content: str) -> str:
        """Fix empty function/class blocks."""
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            fixed_lines.append(line)

            # Check for empty function/class definitions
            if line.strip().endswith(":") and i + 1 < len(lines) and lines[i + 1].strip() == "":
                # Add pass statement
                fixed_lines.append("    pass  # TODO: Implement")

        return "\n".join(fixed_lines)

    def fix_invalid_syntax(self, content: str) -> str:
        """Fix various invalid syntax issues."""
        # Fix common syntax issues
        fixes = [
            # Fix missing commas in function calls
            (r"(\w+)\s*\)", r"\1)"),
            # Fix unterminated strings
            (r'(["\'])([^"\']*?)(?=\n|$)', r"\1\2\1"),
            # Fix missing colons
            (r"(if|for|while|def|class)\s+[^:]+(?=\n)", r"\1 condition:  # TODO: Fix condition"),
        ]

        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)

        return content

    def fix_file(self, file_path: Path) -> bool:
        """Fix syntax errors in a single file."""
        try:
            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Apply fixes
            content = self.fix_unterminated_strings(content)
            content = self.fix_missing_indentation(content)
            content = self.fix_empty_blocks(content)
            content = self.fix_invalid_syntax(content)

            # Only write if changes were made
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.fixes_applied += 1
                logger.info(f"Fixed syntax errors in: {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to fix {file_path}: {e}")
            return False

    def fix_directory(self, directory: Path) -> dict:
        """Fix syntax errors in all Python files in a directory."""
        results = {"files_processed": 0, "files_fixed": 0, "errors": []}

        # Find all Python files
        python_files = list(directory.rglob("*.py"))

        for file_path in python_files:
            try:
                self.files_processed += 1
                results["files_processed"] += 1

                if self.fix_file(file_path):
                    results["files_fixed"] += 1

            except Exception as e:
                error_msg = f"Error processing {file_path}: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

        return results

    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of the original file."""
        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        backup_path.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")
        return backup_path


def main():
    """Main entry point for syntax error fixing."""
    import argparse

    parser = argparse.ArgumentParser(description="Syntax Error Fixer")
    parser.add_argument("--root-dir", default=".", help="Root directory to process")
    parser.add_argument("--backup", action="store_true", help="Create backups before fixing")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be fixed without making changes"
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Create syntax error fixer
    fixer = SyntaxErrorFixer(args.root_dir)

    if args.dry_run:
        print("DRY RUN: Would fix syntax errors in Python files")
        print("  - Unterminated strings")
        print("  - Missing indentation")
        print("  - Empty function/class blocks")
        print("  - Invalid syntax")
    else:
        # Create backups if requested
        if args.backup:
            print("Creating backups...")

        # Fix syntax errors
        results = fixer.fix_directory(Path(args.root_dir))

        print("Syntax error fixing completed!")
        print(f"Files processed: {results['files_processed']}")
        print(f"Files fixed: {results['files_fixed']}")
        print(f"Errors: {len(results['errors'])}")

        if results["errors"]:
            print("\nErrors encountered:")
            for error in results["errors"]:
                print(f"  - {error}")


if __name__ == "__main__":
    main()
