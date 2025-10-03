#!/usr/bin/env python3
"""
Strategic Consultation Templates - Template Management
======================================================

Template management for strategic consultation with Commander Thea.
Provides structured templates and context management.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: strategic_consultation_cli.py (473 lines) - Templates module
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class StrategicTemplate:
    """Strategic consultation template."""
    name: str
    question: str
    context_level: str
    description: str


# Strategic consultation templates
STRATEGIC_TEMPLATES = {
    "priority_guidance": StrategicTemplate(
        name="priority_guidance",
        question="What strategic direction should we prioritize for the next development cycle?",
        context_level="standard",
        description="Get guidance on strategic priorities and direction"
    ),
    "system_enhancement": StrategicTemplate(
        name="system_enhancement",
        question="What should be our next priority for system enhancement?",
        context_level="standard",
        description="Get recommendations for system improvements"
    ),
    "resource_allocation": StrategicTemplate(
        name="resource_allocation",
        question="How should we allocate resources across our 8 specialized agents?",
        context_level="detailed",
        description="Get guidance on resource allocation strategies"
    ),
    "technical_architecture": StrategicTemplate(
        name="technical_architecture",
        question="What architectural improvements should we consider for scalability?",
        context_level="detailed",
        description="Get technical architecture recommendations"
    ),
    "quality_improvement": StrategicTemplate(
        name="quality_improvement",
        question="What quality improvements should we prioritize for V2 compliance?",
        context_level="standard",
        description="Get quality improvement recommendations"
    ),
    "integration_strategy": StrategicTemplate(
        name="integration_strategy",
        question="What integration strategies should we implement for better coordination?",
        context_level="detailed",
        description="Get integration strategy guidance"
    ),
    "crisis_management": StrategicTemplate(
        name="crisis_management",
        question="How should we handle system degradation or agent failures?",
        context_level="emergency",
        description="Get crisis management guidance"
    ),
    "future_planning": StrategicTemplate(
        name="future_planning",
        question="What long-term strategic goals should we establish for the swarm system?",
        context_level="detailed",
        description="Get long-term strategic planning guidance"
    )
}


class ProjectContextManager:
    """Manages project context for strategic consultations."""
    
    def __init__(self):
        """Initialize context manager."""
        self.context_levels = {
            "standard": self._get_standard_context,
            "detailed": self._get_detailed_context,
            "emergency": self._get_emergency_context
        }
    
    def get_context(self, context_level: str) -> Dict[str, Any]:
        """Get project context based on level."""
        if context_level not in self.context_levels:
            context_level = "standard"
        
        return self.context_levels[context_level]()
    
    def _get_standard_context(self) -> Dict[str, Any]:
        """Get standard project context."""
        return {
            "project_name": "V2_SWARM",
            "current_status": "Active development",
            "agent_count": 8,
            "compliance_level": "V2",
            "focus_areas": ["Quality", "Coordination", "Automation"]
        }
    
    def _get_detailed_context(self) -> Dict[str, Any]:
        """Get detailed project context."""
        return {
            "project_name": "V2_SWARM",
            "current_status": "Active development with 96.6% V2 compliance",
            "agent_count": 8,
            "compliance_level": "V2",
            "focus_areas": ["Quality", "Coordination", "Automation"],
            "recent_achievements": [
                "Strategic Consultation CLI refactored",
                "Devlog Storytelling Service refactored",
                "Coordinate Manager refactored"
            ],
            "current_challenges": [
                "Memory leak remediation",
                "Discord Commander integration",
                "AGENTS.md V2 compliance"
            ]
        }
    
    def _get_emergency_context(self) -> Dict[str, Any]:
        """Get emergency project context."""
        return {
            "project_name": "V2_SWARM",
            "status": "Emergency situation",
            "priority": "Critical",
            "immediate_concerns": [
                "System degradation",
                "Agent failures",
                "Critical mission execution"
            ]
        }