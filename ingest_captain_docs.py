#!/usr/bin/env python3
"""
Captain Documentation Vector Database Integration - V2 Compliant (Refactored)
=============================================================================

Refactored Captain documentation ingestion importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import sys
from pathlib import Path

from captain_docs_core import CaptainDocumentationCore

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point for Captain documentation ingestion."""
    print("🚀 Starting Captain Documentation Ingestion")
    
    # Initialize core
    core = CaptainDocumentationCore()
    
    # Define paths
    captain_log_path = "captain_logs/captain_log_2025-01-17.md"
    captain_handbook_path = "docs/captain_handbook.md"
    captain_cheatsheet_path = "docs/captain_cheatsheet.md"
    
    # Ingest documentation
    log_id = core.ingest_captain_log(captain_log_path)
    handbook_id = core.ingest_captain_handbook(captain_handbook_path)
    cheatsheet_id = core.ingest_captain_cheatsheet(captain_cheatsheet_path)
    
    # Search test
    print("\n🔍 Testing Captain documentation search:")
    results = core.search_captain_docs("agent coordination", limit=3)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.get('title', 'No title')}")
    
    # Expertise test
    print("\n🧠 Testing Captain expertise retrieval:")
    expertise = core.get_captain_expertise(limit=3)
    for i, item in enumerate(expertise, 1):
        print(f"{i}. {item.get('title', 'No title')}")
    
    print(f"\n✅ Captain documentation ingestion complete!")
    print(f"📊 Ingested: Log={log_id}, Handbook={handbook_id}, Cheatsheet={cheatsheet_id}")


if __name__ == "__main__":
    main()