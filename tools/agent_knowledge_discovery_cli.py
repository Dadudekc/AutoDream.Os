#!/usr/bin/env python3
"""
Agent Knowledge Discovery CLI
==============================

Command-line interface for agents to discover protocols, guides, and knowledge.
Makes swarm_vector_integration accessible via CLI for quick lookups during cycles.

Usage:
    python tools/agent_knowledge_discovery_cli.py search "gas pipeline"
    python tools/agent_knowledge_discovery_cli.py quick-ref anti_stop
    python tools/agent_knowledge_discovery_cli.py cycle-context DUP_FIX
    python tools/agent_knowledge_discovery_cli.py search-knowledge "validation patterns"

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-10-17
Mission: Cycle 10 - Make knowledge discovery CLI-accessible
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.swarm_vector_integration import (
    search_protocols,
    get_cycle_context,
    get_quick_ref,
    SwarmVectorIntegration
)


def cmd_search_protocols(args):
    """Search protocols command."""
    print(f"🔍 Searching protocols for: '{args.query}'\n")
    print("=" * 80)
    
    results = search_protocols(args.query, agent_id=args.agent)
    
    if not results:
        print("❌ No protocols found matching query.")
        return
    
    print(f"✅ Found {len(results)} relevant protocols:\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. 📚 {result['title']}")
        print(f"   File: {result['file']}")
        print(f"   Preview: {result['content'][:200]}...")
        print()
    
    print("=" * 80)
    print(f"✅ {len(results)} protocols found!")


def cmd_quick_ref(args):
    """Quick reference command."""
    print(f"📖 Quick Reference: {args.topic}\n")
    print("=" * 80)
    
    ref = get_quick_ref(args.topic, agent_id=args.agent)
    
    if not ref:
        print(f"❌ No quick reference available for '{args.topic}'")
        print("\n📋 Available topics:")
        print("  - gas_pipeline")
        print("  - anti_stop")
        print("  - v2_compliance")
        print("  - strategic_rest")
        print("  - code_first")
        return
    
    print(f"✅ {args.topic.upper()}:\n")
    print(f"   {ref}\n")
    print("=" * 80)


def cmd_cycle_context(args):
    """Cycle context command."""
    print(f"🎯 Cycle Context: {args.cycle_type}\n")
    print("=" * 80)
    
    context = get_cycle_context(args.cycle_type, agent_id=args.agent)
    
    if not context:
        print(f"❌ No context available for '{args.cycle_type}'")
        print("\n📋 Available cycle types:")
        print("  - DUP_FIX")
        print("  - REPO_ANALYSIS")
        print("  - TESTING")
        print("  - ANTI_STOP")
        return
    
    print(f"✅ Context for {args.cycle_type}:\n")
    
    if 'protocols' in context:
        print("📚 Protocols to follow:")
        for protocol in context['protocols']:
            print(f"   - {protocol}")
        print()
    
    if 'best_practices' in context:
        print("✅ Best Practices:")
        for practice in context['best_practices']:
            print(f"   - {practice}")
        print()
    
    if 'success_metrics' in context:
        print("🎯 Success Metrics:")
        for metric, value in context['success_metrics'].items():
            print(f"   - {metric}: {value}")
        print()
    
    print("=" * 80)


def cmd_search_knowledge(args):
    """Search swarm knowledge command."""
    print(f"🧠 Searching swarm knowledge for: '{args.query}'\n")
    print("=" * 80)
    
    integration = SwarmVectorIntegration(agent_id=args.agent)
    results = integration.search_swarm_knowledge(args.query, agent_context=True)
    
    if not results:
        print("❌ No knowledge entries found.")
        return
    
    print(f"✅ Found {len(results)} knowledge entries:\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. 🧠 {result['type'].upper()}")
        print(f"   Source: {result['source']}")
        print(f"   Preview: {result['content'][:150]}...")
        print(f"   Agent Relevant: {'✅' if result['agent_relevant'] else '❌'}")
        print()
    
    print("=" * 80)
    print(f"✅ {len(results)} entries found!")


def cmd_list_resources(args):
    """List all available resources."""
    print("🧠 AGENT KNOWLEDGE DISCOVERY RESOURCES\n")
    print("=" * 80)
    
    print("\n📋 QUICK REFERENCES:")
    topics = ['gas_pipeline', 'anti_stop', 'v2_compliance', 'strategic_rest', 'code_first']
    for topic in topics:
        ref = get_quick_ref(topic)
        print(f"  {topic}: {ref[:60]}...")
    
    print("\n\n🎯 CYCLE CONTEXTS:")
    cycles = ['DUP_FIX', 'REPO_ANALYSIS', 'TESTING', 'ANTI_STOP']
    for cycle in cycles:
        context = get_cycle_context(cycle)
        if context:
            print(f"  {cycle}: {len(context.get('protocols', []))} protocols, "
                  f"{len(context.get('best_practices', []))} practices")
    
    print("\n\n📚 PROTOCOL DIRECTORIES:")
    print("  - swarm_brain/protocols/ (22+ protocols)")
    print("  - swarm_brain/procedures/ (15+ procedures)")
    print("  - docs/ (28+ guides)")
    
    print("\n" + "=" * 80)
    print("✅ Use 'search', 'quick-ref', or 'cycle-context' commands to access!")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Agent Knowledge Discovery - Find protocols, guides, and knowledge',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/agent_knowledge_discovery_cli.py search "gas pipeline"
  python tools/agent_knowledge_discovery_cli.py quick-ref anti_stop
  python tools/agent_knowledge_discovery_cli.py cycle-context DUP_FIX
  python tools/agent_knowledge_discovery_cli.py search-knowledge "validation"
  python tools/agent_knowledge_discovery_cli.py list
        """
    )
    
    parser.add_argument('--agent', type=str, default='Agent-5',
                       help='Agent ID (default: Agent-5)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Search protocols
    search_parser = subparsers.add_parser('search', help='Search protocols')
    search_parser.add_argument('query', type=str, help='Search query')
    
    # Quick reference
    quick_parser = subparsers.add_parser('quick-ref', help='Get quick reference')
    quick_parser.add_argument('topic', type=str, help='Topic name')
    
    # Cycle context
    context_parser = subparsers.add_parser('cycle-context', help='Get cycle context')
    context_parser.add_argument('cycle_type', type=str, help='Cycle type')
    
    # Search knowledge
    knowledge_parser = subparsers.add_parser('search-knowledge', help='Search swarm knowledge')
    knowledge_parser.add_argument('query', type=str, help='Search query')
    
    # List resources
    subparsers.add_parser('list', help='List all available resources')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to appropriate command
    if args.command == 'search':
        cmd_search_protocols(args)
    elif args.command == 'quick-ref':
        cmd_quick_ref(args)
    elif args.command == 'cycle-context':
        cmd_cycle_context(args)
    elif args.command == 'search-knowledge':
        cmd_search_knowledge(args)
    elif args.command == 'list':
        cmd_list_resources(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

