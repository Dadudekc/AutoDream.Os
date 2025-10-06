#!/usr/bin/env python3
"""
Consolidation Apply Tool
========================

Apply consolidation manifest:
- Moves files
- Generates deprecation shims
- Rewrites imports project-wide to canonical paths
- Idempotent; creates a backup of changed files in runtime/consolidation/backups/

V2 Compliance: ≤400 lines, focused refactoring executor
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "runtime" / "consolidation" / "backups"
BACKUP.mkdir(parents=True, exist_ok=True)


def rewrite_imports(text: str, src: str, dst: str) -> str:
    """Rewrite import statements from src module to dst module."""
    # Handle "from X import Y" patterns
    pat1 = re.compile(rf"(^|\n)\s*from\s+{re.escape(src)}\s+import\s", re.MULTILINE)
    text = pat1.sub(lambda m: m.group(0).replace(src, dst), text)

    # Handle "import X" patterns
    pat2 = re.compile(rf"(^|\n)\s*import\s+{re.escape(src)}(\s|$)", re.MULTILINE)
    text = pat2.sub(lambda m: m.group(0).replace(src, dst), text)

    return text


def make_shim(module: str, symbol_map: dict[str, str], file_path: str) -> str:
    """Generate deprecation shim module."""
    lines = [
        "#!/usr/bin/env python3",
        '"""',
        f"Deprecation shim for {file_path}",
        "",
        "This module provides backward compatibility while redirecting to the",
        f"canonical implementation: {module}",
        "",
        "DEPRECATED: Use the canonical module directly.",
        '"""',
        "",
        "import warnings",
        "",
        f"# Import from canonical module: {module}",
        f"from {module} import *",
        "",
        "# Symbol mappings for backward compatibility",
    ]

    for old_symbol, new_symbol in symbol_map.items():
        lines.append(f"from {module} import {new_symbol} as {old_symbol}")

    lines.extend(
        [
            "",
            "# Deprecation warning",
            "warnings.warn(",
            f"    'Module {file_path} is deprecated. Use {module} directly.',",
            "    DeprecationWarning,",
            "    stacklevel=2",
            ")",
            "",
        ]
    )

    return "\n".join(lines)


def backup_file(file_path: Path) -> None:
    """Create backup of file before modification."""
    if file_path.exists():
        backup_path = BACKUP / file_path.name
        shutil.copy2(file_path, backup_path)


def apply_manifest(manifest_path: Path) -> None:
    """Apply consolidation manifest actions."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading manifest: {e}")
        return

    actions = manifest.get("actions", [])
    changed_files = []
    redirects = {}

    print(f"Applying {len(actions)} consolidation actions...")

    # Process each action
    for i, action in enumerate(actions, 1):
        act_type = action["action"]
        file_path = ROOT / action["file"]

        print(f"[{i}/{len(actions)}] {act_type}: {action['file']}")

        try:
            if act_type == "move":
                # Move file to new location
                dst_path = ROOT / action["to"]
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                backup_file(file_path)
                shutil.move(str(file_path), str(dst_path))
                changed_files.append(str(dst_path))

                # Track import redirect
                old_mod = action["file"].replace("/", ".").replace("\\", ".").removesuffix(".py")
                new_mod = action["to"].replace("/", ".").replace("\\", ".").removesuffix(".py")
                redirects[old_mod] = new_mod

            elif act_type == "delete":
                # Delete file
                backup_file(file_path)
                file_path.unlink(missing_ok=True)
                print(f"  ✅ Deleted {action['file']}")

            elif act_type == "shim":
                # Create deprecation shim
                module = action["module"]
                symbol_map = action.get("symbol_map", {})

                backup_file(file_path)
                shim_content = make_shim(module, symbol_map, action["file"])
                file_path.write_text(shim_content, encoding="utf-8")
                changed_files.append(str(file_path))

                # Track import redirect
                old_mod = action["file"].replace("/", ".").replace("\\", ".").removesuffix(".py")
                redirects[old_mod] = module

                print(f"  ✅ Created shim redirecting to {module}")

            elif act_type == "merge":
                # Mark for manual merge (pass-2)
                print(f"  ⏳ Deferred to pass-2: {action.get('note', 'Manual merge required')}")

            else:
                print(f"  ⚠️ Unknown action: {act_type}")

        except Exception as e:
            print(f"  ❌ Error processing {action['file']}: {e}")

    # Rewrite imports across the project
    print(f"\nRewriting imports for {len(redirects)} module redirects...")
    import_changes = 0

    for py_file in ROOT.rglob("*.py"):
        if str(py_file).startswith(str(BACKUP)):
            continue

        try:
            original_text = py_file.read_text(encoding="utf-8", errors="ignore")
            modified_text = original_text

            for src_mod, dst_mod in redirects.items():
                modified_text = rewrite_imports(modified_text, src_mod, dst_mod)

            if modified_text != original_text:
                backup_file(py_file)
                py_file.write_text(modified_text, encoding="utf-8")
                import_changes += 1

        except Exception as e:
            print(f"Warning: Could not process {py_file}: {e}")

    # Generate summary
    summary = {
        "timestamp": str(Path(__file__).stat().st_mtime),
        "manifest_file": str(manifest_path),
        "actions_processed": len(actions),
        "files_changed": changed_files,
        "import_redirects": redirects,
        "import_changes": import_changes,
        "backup_location": str(BACKUP),
        "expected_reduction": manifest.get("expected_reduction", {}),
        "pass2_candidates": manifest.get("pass2_candidates", []),
    }

    summary_file = ROOT / "runtime" / "consolidation" / "apply_summary.json"
    summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n✅ Consolidation complete!")
    print(f"   Files changed: {len(changed_files)}")
    print(f"   Import rewrites: {import_changes}")
    print(f"   Module redirects: {len(redirects)}")
    print(f"   Summary: {summary_file}")
    print(f"   Backups: {BACKUP}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Apply consolidation manifest")
    parser.add_argument(
        "--manifest", default="runtime/consolidation/manifest.json", help="Path to manifest file"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )

    args = parser.parse_args()

    manifest_path = ROOT / args.manifest
    if not manifest_path.exists():
        print(f"Error: Manifest file not found: {manifest_path}")
        return 1

    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        # TODO: Implement dry-run logic
        return 0

    apply_manifest(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

