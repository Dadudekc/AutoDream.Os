#!/usr/bin/env python3
"""
V3-015: System Integration Core
===============================

V2 compliant system integration coordinator for Phase 3 Dream.OS integration.
Maintains all functionality while staying under 400 lines.
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import integration modules
from v3.v3_015_integration_components import (
    ComponentManager, ComponentFactory, IntegrationStatus, ComponentType
)
from v3.v3_015_integration_tasks import TaskManager, TaskExecutor


class SystemIntegrationCoordinator:
    """Coordinates system integration components and tasks."""
    
    def __init__(self):
        self.component_manager = ComponentManager()
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor(self.task_manager)
        self.integration_status = IntegrationStatus.PENDING
        self.is_initialized = False
    
    def initialize(self):
        """Initialize system integration."""
        try:
            # Register core components
            factory = ComponentFactory()
            
            # Database components
            db_component = factory.create_database_component("db_main", {
                "host": "localhost",
                "port": 5432,
                "dependencies": []
            })
            self.component_manager.register_component(db_component)
            
            # API components
            api_component = factory.create_api_component("api_gateway", {
                "base_url": "https://api.example.com",
                "dependencies": ["db_main"]
            })
            self.component_manager.register_component(api_component)
            
            # Performance components
            perf_component = factory.create_performance_component("perf_monitor", {
                "metrics_endpoint": "/metrics",
                "dependencies": ["api_gateway"]
            })
            self.component_manager.register_component(perf_component)
            
            # NLP components
            nlp_component = factory.create_nlp_component("nlp_pipeline", {
                "model_path": "/models/nlp",
                "dependencies": ["api_gateway"]
            })
            self.component_manager.register_component(nlp_component)
            
            # Create integration tasks
            self._create_integration_tasks()
            
            self.integration_status = IntegrationStatus.IN_PROGRESS
            self.is_initialized = True
            print("🔧 System Integration Coordinator initialized successfully")
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            raise
    
    def _create_integration_tasks(self):
        """Create predefined integration tasks."""
        # Phase 1: Core Infrastructure
        self.task_manager.create_task(
            "phase1_db", "Database Setup", "Initialize database infrastructure",
            ["db_main"], priority=5
        )
        
        # Phase 2: API Integration
        self.task_manager.create_task(
            "phase2_api", "API Gateway Setup", "Setup API gateway and authentication",
            ["api_gateway"], priority=4
        )
        
        # Phase 3: Performance Monitoring
        self.task_manager.create_task(
            "phase3_perf", "Performance Monitoring", "Setup performance monitoring",
            ["perf_monitor"], priority=3
        )
        
        # Phase 4: NLP Integration
        self.task_manager.create_task(
            "phase4_nlp", "NLP Pipeline", "Integrate NLP processing pipeline",
            ["nlp_pipeline"], priority=2
        )
        
        # Phase 5: System Integration
        self.task_manager.create_task(
            "phase5_integration", "Full System Integration", "Complete system integration",
            ["db_main", "api_gateway", "perf_monitor", "nlp_pipeline"], priority=1
        )
    
    def execute_integration_phase(self, phase: str) -> Dict[str, Any]:
        """Execute a specific integration phase."""
        if not self.is_initialized:
            self.initialize()
        
        phase_tasks = {
            "phase1": "phase1_db",
            "phase2": "phase2_api", 
            "phase3": "phase3_perf",
            "phase4": "phase4_nlp",
            "phase5": "phase5_integration"
        }
        
        task_id = phase_tasks.get(phase)
        if not task_id:
            return {"error": f"Unknown phase: {phase}"}
        
        # Execute the task
        result = self.task_executor.execute_next_task()
        
        # Update integration status based on results
        if result.get("execution_result", {}).get("success", False):
            if phase == "phase5":
                self.integration_status = IntegrationStatus.COMPLETED
        else:
            self.integration_status = IntegrationStatus.FAILED
        
        return {
            "phase": phase,
            "task_id": task_id,
            "result": result,
            "integration_status": self.integration_status.value
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status."""
        if not self.is_initialized:
            return {"status": "not_initialized"}
        
        component_summary = self.component_manager.get_component_status_summary()
        task_summary = self.task_manager.get_task_summary()
        execution_stats = self.task_executor.get_execution_stats()
        
        return {
            "integration_status": self.integration_status.value,
            "initialized": self.is_initialized,
            "components": component_summary,
            "tasks": task_summary,
            "execution": execution_stats,
            "ready_components": self.component_manager.get_ready_components(),
            "last_updated": datetime.now().isoformat()
        }
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health."""
        if not self.is_initialized:
            return {"error": "System not initialized"}
        
        health_results = {}
        all_healthy = True
        
        for component_id in self.component_manager.components.keys():
            health = self.component_manager.check_component_health(component_id)
            health_results[component_id] = health
            if not health.get("healthy", False):
                all_healthy = False
        
        return {
            "overall_healthy": all_healthy,
            "component_health": health_results,
            "integration_status": self.integration_status.value,
            "checked_at": datetime.now().isoformat()
        }
    
    def retry_failed_tasks(self) -> Dict[str, Any]:
        """Retry all failed tasks."""
        if not self.is_initialized:
            return {"error": "System not initialized"}
        
        retry_results = []
        for task_id in self.task_manager.failed_tasks.copy():
            success = self.task_manager.retry_failed_task(task_id)
            retry_results.append({
                "task_id": task_id,
                "retry_success": success
            })
        
        return {
            "retry_attempts": len(retry_results),
            "results": retry_results,
            "failed_tasks_remaining": len(self.task_manager.failed_tasks)
        }
    
    def get_integration_report(self) -> Dict[str, Any]:
        """Get comprehensive integration report."""
        status = self.get_integration_status()
        health = self.check_system_health()
        
        return {
            "report_generated_at": datetime.now().isoformat(),
            "integration_status": status,
            "system_health": health,
            "recommendations": self._generate_recommendations(status, health)
        }
    
    def _generate_recommendations(self, status: Dict[str, Any], health: Dict[str, Any]) -> List[str]:
        """Generate integration recommendations."""
        recommendations = []
        
        if status["integration_status"] == "failed":
            recommendations.append("Review failed tasks and retry after fixing issues")
        
        if not health.get("overall_healthy", True):
            recommendations.append("Address unhealthy components before proceeding")
        
        if status["tasks"]["pending_tasks"] > 0:
            recommendations.append("Execute pending tasks to complete integration")
        
        if status["execution"].get("success_rate", 1.0) < 0.8:
            recommendations.append("Investigate low success rate in task execution")
        
        return recommendations


def main():
    """Main execution function."""
    print("🔧 V3-015 System Integration Core - Testing...")
    
    try:
        # Initialize coordinator
        coordinator = SystemIntegrationCoordinator()
        coordinator.initialize()
        
        # Execute integration phases
        print("\n🚀 Executing integration phases...")
        for phase in ["phase1", "phase2", "phase3", "phase4", "phase5"]:
            result = coordinator.execute_integration_phase(phase)
            print(f"   {phase}: {'✅' if result.get('result', {}).get('execution_result', {}).get('success') else '❌'}")
        
        # Get comprehensive status
        status = coordinator.get_integration_status()
        health = coordinator.check_system_health()
        report = coordinator.get_integration_report()
        
        print(f"\n📊 Integration Status:")
        print(f"   Status: {status['integration_status']}")
        print(f"   Components: {status['components']['total_components']}")
        print(f"   Tasks: {status['tasks']['total_tasks']}")
        print(f"   Success Rate: {status['execution'].get('success_rate', 0):.2%}")
        
        print(f"\n🏥 System Health:")
        print(f"   Overall Healthy: {health['overall_healthy']}")
        print(f"   Components Checked: {len(health['component_health'])}")
        
        print(f"\n📋 Recommendations:")
        for rec in report['recommendations']:
            print(f"   - {rec}")
        
        print("\n✅ V3-015 System Integration Core completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ V3-015 implementation error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

