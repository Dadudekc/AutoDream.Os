import logging
logger = logging.getLogger(__name__)
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
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))
from verification.functionality_scanner import FunctionalityScanner
from verification.functionality_verifier import FunctionalityVerifier
from verification.verification_reporter import VerificationReporter


def main():
    """Main entry point for functionality verification tool."""
    parser = argparse.ArgumentParser(description=
        'Functionality Verification Tool')
    parser.add_argument('--baseline', action='store_true', help=
        'Create baseline signature')
    parser.add_argument('--verify', action='store_true', help=
        'Verify against baseline')
    parser.add_argument('--comprehensive', action='store_true', help=
        'Run comprehensive verification')
    args = parser.parse_args()
    project_root = Path('.')
    scanner = FunctionalityScanner(project_root)
    verifier = FunctionalityVerifier(project_root)
    reporter = VerificationReporter(project_root)
    if args.baseline:
        logger.info('🔍 Creating baseline functionality signature...')
        signature = scanner.generate_functionality_signature()
        baseline_path = verifier.save_baseline(signature)
        logger.info(f'✅ Baseline saved to: {baseline_path}')
    elif args.verify or args.comprehensive:
        logger.info('🔍 Verifying functionality preservation...')
        current_signature = scanner.generate_functionality_signature()
        verification_result = verifier.verify_functionality_preservation(
            current_signature)
        report = reporter.generate_verification_report(verification_result)
        report_path = reporter.save_report(report)
        logger.info(f'📄 Verification report saved to: {report_path}')
        reporter.print_verification_summary(report)
        preservation_score = verification_result.get('preservation_score', 0.0)
        if preservation_score < 80.0:
            logger.info('\n⚠️  Low functionality preservation score!')
            exit(1)
        else:
            logger.info(
                '\n✅ Functionality verification completed successfully!')
            exit(0)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
