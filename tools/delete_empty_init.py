#!/usr/bin/env python3
"""
Delete empty __init__.py files
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
deleted_count = 0

for py_file in ROOT.rglob("__init__.py"):
    if py_file.stat().st_size == 0:
        py_file.unlink()
        print(f"Deleted empty: {py_file.relative_to(ROOT)}")
        deleted_count += 1

print(f"Deleted {deleted_count} empty __init__.py files")

# Also delete the duplicate caching_system.py
duplicate_file = ROOT / "tools" / "projectscanner" / "enhanced_analyzer" / "caching_system.py"
if duplicate_file.exists():
    duplicate_file.unlink()
    print(f"Deleted duplicate: {duplicate_file.relative_to(ROOT)}")
    deleted_count += 1

print(f"Total files deleted: {deleted_count}")

