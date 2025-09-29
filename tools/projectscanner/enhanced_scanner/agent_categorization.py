#!/usr/bin/env python3
"""
Agent Categorization Handler - V2 Compliant
===========================================

Handles agent categorization for enhanced project scanner.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class AgentCategorizationHandler:
    """Handles agent categorization for enhanced project scanner."""
    
    def __init__(self, core):
        """Initialize agent categorization handler."""
        self.core = core
        
        # Agent specialization patterns
        self.specialization_patterns = {
            'Agent-1': ['integration', 'api', 'core', 'system'],
            'Agent-2': ['architecture', 'design', 'pattern', 'structure'],
            'Agent-3': ['database', 'infrastructure', 'devops', 'ml'],
            'Agent-4': ['quality', 'testing', 'validation', 'compliance'],
            'Agent-5': ['business', 'intelligence', 'analytics', 'data'],
            'Agent-6': ['coordination', 'communication', 'messaging', 'chat'],
            'Agent-7': ['web', 'frontend', 'ui', 'react', 'vue'],
            'Agent-8': ['operations', 'support', 'monitoring', 'deployment']
        }
    
    def categorize_agents(self) -> None:
        """Categorize agents based on project analysis."""
        
        logger.info("🤖 Categorizing agents based on project analysis")
        
        agent_categories = {}
        
        for file_path, analysis in self.core.analysis.items():
            # Extract keywords from file content
            keywords = self._extract_keywords(analysis)
            
            # Determine best agent match
            best_agent = self._find_best_agent_match(keywords)
            
            if best_agent:
                if best_agent not in agent_categories:
                    agent_categories[best_agent] = []
                
                agent_categories[best_agent].append({
                    'file_path': file_path,
                    'keywords': keywords,
                    'confidence': self._calculate_confidence(keywords, best_agent)
                })
        
        # Log categorization results
        for agent, files in agent_categories.items():
            logger.info(f"🎯 {agent}: {len(files)} files categorized")
        
        # Store categorization results
        self.core.analysis['_agent_categorization'] = agent_categories
    
    def _extract_keywords(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract keywords from file analysis."""
        
        keywords = []
        
        # Extract from file path
        file_path = analysis.get('file_path', '')
        path_parts = file_path.lower().split('/')
        keywords.extend(path_parts)
        
        # Extract from language
        language = analysis.get('language', '').lower()
        if language:
            keywords.append(language)
        
        # Extract from content analysis
        content_analysis = analysis.get('content_analysis', {})
        if isinstance(content_analysis, dict):
            # Extract function names, class names, etc.
            functions = content_analysis.get('functions', [])
            classes = content_analysis.get('classes', [])
            
            for func in functions:
                keywords.append(func.lower())
            
            for cls in classes:
                keywords.append(cls.lower())
        
        return keywords
    
    def _find_best_agent_match(self, keywords: List[str]) -> str:
        """Find the best agent match for given keywords."""
        
        best_agent = None
        best_score = 0
        
        for agent, patterns in self.specialization_patterns.items():
            score = 0
            
            for keyword in keywords:
                for pattern in patterns:
                    if pattern in keyword or keyword in pattern:
                        score += 1
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent if best_score > 0 else None
    
    def _calculate_confidence(self, keywords: List[str], agent: str) -> float:
        """Calculate confidence score for agent categorization."""
        
        patterns = self.specialization_patterns.get(agent, [])
        matches = 0
        
        for keyword in keywords:
            for pattern in patterns:
                if pattern in keyword or keyword in pattern:
                    matches += 1
                    break
        
        return matches / len(keywords) if keywords else 0.0
