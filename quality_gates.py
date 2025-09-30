#!/usr/bin/env python3
"""
Quality Gates for Agent Work - V2 Compliant (Refactored)
========================================================

Refactored quality gates importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import List

from quality_gates_core import QualityGateChecker, QualityLevel, QualityMetrics

logger = logging.getLogger(__name__)


def main():
    """Main entry point for quality gates."""
    parser = argparse.ArgumentParser(description="Quality Gates for V2 Compliance")
    parser.add_argument("--path", default="src", help="Path to analyze")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    checker = QualityGateChecker()
    # Check individual files in directory
    results = []
    path = Path(args.path)
    if path.is_file():
        results.append(checker.check_file(str(path)))
    else:
        for py_file in path.rglob("*.py"):
            results.append(checker.check_file(str(py_file)))
    
    if args.output:
        checker.save_results(results, args.output)
    else:
        checker.print_results(results)
    
    # Exit with error code if violations found
    if any(r.quality_level in [QualityLevel.POOR, QualityLevel.CRITICAL] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()