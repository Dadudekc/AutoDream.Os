#!/usr/bin/env python3
"""
Current Mission Status Demonstration
===================================

Demonstrate the corrected vector database with current Phase 2 operations
instead of stale 9-month-old mission status.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused mission status demonstration
"""

from mission_status_demonstrator_core import MissionStatusDemonstrator


def main():
    """Demonstrate current mission status in vector database."""
    demonstrator = MissionStatusDemonstrator()
    demonstrator.demonstrate_current_mission_status()


if __name__ == "__main__":
    main()