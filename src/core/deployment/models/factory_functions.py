"""
Deployment Factory Functions - V2 Compliant Module
=================================================

Factory functions for creating deployment models.
Extracted from deployment_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .enums import DeploymentStatus, PatternType, DeploymentPriority
from .data_models import MassDeploymentTarget, MaximumEfficiencyDeploymentStatus, DeploymentMetrics
from .config_models import DeploymentConfig


# Constants
DEFAULT_AGENT_DOMAINS = {
    "Agent-1": "Integration & Core Systems",
    "Agent-2": "Architecture & Design",
    "Agent-3": "Infrastructure & DevOps",
    "Agent-4": "Strategic Oversight & Emergency Intervention",
    "Agent-5": "Business Intelligence",
    "Agent-6": "Gaming & Entertainment",
    "Agent-7": "Web Development",
    "Agent-8": "SSOT & System Integration"
}

DEPLOYMENT_TARGET_PRIORITIES = {
    PatternType.LOGGING: DeploymentPriority.HIGH,
    PatternType.MANAGER: DeploymentPriority.CRITICAL,
    PatternType.CONFIG: DeploymentPriority.MEDIUM,
    PatternType.INTEGRATION: DeploymentPriority.HIGH,
    PatternType.ANALYTICS: DeploymentPriority.LOW
}


def create_default_config() -> DeploymentConfig:
    """Create default deployment configuration."""
    return DeploymentConfig()


def create_deployment_target(file_path: str, pattern_type: str, 
                           priority: str = DeploymentPriority.MEDIUM.value) -> MassDeploymentTarget:
    """Create deployment target with validation."""
    target = MassDeploymentTarget(
        file_path=file_path,
        pattern_type=pattern_type,
        priority=priority
    )
    # Validation happens in __post_init__
    return target


def create_deployment_status(agent_id: str, agent_name: str, 
                           domain: str = "") -> MaximumEfficiencyDeploymentStatus:
    """Create deployment status with validation."""
    if not domain:
        domain = DEFAULT_AGENT_DOMAINS.get(agent_id, "Unknown Domain")
    
    status = MaximumEfficiencyDeploymentStatus(
        agent_id=agent_id,
        agent_name=agent_name,
        domain=domain
    )
    # Validation happens in __post_init__
    return status


def create_deployment_metrics() -> DeploymentMetrics:
    """Create deployment metrics tracker."""
    return DeploymentMetrics(start_time=datetime.now())


def create_deployment_target_from_pattern(file_path: str, pattern_type: PatternType) -> MassDeploymentTarget:
    """Create deployment target from pattern type."""
    priority = DEPLOYMENT_TARGET_PRIORITIES.get(pattern_type, DeploymentPriority.MEDIUM)
    return create_deployment_target(file_path, pattern_type.value, priority.value)


def create_batch_deployment_targets(file_paths: List[str], pattern_type: str, 
                                  priority: str = DeploymentPriority.MEDIUM.value) -> List[MassDeploymentTarget]:
    """Create multiple deployment targets."""
    return [
        create_deployment_target(file_path, pattern_type, priority)
        for file_path in file_paths
    ]


def create_deployment_status_for_agent(agent_id: str) -> MaximumEfficiencyDeploymentStatus:
    """Create deployment status for specific agent."""
    agent_name = f"Agent {agent_id.split('-')[1]}" if '-' in agent_id else agent_id
    return create_deployment_status(agent_id, agent_name)


def create_custom_config(max_concurrent: int = 5, timeout: int = 300, 
                        retry_attempts: int = 3, target_efficiency: float = 0.85) -> DeploymentConfig:
    """Create custom deployment configuration."""
    config = DeploymentConfig()
    config.max_concurrent_deployments = max_concurrent
    config.deployment_timeout_seconds = timeout
    config.retry_attempts = retry_attempts
    config.target_efficiency_score = target_efficiency
    return config


def get_agent_domain(agent_id: str) -> str:
    """Get agent domain by ID."""
    return DEFAULT_AGENT_DOMAINS.get(agent_id, "Unknown Domain")


def get_priority_for_pattern(pattern_type: PatternType) -> DeploymentPriority:
    """Get priority for pattern type."""
    return DEPLOYMENT_TARGET_PRIORITIES.get(pattern_type, DeploymentPriority.MEDIUM)


def get_all_agent_domains() -> Dict[str, str]:
    """Get all agent domains."""
    return DEFAULT_AGENT_DOMAINS.copy()


def get_all_pattern_priorities() -> Dict[PatternType, DeploymentPriority]:
    """Get all pattern priorities."""
    return DEPLOYMENT_TARGET_PRIORITIES.copy()
