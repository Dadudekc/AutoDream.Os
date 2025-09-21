"""
Project Completion System - V2 Compliant (Simplified)
====================================================

Core project completion with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
import threading

logger = logging.getLogger(__name__)


class ProjectPhase(Enum):
    """Project phase enumeration."""
    FOUNDATION = "foundation"
    INTEGRATION = "integration"
    OPTIMIZATION = "optimization"
    COMPLETION = "completion"


class ProjectStatus(Enum):
    """Project status enumeration."""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ProjectCompletionStatus:
    """Project completion status structure."""
    phase: ProjectPhase
    completion_percentage: float
    status: ProjectStatus
    quality_score: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ProjectMilestone:
    """Project milestone structure."""
    name: str
    phase: ProjectPhase
    target_date: datetime
    completed: bool = False
    completion_date: Optional[datetime] = None
    quality_score: float = 0.0


class ProjectTracker:
    """Core project tracker."""
    
    def __init__(self):
        self._status: Dict[str, ProjectCompletionStatus] = {}
        self._milestones: List[ProjectMilestone] = []
        self._lock = threading.Lock()
    
    def add_milestone(self, milestone: ProjectMilestone) -> None:
        """Add a project milestone."""
        with self._lock:
            self._milestones.append(milestone)
            logger.debug(f"Milestone added: {milestone.name}")
    
    def complete_milestone(self, name: str, quality_score: float = 0.0) -> bool:
        """Complete a milestone."""
        with self._lock:
            for milestone in self._milestones:
                if milestone.name == name and not milestone.completed:
                    milestone.completed = True
                    milestone.completion_date = datetime.now()
                    milestone.quality_score = quality_score
                    logger.info(f"Milestone completed: {name}")
                    return True
            return False
    
    def get_milestone(self, name: str) -> Optional[ProjectMilestone]:
        """Get a milestone."""
        for milestone in self._milestones:
            if milestone.name == name:
                return milestone
        return None
    
    def get_milestones_by_phase(self, phase: ProjectPhase) -> List[ProjectMilestone]:
        """Get milestones by phase."""
        return [milestone for milestone in self._milestones if milestone.phase == phase]
    
    def get_completed_milestones(self) -> List[ProjectMilestone]:
        """Get completed milestones."""
        return [milestone for milestone in self._milestones if milestone.completed]
    
    def get_pending_milestones(self) -> List[ProjectMilestone]:
        """Get pending milestones."""
        return [milestone for milestone in self._milestones if not milestone.completed]
    
    def update_phase_status(self, phase: ProjectPhase, completion_percentage: float, 
                           status: ProjectStatus, quality_score: float) -> None:
        """Update phase status."""
        with self._lock:
            self._status[phase.value] = ProjectCompletionStatus(
                phase=phase,
                completion_percentage=completion_percentage,
                status=status,
                quality_score=quality_score
            )
            logger.debug(f"Phase status updated: {phase.value} - {completion_percentage}%")
    
    def get_phase_status(self, phase: ProjectPhase) -> Optional[ProjectCompletionStatus]:
        """Get phase status."""
        return self._status.get(phase.value)
    
    def get_overall_completion(self) -> float:
        """Get overall project completion percentage."""
        if not self._status:
            return 0.0
        
        total_percentage = sum(status.completion_percentage for status in self._status.values())
        return total_percentage / len(self._status)
    
    def get_overall_quality_score(self) -> float:
        """Get overall project quality score."""
        if not self._status:
            return 0.0
        
        total_score = sum(status.quality_score for status in self._status.values())
        return total_score / len(self._status)


class ProjectCompletionManager:
    """Project completion management system."""
    
    def __init__(self):
        self._tracker = ProjectTracker()
        self._enabled = True
    
    def enable(self) -> None:
        """Enable project completion management."""
        self._enabled = True
        logger.info("Project completion management enabled")
    
    def disable(self) -> None:
        """Disable project completion management."""
        self._enabled = False
        logger.info("Project completion management disabled")
    
    def is_enabled(self) -> bool:
        """Check if project completion management is enabled."""
        return self._enabled
    
    def get_tracker(self) -> ProjectTracker:
        """Get project tracker."""
        return self._tracker
    
    def initialize_project_phases(self) -> None:
        """Initialize project phases."""
        phases = [
            ProjectPhase.FOUNDATION,
            ProjectPhase.INTEGRATION,
            ProjectPhase.OPTIMIZATION,
            ProjectPhase.COMPLETION
        ]
        
        for phase in phases:
            self._tracker.update_phase_status(phase, 0.0, ProjectStatus.PLANNING, 0.0)
        
        logger.info("Project phases initialized")
    
    def complete_phase(self, phase: ProjectPhase, quality_score: float = 0.0) -> bool:
        """Complete a project phase."""
        if not self._enabled:
            return False
        
        self._tracker.update_phase_status(phase, 100.0, ProjectStatus.COMPLETED, quality_score)
        logger.info(f"Phase completed: {phase.value}")
        return True
    
    def get_project_summary(self) -> Dict[str, Any]:
        """Get project summary."""
        overall_completion = self._tracker.get_overall_completion()
        overall_quality = self._tracker.get_overall_quality_score()
        completed_milestones = len(self._tracker.get_completed_milestones())
        total_milestones = len(self._tracker._milestones)
        
        return {
            'overall_completion': overall_completion,
            'overall_quality_score': overall_quality,
            'completed_milestones': completed_milestones,
            'total_milestones': total_milestones,
            'completion_rate': (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0,
            'phases': {
                phase.value: {
                    'completion_percentage': status.completion_percentage,
                    'status': status.status.value,
                    'quality_score': status.quality_score
                } for phase, status in self._tracker._status.items()
            },
            'last_update': datetime.now()
        }
    
    def is_project_complete(self) -> bool:
        """Check if project is complete."""
        return self._tracker.get_overall_completion() >= 100.0
    
    def get_next_phase(self) -> Optional[ProjectPhase]:
        """Get the next phase to work on."""
        phases = [ProjectPhase.FOUNDATION, ProjectPhase.INTEGRATION, 
                 ProjectPhase.OPTIMIZATION, ProjectPhase.COMPLETION]
        
        for phase in phases:
            status = self._tracker.get_phase_status(phase)
            if not status or status.status != ProjectStatus.COMPLETED:
                return phase
        
        return None


class ProjectQualityAssessor:
    """Project quality assessment system."""
    
    def __init__(self):
        self._quality_metrics: Dict[str, float] = {}
        self._thresholds: Dict[str, float] = {}
    
    def set_quality_threshold(self, metric: str, threshold: float) -> None:
        """Set quality threshold for a metric."""
        self._thresholds[metric] = threshold
        logger.debug(f"Quality threshold set: {metric} = {threshold}")
    
    def assess_quality(self, metric: str, value: float) -> bool:
        """Assess quality for a metric."""
        threshold = self._thresholds.get(metric, 0.0)
        meets_threshold = value >= threshold
        
        self._quality_metrics[metric] = value
        logger.debug(f"Quality assessed: {metric} = {value} (threshold: {threshold})")
        return meets_threshold
    
    def get_quality_score(self, metric: str) -> float:
        """Get quality score for a metric."""
        return self._quality_metrics.get(metric, 0.0)
    
    def get_overall_quality_score(self) -> float:
        """Get overall quality score."""
        if not self._quality_metrics:
            return 0.0
        
        return sum(self._quality_metrics.values()) / len(self._quality_metrics)
    
    def get_quality_report(self) -> Dict[str, Any]:
        """Get quality report."""
        return {
            'metrics': self._quality_metrics.copy(),
            'thresholds': self._thresholds.copy(),
            'overall_score': self.get_overall_quality_score(),
            'last_assessment': datetime.now()
        }


# Global project completion system
project_completion_manager = ProjectCompletionManager()
project_quality_assessor = ProjectQualityAssessor()


def get_project_completion_manager() -> ProjectCompletionManager:
    """Get the global project completion manager."""
    return project_completion_manager


def get_project_quality_assessor() -> ProjectQualityAssessor:
    """Get the global project quality assessor."""
    return project_quality_assessor


def initialize_project() -> None:
    """Initialize project phases."""
    project_completion_manager.initialize_project_phases()


def get_project_summary() -> Dict[str, Any]:
    """Get project summary."""
    return project_completion_manager.get_project_summary()
