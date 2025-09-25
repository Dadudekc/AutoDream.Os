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
from typing import List, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from swarm_brain import SwarmBrain, Retriever


class CaptainKnowledgeDemo:
    """Demonstrate Captain knowledge queries from vector database."""
    
    def __init__(self):
        """Initialize the knowledge demo."""
        self.brain = SwarmBrain()
        self.retriever = Retriever(self.brain)
        print("🧠 Captain Knowledge Demo initialized")
    
    def demo_captain_queries(self):
        """Demonstrate various Captain knowledge queries."""
        print("🎯 Captain Knowledge Query Demonstrations")
        print("=" * 50)
        
        # Query 1: Daily Operations Protocol
        print("\n📋 Query 1: Captain's Daily Operations Protocol")
        print("-" * 40)
        results = self.retriever.search("Captain's daily operations protocol", k=3)
        self._display_results(results, "Daily Operations")
        
        # Query 2: Swarm Coordination Strategies
        print("\n🤖 Query 2: Swarm Coordination Strategies")
        print("-" * 40)
        results = self.retriever.search("swarm coordination strategies", k=3)
        self._display_results(results, "Swarm Coordination")
        
        # Query 3: Agent Leadership Responsibilities
        print("\n👑 Query 3: Agent Leadership Responsibilities")
        print("-" * 40)
        results = self.retriever.search("agent leadership responsibilities", k=3)
        self._display_results(results, "Leadership")
        
        # Query 4: Strategic Directives Management
        print("\n🎯 Query 4: Strategic Directives Management")
        print("-" * 40)
        results = self.retriever.search("strategic directives management", k=3)
        self._display_results(results, "Strategic Directives")
        
        # Query 5: Quality Assurance Protocols
        print("\n✅ Query 5: Quality Assurance Protocols")
        print("-" * 40)
        results = self.retriever.search("quality assurance protocols", k=3)
        self._display_results(results, "Quality Assurance")
        
        # Query 6: Crisis Management Procedures
        print("\n🚨 Query 6: Crisis Management Procedures")
        print("-" * 40)
        results = self.retriever.search("crisis management procedures", k=3)
        self._display_results(results, "Crisis Management")
    
    def demo_agent_coordination_patterns(self):
        """Demonstrate agent coordination pattern queries."""
        print("\n\n🔄 Agent Coordination Pattern Queries")
        print("=" * 50)
        
        # Query 1: How do agents coordinate tasks?
        print("\n📋 Query: How do agents coordinate tasks?")
        print("-" * 40)
        patterns = self.retriever.how_do_agents_do("coordinate tasks", k=5)
        self._display_patterns(patterns, "Task Coordination")
        
        # Query 2: How do agents handle V2 refactoring?
        print("\n🔧 Query: How do agents handle V2 refactoring?")
        print("-" * 40)
        patterns = self.retriever.how_do_agents_do("V2 refactoring", k=5)
        self._display_patterns(patterns, "V2 Refactoring")
        
        # Query 3: How do agents manage quality?
        print("\n✅ Query: How do agents manage quality?")
        print("-" * 40)
        patterns = self.retriever.how_do_agents_do("manage quality", k=5)
        self._display_patterns(patterns, "Quality Management")
    
    def demo_captain_specific_knowledge(self):
        """Demonstrate Captain-specific knowledge queries."""
        print("\n\n👑 Captain-Specific Knowledge Queries")
        print("=" * 50)
        
        # Query 1: Captain's strategic framework
        print("\n🎯 Query: Captain's strategic framework")
        print("-" * 40)
        results = self.retriever.search("Captain strategic framework", k=3)
        self._display_results(results, "Strategic Framework")
        
        # Query 2: Captain's performance metrics
        print("\n📊 Query: Captain's performance metrics")
        print("-" * 40)
        results = self.retriever.search("Captain performance metrics", k=3)
        self._display_results(results, "Performance Metrics")
        
        # Query 3: Captain's decision-making process
        print("\n🧠 Query: Captain's decision-making process")
        print("-" * 40)
        results = self.retriever.search("Captain decision making process", k=3)
        self._display_results(results, "Decision Making")
    
    def demo_knowledge_integration(self):
        """Demonstrate how Captain knowledge integrates with agent actions."""
        print("\n\n🔗 Knowledge Integration Demonstration")
        print("=" * 50)
        
        # Show how Captain's knowledge can guide agent actions
        print("\n💡 Example: How Captain's knowledge guides agent coordination")
        print("-" * 50)
        
        # Query for coordination patterns
        coordination_patterns = self.retriever.how_do_agents_do("successful coordination", k=3)
        
        if coordination_patterns:
            print("📋 Found successful coordination patterns:")
            for pattern in coordination_patterns:
                print(f"   • {pattern.get('title', 'Unknown')} by {pattern.get('agent_id', 'Unknown')}")
                print(f"     Outcome: {pattern.get('outcome', 'Unknown')}")
                print(f"     Tool: {pattern.get('tool', 'Unknown')}")
        
        # Query for Captain's operational wisdom
        captain_wisdom = self.retriever.search("Captain operational wisdom", k=2)
        
        if captain_wisdom:
            print("\n👑 Captain's operational wisdom:")
            for result in captain_wisdom:
                if isinstance(result, dict):
                    print(f"   • {result.get('title', 'Unknown')}")
                    print(f"     Summary: {result.get('summary', 'No summary')[:100]}...")
    
    def _display_results(self, results: List[Any], category: str):
        """Display search results in a formatted way."""
        if not results:
            print(f"❌ No results found for {category}")
            return
        
        print(f"✅ Found {len(results)} results for {category}:")
        
        for i, result in enumerate(results, 1):
            if isinstance(result, dict):
                title = result.get('title', 'Unknown')
                agent_id = result.get('agent_id', 'Unknown')
                kind = result.get('kind', 'Unknown')
                summary = result.get('summary', 'No summary')[:100]
                
                print(f"   {i}. {title}")
                print(f"      Agent: {agent_id} | Type: {kind}")
                print(f"      Summary: {summary}...")
            else:
                print(f"   {i}. {result}")
            print()
    
    def _display_patterns(self, patterns: List[Dict], category: str):
        """Display agent patterns in a formatted way."""
        if not patterns:
            print(f"❌ No patterns found for {category}")
            return
        
        print(f"✅ Found {len(patterns)} patterns for {category}:")
        
        for i, pattern in enumerate(patterns, 1):
            title = pattern.get('title', 'Unknown')
            agent_id = pattern.get('agent_id', 'Unknown')
            outcome = pattern.get('outcome', 'Unknown')
            tool = pattern.get('tool', 'Unknown')
            
            print(f"   {i}. {title}")
            print(f"      Agent: {agent_id} | Tool: {tool} | Outcome: {outcome}")
            print()
    
    def demo_vector_database_stats(self):
        """Show vector database statistics."""
        print("\n\n📊 Vector Database Statistics")
        print("=" * 50)
        
        try:
            # Get basic stats
            total_docs = self.brain.get_total_documents()
            captain_docs = len([d for d in self.brain.get_all_documents() 
                              if 'captain' in d.get('tags', '').lower()])
            
            print(f"📚 Total Documents: {total_docs}")
            print(f"👑 Captain Documents: {captain_docs}")
            print(f"📈 Captain Knowledge Coverage: {(captain_docs/total_docs)*100:.1f}%")
            
            # Show document types
            doc_types = {}
            for doc in self.brain.get_all_documents():
                kind = doc.get('kind', 'unknown')
                doc_types[kind] = doc_types.get(kind, 0) + 1
            
            print("\n📋 Document Types:")
            for kind, count in sorted(doc_types.items()):
                print(f"   • {kind}: {count}")
                
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")


def main():
    """Main demonstration function."""
    print("🚀 Captain Knowledge Query Demonstration")
    print("=" * 60)
    print("This demo shows how the Captain's documentation is integrated")
    print("into the vector database for swarm intelligence queries.")
    print("=" * 60)
    
    demo = CaptainKnowledgeDemo()
    
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



