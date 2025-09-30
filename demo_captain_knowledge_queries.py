#!/usr/bin/env python3
"""
Captain Knowledge Query Demonstration
===================================

Demonstrate how to query the Captain's documentation and knowledge
from the vector database for swarm intelligence.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused demonstration script
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from captain_knowledge_demo_core import CaptainKnowledgeCore


def main():
    """Main demonstration function."""
    print("🚀 Captain Knowledge Query Demonstration")
    print("=" * 60)
    print("This demo shows how the Captain's documentation is integrated")
    print("into the vector database for swarm intelligence queries.")
    print("=" * 60)

    demo = CaptainKnowledgeCore()

    # Run demonstrations
    demo.demo_captain_queries()
    demo.demo_agent_coordination_patterns()
    demo.demo_captain_specific_knowledge()
    demo.demo_knowledge_integration()
    demo.demo_vector_database_stats()

    print("\n" + "=" * 60)
    print("🎉 Captain Knowledge Integration Complete!")
    print("=" * 60)
    print("✅ Captain's documentation is now part of the swarm intelligence")
    print("✅ Agents can query Captain's knowledge for guidance")
    print("✅ Vector database provides semantic search capabilities")
    print("✅ Living documentation evolves with agent behavior")
    print("\n💡 Use these patterns in your agent coordination!")
    print("🔍 Query: 'How do agents handle X situations?'")
    print("📚 Search: 'Captain's Y procedures'")
    print("🧠 Learn: From successful patterns and outcomes")


if __name__ == "__main__":
    main()