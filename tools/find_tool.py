#!/usr/bin/env python3
"""
Tool Finder - Quick Tool Discovery
================================

Quick command-line tool for finding specific tools by functionality.
Part of the dynamic tool discovery system.

V2 Compliance: ≤400 lines, focused tool finding
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.scan_tools import ToolScanner
except ImportError:
    print("❌ ToolScanner not available")
    sys.exit(1)


class ToolFinder:
    """Quick tool finder with advanced search capabilities."""

    def __init__(self):
        """Initialize tool finder."""
        self.scanner = ToolScanner()
        self.scanner.scan_all_tools()

    def find_tools(self, query: str, category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Find tools matching query with optional category filter."""
        results = self.scanner.search_tools(query)
        
        # Filter by category if specified
        if category:
            results = [r for r in results if r.get('category', '').lower() == category.lower()]
        
        return results[:limit]

    def find_tools_by_functionality(self, functionality: str) -> List[Dict[str, Any]]:
        """Find tools that provide specific functionality."""
        # Common functionality mappings
        functionality_map = {
            'database': ['database', 'db', 'sqlite', 'vector', 'swarm_brain'],
            'messaging': ['messaging', 'communication', 'discord', 'notification'],
            'analysis': ['analysis', 'analyzer', 'scan', 'review', 'audit'],
            'deployment': ['deployment', 'deploy', 'ci', 'cd', 'pipeline'],
            'cleanup': ['cleanup', 'clean', 'remove', 'delete', 'maintenance'],
            'testing': ['test', 'testing', 'validation', 'qa', 'quality'],
            'security': ['security', 'audit', 'compliance', 'vulnerability'],
            'coordination': ['captain', 'coordination', 'orchestration', 'workflow'],
            'monitoring': ['monitor', 'watch', 'observe', 'metrics', 'performance'],
            'documentation': ['doc', 'documentation', 'report', 'generate']
        }
        
        keywords = functionality_map.get(functionality.lower(), [functionality])
        results = []
        
        for keyword in keywords:
            results.extend(self.scanner.search_tools(keyword))
        
        # Remove duplicates and return unique results
        seen = set()
        unique_results = []
        for result in results:
            if result['name'] not in seen:
                seen.add(result['name'])
                unique_results.append(result)
        
        return unique_results

    def get_tool_details(self, tool_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific tool."""
        for tool in self.scanner.tools:
            if tool['name'].lower() == tool_name.lower():
                return tool
        
        return None

    def suggest_tools_for_task(self, task_description: str) -> List[Dict[str, Any]]:
        """Suggest tools for a specific task description."""
        return self.scanner.get_tool_recommendations(task_description)

    def print_tool_info(self, tool: Dict[str, Any], detailed: bool = False):
        """Print formatted tool information."""
        print(f"\n🔧 {tool['name']}")
        print(f"   Path: {tool['path']}")
        print(f"   Category: {tool.get('category', 'unknown')}")
        print(f"   Description: {tool['description']}")
        
        if detailed:
            if tool['functions']:
                print(f"   Functions: {', '.join(tool['functions'])}")
            if tool['usage_examples']:
                print(f"   Usage Examples:")
                for example in tool['usage_examples']:
                    print(f"     {example}")
            if tool['imports']:
                print(f"   Key Imports:")
                for imp in tool['imports']:
                    print(f"     {imp}")


def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description="Find tools by functionality")
    parser.add_argument("--query", "-q", help="Search query for tool functionality")
    parser.add_argument("--category", "-c", help="Filter by tool category")
    parser.add_argument("--functionality", "-f", help="Find tools by functionality type")
    parser.add_argument("--task", "-t", help="Suggest tools for specific task")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed information")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Limit number of results")
    
    args = parser.parse_args()
    
    finder = ToolFinder()
    
    if args.query:
        results = finder.find_tools(args.query, args.category, args.limit)
        print(f"\n🔍 Search results for '{args.query}':")
        for result in results:
            finder.print_tool_info(result, args.detailed)
    
    elif args.functionality:
        results = finder.find_tools_by_functionality(args.functionality)
        print(f"\n🔧 Tools for {args.functionality} functionality:")
        for result in results:
            finder.print_tool_info(result, args.detailed)
    
    elif args.task:
        results = finder.suggest_tools_for_task(args.task)
        print(f"\n💡 Tool suggestions for task: '{args.task}':")
        for result in results:
            finder.print_tool_info(result, args.detailed)
    
    else:
        print("❌ Please specify --query, --functionality, or --task")
        print("\nExamples:")
        print("  python tools/find_tool.py --query 'database'")
        print("  python tools/find_tool.py --functionality 'analysis'")
        print("  python tools/find_tool.py --task 'clean up old files'")
        print("  python tools/find_tool.py --query 'captain' --detailed")


if __name__ == "__main__":
    main()
