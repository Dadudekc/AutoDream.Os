#!/usr/bin/env python3
"""
Modular Project Scanner - V2 Compliant Version

This is the new modular version of the project scanner that replaces
the original 1,036-line monolithic file with a clean, organized structure.

Usage:
    python tools/projectscanner_new.py --project-root .
    python -m tools.projectscanner_new --help
"""

import argparse
import logging
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.projectscanner.core import ProjectScanner

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the modular project scanner."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Modular project scanner with agent categorization and incremental caching."
    )
    parser.add_argument("--project-root", default=".", help="Root directory to scan.")
    parser.add_argument(
        "--modular-reports", action="store_true", help="Generate modular analysis reports."
    )
    parser.add_argument(
        "--legacy-reports", action="store_true", help="Generate legacy single-file reports."
    )
    parser.add_argument(
        "--categorize-agents", action="store_true", help="Categorize agents by maturity and type."
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging."
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize scanner
    scanner = ProjectScanner(args.project_root)
    
    # Run the scan
    def progress_callback(percent):
        if percent % 10 == 0:  # Log every 10%
            logger.info(f"Progress: {percent}%")

    scanner.scan_project(progress_callback)

    # Generate reports based on arguments
    if args.modular_reports:
        logger.info("🔄 Generating modular reports...")
        scanner.generate_modular_reports()

    if args.legacy_reports:
        logger.info("🔄 Generating legacy reports...")
        scanner.report_generator.generate_legacy_reports()

    if args.categorize_agents:
        logger.info("🔄 Categorizing agents...")
        scanner.categorize_agents()

    # Default: generate both types of reports if no specific option chosen
    if not (args.modular_reports or args.legacy_reports):
        logger.info("🔄 Generating both modular and legacy reports...")
        scanner.generate_modular_reports()
        scanner.report_generator.generate_legacy_reports()

    logger.info("✅ Project scan completed successfully!")


if __name__ == "__main__":
    main()
