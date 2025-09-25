#!/usr/bin/env python3
"""
Swarm Brain Retrieval Layer
==========================

Semantic search and pattern retrieval for swarm intelligence.
V2 Compliance: ≤400 lines, focused retrieval functionality.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Tuple, Optional
from .db import SwarmBrain
from .config import CONFIG
from .embeddings.numpy_backend import NumpyBackend

logger = logging.getLogger(__name__)


class Retriever:
    """Semantic search and pattern retrieval for swarm intelligence."""
    
    def __init__(self, brain: Optional[SwarmBrain] = None):
        """Initialize the retriever."""
        self.brain = brain or SwarmBrain()
        self.backend = NumpyBackend(CONFIG.index_path, CONFIG.dim)
        logger.info("Swarm Brain Retriever initialized")
    
    def search(self, query: str, k: int = 10, *, project: str = None, 
              kinds: List[str] = None, agent_id: str = None) -> List[Dict[str, Any]]:
        """
        Search for similar patterns using semantic similarity.
        
        Args:
            query: Search query
            k: Number of results to return
            project: Filter by project
            kinds: Filter by document kinds
            agent_id: Filter by agent
            
        Returns:
            List of matching documents with metadata
        """
        try:
            # Perform semantic search
            dense_results = self.backend.search(query, k=max(k * 3, k))  # Oversample for filtering
            
            if not dense_results:
                return []
            
            # Get document IDs
            doc_ids = [doc_id for doc_id, _ in dense_results]
            id_to_score = dict(dense_results)
            
            # Build SQL query with filters
            conditions = ["d.id IN ({})".format(",".join(["?"] * len(doc_ids)))]
            params = list(doc_ids)
            
            if project:
                conditions.append("d.project = ?")
                params.append(project)
            
            if kinds:
                kind_placeholders = ",".join(["?"] * len(kinds))
                conditions.append(f"d.kind IN ({kind_placeholders})")
                params.extend(kinds)
            
            if agent_id:
                conditions.append("d.agent_id = ?")
                params.append(agent_id)
            
            where_clause = " AND ".join(conditions)
            
            # Execute query
            sql = f"""
                SELECT d.*, 
                       CASE WHEN e.doc_id IS NOT NULL THEN 1 ELSE 0 END as has_embedding
                FROM documents d
                LEFT JOIN embeddings e ON d.id = e.doc_id
                WHERE {where_clause}
                ORDER BY d.ts DESC
            """
            
            rows = self.brain.conn.execute(sql, params).fetchall()
            
            # Score and rank results
            def score_document(row, base_score):
                score = base_score
                
                # Boost score for embedded documents
                if row["has_embedding"]:
                    score += 0.1
                
                # Boost score for recent documents
                import time
                age_days = (time.time() - row["ts"]) / (24 * 60 * 60)
                if age_days < 7:  # Recent documents
                    score += 0.05
                
                return score
            
            # Rank results
            ranked_results = []
            for row in rows:
                base_score = id_to_score.get(row["id"], 0.0)
                final_score = score_document(row, base_score)
                ranked_results.append((dict(row), final_score))
            
            # Sort by final score and return top k
            ranked_results.sort(key=lambda x: x[1], reverse=True)
            results = [doc for doc, _ in ranked_results[:k]]
            
            logger.debug(f"Found {len(results)} results for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def how_do_agents_do(self, topic: str, k: int = 10, *, project: str = None, 
                        agent_id: str = None) -> List[Dict[str, Any]]:
        """
        Find patterns of how agents accomplish specific tasks.
        
        Args:
            topic: What agents do (e.g., "V2 compliance refactoring")
            k: Number of results to return
            project: Filter by project
            agent_id: Filter by agent
            
        Returns:
            List of successful patterns and outcomes
        """
        query = f"best successful patterns and outcomes for: {topic}"
        return self.search(query, k=k, project=project, kinds=["action", "protocol", "workflow"], agent_id=agent_id)
    
    def find_similar_problems(self, problem_description: str, k: int = 10, 
                            *, project: str = None) -> List[Dict[str, Any]]:
        """
        Find similar problems and their solutions.
        
        Args:
            problem_description: Description of the current problem
            k: Number of results to return
            project: Filter by project
            
        Returns:
            List of similar problems and solutions
        """
        query = f"similar problems and solutions for: {problem_description}"
        return self.search(query, k=k, project=project, kinds=["action", "protocol"])
    
    def get_agent_expertise(self, agent_id: str, k: int = 20) -> Dict[str, Any]:
        """
        Get expertise patterns for a specific agent.
        
        Args:
            agent_id: Agent identifier
            k: Number of results to return
            
        Returns:
            Dictionary with agent expertise information
        """
        try:
            # Get agent's successful actions
            successful_actions = self.search(
                f"successful actions by {agent_id}", 
                k=k, 
                agent_id=agent_id, 
                kinds=["action"]
            )
            
            # Get agent's protocols
            protocols = self.search(
                f"protocols by {agent_id}", 
                k=k, 
                agent_id=agent_id, 
                kinds=["protocol"]
            )
            
            # Get agent's workflows
            workflows = self.search(
                f"workflows by {agent_id}", 
                k=k, 
                agent_id=agent_id, 
                kinds=["workflow"]
            )
            
            # Analyze tool usage
            tool_usage = {}
            for action in successful_actions:
                # Get action details
                action_row = self.brain.conn.execute(
                    "SELECT * FROM actions WHERE doc_id = ?", (action["id"],)
                ).fetchone()
                
                if action_row:
                    tool = action_row["tool"]
                    if tool not in tool_usage:
                        tool_usage[tool] = {"count": 0, "success_rate": 0.0}
                    tool_usage[tool]["count"] += 1
            
            # Calculate success rates
            for tool in tool_usage:
                total_uses = self.brain.conn.execute(
                    "SELECT COUNT(*) as count FROM documents d JOIN actions a ON d.id = a.doc_id WHERE d.agent_id = ? AND a.tool = ?",
                    (agent_id, tool)
                ).fetchone()["count"]
                
                successful_uses = self.brain.conn.execute(
                    "SELECT COUNT(*) as count FROM documents d JOIN actions a ON d.id = a.doc_id WHERE d.agent_id = ? AND a.tool = ? AND a.outcome = 'success'",
                    (agent_id, tool)
                ).fetchone()["count"]
                
                if total_uses > 0:
                    tool_usage[tool]["success_rate"] = successful_uses / total_uses
            
            return {
                "agent_id": agent_id,
                "successful_actions": successful_actions,
                "protocols": protocols,
                "workflows": workflows,
                "tool_expertise": tool_usage,
                "total_patterns": len(successful_actions) + len(protocols) + len(workflows)
            }
            
        except Exception as e:
            logger.error(f"Failed to get agent expertise: {e}")
            return {"agent_id": agent_id, "error": str(e)}
    
    def get_project_patterns(self, project: str, k: int = 20) -> Dict[str, Any]:
        """
        Get patterns and insights for a specific project.
        
        Args:
            project: Project identifier
            k: Number of results to return
            
        Returns:
            Dictionary with project patterns and insights
        """
        try:
            # Get all project activities
            activities = self.search(f"activities in {project}", k=k, project=project)
            
            # Get successful patterns
            successful_patterns = self.search(f"successful patterns in {project}", k=k, project=project, kinds=["action", "workflow"])
            
            # Get protocols used
            protocols = self.search(f"protocols used in {project}", k=k, project=project, kinds=["protocol"])
            
            # Analyze agent participation
            agent_participation = {}
            for activity in activities:
                agent_id = activity.get("agent_id")
                if agent_id:
                    if agent_id not in agent_participation:
                        agent_participation[agent_id] = 0
                    agent_participation[agent_id] += 1
            
            return {
                "project": project,
                "total_activities": len(activities),
                "successful_patterns": successful_patterns,
                "protocols": protocols,
                "agent_participation": agent_participation,
                "recent_activities": activities[:10]  # Most recent 10
            }
            
        except Exception as e:
            logger.error(f"Failed to get project patterns: {e}")
            return {"project": project, "error": str(e)}
    
    def suggest_improvements(self, context: str, k: int = 10) -> List[Dict[str, Any]]:
        """
        Suggest improvements based on similar contexts.
        
        Args:
            context: Current context or problem
            k: Number of suggestions to return
            
        Returns:
            List of improvement suggestions
        """
        query = f"improvements and optimizations for: {context}"
        return self.search(query, k=k, kinds=["protocol", "performance", "tool"])




