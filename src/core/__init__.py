#!/usr/bin/env python3
"""
Core Module - Agent Cellphone V2
================================

Core system components and managers.
"""

try:
    # Package imports
    from .core_manager import CoreManager
    from .workspace_manager import WorkspaceManager, WorkspaceConfig
    from .inbox_manager import InboxManager, Message, MessagePriority, MessageStatus
    from .task_manager import TaskManager, Task, TaskPriority, TaskStatus
    # FSM V2 Components (V2 Standards Compliant)
    from .fsm_task_v2 import FSMTask, FSMUpdate, TaskState, TaskPriority, TaskValidator
    # V2 FSM Components (V2 Standards Compliant)
    from .fsm_task_v2 import FSMTask as FSMTaskV2, FSMUpdate as FSMUpdateV2, TaskState as TaskStateV2, TaskPriority as TaskPriorityV2, TaskValidator
    from .fsm_data_v2 import FSMDataManager as FSMDataManagerV2
    from .fsm_core_v2 import FSMCoreV2
    
    # Refactored monitoring system
    from .monitor import AgentStatusMonitor, AgentInfo, AgentStatus, AgentCapability
    
    # Refactored decision-making system
    from .decision import DecisionMakingEngine, DecisionType, DecisionStatus, DecisionRequest, DecisionResult
    
    # Refactored horizontal scaling system
    from .scaling import HorizontalScalingEngine, ScalingStrategy, ScalingStatus, ScalingConfig
    
    # Refactored live status system
    from .status import LiveStatusSystem, UpdateFrequency, StatusEventType, StatusEvent
    
    # Persistent data storage (refactored)
    from .persistent_data_storage import PersistentDataStorage, StorageType, DataIntegrityLevel, StorageMetadata
    
    # Data integrity manager (refactored)
    from .integrity import DataIntegrityManager, IntegrityCheckType, RecoveryStrategy, IntegrityCheck
    
    # Decision coordination system
    from .decision_coordination_system import DecisionCoordinationSystem, CoordinationMode, CoordinationSession

    # Continuous coordination components
    from .continuous_coordinator import ContinuousCoordinator, CoordinationCycle, CoordinationState
    from .collaboration_engine import CollaborationEngine, CollaborationMetrics, CollaborationLevel

except ImportError:
    # Direct execution - add src to path
    import sys
    from pathlib import Path
    src_path = Path(__file__).parent.parent
    sys.path.insert(0, str(src_path))
    
    # Absolute imports
    from core.core_manager import CoreManager
    from core.workspace_manager import WorkspaceManager, WorkspaceConfig
    from core.inbox_manager import InboxManager, Message, MessagePriority, MessageStatus
    from core.task_manager import TaskManager, Task, TaskPriority, TaskStatus
    # FSM V2 Components (V2 Standards Compliant)
    from core.fsm_task_v2 import FSMTask, FSMUpdate, TaskState, TaskPriority, TaskValidator
    # V2 FSM Components (V2 Standards Compliant)
    from core.fsm_task_v2 import FSMTask as FSMTaskV2, FSMUpdate as FSMUpdateV2, TaskState as TaskStateV2, TaskPriority as TaskPriorityV2, TaskValidator
    from core.fsm_data_v2 import FSMDataManager as FSMDataManagerV2
    from core.fsm_core_v2 import FSMCoreV2
    
    # Refactored monitoring system
    from core.monitor import AgentStatusMonitor, AgentInfo, AgentStatus, AgentCapability
    
    # Refactored decision-making system
    from core.decision import DecisionMakingEngine, DecisionType, DecisionStatus, DecisionRequest, DecisionResult
    
    # Refactored horizontal scaling system
    from core.scaling import HorizontalScalingEngine, ScalingStrategy, ScalingStatus, ScalingConfig
    
    # Refactored live status system
    from core.status import LiveStatusSystem, UpdateFrequency, StatusEventType, StatusEvent
    
    # Persistent data storage (refactored)
    from core.persistent_data_storage import PersistentDataStorage, StorageType, DataIntegrityLevel, StorageMetadata
    
    # Data integrity manager (refactored)
    from core.integrity import DataIntegrityManager, IntegrityCheckType, RecoveryStrategy, IntegrityCheck

    # Decision coordination system
    from core.decision_coordination_system import DecisionCoordinationSystem, CoordinationMode, CoordinationSession

    # Continuous coordination components
    from core.continuous_coordinator import ContinuousCoordinator, CoordinationCycle, CoordinationState
    from core.collaboration_engine import CollaborationEngine, CollaborationMetrics, CollaborationLevel

__all__ = [
    # Core managers
    'CoreManager',
    'WorkspaceManager', 'WorkspaceConfig',
    'InboxManager', 'Message', 'MessagePriority', 'MessageStatus',
    'TaskManager', 'Task', 'TaskPriority', 'TaskStatus',
    'FSMTask', 'FSMUpdate', 'TaskState', 'TaskPriority', 'TaskValidator',
    # V2 FSM Components (V2 Standards Compliant)
    'FSMTaskV2', 'FSMUpdateV2', 'TaskStateV2', 'TaskPriorityV2', 'TaskValidator',
    'FSMDataManagerV2', 'FSMCoreV2',
    
    # Refactored agent monitoring system
    'AgentStatusMonitor', 'AgentInfo', 'AgentStatus', 'AgentCapability',
    
    # Refactored decision-making system
    'DecisionMakingEngine', 'DecisionType', 'DecisionStatus', 'DecisionRequest', 'DecisionResult',
    
    # Refactored horizontal scaling system
    'HorizontalScalingEngine', 'ScalingStrategy', 'ScalingStatus', 'ScalingConfig',
    
    # Live status system (to be refactored)
    'LiveStatusSystem', 'UpdateFrequency', 'StatusEventType', 'StatusEvent',
    
    # Persistent data storage (refactored)
    'PersistentDataStorage', 'StorageType', 'DataIntegrityLevel', 'StorageMetadata',
    
    # Data integrity manager (to be refactored)
    'DataIntegrityManager', 'IntegrityCheckType', 'RecoveryStrategy', 'IntegrityCheck',
    
    # Decision coordination system
    'DecisionCoordinationSystem', 'CoordinationMode', 'CoordinationSession',
    
    # Continuous coordination
    'ContinuousCoordinator', 'CoordinationCycle', 'CoordinationState',
    'CollaborationEngine', 'CollaborationMetrics', 'CollaborationLevel'
]


def main():
    """CLI interface for Core Module"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Core Module CLI")
    parser.add_argument("--test", "-t", action="store_true", help="Test core components")
    parser.add_argument("--status", "-s", action="store_true", help="Show core status")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Testing Core Module Components...")
        
        # Test workspace manager
        try:
            workspace_mgr = WorkspaceManager()
            print("✅ WorkspaceManager: OK")
        except Exception as e:
            print(f"❌ WorkspaceManager: {e}")
        
        # Test inbox manager
        try:
            inbox_mgr = InboxManager()
            print("✅ InboxManager: OK")
        except Exception as e:
            print(f"❌ InboxManager: {e}")
        
        # Test task manager
        try:
            task_mgr = TaskManager()
            print("✅ TaskManager: OK")
        except Exception as e:
            print(f"❌ TaskManager: {e}")
        
        # Test FSM orchestrator
        try:
            fsm_org = FSMOrchestrator()
            print("✅ FSMOrchestrator: OK")
        except Exception as e:
            print(f"❌ FSMOrchestrator: {e}")
        
        # Test refactored agent status monitor
        try:
            status_monitor = AgentStatusMonitor()
            print("✅ AgentStatusMonitor (Refactored): OK")
        except Exception as e:
            print(f"❌ AgentStatusMonitor: {e}")
        
        # Test live status system
        try:
            live_status = LiveStatusSystem()
            print("✅ LiveStatusSystem: OK")
        except Exception as e:
            print(f"❌ LiveStatusSystem: {e}")
        
        # Test refactored persistent data storage
        try:
            data_storage = PersistentDataStorage()
            print("✅ PersistentDataStorage (Refactored): OK")
        except Exception as e:
            print(f"❌ PersistentDataStorage: {e}")
        
        # Test data integrity manager
        try:
            integrity_mgr = DataIntegrityManager()
            print("✅ DataIntegrityManager: OK")
        except Exception as e:
            print(f"❌ DataIntegrityManager: {e}")
        
        # Test refactored decision making engine
        try:
            decision_engine = DecisionMakingEngine()
            print("✅ DecisionMakingEngine (Refactored): OK")
        except Exception as e:
            print(f"❌ DecisionMakingEngine: {e}")
        
        # Test decision coordination system
        try:
            coord_system = DecisionCoordinationSystem()
            print("✅ DecisionCoordinationSystem: OK")
        except Exception as e:
            print(f"❌ DecisionCoordinationSystem: {e}")
        
        # Test continuous coordinator
        try:
            cont_coord = ContinuousCoordinator()
            print("✅ ContinuousCoordinator: OK")
        except Exception as e:
            print(f"❌ ContinuousCoordinator: {e}")
        
        # Test collaboration engine
        try:
            collab_engine = CollaborationEngine()
            print("✅ CollaborationEngine: OK")
        except Exception as e:
            print(f"❌ CollaborationEngine: {e}")
        
        # Test refactored horizontal scaling engine
        try:
            scaling_engine = HorizontalScalingEngine()
            print("✅ HorizontalScalingEngine (Refactored): OK")
        except Exception as e:
            print(f"❌ HorizontalScalingEngine: {e}")
        
        print("\n🎉 Core Module Test Complete!")
    
    elif args.status:
        print("📊 Core Module Status:")
        print(f"  Total Components: {len(__all__)}")
        print(f"  Core Managers: 8")
        print(f"  Refactored Systems: 4")
        print(f"  Agent Monitoring: 1 (Refactored)")
        print(f"  Decision Making: 1 (Refactored)")
        print(f"  Horizontal Scaling: 1 (Refactored)")
        print(f"  Persistent Storage: 1 (Refactored)")
        print(f"  Live Status: 1 (Pending Refactoring)")
        print(f"  Data Integrity: 1 (Pending Refactoring)")
        print("  Status: CORE_MODULE_ACTIVE")
    
    else:
        print("Core Module - Use --help for options")


if __name__ == "__main__":
    main()
