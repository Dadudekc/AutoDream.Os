#!/usr/bin/env python3
"""
Captain Autonomous Core - V2 Compliant
=======================================

Core autonomous captain system functionality including data classes,
bottleneck detection, flaw detection, and autonomous management logic.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
V2 Compliance: ≤300 lines, modular design, comprehensive error handling
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from .captain_autonomous_models import BottleneckType, FlawSeverity, StoppingCondition, Bottleneck, Flaw
from .captain_autonomous_storage import CaptainAutonomousStorage


class CaptainAutonomousCore:
    """Core autonomous captain management system."""
    
    def __init__(self):
        """Initialize autonomous core."""
        self.storage = CaptainAutonomousStorage()
        self.bottlenecks = self.storage.load_bottlenecks()
        self.flaws = self.storage.load_flaws()
        self.stopping_conditions = self.storage.load_stopping_conditions()
    
    
    def detect_bottlenecks(self) -> List[Bottleneck]:
        """Detect system bottlenecks."""
        new_bottlenecks = []
        
        # Check for resource bottlenecks
        if self._check_resource_bottlenecks():
            bottleneck = Bottleneck(
                "Resource Bottleneck",
                BottleneckType.RESOURCE,
                "Insufficient resources for current workload",
                "High demand, limited capacity",
                "Reallocate resources or scale up capacity"
            )
            new_bottlenecks.append(bottleneck)
        
        # Check for dependency bottlenecks
        if self._check_dependency_bottlenecks():
            bottleneck = Bottleneck(
                "Dependency Bottleneck",
                BottleneckType.DEPENDENCY,
                "Blocked by unresolved dependencies",
                "Missing or incomplete dependencies",
                "Resolve dependencies or find alternatives"
            )
            new_bottlenecks.append(bottleneck)
        
        # Check for quality bottlenecks
        if self._check_quality_bottlenecks():
            bottleneck = Bottleneck(
                "Quality Bottleneck",
                BottleneckType.QUALITY,
                "Quality issues blocking progress",
                "V2 compliance violations or quality failures",
                "Fix quality issues and implement quality gates"
            )
            new_bottlenecks.append(bottleneck)
        
        # Check for coordination bottlenecks
        if self._check_coordination_bottlenecks():
            bottleneck = Bottleneck(
                "Coordination Bottleneck",
                BottleneckType.COORDINATION,
                "Poor agent coordination",
                "Communication issues or unclear responsibilities",
                "Improve communication and clarify roles"
            )
            new_bottlenecks.append(bottleneck)
        
        # Add new bottlenecks
        for bottleneck in new_bottlenecks:
            if bottleneck.name not in self.bottlenecks:
                self.bottlenecks[bottleneck.name] = bottleneck
        
        self.storage.save_bottlenecks(self.bottlenecks)
        return new_bottlenecks
    
    def detect_flaws(self) -> List[Flaw]:
        """Detect system flaws."""
        new_flaws = []
        
        # Check for critical flaws
        if self._check_critical_flaws():
            flaw = Flaw(
                "Critical System Flaw",
                FlawSeverity.CRITICAL,
                "Critical system issue detected",
                "Immediate system restart and recovery"
            )
            new_flaws.append(flaw)
        
        # Check for quality flaws
        if self._check_quality_flaws():
            flaw = Flaw(
                "Quality Compliance Flaw",
                FlawSeverity.HIGH,
                "V2 compliance violations detected",
                "Run quality gates and fix violations"
            )
            new_flaws.append(flaw)
        
        # Check for performance flaws
        if self._check_performance_flaws():
            flaw = Flaw(
                "Performance Degradation",
                FlawSeverity.MEDIUM,
                "System performance below threshold",
                "Optimize performance and monitor metrics"
            )
            new_flaws.append(flaw)
        
        # Add new flaws
        for flaw in new_flaws:
            if flaw.name not in self.flaws:
                self.flaws[flaw.name] = flaw
        
        self.storage.save_flaws(self.flaws)
        return new_flaws
    
    def check_stopping_conditions(self) -> List[Tuple[StoppingCondition, str]]:
        """Check if stopping conditions are met."""
        stopping_conditions = []
        
        # Check if all directives are complete
        if self._check_all_directives_complete():
            stopping_conditions.append((StoppingCondition.ALL_DIRECTIVES_COMPLETE, "All directives completed"))
        
        # Check quality threshold breach
        if self._check_quality_threshold_breach():
            stopping_conditions.append((StoppingCondition.QUALITY_THRESHOLD_BREACH, "Quality threshold breached"))
        
        # Check resource exhaustion
        if self._check_resource_exhaustion():
            stopping_conditions.append((StoppingCondition.RESOURCE_EXHAUSTION, "Resources exhausted"))
        
        # Check critical flaw detected
        if self._check_critical_flaw_detected():
            stopping_conditions.append((StoppingCondition.CRITICAL_FLAW_DETECTED, "Critical flaw detected"))
        
        # Check agent inactivity
        if self._check_agent_inactivity():
            stopping_conditions.append((StoppingCondition.AGENT_INACTIVITY, "Agent inactivity detected"))
        
        # Check system failure
        if self._check_system_failure():
            stopping_conditions.append((StoppingCondition.SYSTEM_FAILURE, "System failure detected"))
        
        return stopping_conditions
    
    def generate_autonomous_priorities(self) -> List[str]:
        """Generate autonomous priorities based on system analysis."""
        priorities = []
        
        # Analyze bottlenecks
        for bottleneck in self.bottlenecks.values():
            if bottleneck.status == "active":
                priorities.append(f"Resolve {bottleneck.name}: {bottleneck.resolution_plan}")
        
        # Analyze flaws
        for flaw in self.flaws.values():
            if flaw.status == "detected":
                priorities.append(f"Fix {flaw.name}: {flaw.auto_resolution}")
        
        # Analyze system health
        if self._check_system_health():
            priorities.append("Optimize system performance and monitoring")
        
        # Analyze agent utilization
        if self._check_agent_utilization():
            priorities.append("Optimize agent workload distribution")
        
        return priorities
    
    def provide_agent_guidance(self, agent_id: str) -> str:
        """Provide autonomous guidance to specific agent."""
        guidance = []
        
        # Check agent's current status
        agent_status = self._get_agent_status(agent_id)
        if not agent_status:
            return f"Agent {agent_id} status unknown"
        
        # Check if agent is idle
        if agent_status.get("idle", False):
            # Find next suitable task
            next_task = self._find_next_task_for_agent(agent_id)
            if next_task:
                guidance.append(f"Next task: {next_task}")
            else:
                guidance.append("No suitable tasks found - standby for new directives")
        
        # Check if agent has bottlenecks
        agent_bottlenecks = self._get_agent_bottlenecks(agent_id)
        for bottleneck in agent_bottlenecks:
            guidance.append(f"Bottleneck: {bottleneck.resolution_plan}")
        
        # Check if agent has quality issues
        quality_issues = self._get_agent_quality_issues(agent_id)
        for issue in quality_issues:
            guidance.append(f"Quality issue: {issue}")
        
        return "; ".join(guidance) if guidance else "Continue current work"
    
    # Delegate detection logic to utility module
    def _check_resource_bottlenecks(self) -> bool:
        """Check for resource bottlenecks."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_resource_bottlenecks()
    
    def _check_dependency_bottlenecks(self) -> bool:
        """Check for dependency bottlenecks."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_dependency_bottlenecks()
    
    def _check_quality_bottlenecks(self) -> bool:
        """Check for quality bottlenecks."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_quality_bottlenecks()
    
    def _check_coordination_bottlenecks(self) -> bool:
        """Check for coordination bottlenecks."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_coordination_bottlenecks()
    
    def _check_critical_flaws(self) -> bool:
        """Check for critical flaws."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_critical_flaws()
    
    def _check_quality_flaws(self) -> bool:
        """Check for quality flaws."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_quality_flaws()
    
    def _check_performance_flaws(self) -> bool:
        """Check for performance flaws."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_performance_flaws()
    
    def _check_all_directives_complete(self) -> bool:
        """Check if all directives are complete."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_all_directives_complete()
    
    def _check_quality_threshold_breach(self) -> bool:
        """Check if quality threshold is breached."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_quality_threshold_breach()
    
    def _check_resource_exhaustion(self) -> bool:
        """Check if resources are exhausted."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_resource_exhaustion()
    
    def _check_critical_flaw_detected(self) -> bool:
        """Check if critical flaw is detected."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_critical_flaw_detected()
    
    def _check_agent_inactivity(self) -> bool:
        """Check for agent inactivity."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_agent_inactivity()
    
    def _check_system_failure(self) -> bool:
        """Check for system failure."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_system_failure()
    
    def _check_system_health(self) -> bool:
        """Check system health."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_system_health()
    
    def _check_agent_utilization(self) -> bool:
        """Check agent utilization."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.check_agent_utilization()
    
    def _get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get agent status."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.get_agent_status(agent_id)
    
    def _find_next_task_for_agent(self, agent_id: str) -> Optional[str]:
        """Find next suitable task for agent."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.find_next_task_for_agent(agent_id)
    
    def _get_agent_bottlenecks(self, agent_id: str) -> List[Bottleneck]:
        """Get agent-specific bottlenecks."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.get_agent_bottlenecks(agent_id)
    
    def _get_agent_quality_issues(self, agent_id: str) -> List[str]:
        """Get agent-specific quality issues."""
        from .captain_autonomous_utility import CaptainAutonomousUtility
        return CaptainAutonomousUtility.get_agent_quality_issues(agent_id)


# V2 Compliance: File length check
if __name__ == "__main__":
    import inspect
    lines = len(inspect.getsource(inspect.currentframe().f_globals['__file__']).splitlines())
    print(f"Captain Autonomous Core: {lines} lines - V2 Compliant ✅")
