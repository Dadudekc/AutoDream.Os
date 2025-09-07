#!/usr/bin/env python3
"""Captain task distribution CLI."""
import argparse
import logging
import sys
from pathlib import Path

# Ensure project root is on path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.task_distribution.distributor import CaptainTaskDistributor  # noqa: E402


def main() -> int:
    """Entry point for CLI."""
    parser = argparse.ArgumentParser(description="Captain task distribution operations")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("save", help="Generate contracts and save them to files")
    sub.add_parser("summary", help="Print distribution summary")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    distributor = CaptainTaskDistributor()

    if args.command == "save":
        return 0 if distributor.save_contracts() else 1
    if args.command == "summary":
        print(distributor.get_distribution_summary())
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
