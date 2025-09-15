#!/usr/bin/env python3
"""
Functionality Verification Tool - V2 Compliance Wrapper
=====================================================

V2 compliant wrapper for the modular functionality verification system.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Usage: python tools/functionality_verification.py --baseline
"""

import argparse
import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

from verification.functionality_scanner import FunctionalityScanner
from verification.functionality_verifier import FunctionalityVerifier
from verification.verification_reporter import VerificationReporter


def main():
    """Main entry point for functionality verification tool."""
    parser = argparse.ArgumentParser(description="Functionality Verification Tool")
    parser.add_argument("--baseline", action="store_true", help="Create baseline signature")
    parser.add_argument("--verify", action="store_true", help="Verify against baseline")
    parser.add_argument("--comprehensive", action="store_true", help="Run comprehensive verification")
    
    args = parser.parse_args()
    
    project_root = Path(".")
    scanner = FunctionalityScanner(project_root)
    verifier = FunctionalityVerifier(project_root)
    reporter = VerificationReporter(project_root)
    
    if args.baseline:
        print("🔍 Creating baseline functionality signature...")
        signature = scanner.generate_functionality_signature()
        baseline_path = verifier.save_baseline(signature)
        print(f"✅ Baseline saved to: {baseline_path}")
        
    elif args.verify or args.comprehensive:
        print("🔍 Verifying functionality preservation...")
        
        # Generate current signature
        current_signature = scanner.generate_functionality_signature()
        
        # Verify against baseline
        verification_result = verifier.verify_functionality_preservation(current_signature)
        
        # Generate report
        report = reporter.generate_verification_report(verification_result)
        
        # Save report
        report_path = reporter.save_report(report)
        print(f"📄 Verification report saved to: {report_path}")
        
        # Print summary
        reporter.print_verification_summary(report)
        
        # Exit with appropriate code
        preservation_score = verification_result.get("preservation_score", 0.0)
        if preservation_score < 80.0:
            print("\n⚠️  Low functionality preservation score!")
            exit(1)
        else:
            print("\n✅ Functionality verification completed successfully!")
            exit(0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
