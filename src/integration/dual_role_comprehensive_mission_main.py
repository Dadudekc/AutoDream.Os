"""
Dual Role Comprehensive Mission Main
Main mission system with comprehensive assessment capabilities
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from .dual_role_comprehensive_mission_core import (
    MissionAssessment,
    MissionConfiguration,
    MissionCore,
    MissionMetrics,
    MissionPhase,
    MissionTask,
    TaskStatus
)
from .dual_role_comprehensive_mission_utils import (
    MissionAnalyzer,
    MissionReporter,
    MissionTimer,
    MissionValidator,
    create_mission_configuration,
    format_execution_time
)


class DualRoleComprehensiveMission:
    """Dual Role Comprehensive Mission System"""
    
    def __init__(self):
        self.core = MissionCore()
        self.validator = MissionValidator()
        self.analyzer = MissionAnalyzer()
        self.reporter = MissionReporter()
        self.timer = MissionTimer()
        self.current_phase = MissionPhase.PLANNING
    
    def initialize_mission(self, config: MissionConfiguration) -> bool:
        """Initialize mission with configuration"""
        issues = self.validator.validate_configuration(config)
        if issues:
            print(f"Configuration validation failed: {', '.join(issues)}")
            return False
        
        self.core.configuration = config
        self.current_phase = MissionPhase.PLANNING
        return True
    
    def start_mission_execution(self) -> bool:
        """Start mission execution phase"""
        if not self.core.configuration:
            print("Mission not initialized")
            return False
        
        self.current_phase = MissionPhase.EXECUTION
        self.timer.start()
        return True
    
    def execute_task(self, task: MissionTask) -> MissionAssessment:
        """Execute a specific task"""
        assessment = self.core.create_assessment(task, TaskStatus.IN_PROGRESS)
        assessment.phase = self.current_phase
        
        # Simulate task execution based on task type
        if task == MissionTask.TEST_AGENT7_INTERFACE:
            assessment.score = self._test_agent7_interface()
        elif task == MissionTask.VALIDATE_AGENT6_VSCODE:
            assessment.score = self._validate_agent6_vscode()
        elif task == MissionTask.DEVELOP_TESTING_FRAMEWORK:
            assessment.score = self._develop_testing_framework()
        elif task == MissionTask.ENSURE_CROSS_PLATFORM:
            assessment.score = self._ensure_cross_platform()
        elif task == MissionTask.OPTIMIZE_PERFORMANCE:
            assessment.score = self._optimize_performance()
        
        assessment.status = TaskStatus.COMPLETED if assessment.score >= 70 else TaskStatus.FAILED
        assessment.progress = 100.0
        assessment.execution_time = self.timer.get_elapsed_time()
        
        return assessment
    
    def _test_agent7_interface(self) -> float:
        """Test Agent-7 interface functionality"""
        # Simulate interface testing
        score = 85.0
        return score
    
    def _validate_agent6_vscode(self) -> float:
        """Validate Agent-6 VSCode integration"""
        # Simulate VSCode validation
        score = 90.0
        return score
    
    def _develop_testing_framework(self) -> float:
        """Develop comprehensive testing framework"""
        # Simulate framework development
        score = 88.0
        return score
    
    def _ensure_cross_platform(self) -> float:
        """Ensure cross-platform compatibility"""
        # Simulate cross-platform testing
        score = 82.0
        return score
    
    def _optimize_performance(self) -> float:
        """Optimize system performance"""
        # Simulate performance optimization
        score = 87.0
        return score
    
    def complete_mission(self) -> MissionMetrics:
        """Complete mission and return final metrics"""
        self.current_phase = MissionPhase.COMPLETION
        self.timer.stop()
        
        metrics = self.core.calculate_metrics()
        return metrics
    
    def generate_final_report(self) -> str:
        """Generate final mission report"""
        if not self.core.metrics:
            self.core.calculate_metrics()
        
        summary = self.reporter.generate_summary_report(self.core.metrics)
        detailed = self.reporter.generate_detailed_report(self.core.assessments)
        
        return summary + "\n" + detailed
    
    def get_mission_status(self) -> Dict[str, Any]:
        """Get current mission status"""
        return {
            "phase": self.current_phase.value,
            "total_tasks": len(self.core.assessments),
            "completed_tasks": sum(1 for a in self.core.assessments if a.status == TaskStatus.COMPLETED),
            "failed_tasks": sum(1 for a in self.core.assessments if a.status == TaskStatus.FAILED),
            "elapsed_time": self.timer.get_elapsed_time(),
            "configuration": self.core.configuration.title if self.core.configuration else None
        }


class MissionManager:
    """Mission management system"""
    
    def __init__(self):
        self.missions: Dict[str, DualRoleComprehensiveMission] = {}
    
    def create_mission(self, config: MissionConfiguration) -> Optional[DualRoleComprehensiveMission]:
        """Create a new mission"""
        mission = DualRoleComprehensiveMission()
        if mission.initialize_mission(config):
            self.missions[config.mission_id] = mission
            return mission
        return None
    
    def get_mission(self, mission_id: str) -> Optional[DualRoleComprehensiveMission]:
        """Get mission by ID"""
        return self.missions.get(mission_id)
    
    def list_missions(self) -> List[str]:
        """List all mission IDs"""
        return list(self.missions.keys())
    
    def execute_all_missions(self) -> Dict[str, MissionMetrics]:
        """Execute all missions and return results"""
        results = {}
        
        for mission_id, mission in self.missions.items():
            if mission.start_mission_execution():
                # Execute all tasks
                for task in MissionTask:
                    mission.execute_task(task)
                
                metrics = mission.complete_mission()
                results[mission_id] = metrics
        
        return results


def create_dual_role_mission(
    mission_id: str,
    title: str,
    description: str,
    priority: str = "normal"
) -> DualRoleComprehensiveMission:
    """Create a dual role mission"""
    config = create_mission_configuration(
        mission_id=mission_id,
        title=title,
        description=description,
        priority=priority
    )
    
    mission = DualRoleComprehensiveMission()
    mission.initialize_mission(config)
    return mission


def run_comprehensive_assessment() -> Dict[str, Any]:
    """Run comprehensive assessment of all missions"""
    manager = MissionManager()
    
    # Create test mission
    config = create_mission_configuration(
        mission_id="test_mission_001",
        title="Comprehensive Testing Mission",
        description="Full assessment of dual role capabilities",
        priority="high"
    )
    
    mission = manager.create_mission(config)
    if not mission:
        return {"error": "Failed to create mission"}
    
    # Execute mission
    mission.start_mission_execution()
    
    results = {}
    for task in MissionTask:
        assessment = mission.execute_task(task)
        results[task.value] = {
            "score": assessment.score,
            "status": assessment.status.value,
            "execution_time": assessment.execution_time
        }
    
    # Complete mission
    metrics = mission.complete_mission()
    results["final_metrics"] = {
        "total_tasks": metrics.total_tasks,
        "completed_tasks": metrics.completed_tasks,
        "success_rate": metrics.success_rate,
        "average_score": metrics.average_score,
        "quality_score": metrics.quality_score
    }
    
    return results
