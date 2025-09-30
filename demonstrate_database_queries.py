#!/usr/bin/env python3
"""
Demonstrate Database Queries
============================

This script demonstrates what we can now query from the database
instead of reading static documentation files.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused query demonstration
"""

from database_query_demonstrator_core import DatabaseQueryDemonstrator


def main():
    """Main demonstration."""
    demonstrator = DatabaseQueryDemonstrator()
    demonstrator.run_all_demonstrations()


if __name__ == "__main__":
    main()