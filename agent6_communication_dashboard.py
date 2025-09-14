#!/usr/bin/env python3
"""
🔄 UNIFIED DASHBOARD WRAPPER - Communication
======================================================

This file replaces the original agent6_communication_dashboard.py with a wrapper
that uses the unified dashboard system.

Original file: /workspace/agent6_communication_dashboard.py
Dashboard type: communication
Migration date: 2025-09-14T20:13:06.390714

This wrapper maintains backward compatibility while using the unified system.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from web.unified_dashboard_manager import create_dashboard, DashboardType

def main():
    """Main entry point for the unified dashboard."""
    try:
        # Create dashboard instance
        dashboard = create_dashboard("communication")
        
        # Run the dashboard
        dashboard.run()
        
    except Exception as e:
        print(f"Error running communication dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
