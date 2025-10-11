"""
Complexity Analyzer CLI - Command Line Interface
================================================
CLI entry point for complexity analysis tool.
Extracted for V2 compliance.

Author: Agent-5 (extracted from Agent-6's complexity_analyzer.py)
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from complexity_analyzer_core import ComplexityAnalysisService


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Complexity Analyzer - AST-based complexity metrics"
    )
    parser.add_argument("path", nargs="?", default=".", help="File or directory to analyze")
    parser.add_argument("--pattern", default="**/*.py", help="File pattern for directory scan")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed metrics")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Limit results in summary")
    args = parser.parse_args()
    service = ComplexityAnalysisService()
    path = Path(args.path)
    if path.is_file():
        # Analyze single file
        result = service.analyze_file(str(path), args.verbose)
        if result:
            print(result)
        else:
            print(f"❌ Could not analyze {path}")
    elif path.is_dir():
        # Analyze directory
        reports = service.analyze_directory(str(path), args.pattern, args.verbose)
        if not reports:
            print(f"❌ No Python files found in {path}")
        else:
            # Show summary
            summary = service.generate_summary_report(reports, args.limit)
            print(summary)
            # Show individual reports if verbose
            if args.verbose:
                for report in reports:
                    if report.has_violations:
                        print("\n")
                        print(service.analyzer.format_report(report, True))
    else:
        print(f"❌ Path not found: {path}")


if __name__ == "__main__":
    main()
