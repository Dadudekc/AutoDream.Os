#!/usr/bin/env python3
"""
Agent Vector Search Tool
========================

Simple tool for agents to search their collective knowledge using vector database.
Enables semantic search across all agent messages and experiences.

Author: Agent-4 (Captain)
Date: 2025-01-15
V2 Compliance: ≤400 lines, modular design
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.services.messaging.enhanced_messaging_service import get_enhanced_messaging_service
    from src.services.vector_database.vector_database_integration import VectorDatabaseIntegration

    VECTOR_DB_AVAILABLE = True
except ImportError as e:
    print(f"❌ Vector database not available: {e}")
    VECTOR_DB_AVAILABLE = False


def search_similar_messages(
    query: str, agent_id: str = None, limit: int = 5
) -> list[dict[str, Any]]:
    """Search for similar messages using vector database."""
    if not VECTOR_DB_AVAILABLE:
        print("❌ Vector database not available")
        return []

    try:
        messaging_service = get_enhanced_messaging_service()
        results = messaging_service.search_similar_messages(query, agent_id, limit)
        return results
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []


def search_agent_experience(agent_id: str, query: str, limit: int = 3) -> list[dict[str, Any]]:
    """Search for similar experiences from an agent's history."""
    if not VECTOR_DB_AVAILABLE:
        print("❌ Vector database not available")
        return []

    try:
        messaging_service = get_enhanced_messaging_service()
        results = messaging_service.search_agent_experience(agent_id, query, limit)
        return results
    except Exception as e:
        print(f"❌ Experience search failed: {e}")
        return []


def get_agent_knowledge_summary(agent_id: str, time_range_hours: int = 24) -> dict[str, Any]:
    """Get knowledge summary for an agent."""
    if not VECTOR_DB_AVAILABLE:
        return {"error": "Vector database not available"}

    try:
        messaging_service = get_enhanced_messaging_service()
        summary = messaging_service.get_agent_knowledge_summary(agent_id, time_range_hours)
        return summary
    except Exception as e:
        return {"error": str(e)}


def get_swarm_knowledge_summary() -> dict[str, Any]:
    """Get summary of swarm knowledge."""
    if not VECTOR_DB_AVAILABLE:
        return {"error": "Vector database not available"}

    try:
        messaging_service = get_enhanced_messaging_service()
        summary = messaging_service.get_swarm_knowledge_summary()
        return summary
    except Exception as e:
        return {"error": str(e)}


def print_search_results(results: list[dict[str, Any]], query: str):
    """Print search results in a readable format."""
    if not results:
        print(f"🔍 No similar messages found for: '{query}'")
        return

    print(f"🔍 Found {len(results)} similar messages for: '{query}'")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        similarity = result.get("similarity", 0)
        content = (
            result.get("content", "")[:100] + "..."
            if len(result.get("content", "")) > 100
            else result.get("content", "")
        )
        from_agent = result.get("from_agent", "Unknown")
        to_agent = result.get("to_agent", "Unknown")
        timestamp = result.get("timestamp", "Unknown")
        priority = result.get("priority", "NORMAL")

        print(f"\n{i}. Similarity: {similarity:.2f} | Priority: {priority}")
        print(f"   From: {from_agent} → To: {to_agent}")
        print(f"   Time: {timestamp}")
        print(f"   Content: {content}")


def print_experience_results(results: list[dict[str, Any]], agent_id: str, query: str):
    """Print experience search results."""
    if not results:
        print(f"🧠 No similar experiences found for {agent_id}: '{query}'")
        return

    print(f"🧠 Found {len(results)} similar experiences for {agent_id}: '{query}'")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        relevance = result.get("relevance", 0)
        experience = (
            result.get("experience", "")[:100] + "..."
            if len(result.get("experience", "")) > 100
            else result.get("experience", "")
        )
        context = result.get("context", "Unknown")
        timestamp = result.get("timestamp", "Unknown")
        priority = result.get("priority", "NORMAL")

        print(f"\n{i}. Relevance: {relevance:.2f} | Priority: {priority}")
        print(f"   Context: {context}")
        print(f"   Time: {timestamp}")
        print(f"   Experience: {experience}")


def main():
    """Main function for agent vector search tool."""
    parser = argparse.ArgumentParser(description="Agent Vector Search Tool")
    parser.add_argument("--agent", help="Agent ID (e.g., Agent-1, Agent-2)")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results")
    parser.add_argument(
        "--experience", action="store_true", help="Search agent experiences instead of messages"
    )
    parser.add_argument(
        "--knowledge-summary", action="store_true", help="Get agent knowledge summary"
    )
    parser.add_argument("--swarm-summary", action="store_true", help="Get swarm knowledge summary")
    parser.add_argument("--status", action="store_true", help="Check vector database status")

    args = parser.parse_args()

    # Check vector database status
    if args.status:
        if VECTOR_DB_AVAILABLE:
            try:
                messaging_service = get_enhanced_messaging_service()
                status = messaging_service.get_vector_db_status()
                print("✅ Vector Database Status:")
                print(json.dumps(status, indent=2))
            except Exception as e:
                print(f"❌ Status check failed: {e}")
        else:
            print("❌ Vector database not available")
        return

    # Get swarm knowledge summary
    if args.swarm_summary:
        summary = get_swarm_knowledge_summary()
        print("🐝 Swarm Knowledge Summary:")
        print(json.dumps(summary, indent=2))
        return

    # Get agent knowledge summary
    if args.knowledge_summary:
        if not args.agent:
            print("❌ Agent ID required for knowledge summary")
            return

        summary = get_agent_knowledge_summary(args.agent, 24)
        print(f"🧠 Knowledge Summary for {args.agent}:")
        print(json.dumps(summary, indent=2))
        return

    # Search agent experiences
    if args.experience:
        if not args.agent:
            print("❌ Agent ID required for experience search")
            return

        results = search_agent_experience(args.agent, args.query, args.limit)
        print_experience_results(results, args.agent, args.query)
        return

    # Search similar messages
    if args.query:
        results = search_similar_messages(args.query, args.agent, args.limit)
        print_search_results(results, args.query)
    else:
        print("❌ Query required for message search. Use --query 'your search term'")


if __name__ == "__main__":
    main()
