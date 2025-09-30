#!/usr/bin/env python3
"""
Core logic for onboarding knowledge query demonstration.
"""

from swarm_brain import Retriever, SwarmBrain


class OnboardingKnowledgeDemo:
    """Demonstrate onboarding knowledge queries."""
    
    def __init__(self):
        """Initialize the demo."""
        self.retriever = Retriever(SwarmBrain())
    
    def query_agent_roles(self):
        """Query agent roles and responsibilities."""
        print("\n🤖 Query 1: What are the agent roles and responsibilities?")
        print("-" * 50)
        results = self.retriever.search("agent roles and responsibilities", k=3)
        for i, result in enumerate(results, 1):
            if isinstance(result, dict):
                print(f"{i}. {result.get('title', 'Unknown')}")
                print(f"   Agent: {result.get('agent_id', 'Unknown')}")
                print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    def query_captain_onboarding(self):
        """Query captain onboarding process."""
        print("\n👑 Query 2: How does the captain onboarding process work?")
        print("-" * 50)
        results = self.retriever.search("captain onboarding process", k=3)
        for i, result in enumerate(results, 1):
            if isinstance(result, dict):
                print(f"{i}. {result.get('title', 'Unknown')}")
                print(f"   Type: {result.get('kind', 'Unknown')}")
                print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    def query_workflow_system(self):
        """Query workflow system usage."""
        print("\n📋 Query 3: How do I use the workflow system?")
        print("-" * 50)
        results = self.retriever.search("workflow system usage", k=3)
        for i, result in enumerate(results, 1):
            if isinstance(result, dict):
                print(f"{i}. {result.get('title', 'Unknown')}")
                print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    def query_discord_commander(self):
        """Query Discord commander setup."""
        print("\n💬 Query 4: How do I set up the Discord commander?")
        print("-" * 50)
        results = self.retriever.search("discord commander setup", k=3)
        for i, result in enumerate(results, 1):
            if isinstance(result, dict):
                print(f"{i}. {result.get('title', 'Unknown')}")
                print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    def query_agent_messaging(self):
        """Query agent messaging workflow."""
        print("\n📨 Query 5: How does agent messaging workflow work?")
        print("-" * 50)
        results = self.retriever.search("agent messaging workflow", k=3)
        for i, result in enumerate(results, 1):
            if isinstance(result, dict):
                print(f"{i}. {result.get('title', 'Unknown')}")
                print(f"   Summary: {result.get('summary', 'No summary')[:100]}...")
    
    def run_demo(self):
        """Run the complete demonstration."""
        print("🎯 Onboarding Knowledge Query Demonstrations")
        print("=" * 60)
        
        self.query_agent_roles()
        self.query_captain_onboarding()
        self.query_workflow_system()
        self.query_discord_commander()
        self.query_agent_messaging()
        
        print("\n" + "=" * 60)
        print("🎉 All onboarding documentation is now in the vector database!")
        print("🔍 You can query any aspect of agent setup, roles, or workflows.")
        print("📚 The local files can now be safely deleted.")
