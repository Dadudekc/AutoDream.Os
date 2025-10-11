#!/usr/bin/env python3
"""
Find Duplicate Files Script
===========================

Command-line script to find duplicate files by SHA-256 content hash.

V2 Adapted from: trading-platform repository
Author: Agent-7 - Repository Cloning Specialist
Team Beta: Repo 6 Integration
"""

import argparse
import json
import logging
from pathlib import Path

from .file_hash import find_duplicate_files

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        argv: Optional argument list (defaults to sys.argv)

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(description="Find duplicate files by SHA-256 content hash")
    parser.add_argument(
        "path", nargs="?", default=".", help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--json", dest="as_json", action="store_true", help="Output JSON mapping of digest -> paths"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for duplicate file finder.

    Args:
        argv: Optional argument list

    Returns:
        Exit code: 0 if no duplicates found, 1 if duplicates found, 2 on error
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    args = parse_args(argv)
    root = Path(args.path).resolve()

    if not root.exists():
        logger.error(f"Path not found: {root}")
        return 2

    if not root.is_dir():
        logger.error(f"Path is not a directory: {root}")
        return 2

    logger.info(f"Scanning directory: {root}")
    files = [p for p in root.rglob("*") if p.is_file()]
    logger.info(f"Found {len(files)} files")

    dups = find_duplicate_files(files)

    if args.as_json:
        payload = {digest: [str(p) for p in paths] for digest, paths in dups.items()}
        print(json.dumps(payload, indent=2))
    else:
        if not dups:
            logger.info("No duplicate files found.")
        else:
            logger.info("Duplicate files detected:")
            for digest, paths in dups.items():
                logger.info(f"- {digest}")
                for p in paths:
                    logger.info(f"  - {p}")

    return 1 if dups else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
