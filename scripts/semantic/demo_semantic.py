#!/usr/bin/env python3
"""
Semantic Search Demo - Showcases agent coordination intelligence
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.semantic.router_hooks import route_message, similar_status


def demo_routing():
    """Demonstrate intelligent task routing."""
    print("🎯 SEMANTIC TASK ROUTING DEMO")
    print("=" * 50)

    tasks = [
        "fix critical security vulnerability in authentication system",
        "design new user interface for dashboard analytics",
        "optimize database query performance and add monitoring",
        "coordinate deployment of microservices architecture",
        "analyze system performance bottlenecks and bottlenecks",
    ]

    for task in tasks:
        print(f"\n📋 Task: {task}")
        result = route_message(task)

        print(f"🎯 Priority: {result['priority']}")

        print("🤖 Agent Suggestions:")
        for i, agent in enumerate(result["agent_suggestions"][:3], 1):
            print(".3f")

        if "context_hits" in result and result["context_hits"]:
            print("📊 Context Insights:")
            for i, hit in enumerate(result["context_hits"][:2], 1):
                agent_id = hit["meta"].get("agent_id", hit["id"])
                status = hit["meta"].get("status", "Unknown")
                print(".3f")


def demo_similarity():

EXAMPLE USAGE:
==============

# Run the script directly
python demo_semantic.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.semantic.demo_semantic import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.semantic.demo_semantic import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

    """Demonstrate status similarity search."""
    print("\n🔍 STATUS SIMILARITY SEARCH DEMO")
    print("=" * 50)

    queries = [
        "survey completed successfully",
        "infrastructure audit in progress",
        "consolidation planning phase",
    ]

    for query in queries:
        print(f"\n🔎 Query: '{query}'")
        result = similar_status(query)

        print("📋 Similar Statuses:")
        for i, hit in enumerate(result["results"][:3], 1):
            agent_id = hit["meta"].get("agent_id", hit["id"])
            status = hit["meta"].get("status", "Unknown")
            print(".3f")


if __name__ == "__main__":
    print("🧠 AGENT COORDINATION INTELLIGENCE DEMO")
    print("Powered by Semantic Search & Vector Similarity")
    print()

    try:
        demo_routing()
        demo_similarity()

        print("\n" + "=" * 50)
        print("✅ SEMANTIC SEARCH DEMO COMPLETED SUCCESSFULLY!")
        print("🎉 Agent coordination intelligence is operational!")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()
