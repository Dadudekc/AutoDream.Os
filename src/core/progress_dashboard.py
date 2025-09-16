#!/usr/bin/env python3
"""
Progress Dashboard - Progress Tracking Dashboard
=============================================

Progress tracking dashboard for monitoring and visualization.
Part of the modularization of unified_progress_tracking.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .progress_models import AgentProgress, ProgressMilestone, SuperiorityMetrics, SystemProgress
from .progress_phases_enums import ProgressPhase, SuperiorityBenchmark

logger = logging.getLogger(__name__)


class UnifiedProgressDashboard:
    """Unified progress tracking dashboard."""
    
    def __init__(self) -> None:
        self._system_progress: Optional[SystemProgress] = None
        self._metrics: SuperiorityMetrics = SuperiorityMetrics()
        self._observers: List[Any] = []
    
    def initialize_dashboard(self, system_name: str) -> bool:
        """Initialize the progress dashboard."""
        try:
            self._system_progress = SystemProgress(system_name=system_name, overall_phase="initialization")
            logger.info(f"Dashboard initialized for system: {system_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize dashboard: {e}")
            return False
    
    def add_agent_progress(self, agent_progress: AgentProgress) -> bool:
        """Add agent progress to dashboard."""
        if not self._system_progress:
            logger.warning("Dashboard not initialized")
            return False
        
        try:
            self._system_progress.agent_progress.append(agent_progress)
            self._update_overall_progress()
            self._notify_observers("agent_progress_added", agent_progress)
            logger.debug(f"Added progress for agent: {agent_progress.agent_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add agent progress: {e}")
            return False
    
    def update_milestone(self, agent_id: str, milestone_id: str, completed: bool = True) -> bool:
        """Update milestone completion status."""
        if not self._system_progress:
            logger.warning("Dashboard not initialized")
            return False
        
        try:
            for agent_progress in self._system_progress.agent_progress:
                if agent_progress.agent_id == agent_id:
                    for milestone in agent_progress.milestones:
                        if milestone.id == milestone_id:
                            milestone.completed = completed
                            if completed:
                                milestone.completion_date = datetime.now()
                            self._update_overall_progress()
                            self._notify_observers("milestone_updated", {"agent_id": agent_id, "milestone_id": milestone_id})
                            logger.debug(f"Updated milestone {milestone_id} for agent {agent_id}")
                            return True
            
            logger.warning(f"Milestone {milestone_id} not found for agent {agent_id}")
            return False
        except Exception as e:
            logger.error(f"Failed to update milestone: {e}")
            return False
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get complete dashboard data."""
        if not self._system_progress:
            return {"error": "Dashboard not initialized"}
        
        return {
            "system_progress": self._system_progress,
            "metrics": self._metrics,
            "last_updated": datetime.now().isoformat()
        }
    
    def _update_overall_progress(self) -> None:
        """Update overall system progress."""
        if not self._system_progress:
            return
        
        total_milestones = 0
        completed_milestones = 0
        
        for agent_progress in self._system_progress.agent_progress:
            total_milestones += len(agent_progress.milestones)
            completed_milestones += sum(1 for m in agent_progress.milestones if m.completed)
        
        self._system_progress.total_milestones = total_milestones
        self._system_progress.completed_milestones = completed_milestones
        
        if total_milestones > 0:
            self._system_progress.progress_percentage = (completed_milestones / total_milestones) * 100
        
        self._system_progress.last_updated = datetime.now()
    
    def _notify_observers(self, event: str, data: Any) -> None:
        """Notify dashboard observers of changes."""
        for observer in self._observers:
            try:
                if hasattr(observer, 'update'):
                    observer.update(event, data)
            except Exception as e:
                logger.error(f"Error notifying observer: {e}")
    
    def add_observer(self, observer: Any) -> bool:
        """Add dashboard observer."""
        try:
            self._observers.append(observer)
            logger.debug("Added dashboard observer")
            return True
        except Exception as e:
            logger.error(f"Failed to add observer: {e}")
            return False
    
    def remove_observer(self, observer: Any) -> bool:
        """Remove dashboard observer."""
        try:
            if observer in self._observers:
                self._observers.remove(observer)
                logger.debug("Removed dashboard observer")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove observer: {e}")
            return False





