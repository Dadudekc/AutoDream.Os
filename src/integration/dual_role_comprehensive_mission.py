"""
Dual Role Comprehensive Mission System
Testing & Documentation + Integration Specialist comprehensive assessment
Refactored into modular components for V2 compliance
"""

# Import all components from refactored modules
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
from .dual_role_comprehensive_mission_main import (
    DualRoleComprehensiveMission,
    MissionManager,
    create_dual_role_mission,
    run_comprehensive_assessment
)

# Re-export main classes for backward compatibility
__all__ = [
    'MissionTask',
    'TaskStatus',
    'MissionPhase',
    'MissionAssessment',
    'MissionConfiguration',
    'MissionMetrics',
    'MissionCore',
    'MissionValidator',
    'MissionAnalyzer',
    'MissionReporter',
    'MissionTimer',
    'DualRoleComprehensiveMission',
    'MissionManager',
    'create_mission_configuration',
    'create_dual_role_mission',
    'run_comprehensive_assessment',
    'format_execution_time'
]