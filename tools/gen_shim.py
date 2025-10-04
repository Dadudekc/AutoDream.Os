#!/usr/bin/env python3
"""
Shim Generator Tool
==================
Generate deprecation shims for consolidated modules.
"""

import json
import sys
from pathlib import Path


def make_shim(module: str, symbol_map: dict[str, str]) -> str:
    """Generate shim content for a module."""
    lines = [
        "#!/usr/bin/env python3",
        '"""',
        f"Deprecation shim for {module}",
        "",
        "This module provides backward compatibility while redirecting to the",
        "canonical implementation.",
        "",
        "DEPRECATED: Use the canonical module directly.",
        '"""',
        "",
        "import warnings",
        "",
        f"from {module} import *",
        "",
    ]

    if symbol_map:
        lines.extend(
            [
                "# Symbol mappings for backward compatibility",
                f"# Import from canonical module: {module}",
                "",
            ]
        )
        for old, new in symbol_map.items():
            lines.append(f"from {module} import {new} as {old}")
        lines.append("")

    lines.extend(
        [
            "# Deprecation warning",
            "warnings.warn(",
            f'    "Module {module} is deprecated. Use canonical module directly.",',
            "    DeprecationWarning,",
            "    stacklevel=2,",
            ")",
        ]
    )

    return "\n".join(lines)


def main(manifest_path: str = "runtime/consolidation/manifest.json"):
    """Main function to generate shims from manifest."""
    manifest_file = Path(manifest_path)
    if not manifest_file.exists():
        print(f"Error: Manifest file not found: {manifest_file}")
        return 1

    try:
        with open(manifest_file, encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"Error loading manifest: {e}")
        return 1

    shims_created = 0

    # Generate shims for shim_actions
    for action in manifest.get("shim_actions", []):
        if action["action"] == "shim":
            target_file = Path(action["file"])
            module = action["module"]
            symbol_map = action.get("symbol_map", {})

            # Create parent directory if needed
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # Generate shim content
            shim_content = make_shim(module, symbol_map)

            # Write shim file
            target_file.write_text(shim_content, encoding="utf-8")
            print(f"✅ shim: {target_file}")
            shims_created += 1

    print(f"\nGenerated {shims_created} shim files")
    return 0


if __name__ == "__main__":
    manifest_path = sys.argv[1] if len(sys.argv) > 1 else "runtime/consolidation/manifest.json"
    exit(main(manifest_path))
