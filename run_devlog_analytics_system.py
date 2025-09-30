#!/usr/bin/env python3
"""
Devlog Analytics System Startup Script
=====================================

Starts all components of the devlog analytics system:
1. Devlog Analytics API (port 8002)
2. Enhanced WebSocket Server (port 8001)
3. React Dashboard (port 3000)

Usage:
    python run_devlog_analytics_system.py

Components:
- Analytics API: REST endpoints for querying devlogs
- WebSocket Server: Real-time updates for dashboard
- React Dashboard: Web interface for visualization
"""

from devlog_analytics_system_core import DevlogAnalyticsSystem


def main():
    """Main startup function."""
    system = DevlogAnalyticsSystem()
    system.run()


if __name__ == "__main__":
    main()