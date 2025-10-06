#!/usr/bin/env python3
"""
Tool Scanner - Dynamic Tool Discovery
====================================

Scans the tools directory and provides agents with up-to-date tool information.
Enables dynamic tool discovery beyond initial onboarding.

V2 Compliance: ≤400 lines, focused tool discovery
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from swarm_brain import Retriever
    SWARM_BRAIN_AVAILABLE = True
except ImportError:
    SWARM_BRAIN_AVAILABLE = False
    Retriever = None


class ToolScanner:
    """Scans and categorizes available tools for agent discovery."""

    def __init__(self):
        """Initialize tool scanner."""
        self.tools_dir = project_root / "tools"
        self.tools = []
        self.categories = {}
        
        if SWARM_BRAIN_AVAILABLE:
            self.retriever = Retriever()

    def scan_all_tools(self) -> List[Dict[str, Any]]:
        """Scan all tools in the tools directory."""
        if not self.tools_dir.exists():
            print("❌ Tools directory not found")
            return []

        print(f"🔍 Scanning tools in {self.tools_dir}")
        
        for py_file in self.tools_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
                
            tool_info = self._analyze_tool_file(py_file)
            if tool_info:
                self.tools.append(tool_info)

        self._categorize_tools()
        return self.tools

    def _analyze_tool_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single tool file for metadata."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic info
            tool_info = {
                "name": file_path.name,
                "path": str(file_path.relative_to(project_root)),
                "size": file_path.stat().st_size,
                "category": self._infer_category(file_path, content),
                "description": self._extract_description(content),
                "functions": self._extract_functions(content),
                "imports": self._extract_imports(content),
                "usage_examples": self._extract_usage_examples(content)
            }
            
            return tool_info
            
        except Exception as e:
            print(f"⚠️ Error analyzing {file_path}: {e}")
            return None

    def _infer_category(self, file_path: Path, content: str) -> str:
        """Infer tool category from filename and content."""
        name_lower = file_path.name.lower()
        
        # Category mapping based on filename patterns
        if any(keyword in name_lower for keyword in ['captain', 'coordination']):
            return "coordination"
        elif any(keyword in name_lower for keyword in ['analysis', 'analyzer', 'scan']):
            return "analysis"
        elif any(keyword in name_lower for keyword in ['messaging', 'communication']):
            return "messaging"
        elif any(keyword in name_lower for keyword in ['database', 'db']):
            return "database"
        elif any(keyword in name_lower for keyword in ['deployment', 'deploy']):
            return "deployment"
        elif any(keyword in name_lower for keyword in ['cleanup', 'clean']):
            return "maintenance"
        elif any(keyword in name_lower for keyword in ['test', 'testing']):
            return "testing"
        elif any(keyword in name_lower for keyword in ['security', 'audit']):
            return "security"
        else:
            return "utility"

    def _extract_description(self, content: str) -> str:
        """Extract tool description from docstring."""
        lines = content.split('\n')
        description = ""
        
        in_docstring = False
        for line in lines:
            line = line.strip()
            if line.startswith('"""') and not in_docstring:
                in_docstring = True
                description = line.replace('"""', '').strip()
                if description:
                    break
            elif in_docstring and line.endswith('"""'):
                description += " " + line.replace('"""', '')
                break
            elif in_docstring:
                description += " " + line
        
        return description[:200] if description else "No description available"

    def _extract_functions(self, content: str) -> List[str]:
        """Extract main functions from tool file."""
        functions = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('def ') and not line.startswith('def _'):
                func_name = line.split('(')[0].replace('def ', '')
                functions.append(func_name)
        
        return functions[:5]  # Limit to first 5 functions

    def _extract_imports(self, content: str) -> List[str]:
        """Extract key imports from tool file."""
        imports = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('from ') or line.startswith('import '):
                if 'swarm_brain' in line or 'messaging' in line or 'database' in line:
                    imports.append(line)
        
        return imports[:3]  # Limit to first 3 relevant imports

    def _extract_usage_examples(self, content: str) -> List[str]:
        """Extract usage examples from comments."""
        examples = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('#') and ('python' in line.lower() or 'usage' in line.lower()):
                examples.append(line.replace('#', '').strip())
        
        return examples[:2]  # Limit to first 2 examples

    def _categorize_tools(self):
        """Categorize tools by type."""
        for tool in self.tools:
            category = tool['category']
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(tool)

    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        """Search tools by query string."""
        query_lower = query.lower()
        results = []
        
        for tool in self.tools:
            # Search in name, description, and functions
            if (query_lower in tool['name'].lower() or 
                query_lower in tool['description'].lower() or
                any(query_lower in func.lower() for func in tool['functions'])):
                results.append(tool)
        
        # If Swarm Brain is available, also search there
        if SWARM_BRAIN_AVAILABLE and len(results) < 5:
            try:
                swarm_results = self.retriever.search(f"tool {query}", k=5)
                for result in swarm_results:
                    # Add Swarm Brain results as additional context
                    results.append({
                        "name": f"Swarm Brain: {result.get('title', 'Unknown')}",
                        "description": result.get('summary', ''),
                        "source": "swarm_brain",
                        "relevance_score": result.get('score', 0)
                    })
            except Exception as e:
                print(f"⚠️ Swarm Brain search failed: {e}")
        
        return results

    def get_tool_recommendations(self, task_description: str) -> List[Dict[str, Any]]:
        """Get tool recommendations based on task description."""
        if not SWARM_BRAIN_AVAILABLE:
            return self.search_tools(task_description)
        
        try:
            # Search Swarm Brain for similar tasks and tools
            results = self.retriever.search(f"tool for {task_description}", k=10)
            recommendations = []
            
            for result in results:
                recommendations.append({
                    "name": result.get('title', 'Unknown Tool'),
                    "description": result.get('summary', ''),
                    "relevance_score": result.get('score', 0),
                    "source": "swarm_brain_pattern"
                })
            
            return recommendations
            
        except Exception as e:
            print(f"⚠️ Swarm Brain recommendation failed: {e}")
            return self.search_tools(task_description)

    def print_summary(self):
        """Print a summary of discovered tools."""
        print(f"\n📊 TOOL DISCOVERY SUMMARY")
        print(f"=" * 50)
        print(f"Total tools found: {len(self.tools)}")
        print(f"Categories: {len(self.categories)}")
        
        for category, tools in self.categories.items():
            print(f"\n🔧 {category.upper()} ({len(tools)} tools):")
            for tool in tools[:3]:  # Show first 3 in each category
                print(f"  • {tool['name']}: {tool['description'][:60]}...")
            if len(tools) > 3:
                print(f"  ... and {len(tools) - 3} more")


def main():
    """Main function for command line usage."""
    scanner = ToolScanner()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--search" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            results = scanner.search_tools(query)
            print(f"\n🔍 Search results for '{query}':")
            for result in results:
                print(f"  • {result['name']}: {result['description']}")
        elif sys.argv[1] == "--recommend" and len(sys.argv) > 2:
            task = " ".join(sys.argv[2:])
            recommendations = scanner.get_tool_recommendations(task)
            print(f"\n💡 Tool recommendations for '{task}':")
            for rec in recommendations:
                print(f"  • {rec['name']}: {rec['description']}")
        else:
            print("Usage: python tools/scan_tools.py [--search query] [--recommend task]")
    else:
        # Full scan and summary
        scanner.scan_all_tools()
        scanner.print_summary()


if __name__ == "__main__":
    main()
