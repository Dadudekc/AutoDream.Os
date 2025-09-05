"""
Deployment Config Models - V2 Compliant Module
=============================================

Configuration models for deployment operations.
Extracted from deployment_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from datetime import datetime

from .enums import DeploymentStatus, PatternType, DeploymentPriority


@dataclass
class DeploymentConfig:
    """Configuration for mass deployment operations."""
    
    # Core settings
    max_concurrent_deployments: int = 5
    deployment_timeout_seconds: int = 300
    retry_attempts: int = 3
    retry_delay_seconds: float = 2.0
    
    # Target settings
    enable_logging_deployment: bool = True
    enable_manager_consolidation: bool = True
    enable_config_integration: bool = True
    enable_pattern_elimination: bool = True
    
    # Priority settings
    priority_order: List[str] = field(default_factory=lambda: [
        DeploymentPriority.CRITICAL.value,
        DeploymentPriority.HIGH.value,
        DeploymentPriority.MEDIUM.value,
        DeploymentPriority.LOW.value
    ])
    
    # Performance settings
    target_efficiency_score: float = 0.85
    max_deployment_errors: int = 10
    cleanup_failed_deployments: bool = True
    
    # File patterns
    logging_file_patterns: List[str] = field(default_factory=lambda: [
        "**/*logging*.py",
        "**/logs/*.py",
        "**/logger*.py"
    ])
    
    manager_file_patterns: List[str] = field(default_factory=lambda: [
        "**/*manager*.py",
        "**/*coordinator*.py",
        "**/*orchestrator*.py"
    ])
    
    config_file_patterns: List[str] = field(default_factory=lambda: [
        "**/*config*.py",
        "**/configuration*.py",
        "**/settings*.py"
    ])
    
    integration_file_patterns: List[str] = field(default_factory=lambda: [
        "**/*integration*.py",
        "**/integrate*.py",
        "**/connect*.py"
    ])
    
    analytics_file_patterns: List[str] = field(default_factory=lambda: [
        "**/*analytics*.py",
        "**/analysis*.py",
        "**/metrics*.py"
    ])
    
    def validate(self) -> bool:
        """Validate deployment configuration."""
        try:
            # Validate core settings
            if self.max_concurrent_deployments <= 0:
                raise ValueError("Max concurrent deployments must be positive")
            
            if self.deployment_timeout_seconds <= 0:
                raise ValueError("Deployment timeout must be positive")
            
            if self.retry_attempts < 0:
                raise ValueError("Retry attempts must be non-negative")
            
            if self.retry_delay_seconds < 0:
                raise ValueError("Retry delay must be non-negative")
            
            # Validate target efficiency score
            if not 0.0 <= self.target_efficiency_score <= 1.0:
                raise ValueError("Target efficiency score must be between 0.0 and 1.0")
            
            # Validate max deployment errors
            if self.max_deployment_errors < 0:
                raise ValueError("Max deployment errors must be non-negative")
            
            # Validate priority order
            valid_priorities = [dp.value for dp in DeploymentPriority]
            for priority in self.priority_order:
                if priority not in valid_priorities:
                    raise ValueError(f"Invalid priority in order: {priority}")
            
            return True
            
        except ValueError:
            return False
    
    def get_file_patterns(self) -> Dict[str, List[str]]:
        """Get all file patterns as dictionary."""
        return {
            "logging": self.logging_file_patterns,
            "manager": self.manager_file_patterns,
            "config": self.config_file_patterns,
            "integration": self.integration_file_patterns,
            "analytics": self.analytics_file_patterns
        }
    
    def get_pattern_for_type(self, pattern_type: str) -> List[str]:
        """Get file patterns for specific type."""
        pattern_map = {
            PatternType.LOGGING.value: self.logging_file_patterns,
            PatternType.MANAGER.value: self.manager_file_patterns,
            PatternType.CONFIG.value: self.config_file_patterns,
            PatternType.INTEGRATION.value: self.integration_file_patterns,
            PatternType.ANALYTICS.value: self.analytics_file_patterns
        }
        return pattern_map.get(pattern_type, [])
    
    def update_file_patterns(self, pattern_type: str, patterns: List[str]) -> bool:
        """Update file patterns for specific type."""
        pattern_map = {
            PatternType.LOGGING.value: "logging_file_patterns",
            PatternType.MANAGER.value: "manager_file_patterns",
            PatternType.CONFIG.value: "config_file_patterns",
            PatternType.INTEGRATION.value: "integration_file_patterns",
            PatternType.ANALYTICS.value: "analytics_file_patterns"
        }
        
        if pattern_type in pattern_map:
            setattr(self, pattern_map[pattern_type], patterns)
            return True
        return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary."""
        return {
            "max_concurrent_deployments": self.max_concurrent_deployments,
            "deployment_timeout_seconds": self.deployment_timeout_seconds,
            "retry_attempts": self.retry_attempts,
            "target_efficiency_score": self.target_efficiency_score,
            "enabled_features": {
                "logging_deployment": self.enable_logging_deployment,
                "manager_consolidation": self.enable_manager_consolidation,
                "config_integration": self.enable_config_integration,
                "pattern_elimination": self.enable_pattern_elimination
            },
            "priority_order": self.priority_order,
            "file_patterns_count": sum(len(patterns) for patterns in self.get_file_patterns().values())
        }
