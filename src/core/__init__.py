import argparse
import sys

# Core component imports (conditional to avoid import errors)
try:
    from .agent_manager import AgentManager
except ImportError:
    AgentManager = None

try:
    from .api_gateway import APIGateway
except ImportError:
    APIGateway = None

try:
    from .base_manager import BaseManager, ManagerStatus, ManagerPriority, ManagerMetrics
except ImportError:
    BaseManager = ManagerStatus = ManagerPriority = ManagerMetrics = None

try:
    from .communication import CommunicationManager
except ImportError:
    CommunicationManager = None

try:
    from .core_manager import CoreManager
except ImportError:
    CoreManager = None

try:
    from .health_monitor import HealthMonitor
except ImportError:
    HealthMonitor = None

try:
    from .manager_orchestrator import ManagerOrchestrator
except ImportError:
    ManagerOrchestrator = None

try:
    from .performance import PerformanceMonitor, MetricType
except ImportError:
    PerformanceMonitor = MetricType = None

try:
    from .task_manager import TaskManager
except ImportError:
    TaskManager = None

try:
    from .tasks.executor import TaskExecutor
except ImportError:
    TaskExecutor = None

try:
    from .tasks.monitoring import TaskMonitor
except ImportError:
    TaskMonitor = None

try:
    from .tasks.recovery import TaskRecovery
except ImportError:
    TaskRecovery = None

try:
    from .tasks.scheduling import TaskScheduler, Task, TaskPriority, TaskStatus
except ImportError:
    TaskScheduler = Task = TaskPriority = TaskStatus = None

"""
🔧 Core Package - Agent_Cellphone_V2

This package contains the core components for the Agent_Cellphone_V2 system:
- Performance monitoring and tracking
- API gateway and communication
- Health monitoring and alerting
- Agent communication protocols

**SSOT IMPLEMENTATION**: All core classes are now consolidated here to eliminate
duplication and provide a single source of truth across the codebase.

Following V2 coding standards: ≤300 LOC per file, OOP design, SRP.
"""

__version__ = "2.0.0"
__author__ = "Integration & Performance Optimization Captain"
__status__ = "ACTIVE"


# SSOT: Core component imports - Single source of truth for all core classes
try:
    # Performance monitoring (SSOT: Unified from multiple locations)
    
    # Task management (SSOT: Unified task system)
    
    # Core management (SSOT: Unified manager system)
    
    # Communication (SSOT: Unified communication system)

    # Agent management (lifecycle/communication/learning)
    
    # Health monitoring (SSOT: Unified health system)
    
    # API gateway (SSOT: Unified API system)
    
    __all__ = [
        # Performance
        "PerformanceMonitor", "MetricType",
        
        # Task Management
        "TaskManager", "TaskScheduler", "Task", "TaskPriority", "TaskStatus",
        "TaskExecutor", "TaskMonitor", "TaskRecovery",
        
        # Core Management
        "BaseManager", "ManagerStatus", "ManagerPriority", "ManagerMetrics",
        "CoreManager", "ManagerOrchestrator",
        
        # Communication
        "CommunicationManager",

        # Agent Management
        "AgentManager",
        
        # Health & API
        "HealthMonitor", "APIGateway",
    ]
    
except ImportError as e:
    print(f"⚠️ Warning: Some core components not available: {e}")
    __all__ = []


def main():
    """CLI interface for core module"""
    parser = argparse.ArgumentParser(description="Core Package CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--components", action="store_true", help="List available components")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Core Package v{__version__}")
    elif args.status:
        print(f"Status: {__status__}")
        print(f"Available components: {len(__all__)}")
    elif args.components:
        print("Available Core Components:")
        for component in __all__:
            print(f"  - {component}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
