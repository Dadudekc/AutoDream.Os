#!/usr/bin/env python3
"""
Complete Onboarding Documentation Vector Database Integration - V2 Compliant (Refactored)
=========================================================================================

Refactored complete onboarding documentation ingestion importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import sys
from pathlib import Path

from complete_onboarding_core import CompleteOnboardingCore

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point for complete onboarding documentation ingestion."""
    print("🚀 Starting Complete Onboarding Documentation Ingestion")
    
    # Initialize core
    core = CompleteOnboardingCore()
    
    # Ingest all documentation
    agent_ids = core.ingest_agent_definitions()
    onboarding_ids = core.ingest_onboarding_managers()
    workflow_ids = core.ingest_workflow_guides()
    protocol_ids = core.ingest_agent_protocols()
    
    # Search test
    print("\n🔍 Testing onboarding documentation search:")
    results = core.search_onboarding_docs("agent onboarding", limit=3)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.get('title', 'No title')}")
    
    # Expertise test
    print("\n🧠 Testing onboarding expertise retrieval:")
    expertise = core.get_onboarding_expertise(limit=3)
    for i, item in enumerate(expertise, 1):
        print(f"{i}. {item.get('title', 'No title')}")
    
    # Summary
    total_ingested = len(agent_ids) + len(onboarding_ids) + len(workflow_ids) + len(protocol_ids)
    
    print(f"\n✅ Complete onboarding documentation ingestion complete!")
    print(f"📊 Total ingested: {total_ingested} documents")
    print(f"   🤖 Agent definitions: {len(agent_ids)}")
    print(f"   📋 Onboarding managers: {len(onboarding_ids)}")
    print(f"   🔄 Workflow guides: {len(workflow_ids)}")
    print(f"   📜 Agent protocols: {len(protocol_ids)}")


if __name__ == "__main__":
    main()