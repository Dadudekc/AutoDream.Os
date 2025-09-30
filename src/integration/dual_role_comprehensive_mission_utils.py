"""
Dual Role Comprehensive Mission Utils
Utility functions for mission assessment and validation
"""

import platform
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from .dual_role_comprehensive_mission_core import (
    MissionAssessment,
    MissionConfiguration,
    MissionMetrics,
    MissionPhase,
    MissionTask,
    TaskStatus
)


class MissionValidator:
    """Mission validation utilities"""
    
    @staticmethod
    def validate_assessment(assessment: MissionAssessment) -> List[str]:
        """Validate mission assessment"""
        issues = []
        
        if assessment.score < 0 or assessment.score > 100:
            issues.append("Score must be between 0 and 100")
        
        if assessment.progress < 0 or assessment.progress > 100:
            issues.append("Progress must be between 0 and 100")
        
        if assessment.execution_time < 0:
            issues.append("Execution time cannot be negative")
        
        if not assessment.task:
            issues.append("Task must be specified")
        
        if not assessment.status:
            issues.append("Status must be specified")
        
        return issues
    
    @staticmethod
    def validate_configuration(config: MissionConfiguration) -> List[str]:
        """Validate mission configuration"""
        issues = []
        
        if not config.mission_id:
            issues.append("Mission ID must be specified")
        
        if not config.title:
            issues.append("Title must be specified")
        
        if not config.description:
            issues.append("Description must be specified")
        
        if config.deadline and config.deadline < datetime.now():
            issues.append("Deadline cannot be in the past")
        
        return issues


class MissionAnalyzer:
    """Mission analysis utilities"""
    
    @staticmethod
    def analyze_performance(assessments: List[MissionAssessment]) -> Dict[str, Any]:
        """Analyze mission performance"""
        if not assessments:
            return {"error": "No assessments to analyze"}
        
        total_time = sum(a.execution_time for a in assessments)
        avg_score = sum(a.score for a in assessments) / len(assessments)
        completion_rate = sum(1 for a in assessments if a.status == TaskStatus.COMPLETED) / len(assessments)
        
        return {
            "total_execution_time": total_time,
            "average_score": avg_score,
            "completion_rate": completion_rate,
            "total_assessments": len(assessments),
            "performance_grade": MissionAnalyzer._calculate_grade(avg_score)
        }
    
    @staticmethod
    def _calculate_grade(score: float) -> str:
        """Calculate performance grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    @staticmethod
    def identify_bottlenecks(assessments: List[MissionAssessment]) -> List[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        # Find tasks with longest execution time
        if assessments:
            max_time = max(a.execution_time for a in assessments)
            slow_tasks = [a.task.value for a in assessments if a.execution_time == max_time]
            if slow_tasks:
                bottlenecks.append(f"Slowest tasks: {', '.join(slow_tasks)}")
        
        # Find failed tasks
        failed_tasks = [a.task.value for a in assessments if a.status == TaskStatus.FAILED]
        if failed_tasks:
            bottlenecks.append(f"Failed tasks: {', '.join(failed_tasks)}")
        
        # Find low-scoring tasks
        low_score_tasks = [a.task.value for a in assessments if a.score < 60]
        if low_score_tasks:
            bottlenecks.append(f"Low-scoring tasks: {', '.join(low_score_tasks)}")
        
        return bottlenecks


class MissionReporter:
    """Mission reporting utilities"""
    
    @staticmethod
    def generate_summary_report(metrics: MissionMetrics) -> str:
        """Generate summary report"""
        return f"""
Mission Summary Report
====================
Total Tasks: {metrics.total_tasks}
Completed: {metrics.completed_tasks}
Failed: {metrics.failed_tasks}
Success Rate: {metrics.success_rate:.1f}%
Average Score: {metrics.average_score:.1f}
Quality Score: {metrics.quality_score:.1f}
Total Execution Time: {metrics.total_execution_time:.2f}s
"""
    
    @staticmethod
    def generate_detailed_report(assessments: List[MissionAssessment]) -> str:
        """Generate detailed report"""
        report = "Detailed Mission Report\n"
        report += "======================\n\n"
        
        for assessment in assessments:
            report += f"Task: {assessment.task.value}\n"
            report += f"Status: {assessment.status.value}\n"
            report += f"Score: {assessment.score:.1f}\n"
            report += f"Progress: {assessment.progress:.1f}%\n"
            report += f"Execution Time: {assessment.execution_time:.2f}s\n"
            report += f"Phase: {assessment.phase.value}\n"
            
            if assessment.issues:
                report += f"Issues: {', '.join(assessment.issues)}\n"
            
            if assessment.recommendations:
                report += f"Recommendations: {', '.join(assessment.recommendations)}\n"
            
            report += "\n"
        
        return report


class MissionTimer:
    """Mission timing utilities"""
    
    def __init__(self):
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self):
        """Start timing"""
        self.start_time = datetime.now()
    
    def stop(self) -> float:
        """Stop timing and return elapsed time"""
        self.end_time = datetime.now()
        if self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def get_elapsed_time(self) -> float:
        """Get current elapsed time"""
        if self.start_time:
            current_time = datetime.now()
            return (current_time - self.start_time).total_seconds()
        return 0.0


def create_mission_configuration(
    mission_id: str,
    title: str,
    description: str,
    priority: str = "normal",
    deadline: Optional[datetime] = None,
    assigned_agents: Optional[List[str]] = None,
    dependencies: Optional[List[str]] = None,
    success_criteria: Optional[List[str]] = None
) -> MissionConfiguration:
    """Create mission configuration"""
    return MissionConfiguration(
        mission_id=mission_id,
        title=title,
        description=description,
        priority=priority,
        deadline=deadline,
        assigned_agents=assigned_agents or [],
        dependencies=dependencies or [],
        success_criteria=success_criteria or []
    )


def format_execution_time(seconds: float) -> str:
    """Format execution time in human-readable format"""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"
