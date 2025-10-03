#!/usr/bin/env python3
"""
Vector Database Cleanup - Remove Stale Mission Status - V2 Compliant (Refactored)
=================================================================================

Refactored stale database cleanup importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import sys
from pathlib import Path

from cleanup_stale_database_core import StaleDatabaseCleanupCore

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point for stale database cleanup."""
    print("🚀 Starting Vector Database Cleanup")

    # Initialize cleanup core
    cleanup_core = StaleDatabaseCleanupCore()

    # Run comprehensive cleanup
    results = cleanup_core.run_comprehensive_cleanup()

    if "error" in results:
        print(f"❌ Database cleanup failed: {results['error']}")
        return False

    print("\n✅ Vector database cleanup completed successfully!")
    print("📊 Summary:")
    print(f"   Status: {results['status']}")
    print(f"   Stale records identified: {results['stale_records_identified']}")
    print(f"   Records cleaned: {results['records_cleaned']}")
    print(f"   Tasks updated: {results['tasks_updated']}")

    return True


if __name__ == "__main__":
    main()
