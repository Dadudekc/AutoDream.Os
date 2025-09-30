"""
Dual Role Comprehensive Mission Core
Core classes and data structures for mission assessment
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MissionTask(Enum):
    """Mission task enumeration"""
    TEST_AGENT7_INTERFACE = "test_agent7_interface"
    VALIDATE_AGENT6_VSCODE = "validate_agent6_vscode"
    DEVELOP_TESTING_FRAMEWORK = "develop_testing_framework"
    ENSURE_CROSS_PLATFORM = "ensure_cross_platform"
    OPTIMIZE_PERFORMANCE = "optimize_performance"


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MissionPhase(Enum):
    """Mission phase enumeration"""
    PLANNING = "planning"
    EXECUTION = "execution"
    VALIDATION = "validation"
    COMPLETION = "completion"


@dataclass
class MissionAssessment:
    """Mission assessment structure"""
    task: MissionTask
    status: TaskStatus
    score: float
    progress: float
    issues: List[str]
    recommendations: List[str]
    execution_time: float
    priority: str
    phase: MissionPhase
    created_at: datetime
    updated_at: datetime


@dataclass
class MissionMetrics:
    """Mission metrics structure"""
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    average_score: float
    total_execution_time: float
    success_rate: float
    quality_score: float


@dataclass
class MissionConfiguration:
    """Mission configuration structure"""
    mission_id: str
    title: str
    description: str
    priority: str
    deadline: Optional[datetime]
    assigned_agents: List[str]
    dependencies: List[str]
    success_criteria: List[str]


class MissionCore:
    """Core mission management functionality"""
    
    def __init__(self):
        self.assessments: List[MissionAssessment] = []
        self.metrics: Optional[MissionMetrics] = None
        self.configuration: Optional[MissionConfiguration] = None
    
    def create_assessment(self, task: MissionTask, status: TaskStatus = TaskStatus.PENDING) -> MissionAssessment:
        """Create a new mission assessment"""
        assessment = MissionAssessment(
            task=task,
            status=status,
            score=0.0,
            progress=0.0,
            issues=[],
            recommendations=[],
            execution_time=0.0,
            priority="normal",
            phase=MissionPhase.PLANNING,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.assessments.append(assessment)
        return assessment
    
    def update_assessment(self, assessment: MissionAssessment, **kwargs) -> MissionAssessment:
        """Update an existing assessment"""
        for key, value in kwargs.items():
            if hasattr(assessment, key):
                setattr(assessment, key, value)
        assessment.updated_at = datetime.now()
        return assessment
    
    def get_assessment_by_task(self, task: MissionTask) -> Optional[MissionAssessment]:
        """Get assessment by task"""
        for assessment in self.assessments:
            if assessment.task == task:
                return assessment
        return None
    
    def calculate_metrics(self) -> MissionMetrics:
        """Calculate mission metrics"""
        if not self.assessments:
            return MissionMetrics(0, 0, 0, 0.0, 0.0, 0.0, 0.0)
        
        total_tasks = len(self.assessments)
        completed_tasks = sum(1 for a in self.assessments if a.status == TaskStatus.COMPLETED)
        failed_tasks = sum(1 for a in self.assessments if a.status == TaskStatus.FAILED)
        average_score = sum(a.score for a in self.assessments) / total_tasks
        total_execution_time = sum(a.execution_time for a in self.assessments)
        success_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0.0
        quality_score = average_score * (success_rate / 100)
        
        self.metrics = MissionMetrics(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            failed_tasks=failed_tasks,
            average_score=average_score,
            total_execution_time=total_execution_time,
            success_rate=success_rate,
            quality_score=quality_score
        )
        return self.metrics
