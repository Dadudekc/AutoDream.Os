#!/usr/bin/env python3
"""
Devlog Inventory Script
======================

This script provides a comprehensive inventory of all devlogs in the system,
including database devlogs, file devlogs, and exported files.
"""

from devlog_inventory_core import DevlogInventory


def main():
    """Run the devlog inventory."""
    inventory = DevlogInventory()
    inventory.run_inventory()


if __name__ == "__main__":
    main()