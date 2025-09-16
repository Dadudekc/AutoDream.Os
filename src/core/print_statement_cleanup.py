"""
Print Statement Cleanup System
=============================

Automated system to clean up remaining print statements and implement
consistent logging patterns across the codebase.

Usage:
    python src/core/print_statement_cleanup.py
"""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PrintStatementCleanup:
    """Clean up remaining print statements and implement logging patterns."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.files_processed = 0
        self.files_modified = 0
        self.print_statements_removed = 0

    def should_skip_file(self, path: Path) -> bool:
        """Check if file should be skipped."""
        path_str = str(path)

        # Skip test files
        if "test" in path_str.lower() or path_str.endswith("conftest.py"):
            return True

        # Skip directories
        skip_dirs = ["__pycache__", ".venv", "node_modules", ".git", ".pytest_cache"]
        if any(skip_dir in path_str for skip_dir in skip_dirs):
            return True

        return False

    def clean_file(self, file_path: Path) -> bool:
        """Clean print statements from a single file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content
            print_count = content.count("print(")

            if print_count == 0:
                return False

            # Remove debug print statements
            content = self._remove_debug_prints(content)

            # Replace remaining prints with logging
            content = self._replace_prints_with_logging(content)

            # Add logging import if needed
            content = self._ensure_logging_import(content)

            # Only write if content changed
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return True

        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return False

        return False

    def _remove_debug_prints(self, content: str) -> str:
        """Remove debug print statements."""
        lines = content.split("\n")
        cleaned_lines = []

        for line in lines:
            # Skip debug prints
            if re.match(r'^\s*print\s*\(\s*["\']debug', line, re.IGNORECASE):
                continue
            if re.match(r'^\s*print\s*\(\s*["\']DEBUG', line):
                continue
            if re.match(r'^\s*print\s*\(\s*f?["\'].*debug.*["\']', line, re.IGNORECASE):
                continue
            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def _replace_prints_with_logging(self, content: str) -> str:
        """Replace print statements with logging calls."""
        # Simple logger.info("") -> logger.info("")
        content = re.sub(r"print\s*\(\s*\)", 'logger.info("")', content)

        # logger.info("string") -> logger.info("string")
        content = re.sub(r'print\s*\(\s*(["\'].*?["\'])\s*\)', r"logger.info(\1)", content)

        # logger.info(f"string") -> logger.info(f"string")
        content = re.sub(r'print\s*\(\s*(f["\'].*?["\'])\s*\)', r"logger.info(\1)", content)

        # logger.info(f"{variable}") -> logger.info(f"{variable}")
        content = re.sub(
            r"print\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)", r'logger.info(f"{\1}")', content
        )

        return content

    def _ensure_logging_import(self, content: str) -> str:
        """Ensure logging import is present."""
        if "import logging" not in content:
            if "logger =" not in content and "logger=" not in content:
                # Add at the top after other imports
                lines = content.split("\n")
                import_index = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith("import ") or line.strip().startswith("from "):
                        import_index = i + 1
                    elif line.strip() and not line.strip().startswith("#"):
                        break

                lines.insert(import_index, "import logging")
                lines.insert(import_index + 1, "logger = logging.getLogger(__name__)")
                content = "\n".join(lines)

        return content

    def run_cleanup(self) -> dict[str, Any]:
        """Run the complete cleanup process."""
        self.logger.info("🧹 Starting print statement cleanup...")

        root_dir = Path(".")

        for py_file in root_dir.rglob("*.py"):
            if self.should_skip_file(py_file):
                continue

            self.files_processed += 1

            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                print_count = content.count("print(")
                if print_count > 0:
                    self.print_statements_removed += print_count
                    self.logger.info(f"Found {print_count} print statements in {py_file}")

                if self.clean_file(py_file):
                    self.files_modified += 1
                    self.logger.info(f"✅ Cleaned {py_file}")

            except Exception as e:
                self.logger.error(f"❌ Error processing {py_file}: {e}")

        summary = {
            "files_processed": self.files_processed,
            "files_modified": self.files_modified,
            "print_statements_removed": self.print_statements_removed,
        }

        self.logger.info("🎯 CLEANUP SUMMARY:")
        self.logger.info(f"Files processed: {summary['files_processed']}")
        self.logger.info(f"Files modified: {summary['files_modified']}")
        self.logger.info(f"Print statements removed: {summary['print_statements_removed']}")

        return summary


def main():
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    cleanup = PrintStatementCleanup()
    result = cleanup.run_cleanup()

    if result["print_statements_removed"] == 0:
        logger.info("✅ SUCCESS: No print statements found!")
    else:
        logger.info(f"✅ SUCCESS: Removed {result['print_statements_removed']} print statements")


if __name__ == "__main__":
    main()
