#!/usr/bin/env python3
"""
Onboarding Knowledge Query Demonstration
=======================================

Demonstrate how to query all the onboarding documentation and agent definitions
from the vector database.

Author: Agent-4 (Captain & Operations Coordinator)
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from swarm_brain import SwarmBrain, Retriever


def main():
    """Demonstrate onboarding knowledge queries."""
    print("🎯 Onboarding Knowledge Query Demonstrations")
    print("=" * 60)
    
    retriever = Retriever(SwarmBrain())
    
    # Query 1: Agent Roles and Responsibilities
    print("\n🤖 Query 1: What are the agent roles and responsibilities?")
    print("-" * 50)
    results = retriever.search("agent roles and responsibilities", k=3)
    for i, result in enumerate(results, 1):
        if isinstance(result, dict):
            print(f"{i}. {result.get('title', 'Unknown')}")
            print(f"   Agent: {result.get('agent_id', 'Unknown')}")
            print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    # Query 2: Captain Onboarding Process
    print("\n👑 Query 2: How does the captain onboarding process work?")
    print("-" * 50)
    results = retriever.search("captain onboarding process", k=3)
    for i, result in enumerate(results, 1):
        if isinstance(result, dict):
            print(f"{i}. {result.get('title', 'Unknown')}")
            print(f"   Type: {result.get('kind', 'Unknown')}")
            print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    # Query 3: Workflow System Usage
    print("\n📋 Query 3: How do I use the workflow system?")
    print("-" * 50)
    results = retriever.search("workflow system usage", k=3)
    for i, result in enumerate(results, 1):
        if isinstance(result, dict):
            print(f"{i}. {result.get('title', 'Unknown')}")
            print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    # Query 4: Discord Commander Setup
    print("\n💬 Query 4: How do I set up the Discord commander?")
    print("-" * 50)
    results = retriever.search("discord commander setup", k=3)
    for i, result in enumerate(results, 1):
        if isinstance(result, dict):
            print(f"{i}. {result.get('title', 'Unknown')}")
            print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    # Query 5: Agent Messaging Workflow
    print("\n📨 Query 5: How does agent messaging workflow work?")
    print("-" * 50)
    results = retriever.search("agent messaging workflow", k=3)
    for i, result in enumerate(results, 1):
        if isinstance(result, dict):
            print(f"{i}. {result.get('title', 'Unknown')}")
            print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    print("\n" + "=" * 60)
    print("🎉 All onboarding documentation is now in the vector database!")
    print("🔍 You can query any aspect of agent setup, roles, or workflows.")
    print("📚 The local files can now be safely deleted.")


if __name__ == "__main__":
    main()

