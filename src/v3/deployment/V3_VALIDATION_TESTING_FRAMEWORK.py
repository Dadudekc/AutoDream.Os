#!/usr/bin/env python3
"""
V3 Validation Testing Framework - V2 Compliant
==============================================

Refactored validation framework using modular design.
V2 Compliance: ≤100 lines, single responsibility, KISS principle.
"""

import sys
from src.validation import V3ValidationFrameworkCore


class V3ValidationTestingFramework:
    """V3 Validation Testing Framework - Legacy compatibility wrapper."""
    
    def __init__(self):
        self.core_framework = V3ValidationFrameworkCore()
    
    def run_full_validation(self):
        """Run full V3 validation suite using modular framework."""
        return self.core_framework.run_full_validation()


def main():
    """Main validation function."""
    framework = V3ValidationTestingFramework()
    results = framework.run_full_validation()
    
    return results["overall_status"] == "PASSED"


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
