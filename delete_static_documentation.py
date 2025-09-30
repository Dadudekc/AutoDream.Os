#!/usr/bin/env python3
"""
Delete Static Documentation
===========================

This script deletes static documentation files that have been ingested
into the Swarm Brain database and can now be replaced with database queries.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused deletion functionality
"""

from static_documentation_deleter_core import StaticDocumentationDeleter


def main():
    """Main deletion process."""
    deleter = StaticDocumentationDeleter()
    deleter.run_deletion_process()


if __name__ == "__main__":
    main()