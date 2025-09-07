#!/usr/bin/env python3
"""Orchestrator for V2 standards checking.

This lightweight module wires together configuration, validation and
reporting utilities. The heavy validation logic lives in companion
modules allowing this file to remain small and focused on CLI handling.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any

# Allow running directly from repository root
sys.path.insert(0, str(Path(__file__).parent))

from v2_standards_config import StandardsConfig
from v2_standards_checker_core import check_all, check_single
from v2_standards_reporter import print_summary, print_loc_details


class V2StandardsChecker:
    """Thin wrapper around core validation helpers."""

    def __init__(self, config: StandardsConfig | None = None) -> None:
        self.config = config or StandardsConfig()

    def check_all_standards(self) -> Dict[str, Any]:
        return check_all(self.config)

    def check_loc_compliance(self) -> Dict[str, Any]:
        return check_single("loc", self.config)

    def check_oop_compliance(self) -> Dict[str, Any]:
        return check_single("oop", self.config)

    def check_cli_compliance(self) -> Dict[str, Any]:
        return check_single("cli", self.config)

    def check_srp_compliance(self) -> Dict[str, Any]:
        return check_single("srp", self.config)


def validate_v2_standards() -> Dict[str, Any]:
    """Validate all standards and return raw results."""
    checker = V2StandardsChecker()
    return checker.check_all_standards()


def main() -> None:
    parser = argparse.ArgumentParser(description="V2 Standards Checker")
    parser.add_argument("--all", "-a", action="store_true", help="Run full check")
    parser.add_argument("--loc-check", "-l", action="store_true", help="LOC only")
    parser.add_argument("--oop-check", "-o", action="store_true", help="OOP only")
    parser.add_argument("--cli-check", "-c", action="store_true", help="CLI only")
    parser.add_argument("--srp-check", "-s", action="store_true", help="SRP only")
    args = parser.parse_args()

    checker = V2StandardsChecker()

    if args.loc_check:
        results = checker.check_loc_compliance()
        print_loc_details(results)
        sys.exit(0 if results["non_compliant_files"] == 0 else 1)
    elif args.oop_check:
        results = checker.check_oop_compliance()
        print_summary(results)
        sys.exit(0 if results["non_compliant_files"] == 0 else 1)
    elif args.cli_check:
        results = checker.check_cli_compliance()
        print_summary(results)
        sys.exit(0 if results["non_compliant_files"] == 0 else 1)
    elif args.srp_check:
        results = checker.check_srp_compliance()
        print_summary(results)
        sys.exit(0 if results["non_compliant_files"] == 0 else 1)
    else:
        results = checker.check_all_standards()
        print_summary(results)
        sys.exit(0 if results["overall_compliance"] >= 80 else 1)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"💥 V2 standards check failed: {exc}")
        sys.exit(1)
