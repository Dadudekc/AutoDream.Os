"""
Project Scanner CLI
==================

Command-line interface for project scanning.
"""

import argparse
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point for project scanner."""
    parser = argparse.ArgumentParser(
        description="Project Scanner - Analyze project structure and code quality"
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Root directory of the project to scan (default: current directory)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help="Number of worker threads (default: 4)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Output directory for reports (default: current directory)",
    )
    parser.add_argument(
        "--cache-file",
        "-c",
        default="dependency_cache.json",
        help="Cache file for dependency analysis (default: dependency_cache.json)",
    )

    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        # Import and run scanner
        from .core import ProjectScanner

        project_root = Path(args.project_root).resolve()
        if not project_root.exists():
            logger.error(f"Project root does not exist: {project_root}")
            sys.exit(1)

        logger.info(f"🔍 Starting project scan of: {project_root}")

        # Initialize and run scanner
        scanner = ProjectScanner(project_root=str(project_root))
        scanner.scan_project()
        scanner.generate_init_files(overwrite=True)
        scanner.categorize_agents()
        scanner.report_generator.save_report()
        scanner.export_chatgpt_context()
        scanner.modular_reporter.generate_modular_reports()

        logger.info("✅ Project scan completed successfully")
        print("🐝 WE. ARE. SWARM. ⚡️🔥")

    except ImportError as e:
        logger.error(f"Failed to import ProjectScanner: {e}")
        sys.exit(2)
    except Exception as e:
        logger.error(f"Project scan failed: {e}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
