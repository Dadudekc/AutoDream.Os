#!/usr/bin/env python3
"""
Knowledge Base Search Tool
==========================

Quick search tool for Agent Knowledge Base to find solutions without asking.
Searches through established patterns, solutions, and answers.

Agent-3: Infrastructure & DevOps Specialist
Mission: V3 Infrastructure Deployment
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logger = None


class KnowledgeBaseSearch:
    """Knowledge Base Search Tool."""
    
    def __init__(self, knowledge_base_path: str = "docs/AGENT_KNOWLEDGE_BASE.md"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.content = self._load_knowledge_base()
        self.sections = self._parse_sections()
    
    def _load_knowledge_base(self) -> str:
        """Load knowledge base content."""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def _parse_sections(self) -> Dict[str, str]:
        """Parse knowledge base into sections."""
        sections = {}
        current_section = ""
        current_content = []
        
        for line in self.content.split('\n'):
            if line.startswith('## ') and not line.startswith('###'):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line[3:].strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def search(self, query: str, category: Optional[str] = None) -> List[Dict[str, str]]:
        """Search knowledge base for solutions."""
        results = []
        query_lower = query.lower()
        
        # Search in specific category or all sections
        sections_to_search = [category] if category and category in self.sections else self.sections.keys()
        
        for section_name in sections_to_search:
            section_content = self.sections[section_name]
            
            # Look for Q&A patterns
            qa_pattern = r'### \*\*(.+?)\*\*\s*\n\*\*Question\*\*: (.+?)\n\*\*Solution\*\*: (.+?)(?=\n###|\n##|\Z)'
            qa_matches = re.findall(qa_pattern, section_content, re.DOTALL)
            
            for match in qa_matches:
                title, question, solution = match
                if self._matches_query(query_lower, question + " " + solution):
                    results.append({
                        'section': section_name,
                        'title': title.strip(),
                        'question': question.strip(),
                        'solution': solution.strip(),
                        'relevance': self._calculate_relevance(query_lower, question + " " + solution)
                    })
            
            # Look for problem-solution patterns
            problem_pattern = r'\*\*Problem\*\*: (.+?)\n\*\*Solution\*\*: (.+?)(?=\n\*\*|\n##|\Z)'
            problem_matches = re.findall(problem_pattern, section_content, re.DOTALL)
            
            for match in problem_matches:
                problem, solution = match
                if self._matches_query(query_lower, problem + " " + solution):
                    results.append({
                        'section': section_name,
                        'title': f"Problem: {problem[:50]}...",
                        'question': problem.strip(),
                        'solution': solution.strip(),
                        'relevance': self._calculate_relevance(query_lower, problem + " " + solution)
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results
    
    def _matches_query(self, query: str, text: str) -> bool:
        """Check if query matches text."""
        text_lower = text.lower()
        
        # Exact phrase match
        if query in text_lower:
            return True
        
        # Individual word matches
        query_words = query.split()
        text_words = text_lower.split()
        
        # Check if all query words appear in text
        return all(any(word in text_word for text_word in text_words) for word in query_words)
    
    def _calculate_relevance(self, query: str, text: str) -> float:
        """Calculate relevance score."""
        text_lower = text.lower()
        query_words = query.split()
        
        score = 0.0
        
        # Exact phrase match gets highest score
        if query in text_lower:
            score += 10.0
        
        # Word matches
        for word in query_words:
            if word in text_lower:
                score += 1.0
        
        # Bonus for question matches
        if any(word in text_lower for word in ['question', 'how do i', 'what is']):
            score += 0.5
        
        return score
    
    def get_categories(self) -> List[str]:
        """Get available categories."""
        return list(self.sections.keys())
    
    def get_quick_solutions(self, limit: int = 5) -> List[Dict[str, str]]:
        """Get quick solutions for common problems."""
        common_problems = [
            "import error",
            "json serialization",
            "dataclass error",
            "encoding error",
            "v2 compliance",
            "messaging system",
            "branch management",
            "commit message",
            "git workflow",
            "quality gates"
        ]
        
        results = []
        for problem in common_problems:
            matches = self.search(problem)
            if matches:
                results.extend(matches[:2])  # Top 2 matches per problem
        
        return results[:limit]


def print_search_results(results: List[Dict[str, str]], query: str) -> None:
    """Print search results."""
    if not results:
        print(f"❌ No solutions found for: '{query}'")
        print("\n💡 Try these common searches:")
        print("  • import error")
        print("  • json serialization")
        print("  • v2 compliance")
        print("  • messaging system")
        print("  • git workflow")
        return
    
    print(f"🔍 Found {len(results)} solution(s) for: '{query}'")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        print(f"\n📋 Solution {i}: {result['title']}")
        print(f"📁 Category: {result['section']}")
        print(f"❓ Question: {result['question']}")
        print(f"✅ Solution: {result['solution'][:200]}{'...' if len(result['solution']) > 200 else ''}")
        print("-" * 40)


def print_quick_solutions(solutions: List[Dict[str, str]]) -> None:
    """Print quick solutions."""
    print("🚀 QUICK SOLUTIONS - Common Problems")
    print("=" * 80)
    
    for i, solution in enumerate(solutions, 1):
        print(f"\n{i}. {solution['title']}")
        print(f"   ❓ {solution['question'][:100]}{'...' if len(solution['question']) > 100 else ''}")
        print(f"   ✅ {solution['solution'][:150]}{'...' if len(solution['solution']) > 150 else ''}")
        print("-" * 40)


def main():
    """Main function for Knowledge Base Search."""
    parser = argparse.ArgumentParser(description="Knowledge Base Search Tool")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--category", help="Search in specific category")
    parser.add_argument("--list-categories", action="store_true", help="List available categories")
    parser.add_argument("--quick-solutions", action="store_true", help="Show quick solutions for common problems")
    parser.add_argument("--interactive", action="store_true", help="Interactive search mode")
    
    args = parser.parse_args()
    
    search_tool = KnowledgeBaseSearch()
    
    if args.list_categories:
        print("📚 Available Categories:")
        for category in search_tool.get_categories():
            print(f"  • {category}")
        return
    
    if args.quick_solutions:
        solutions = search_tool.get_quick_solutions()
        print_quick_solutions(solutions)
        return
    
    if args.interactive:
        print("🔍 Interactive Knowledge Base Search")
        print("Type 'quit' to exit, 'help' for commands")
        print("-" * 40)
        
        while True:
            query = input("\n🔍 Search: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if query.lower() == 'help':
                print("\n📚 Commands:")
                print("  • Type any search query")
                print("  • 'categories' - list available categories")
                print("  • 'quick' - show quick solutions")
                print("  • 'quit' - exit")
                continue
            
            if query.lower() == 'categories':
                print("\n📚 Available Categories:")
                for category in search_tool.get_categories():
                    print(f"  • {category}")
                continue
            
            if query.lower() == 'quick':
                solutions = search_tool.get_quick_solutions()
                print_quick_solutions(solutions)
                continue
            
            if query:
                results = search_tool.search(query)
                print_search_results(results, query)
    
    elif args.query:
        results = search_tool.search(args.query, args.category)
        print_search_results(results, args.query)
    
    else:
        # Show quick solutions by default
        solutions = search_tool.get_quick_solutions()
        print_quick_solutions(solutions)
        
        print("\n💡 Usage Examples:")
        print("  python tools/knowledge_base_search.py 'import error'")
        print("  python tools/knowledge_base_search.py --category 'Infrastructure' 'database'")
        print("  python tools/knowledge_base_search.py --interactive")
        print("  python tools/knowledge_base_search.py --quick-solutions")


if __name__ == "__main__":
    main()


