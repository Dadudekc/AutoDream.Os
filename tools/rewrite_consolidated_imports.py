#!/usr/bin/env python3
"""
Consolidated Import Rewriter
===========================

Automated tool to rewrite old consolidated_messaging imports to canonical paths.
This tool helps gradually migrate from old import paths to new ones.

Usage:
    python tools/rewrite_consolidated_imports.py

Features:
- Scans all Python files in the project
- Rewrites old import paths to canonical paths
- Preserves shims for external dependencies
- Skips runtime directories
- Reports number of files changed

Warning: This tool modifies files in place. Use with caution.
"""

from __future__ import annotations

import re
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent

# Import path mappings (old -> new)
IMPORT_MAPPINGS = {
    "src.services.consolidated_messaging_service": "src.services.messaging_service",
    "src.services.consolidated_messaging_core": "src.services.messaging_service_core", 
    "src.services.consolidated_messaging_service_core": "src.services.messaging_service",
    "src.services.consolidated_messaging_service_utils": "src.services.messaging_service_utils",
    "src.services.consolidated_messaging_service_main": "src.services.messaging_service_main",
}

# Directories to skip
SKIP_DIRS = {
    "runtime",
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "venv",
    "env",
}


def should_skip_path(path: Path) -> bool:
    """Check if path should be skipped."""
    # Skip if any parent directory is in skip list
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def rewrite_imports(text: str) -> str:
    """
    Rewrite import statements in text.
    
    Handles:
    - from old_path import ...
    - import old_path
    """
    modified_text = text
    
    for old_path, new_path in IMPORT_MAPPINGS.items():
        # Escape dots for regex
        old_path_escaped = re.escape(old_path)
        
        # Pattern 1: from old_path import ...
        pattern1 = rf"(^|\n)\s*from\s+{old_path_escaped}\s+import\s"
        replacement1 = rf"\1from {new_path} import "
        modified_text = re.sub(pattern1, replacement1, modified_text, flags=re.MULTILINE)
        
        # Pattern 2: import old_path
        pattern2 = rf"(^|\n)\s*import\s+{old_path_escaped}(\s|$)"
        replacement2 = rf"\1import {new_path}\2"
        modified_text = re.sub(pattern2, replacement2, modified_text, flags=re.MULTILINE)
        
        # Pattern 3: import old_path as ...
        pattern3 = rf"(^|\n)\s*import\s+{old_path_escaped}\s+as\s+"
        replacement3 = rf"\1import {new_path} as "
        modified_text = re.sub(pattern3, replacement3, modified_text, flags=re.MULTILINE)
    
    return modified_text


def process_file(file_path: Path) -> bool:
    """
    Process a single Python file.
    
    Returns:
        True if file was modified, False otherwise
    """
    try:
        original_text = file_path.read_text(encoding="utf-8", errors="ignore")
        modified_text = rewrite_imports(original_text)
        
        if modified_text != original_text:
            file_path.write_text(modified_text, encoding="utf-8")
            return True
        
        return False
        
    except Exception as e:
        print(f"⚠️  Error processing {file_path}: {e}")
        return False


def main() -> int:
    """Main function."""
    print("🔄 Consolidated Import Rewriter")
    print("=" * 40)
    print(f"📁 Scanning: {ROOT}")
    print(f"🎯 Mappings:")
    for old, new in IMPORT_MAPPINGS.items():
        print(f"   {old} → {new}")
    print()
    
    files_processed = 0
    files_modified = 0
    
    # Find all Python files
    for py_file in ROOT.rglob("*.py"):
        if should_skip_path(py_file):
            continue
            
        files_processed += 1
        
        if process_file(py_file):
            files_modified += 1
            print(f"✅ Modified: {py_file.relative_to(ROOT)}")
    
    print("\n" + "=" * 40)
    print("📊 Results:")
    print(f"  📁 Files processed: {files_processed}")
    print(f"  ✏️  Files modified: {files_modified}")
    
    if files_modified > 0:
        print(f"\n✅ Successfully rewrote imports in {files_modified} files")
        print("💡 Consider running tests to verify everything still works")
        print("🔍 Review changes with: git diff")
    else:
        print("\n✅ No files needed import rewriting")
        print("🎯 All imports are already using canonical paths")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

