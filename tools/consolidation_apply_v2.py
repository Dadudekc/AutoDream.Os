#!/usr/bin/env python3
"""
Consolidation Apply Tool v2
===========================
Apply consolidation changes based on manifest and redirects.
"""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime" / "consolidation"
BACKUP = RUNTIME / "backups"


def rewrite_imports(text: str, src: str, dst: str) -> str:
    """Rewrite imports from src to dst."""
    patterns = [
        # from src import ...
        (rf"(^|\n)\s*from\s+{re.escape(src)}\s+import\s", f"from {dst} import "),
        # import src ...
        (rf"(^|\n)\s*import\s+{re.escape(src)}(\s|$)", f"import {dst} "),
        # from src.xxx import ...
        (rf"(^|\n)\s*from\s+{re.escape(src)}\.", f"from {dst}."),
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    return text


def backup_file(file_path: Path) -> Path:
    """Backup a file to the backup directory."""
    backup_file = BACKUP / file_path.name
    if not backup_file.exists():
        shutil.copy2(file_path, backup_file)
    return backup_file


def main():
    """Main function to apply consolidation."""
    print("🔧 Starting consolidation apply...")

    # Ensure backup directory exists
    BACKUP.mkdir(parents=True, exist_ok=True)

    # Load manifest and redirects
    try:
        with open(RUNTIME / "manifest.json", encoding="utf-8") as f:
            manifest = json.load(f)

        with open(RUNTIME / "redirects.json", encoding="utf-8") as f:
            redirects_data = json.load(f)
            redirects = redirects_data["redirects"]

    except Exception as e:
        print(f"Error loading configuration: {e}")
        return 1

    files_modified = 0
    files_backed_up = 0

    # Process all Python files
    for py_file in ROOT.rglob("*.py"):
        # Skip backup directory and certain files
        if (
            str(py_file).startswith(str(BACKUP))
            or str(py_file).startswith(str(RUNTIME))
            or py_file.name == "__pycache__"
        ):
            continue

        try:
            # Read original content
            original_content = py_file.read_text(encoding="utf-8", errors="ignore")
            modified_content = original_content

            # Apply import redirects
            for src_module, dst_module in redirects.items():
                if src_module in modified_content:
                    modified_content = rewrite_imports(modified_content, src_module, dst_module)

            # If content changed, backup and write
            if modified_content != original_content:
                backup_file(py_file)
                files_backed_up += 1

                py_file.write_text(modified_content, encoding="utf-8")
                files_modified += 1
                print(f"✅ rewrote: {py_file.relative_to(ROOT)}")

        except Exception as e:
            print(f"Error processing {py_file}: {e}")
            continue

    print("\n📊 Consolidation apply complete:")
    print(f"   Files backed up: {files_backed_up}")
    print(f"   Files modified: {files_modified}")
    print(f"   Backup location: {BACKUP}")

    return 0


if __name__ == "__main__":
    exit(main())
