"""
Target Discovery Engine - V2 Compliant Module
============================================

Handles discovery and prioritization of deployment targets.
Extracted from deployment_coordinator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import os
import glob
import re
from typing import List, Dict, Set
import logging

from ..deployment_models import (
    MassDeploymentTarget, PatternType, DeploymentPriority,
    create_deployment_target
)


class TargetDiscoveryEngine:
    """
    Engine for discovering and prioritizing deployment targets.
    
    Handles file pattern matching, target creation, and priority determination.
    """
    
    def __init__(self, config):
        """Initialize target discovery engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def discover_deployment_targets(self, base_path: str = "src") -> List[MassDeploymentTarget]:
        """Discover deployment targets based on file patterns."""
        targets = []
        
        try:
            # Discover logging files
            if self.config.enable_logging_deployment:
                logging_targets = self._discover_pattern_targets(
                    base_path, self.config.logging_file_patterns, PatternType.LOGGING
                )
                targets.extend(logging_targets)
            
            # Discover manager files
            if self.config.enable_manager_consolidation:
                manager_targets = self._discover_pattern_targets(
                    base_path, self.config.manager_file_patterns, PatternType.MANAGER
                )
                targets.extend(manager_targets)
            
            # Discover config files
            if self.config.enable_config_integration:
                config_targets = self._discover_pattern_targets(
                    base_path, self.config.config_file_patterns, PatternType.CONFIG
                )
                targets.extend(config_targets)
            
            self.logger.info(f"Discovered {len(targets)} deployment targets")
            return targets
            
        except Exception as e:
            self.logger.error(f"Error discovering deployment targets: {e}")
            return []
    
    def _discover_pattern_targets(self, base_path: str, patterns: List[str], 
                                 pattern_type: PatternType) -> List[MassDeploymentTarget]:
        """Discover targets matching specific patterns."""
        targets = []
        
        try:
            for pattern in patterns:
                # Construct full pattern path
                full_pattern = os.path.join(base_path, pattern)
                
                # Find matching files
                matching_files = glob.glob(full_pattern, recursive=True)
                
                for file_path in matching_files:
                    # Skip if file doesn't exist or is not readable
                    if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
                        continue
                    
                    # Determine priority based on pattern type
                    priority = self._determine_priority(pattern_type, file_path)
                    
                    # Create deployment target
                    target = create_deployment_target(
                        file_path=file_path,
                        pattern_type=pattern_type.value,
                        priority=priority.value
                    )
                    
                    targets.append(target)
            
        except Exception as e:
            self.logger.error(f"Error discovering {pattern_type.value} targets: {e}")
        
        return targets
    
    def _determine_priority(self, pattern_type: PatternType, file_path: str) -> DeploymentPriority:
        """Determine deployment priority for target."""
        # Base priority from pattern type
        base_priority = {
            PatternType.LOGGING: DeploymentPriority.HIGH,
            PatternType.MANAGER: DeploymentPriority.CRITICAL,
            PatternType.CONFIG: DeploymentPriority.MEDIUM
        }
        
        priority = base_priority.get(pattern_type, DeploymentPriority.LOW)
        
        # Adjust priority based on file characteristics
        if self._is_critical_file(file_path):
            priority = DeploymentPriority.CRITICAL
        elif self._is_high_priority_file(file_path):
            priority = DeploymentPriority.HIGH
        elif self._is_low_priority_file(file_path):
            priority = DeploymentPriority.LOW
        
        return priority
    
    def _is_critical_file(self, file_path: str) -> bool:
        """Check if file is critical for deployment."""
        critical_patterns = [
            r'coordinator',
            r'orchestrator',
            r'main',
            r'core',
            r'deployment'
        ]
        
        return any(re.search(pattern, file_path.lower()) for pattern in critical_patterns)
    
    def _is_high_priority_file(self, file_path: str) -> bool:
        """Check if file is high priority for deployment."""
        high_priority_patterns = [
            r'service',
            r'manager',
            r'handler',
            r'controller'
        ]
        
        return any(re.search(pattern, file_path.lower()) for pattern in high_priority_patterns)
    
    def _is_low_priority_file(self, file_path: str) -> bool:
        """Check if file is low priority for deployment."""
        low_priority_patterns = [
            r'test',
            r'example',
            r'demo',
            r'temp',
            r'backup'
        ]
        
        return any(re.search(pattern, file_path.lower()) for pattern in low_priority_patterns)
    
    def filter_targets_by_agent(self, targets: List[MassDeploymentTarget], 
                               agent_filter: Set[str]) -> List[MassDeploymentTarget]:
        """Filter targets by agent IDs."""
        filtered_targets = []
        
        for target in targets:
            # Extract agent ID from file path
            agent_id = self._extract_agent_id_from_path(target.file_path)
            
            if agent_id in agent_filter:
                filtered_targets.append(target)
        
        return filtered_targets
    
    def _extract_agent_id_from_path(self, file_path: str) -> str:
        """Extract agent ID from file path."""
        # Simple heuristic - look for Agent-X patterns in path
        match = re.search(r'agent[_-]?(\d+)', file_path.lower())
        if match:
            return f"Agent-{match.group(1)}"
        
        # Default fallback based on directory structure
        if "agent_workspaces" in file_path:
            parts = file_path.split(os.sep)
            for part in parts:
                if part.startswith("Agent-"):
                    return part
        
        return "Unknown"
    
    def sort_targets_by_priority(self, targets: List[MassDeploymentTarget]) -> List[MassDeploymentTarget]:
        """Sort targets by deployment priority."""
        priority_order = {
            DeploymentPriority.CRITICAL.value: 0,
            DeploymentPriority.HIGH.value: 1,
            DeploymentPriority.MEDIUM.value: 2,
            DeploymentPriority.LOW.value: 3
        }
        
        return sorted(targets, key=lambda t: priority_order.get(t.priority, 999))
    
    def get_targets_by_pattern_type(self, targets: List[MassDeploymentTarget]) -> Dict[str, int]:
        """Get target count by pattern type."""
        counts = {}
        for target in targets:
            counts[target.pattern_type] = counts.get(target.pattern_type, 0) + 1
        return counts
    
    def get_targets_by_priority(self, targets: List[MassDeploymentTarget]) -> Dict[str, int]:
        """Get target count by priority."""
        counts = {}
        for target in targets:
            counts[target.priority] = counts.get(target.priority, 0) + 1
        return counts
    
    def get_targets_by_status(self, targets: List[MassDeploymentTarget]) -> Dict[str, int]:
        """Get target count by deployment status."""
        counts = {}
        for target in targets:
            counts[target.deployment_status] = counts.get(target.deployment_status, 0) + 1
        return counts
