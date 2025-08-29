"""Command line interface for the modularizer."""
from __future__ import annotations

import json

from .backup import create_backup
from .analysis import get_targets
from .reporting import generate_report


def main() -> None:
    backup_dir = create_backup()
    print(f"📦 Backup created at {backup_dir}")

    for modularize in get_targets():
        modularize()

    report = generate_report()
    print(json.dumps(report, indent=2))

if __name__ == "__main__":  # pragma: no cover
    main()
