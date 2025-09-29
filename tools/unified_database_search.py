#!/usr/bin/env python3
"""
Unified Database Search Interface
=================================

Provides unified search across Swarm Brain, Vector Database, and Devlog Database.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from swarm_brain import Retriever

logger = logging.getLogger(__name__)


class UnifiedDatabaseSearch:
    """Unified search interface for all database systems."""
    
    def __init__(self):
        """Initialize unified search."""
        self.retriever = Retriever()
        self.vector_file = Path("vector_database/devlog_vectors.json")
        self.devlog_file = Path("devlogs/agent_devlogs.json")
        self.project_analysis_file = Path("project_analysis.json")
        
        # Load databases
        self.vector_db = self._load_vector_db()
        self.devlog_db = self._load_devlog_db()
        self.project_data = self._load_project_analysis()
    
    def _load_vector_db(self) -> List[Dict]:
        """Load vector database."""
        if self.vector_file.exists():
            with open(self.vector_file, 'r') as f:
                return json.load(f)
        return []
    
    def _load_devlog_db(self) -> List[Dict]:
        """Load devlog database."""
        if self.devlog_file.exists():
            with open(self.devlog_file, 'r') as f:
                return json.load(f)
        return []
    
    def _load_project_analysis(self) -> Dict:
        """Load project analysis data."""
        if self.project_analysis_file.exists():
            with open(self.project_analysis_file, 'r') as f:
                return json.load(f)
        return {}
    
    def search_all(self, query: str, limit: int = 20) -> Dict[str, List[Dict]]:
        """Search across all databases."""
        results = {
            "swarm_brain": [],
            "vector_database": [],
            "devlogs": [],
            "project_analysis": []
        }
        
        # Search Swarm Brain
        try:
            swarm_results = self.retriever.search(query, k=limit//2)
            results["swarm_brain"] = swarm_results
        except Exception as e:
            logger.error(f"Swarm Brain search failed: {e}")
        
        # Search Vector Database
        query_lower = query.lower()
        for vector in self.vector_db:
            content = vector.get('content', '').lower()
            metadata = vector.get('metadata', {})
            
            if (query_lower in content or 
                query_lower in metadata.get('agent_id', '').lower() or
                query_lower in metadata.get('kind', '').lower()):
                results["vector_database"].append(vector)
        
        # Search Devlogs
        for devlog in self.devlog_db:
            if (query_lower in devlog.get('action', '').lower() or
                query_lower in devlog.get('details', '').lower() or
                query_lower in devlog.get('agent_id', '').lower()):
                results["devlogs"].append(devlog)
        
        # Search Project Analysis
        if self.project_data:
            project_text = json.dumps(self.project_data).lower()
            if query_lower in project_text:
                results["project_analysis"] = [self.project_data]
        
        return results
    
    def search_by_agent(self, agent_id: str, limit: int = 10) -> Dict[str, List[Dict]]:
        """Search for all entries by a specific agent."""
        results = {
            "swarm_brain": [],
            "vector_database": [],
            "devlogs": []
        }
        
        # Search Swarm Brain
        try:
            swarm_results = self.retriever.search("", k=1000, agent_id=agent_id)
            results["swarm_brain"] = swarm_results[:limit]
        except Exception as e:
            logger.error(f"Swarm Brain agent search failed: {e}")
        
        # Search Vector Database
        for vector in self.vector_db:
            if vector.get('metadata', {}).get('agent_id') == agent_id:
                results["vector_database"].append(vector)
        
        # Search Devlogs
        for devlog in self.devlog_db:
            if devlog.get('agent_id') == agent_id:
                results["devlogs"].append(devlog)
        
        return results
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics."""
        stats = {
            "swarm_brain": {
                "total_documents": len(self.retriever.search("", k=1000)),
                "agents": set(),
                "document_types": set()
            },
            "vector_database": {
                "total_vectors": len(self.vector_db),
                "agents": set(),
                "vector_types": set(),
                "sources": set()
            },
            "devlogs": {
                "total_entries": len(self.devlog_db),
                "agents": set(),
                "statuses": set()
            },
            "project_analysis": {
                "files_analyzed": self.project_data.get('analysis', {}).get('project_structure', {}).get('total_files', 0),
                "python_files": self.project_data.get('analysis', {}).get('project_structure', {}).get('python_files', 0),
                "v2_compliant": self.project_data.get('analysis', {}).get('python_analysis', {}).get('v2_compliant_files', 0)
            }
        }
        
        # Analyze Swarm Brain
        swarm_docs = self.retriever.search("", k=1000)
        for doc in swarm_docs:
            if doc.get('agent_id'):
                stats["swarm_brain"]["agents"].add(doc['agent_id'])
            if doc.get('kind'):
                stats["swarm_brain"]["document_types"].add(doc['kind'])
        
        # Analyze Vector Database
        for vector in self.vector_db:
            metadata = vector.get('metadata', {})
            if metadata.get('agent_id'):
                stats["vector_database"]["agents"].add(metadata['agent_id'])
            if vector.get('vector_type'):
                stats["vector_database"]["vector_types"].add(vector['vector_type'])
            if metadata.get('source'):
                stats["vector_database"]["sources"].add(metadata['source'])
        
        # Analyze Devlogs
        for devlog in self.devlog_db:
            if devlog.get('agent_id'):
                stats["devlogs"]["agents"].add(devlog['agent_id'])
            if devlog.get('status'):
                stats["devlogs"]["statuses"].add(devlog['status'])
        
        # Convert sets to lists for JSON serialization
        for db_name in stats:
            if db_name != "project_analysis":
                for key, value in stats[db_name].items():
                    if isinstance(value, set):
                        stats[db_name][key] = list(value)
        
        return stats
    
    def print_search_results(self, results: Dict[str, List[Dict]], query: str):
        """Print formatted search results."""
        print(f"\n🔍 SEARCH RESULTS FOR: '{query}'")
        print("=" * 60)
        
        for db_name, entries in results.items():
            if not entries:
                continue
                
            print(f"\n📊 {db_name.upper().replace('_', ' ')} ({len(entries)} results)")
            print("-" * 40)
            
            for entry in entries[:5]:  # Show first 5 results
                if db_name == "swarm_brain":
                    print(f"  📝 {entry.get('title', 'No title')[:60]}...")
                    print(f"     Agent: {entry.get('agent_id', 'Unknown')} | Type: {entry.get('kind', 'Unknown')}")
                elif db_name == "vector_database":
                    metadata = entry.get('metadata', {})
                    print(f"  🧠 {entry.get('content', 'No content')[:60]}...")
                    print(f"     Agent: {metadata.get('agent_id', 'Unknown')} | Source: {metadata.get('source', 'Unknown')}")
                elif db_name == "devlogs":
                    print(f"  📋 {entry.get('action', 'No action')[:60]}...")
                    print(f"     Agent: {entry.get('agent_id', 'Unknown')} | Status: {entry.get('status', 'Unknown')}")
                elif db_name == "project_analysis":
                    print(f"  📊 Project Analysis Data Found")
                    print(f"     Files: {entry.get('analysis', {}).get('project_structure', {}).get('total_files', 0)}")
    
    def print_database_stats(self):
        """Print comprehensive database statistics."""
        stats = self.get_database_stats()
        
        print("\n📊 UNIFIED DATABASE STATISTICS")
        print("=" * 60)
        
        # Swarm Brain Stats
        sb_stats = stats["swarm_brain"]
        print(f"\n🗃️ SWARM BRAIN DATABASE")
        print(f"   Total Documents: {sb_stats['total_documents']}")
        print(f"   Unique Agents: {len(sb_stats['agents'])}")
        print(f"   Document Types: {', '.join(sb_stats['document_types'])}")
        
        # Vector Database Stats
        vd_stats = stats["vector_database"]
        print(f"\n🧠 VECTOR DATABASE")
        print(f"   Total Vectors: {vd_stats['total_vectors']}")
        print(f"   Unique Agents: {len(vd_stats['agents'])}")
        print(f"   Vector Types: {', '.join(vd_stats['vector_types'])}")
        print(f"   Sources: {', '.join(vd_stats['sources'])}")
        
        # Devlog Database Stats
        dl_stats = stats["devlogs"]
        print(f"\n📋 DEVLOG DATABASE")
        print(f"   Total Entries: {dl_stats['total_entries']}")
        print(f"   Unique Agents: {len(dl_stats['agents'])}")
        print(f"   Status Types: {', '.join(dl_stats['statuses'])}")
        
        # Project Analysis Stats
        pa_stats = stats["project_analysis"]
        print(f"\n📊 PROJECT ANALYSIS")
        print(f"   Files Analyzed: {pa_stats['files_analyzed']}")
        print(f"   Python Files: {pa_stats['python_files']}")
        print(f"   V2 Compliant: {pa_stats['v2_compliant']}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified Database Search")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--agent", type=str, help="Search by agent ID")
    parser.add_argument("--stats", action="store_true", help="Show database statistics")
    parser.add_argument("--limit", type=int, default=10, help="Limit results")
    
    args = parser.parse_args()
    
    search_interface = UnifiedDatabaseSearch()
    
    if args.search:
        results = search_interface.search_all(args.search, args.limit)
        search_interface.print_search_results(results, args.search)
    elif args.agent:
        results = search_interface.search_by_agent(args.agent, args.limit)
        search_interface.print_search_results(results, f"Agent: {args.agent}")
    elif args.stats:
        search_interface.print_database_stats()
    else:
        print("Use --search, --agent, or --stats")
        search_interface.print_database_stats()


if __name__ == "__main__":
    main()
