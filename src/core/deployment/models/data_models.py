"""
Deployment Data Models - V2 Compliant Module
===========================================

Data models for deployment operations.
Extracted from deployment_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime

from .enums import DeploymentStatus, PatternType, DeploymentPriority


@dataclass
class MassDeploymentTarget:
    """Target for mass deployment operations."""
    file_path: str
    pattern_type: str
    priority: str = DeploymentPriority.MEDIUM.value
    status: str = DeploymentStatus.PENDING.value
    agent_id: Optional[str] = None
    deployment_notes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate deployment target after initialization."""
        if not self.file_path:
            raise ValueError("File path is required")
        
        if self.pattern_type not in [pt.value for pt in PatternType]:
            raise ValueError(f"Invalid pattern type: {self.pattern_type}")
        
        if self.priority not in [dp.value for dp in DeploymentPriority]:
            raise ValueError(f"Invalid priority: {self.priority}")
        
        if self.status not in [ds.value for ds in DeploymentStatus]:
            raise ValueError(f"Invalid status: {self.status}")
    
    def update_status(self, new_status: str, notes: str = ""):
        """Update deployment status."""
        if new_status not in [ds.value for ds in DeploymentStatus]:
            raise ValueError(f"Invalid status: {new_status}")
        
        self.status = new_status
        self.last_modified = datetime.now()
        
        if notes:
            self.deployment_notes.append(f"{datetime.now().isoformat()}: {notes}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        data['created_at'] = self.created_at.isoformat()
        data['last_modified'] = self.last_modified.isoformat()
        return data


@dataclass
class MaximumEfficiencyDeploymentStatus:
    """Status tracking for maximum efficiency deployment."""
    agent_id: str
    agent_name: str
    domain: str = ""
    status: str = DeploymentStatus.PENDING.value
    logging_files_deployed: int = 0
    manager_patterns_consolidated: int = 0
    config_patterns_integrated: int = 0
    total_patterns_eliminated: int = 0
    efficiency_score: float = 0.0
    last_deployment_attempt: Optional[str] = None
    deployment_errors: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate deployment status after initialization."""
        if not self.agent_id or not self.agent_name:
            raise ValueError("Agent ID and name are required")
        
        # Ensure deployment_errors is a list
        if self.deployment_errors is None:
            self.deployment_errors = []
    
    def calculate_efficiency_score(self) -> float:
        """Calculate overall efficiency score."""
        total_deployments = (
            self.logging_files_deployed +
            self.manager_patterns_consolidated +
            self.config_patterns_integrated
        )
        
        if total_deployments == 0:
            self.efficiency_score = 0.0
        else:
            # Base score from pattern elimination
            pattern_score = (self.total_patterns_eliminated / max(total_deployments, 1)) * 0.6
            
            # Success rate score
            success_rate = 1.0 if len(self.deployment_errors) == 0 else max(0.0, 1.0 - len(self.deployment_errors) / 10)
            success_score = success_rate * 0.4
            
            self.efficiency_score = min(1.0, pattern_score + success_score)
        
        return self.efficiency_score
    
    def update_progress(self, logging_deployed: int = 0, manager_consolidated: int = 0,
                       config_integrated: int = 0, patterns_eliminated: int = 0):
        """Update deployment progress metrics."""
        self.logging_files_deployed += logging_deployed
        self.manager_patterns_consolidated += manager_consolidated
        self.config_patterns_integrated += config_integrated
        self.total_patterns_eliminated += patterns_eliminated
        
        self.calculate_efficiency_score()
        self.last_deployment_attempt = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class DeploymentMetrics:
    """Metrics tracking for deployment operations."""
    start_time: datetime
    end_time: Optional[datetime] = None
    total_deployments: int = 0
    successful_deployments: int = 0
    failed_deployments: int = 0
    skipped_deployments: int = 0
    average_deployment_time: float = 0.0
    total_deployment_time: float = 0.0
    efficiency_score: float = 0.0
    
    def add_deployment_result(self, success: bool, deployment_time: float):
        """Add deployment result to metrics."""
        self.total_deployments += 1
        self.total_deployment_time += deployment_time
        
        if success:
            self.successful_deployments += 1
        else:
            self.failed_deployments += 1
        
        # Update average deployment time
        if self.successful_deployments == 0:
            self.average_deployment_time = deployment_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.average_deployment_time = (
                alpha * deployment_time + (1 - alpha) * self.average_deployment_time
            )
    
    def calculate_efficiency_score(self) -> float:
        """Calculate overall efficiency score."""
        if self.total_deployments == 0:
            self.efficiency_score = 0.0
        else:
            success_rate = self.successful_deployments / self.total_deployments
            time_efficiency = 1.0 / max(self.average_deployment_time, 0.1)  # Higher is better
            self.efficiency_score = min(1.0, (success_rate * 0.7) + (time_efficiency * 0.3))
        
        return self.efficiency_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        if self.start_time:
            data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data
