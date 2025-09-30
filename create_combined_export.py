#!/usr/bin/env python3
"""
Create Combined Devlog Export
============================

This script creates a comprehensive export of all devlogs from both
the database and file system.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused export functionality
"""

from combined_export_core import CombinedExportCore


def main():
    """Main function to create combined export."""
    print("🤖 COMPLETE DEVLOG EXPORT")
    print("=" * 30)
    
    exporter = CombinedExportCore()
    filename = exporter.create_combined_export()
    
    print()
    print("🎉 All devlogs have been successfully exported!")
    print("💾 The export file is ready for upload to any system.")


if __name__ == "__main__":
    main()