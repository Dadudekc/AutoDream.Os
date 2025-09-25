#!/usr/bin/env python3
"""
Project Scanner CLI
===================

Command-line interface for the project scanner.
V2 Compliance: ≤400 lines, focused CLI functionality.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.projectscanner.core import ProjectScanner
from tools.projectscanner.reporters import ReportGenerator

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def scan_project(args) -> Dict[str, Any]:
    """Scan project and generate reports."""
    scanner = ProjectScanner(args.project_root)
    
    # Perform scan
    analysis = scanner.scan_project()
    
    # Generate reports
    reporter = ReportGenerator(Path(args.project_root))
    reporter.save_report()
    
    return analysis


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Project Scanner - Analyze project structure and quality"
    )
    
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory (default: current directory)"
    )
    
    parser.add_argument(
        "--output",
        default="project_analysis.json",
        help="Output file for analysis results"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "summary"],
        default="summary",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    try:
        # Perform scan
        analysis = scan_project(args)
        
        # Output results
        if args.format == "json":
            with open(args.output, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"Analysis saved to {args.output}")
        else:
            # Summary output
            print("🎯 PROJECT ANALYSIS SUMMARY")
            print("=" * 50)
            
            if "project_structure" in analysis:
                structure = analysis["project_structure"]
                print(f"📁 Total files: {structure['total_files']:,}")
                print(f"🐍 Python files: {structure['python_files']}")
            
            if "python_analysis" in analysis:
                python_analysis = analysis["python_analysis"]
                print(f"✅ V2 compliant: {python_analysis['v2_compliant_files']}")
                print(f"❌ Non-compliant: {len(python_analysis['non_compliant_files'])}")
                print(f"📊 Compliance rate: {python_analysis['v2_compliant_files']/python_analysis['total_python_files']*100:.1f}%")
            
            if "dependencies" in analysis:
                deps = analysis["dependencies"]
                print(f"🐍 Python version: {deps['python_version']}")
                print(f"📦 Requirements files: {', '.join(deps['requirements_files'])}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        if args.verbose:
            logger.exception("Full traceback:")
        return 1


if __name__ == "__main__":
    sys.exit(main())




