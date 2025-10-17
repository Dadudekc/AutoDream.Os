#!/usr/bin/env python3
"""
Swarm Vector Database Integration
==================================

Integrates vector database with swarm protocols and autonomous cycles.
Enables agents to use semantic search for knowledge retrieval during execution.

Features:
- Protocol knowledge retrieval
- Cycle context awareness
- Agent-specific embeddings
- Swarm brain semantic search
- Real-time knowledge access

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-10-17
Mission: Cycle 8 - Vector DB Swarm Integration
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SwarmVectorIntegration:
    """
    Integrates vector database with swarm protocols and cycles.
    
    Enables agents to:
    - Search protocols semantically
    - Retrieve relevant context for tasks
    - Access swarm brain knowledge
    - Find similar past cycles
    - Get agent-specific recommendations
    """
    
    def __init__(self, agent_id: str = "Agent-5"):
        """
        Initialize swarm vector integration.
        
        Args:
            agent_id: ID of the agent using this integration
        """
        self.agent_id = agent_id
        self.vector_db = None  # Lazy load when needed
        self.protocol_cache = {}
        self.cycle_context = {}
    
    def _ensure_vector_db(self):
        """Lazy load vector database."""
        if self.vector_db is None:
            try:
                from src.core.vector_database import VectorDatabase
                self.vector_db = VectorDatabase()
            except ImportError:
                logger.warning("Vector database not available, using fallback")
                self.vector_db = None
    
    def search_protocols(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search swarm protocols using semantic similarity.
        
        Args:
            query: Search query (e.g., "how to handle stop detection")
            top_k: Number of results to return
            
        Returns:
            List of relevant protocol sections
        """
        self._ensure_vector_db()
        
        results = []
        
        # Search swarm_brain/protocols directory
        protocols_path = Path("swarm_brain/protocols")
        if protocols_path.exists():
            for protocol_file in protocols_path.glob("*.md"):
                try:
                    content = protocol_file.read_text(encoding='utf-8')
                    
                    # Simple keyword matching (enhanced with vector DB later)
                    if self._matches_query(query, content):
                        results.append({
                            'file': str(protocol_file),
                            'title': protocol_file.stem.replace('_', ' ').title(),
                            'content': content[:500],
                            'relevance': 1.0
                        })
                except Exception as e:
                    logger.error(f"Error reading protocol {protocol_file}: {e}")
        
        return results[:top_k]
    
    def _matches_query(self, query: str, content: str) -> bool:
        """Simple keyword matching (to be enhanced with embeddings)."""
        query_terms = query.lower().split()
        content_lower = content.lower()
        return any(term in content_lower for term in query_terms)
    
    def get_cycle_context(self, cycle_type: str) -> Dict[str, Any]:
        """
        Get relevant context for current cycle type.
        
        Args:
            cycle_type: Type of cycle (e.g., "DUP_FIX", "REPO_ANALYSIS", "TESTING")
            
        Returns:
            Dictionary with relevant context for this cycle
        """
        contexts = {
            'DUP_FIX': {
                'protocols': ['ANTI_STOP', 'V2_COMPLIANCE'],
                'best_practices': ['Consolidate first', 'Test thoroughly', 'Update imports'],
                'success_metrics': {'lines_consolidated': 100, 'tests_added': 10}
            },
            'REPO_ANALYSIS': {
                'protocols': ['REPOSITORY_ANALYSIS_STANDARD'],
                'best_practices': ['90% hidden value methodology', 'ROI calculation'],
                'success_metrics': {'repos_analyzed': 10, 'goldmines_found': 2}
            },
            'TESTING': {
                'protocols': ['PROCEDURE_TEST_EXECUTION'],
                'best_practices': ['85% coverage minimum', 'Mock external services'],
                'success_metrics': {'coverage_percent': 85, 'tests_passing': True}
            },
            'ANTI_STOP': {
                'protocols': ['ANTI_STOP_PROTOCOL', 'NEVER_STOP_V2', 'ANTI_CHEERLEADER'],
                'best_practices': ['8+ cycles per session', 'Code:Celebrate = 3:1', 'Measurable deliverables'],
                'success_metrics': {'cycles_complete': 8, 'lines_coded': 1000, 'deliverables': 8}
            }
        }
        
        return contexts.get(cycle_type, {})
    
    def find_similar_cycles(self, current_cycle_description: str) -> List[Dict[str, Any]]:
        """
        Find similar past cycles using semantic search.
        
        Args:
            current_cycle_description: Description of current cycle
            
        Returns:
            List of similar past cycles with outcomes
        """
        # Search swarm brain for similar cycle reports
        similar = []
        
        devlogs_path = Path("swarm_brain/devlogs/agent_sessions")
        if devlogs_path.exists():
            for session_file in devlogs_path.glob("*.md"):
                try:
                    content = session_file.read_text(encoding='utf-8')
                    if self._matches_query(current_cycle_description, content):
                        similar.append({
                            'session': session_file.stem,
                            'agent': self._extract_agent(content),
                            'summary': content[:300]
                        })
                except Exception:
                    pass
        
        return similar[:5]
    
    def _extract_agent(self, content: str) -> str:
        """Extract agent ID from content."""
        import re
        match = re.search(r'Agent-(\d+)', content)
        return match.group(0) if match else "Unknown"
    
    def get_agent_recommendations(self, task_type: str) -> List[str]:
        """
        Get recommendations for agent based on task type and past performance.
        
        Args:
            task_type: Type of task (e.g., "DUP_FIX", "REPO_ANALYSIS")
            
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        # Get context for this task type
        context = self.get_cycle_context(task_type)
        
        if context:
            # Protocol recommendations
            if 'protocols' in context:
                recommendations.append(
                    f"📚 Review protocols: {', '.join(context['protocols'])}"
                )
            
            # Best practices
            if 'best_practices' in context:
                for practice in context['best_practices']:
                    recommendations.append(f"✅ {practice}")
            
            # Success metrics
            if 'success_metrics' in context:
                for metric, value in context['success_metrics'].items():
                    recommendations.append(f"🎯 Target {metric}: {value}")
        
        return recommendations
    
    def search_swarm_knowledge(self, query: str, 
                               agent_context: bool = True) -> List[Dict[str, Any]]:
        """
        Search entire swarm knowledge base.
        
        Args:
            query: Search query
            agent_context: If True, prioritize agent's specialty area
            
        Returns:
            List of relevant knowledge entries
        """
        results = []
        
        # Search multiple knowledge sources
        sources = [
            Path("swarm_brain/knowledge"),
            Path("swarm_brain/shared_learnings"),
            Path("swarm_brain/decisions"),
            Path("swarm_brain/protocols"),
        ]
        
        for source_dir in sources:
            if source_dir.exists():
                for knowledge_file in source_dir.rglob("*.md"):
                    try:
                        content = knowledge_file.read_text(encoding='utf-8')
                        if self._matches_query(query, content):
                            results.append({
                                'source': str(knowledge_file),
                                'type': source_dir.name,
                                'content': content[:400],
                                'agent_relevant': self._is_agent_relevant(content)
                            })
                    except Exception:
                        pass
        
        # Sort by agent relevance if requested
        if agent_context:
            results.sort(key=lambda x: x['agent_relevant'], reverse=True)
        
        return results[:10]
    
    def _is_agent_relevant(self, content: str) -> bool:
        """Check if content is relevant to current agent."""
        agent_keywords = {
            'Agent-5': ['business intelligence', 'analytics', 'bi engine', 'metrics', 'data'],
            'Agent-1': ['integration', 'core systems', 'configuration'],
            'Agent-2': ['architecture', 'design', 'patterns'],
            'Agent-3': ['infrastructure', 'devops', 'deployment'],
            'Agent-6': ['quality', 'testing', 'compliance'],
            'Agent-7': ['web development', 'frontend', 'ui'],
            'Agent-8': ['ssot', 'documentation', 'integration'],
        }
        
        keywords = agent_keywords.get(self.agent_id, [])
        content_lower = content.lower()
        
        return any(keyword in content_lower for keyword in keywords)
    
    def index_agent_cycle(self, cycle_data: Dict[str, Any]) -> bool:
        """
        Index completed cycle for future retrieval.
        
        Args:
            cycle_data: Dictionary with cycle information
                - cycle_number: int
                - task_type: str
                - deliverables: List[str]
                - code_lines: int
                - points: int
                - learnings: List[str]
                
        Returns:
            True if indexed successfully
        """
        try:
            # Store in swarm brain for future agents
            cycle_file = Path(f"swarm_brain/agent_cycles/{self.agent_id}_cycle_{cycle_data['cycle_number']}.json")
            cycle_file.parent.mkdir(parents=True, exist_ok=True)
            
            import json
            cycle_file.write_text(json.dumps(cycle_data, indent=2))
            
            logger.info(f"Indexed cycle {cycle_data['cycle_number']} for {self.agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing cycle: {e}")
            return False
    
    def get_quick_reference(self, topic: str) -> Optional[str]:
        """
        Get quick reference for common topics.
        
        Args:
            topic: Topic to get reference for
            
        Returns:
            Quick reference text or None
        """
        quick_refs = {
            'gas_pipeline': "Send gas at 75-80% completion. 3-send redundancy: 75%, 90%, 100%. Keep pipeline flowing!",
            'anti_stop': "8+ cycles per session. Update status every 15-30 min. Always have 3-5 tasks queued. Code:Celebrate = 3:1.",
            'v2_compliance': "Files <400 lines, classes <200 lines, functions <30 lines. 85% test coverage minimum.",
            'strategic_rest': "READY mode = Alert for opportunities, proactive value delivery, team coordination active.",
            'code_first': "75% execution (coding), 25% support (gas/celebration). Code BEFORE celebrating!",
        }
        
        return quick_refs.get(topic.lower())


# Singleton instance
_swarm_vector_integration = None


def get_swarm_vector_integration(agent_id: str = "Agent-5") -> SwarmVectorIntegration:
    """Get or create swarm vector integration instance."""
    global _swarm_vector_integration
    
    if _swarm_vector_integration is None:
        _swarm_vector_integration = SwarmVectorIntegration(agent_id=agent_id)
    
    return _swarm_vector_integration


# Convenience functions for agents
def search_protocols(query: str, agent_id: str = "Agent-5") -> List[Dict[str, Any]]:
    """Search protocols - convenience function."""
    integration = get_swarm_vector_integration(agent_id)
    return integration.search_protocols(query)


def get_cycle_context(cycle_type: str, agent_id: str = "Agent-5") -> Dict[str, Any]:
    """Get cycle context - convenience function."""
    integration = get_swarm_vector_integration(agent_id)
    return integration.get_cycle_context(cycle_type)


def get_quick_ref(topic: str, agent_id: str = "Agent-5") -> Optional[str]:
    """Get quick reference - convenience function."""
    integration = get_swarm_vector_integration(agent_id)
    return integration.get_quick_reference(topic)

