import sys
from pathlib import Path
import argparse
import json
from typing import Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from emergency_database_recovery import EmergencyContractDatabaseRecovery
from emergency_database_recovery.core.database_auditor import DatabaseAuditor
from emergency_database_recovery.core.integrity_checker import IntegrityChecker
from emergency_database_recovery.core.corruption_scanner import CorruptionScanner
from emergency_database_recovery.core.recovery_executor import RecoveryExecutor


def print_banner():
    """Print the system banner."""
    print("🚨 Emergency Database Recovery System 🚨")
    print("=" * 50)
    print("Agent-2 - PHASE TRANSITION OPTIMIZATION MANAGER")
    print("Modularized Emergency Database Recovery")
    print("=" * 50)


def print_json_output(data: Dict[str, Any], pretty: bool = True):
    """Print data as JSON output."""
    if pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))


def audit_database(args):
    """Perform database audit."""
    print("🔍 Performing database audit...")
    
    try:
        auditor = DatabaseAuditor()
        audit_results = auditor.audit_database_structure()
        
        print("✅ Database audit completed successfully!")
        print_json_output(audit_results, args.pretty)
        
        return 0
    except Exception as e:
        print(f"❌ Database audit failed: {e}")
        return 1


def check_integrity(args):
    """Perform integrity check."""
    print("🔒 Performing integrity check...")
    
    try:
        checker = IntegrityChecker()
        integrity_results = checker.validate_contract_status_accuracy()
        
        print("✅ Integrity check completed successfully!")
        print_json_output(integrity_results, args.pretty)
        
        return 0
    except Exception as e:
        print(f"❌ Integrity check failed: {e}")
        return 1


def scan_corruption(args):
    """Scan for corruption."""
    print("🔍 Scanning for corruption...")
    
    try:
        scanner = CorruptionScanner()
        corruption_results = scanner.scan_for_corruption()
        
        print("✅ Corruption scan completed successfully!")
        print_json_output(corruption_results, args.pretty)
        
        return 0
    except Exception as e:
        print(f"❌ Corruption scan failed: {e}")
        return 1


def execute_recovery(args):
    """Execute recovery procedures."""
    print("🚀 Executing recovery procedures...")
    
    try:
        executor = RecoveryExecutor()
        recovery_results = executor.implement_integrity_checks()
        
        print("✅ Recovery execution completed successfully!")
        print_json_output(recovery_results, args.pretty)
        
        return 0
    except Exception as e:
        print(f"❌ Recovery execution failed: {e}")
        return 1


def run_full_recovery(args):
    """Run full emergency recovery process."""
    print("🚨 Executing full emergency recovery process...")
    
    try:
        system = EmergencyContractDatabaseRecovery()
        recovery_report = system.execute_emergency_recovery()
        
        print("✅ Full emergency recovery completed successfully!")
        print_json_output(recovery_report, args.pretty)
        
        return 0
    except Exception as e:
        print(f"❌ Full emergency recovery failed: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Emergency Database Recovery System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Perform database audit
  python cli.py audit

  # Check database integrity
  python cli.py integrity

  # Scan for corruption
  python cli.py scan

  # Execute recovery procedures
  python cli.py recover

  # Run full emergency recovery
  python cli.py full-recovery

  # Get help for specific command
  python cli.py audit --help
        """
    )
    
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print JSON output"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )
    
    # Audit command
    audit_parser = subparsers.add_parser(
        "audit",
        help="Perform database audit"
    )
    audit_parser.set_defaults(func=audit_database)
    
    # Integrity command
    integrity_parser = subparsers.add_parser(
        "integrity",
        help="Check database integrity"
    )
    integrity_parser.set_defaults(func=check_integrity)
    
    # Scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan for corruption"
    )
    scan_parser.set_defaults(func=scan_corruption)
    
    # Recover command
    recover_parser = subparsers.add_parser(
        "recover",
        help="Execute recovery procedures"
    )
    recover_parser.set_defaults(func=execute_recovery)
    
    # Full recovery command
    full_recovery_parser = subparsers.add_parser(
        "full-recovery",
        help="Run full emergency recovery process"
    )
    full_recovery_parser.set_defaults(func=run_full_recovery)
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        print(f"❌ Command execution failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
