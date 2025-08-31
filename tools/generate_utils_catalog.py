#!/usr/bin/env python3
"""Generate a concise catalog of functions in all utils directories."""
import ast
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
entries = []

for py_file in ROOT.rglob("*.py"):
    if "utils" not in py_file.parts:
        continue
    rel_path = py_file.relative_to(ROOT)
    with py_file.open("r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            continue
    funcs = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    entries.append((str(rel_path), sorted(funcs), sorted(classes)))

lines = ["# Utils Function Catalog", "", "Summary of top-level functions and classes within directories containing 'utils'.", ""]
for path, funcs, classes in sorted(entries):
    lines.append(f"## {path}")
    if funcs:
        lines.append("- Functions: " + ", ".join(funcs))
    if classes:
        lines.append("- Classes: " + ", ".join(classes))
    lines.append("")

output_path = ROOT / "docs" / "utils_function_catalog.md"
output_path.write_text("\n".join(lines), encoding="utf-8")
