"""
V2 Compliance Analysis CLI Interface
===================================

Command-line interface for V2 compliance analysis tool.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from .core import AnalysisCore
from .violations import ViolationDetector, format_violations_text
from .refactor import generate_refactor_suggestions, format_refactor_report

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="V2 Compliance Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/analysis/cli.py --violations --n 100000 > runtime/violations_full.txt
  python tools/analysis/cli.py --ci-gate
  python tools/analysis/cli.py --refactor --output refactor_plan.json
        """
    )
    
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory to analyze (default: current directory)"
    )
    
    parser.add_argument(
        "--violations",
        action="store_true",
        help="Generate violations report"
    )
    
    parser.add_argument(
        "--ci-gate",
        action="store_true",
        help="Run CI gate check (exit with error code if violations found)"
    )
    
    parser.add_argument(
        "--refactor",
        action="store_true",
        help="Generate refactoring suggestions"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for results (JSON format)"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--n",
        type=int,
        default=100000,
        help="Maximum number of files to analyze (default: 100000)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    try:
        # Initialize detector
        detector = ViolationDetector()
        
        # Analyze project
        logger.info(f"Analyzing project: {args.project_root}")
        results = detector.analyze_project(args.project_root, args.n)
        
        # Generate output based on requested actions
        output_data = {}
        
        if args.violations:
            if args.format == "text":
                violations_text = format_violations_text(results)
                print(violations_text)
                output_data["violations_text"] = violations_text
            else:
                output_data["violations"] = results
        
        if args.refactor:
            refactor_plan = generate_refactor_suggestions(results)
            if args.format == "text":
                refactor_text = format_refactor_report(refactor_plan)
                print("\n" + "="*80 + "\n")
                print(refactor_text)
                output_data["refactor_text"] = refactor_text
            else:
                output_data["refactor_plan"] = refactor_plan
        
        if args.ci_gate:
            passed, message = detector.ci_gate_check(results)
            print(f"CI Gate: {message}")
            output_data["ci_gate"] = {"passed": passed, "message": message}
            
            if not passed:
                return 1
        
        # Save output to file if requested
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2)
            logger.info(f"Results saved to: {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


