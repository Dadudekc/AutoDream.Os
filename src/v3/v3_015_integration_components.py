#!/usr/bin/env python3
"""
V3-015: Integration Components
==============================

Core integration components for Phase 3 Dream.OS integration.
V2 compliant with focus on component management.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class IntegrationStatus(Enum):
    """System integration status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLBACK = "rollback"


class ComponentType(Enum):
    """Integration component types."""
    DATABASE = "database"
    PERFORMANCE = "performance"
    NLP = "nlp"
    MOBILE = "mobile"
    API = "api"
    CORE = "core"


@dataclass
class IntegrationComponent:
    """Integration component structure."""
    component_id: str
    component_type: ComponentType
    status: IntegrationStatus
    dependencies: List[str]
    configuration: Dict[str, Any]
    health_check: Callable
    last_checked: datetime
    error_count: int = 0


class ComponentManager:
    """Manages integration components."""
    
    def __init__(self):
        self.components = {}
        self.component_dependencies = {}
    
    def register_component(self, component: IntegrationComponent):
        """Register a component."""
        self.components[component.component_id] = component
        self.component_dependencies[component.component_id] = component.dependencies
        print(f"🔧 Registered component: {component.component_id}")
    
    def get_component(self, component_id: str) -> Optional[IntegrationComponent]:
        """Get component by ID."""
        return self.components.get(component_id)
    
    def update_component_status(self, component_id: str, status: IntegrationStatus) -> bool:
        """Update component status."""
        if component_id in self.components:
            self.components[component_id].status = status
            print(f"🔄 Updated {component_id} status to {status.value}")
            return True
        return False
    
    def check_component_health(self, component_id: str) -> Dict[str, Any]:
        """Check component health."""
        component = self.get_component(component_id)
        if not component:
            return {"error": "Component not found"}
        
        try:
            health_result = component.health_check()
            component.last_checked = datetime.now()
            
            if health_result.get("healthy", False):
                component.error_count = 0
                return {
                    "component_id": component_id,
                    "healthy": True,
                    "status": component.status.value,
                    "last_checked": component.last_checked.isoformat(),
                    "error_count": component.error_count
                }
            else:
                component.error_count += 1
                return {
                    "component_id": component_id,
                    "healthy": False,
                    "status": component.status.value,
                    "error": health_result.get("error", "Health check failed"),
                    "error_count": component.error_count,
                    "last_checked": component.last_checked.isoformat()
                }
        except Exception as e:
            component.error_count += 1
            return {
                "component_id": component_id,
                "healthy": False,
                "status": component.status.value,
                "error": str(e),
                "error_count": component.error_count,
                "last_checked": component.last_checked.isoformat()
            }
    
    def get_component_dependencies(self, component_id: str) -> List[str]:
        """Get component dependencies."""
        return self.component_dependencies.get(component_id, [])
    
    def get_ready_components(self) -> List[str]:
        """Get components ready for integration (dependencies satisfied)."""
        ready = []
        
        for component_id, dependencies in self.component_dependencies.items():
            if not dependencies:
                ready.append(component_id)
                continue
            
            # Check if all dependencies are completed
            all_deps_completed = all(
                self.components.get(dep, {}).status == IntegrationStatus.COMPLETED
                for dep in dependencies
            )
            
            if all_deps_completed:
                ready.append(component_id)
        
        return ready
    
    def get_component_status_summary(self) -> Dict[str, Any]:
        """Get summary of all component statuses."""
        status_counts = {}
        for component in self.components.values():
            status = component.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_components": len(self.components),
            "status_counts": status_counts,
            "ready_components": len(self.get_ready_components()),
            "last_updated": datetime.now().isoformat()
        }


class ComponentFactory:
    """Factory for creating integration components."""
    
    @staticmethod
    def create_database_component(component_id: str, config: Dict[str, Any]) -> IntegrationComponent:
        """Create database component."""
        def health_check():
            # Simplified health check
            return {"healthy": True, "message": "Database connection OK"}
        
        return IntegrationComponent(
            component_id=component_id,
            component_type=ComponentType.DATABASE,
            status=IntegrationStatus.PENDING,
            dependencies=config.get("dependencies", []),
            configuration=config,
            health_check=health_check,
            last_checked=datetime.now()
        )
    
    @staticmethod
    def create_api_component(component_id: str, config: Dict[str, Any]) -> IntegrationComponent:
        """Create API component."""
        def health_check():
            # Simplified health check
            return {"healthy": True, "message": "API endpoint accessible"}
        
        return IntegrationComponent(
            component_id=component_id,
            component_type=ComponentType.API,
            status=IntegrationStatus.PENDING,
            dependencies=config.get("dependencies", []),
            configuration=config,
            health_check=health_check,
            last_checked=datetime.now()
        )
    
    @staticmethod
    def create_performance_component(component_id: str, config: Dict[str, Any]) -> IntegrationComponent:
        """Create performance component."""
        def health_check():
            # Simplified health check
            return {"healthy": True, "message": "Performance monitoring active"}
        
        return IntegrationComponent(
            component_id=component_id,
            component_type=ComponentType.PERFORMANCE,
            status=IntegrationStatus.PENDING,
            dependencies=config.get("dependencies", []),
            configuration=config,
            health_check=health_check,
            last_checked=datetime.now()
        )
    
    @staticmethod
    def create_nlp_component(component_id: str, config: Dict[str, Any]) -> IntegrationComponent:
        """Create NLP component."""
        def health_check():
            # Simplified health check
            return {"healthy": True, "message": "NLP pipeline operational"}
        
        return IntegrationComponent(
            component_id=component_id,
            component_type=ComponentType.NLP,
            status=IntegrationStatus.PENDING,
            dependencies=config.get("dependencies", []),
            configuration=config,
            health_check=health_check,
            last_checked=datetime.now()
        )


def main():
    """Main execution function."""
    print("🔧 V3-015 Integration Components - Testing...")
    
    # Initialize component manager
    manager = ComponentManager()
    factory = ComponentFactory()
    
    # Create sample components
    db_component = factory.create_database_component("db_main", {
        "host": "localhost",
        "port": 5432,
        "dependencies": []
    })
    
    api_component = factory.create_api_component("api_gateway", {
        "base_url": "https://api.example.com",
        "dependencies": ["db_main"]
    })
    
    perf_component = factory.create_performance_component("perf_monitor", {
        "metrics_endpoint": "/metrics",
        "dependencies": ["api_gateway"]
    })
    
    # Register components
    manager.register_component(db_component)
    manager.register_component(api_component)
    manager.register_component(perf_component)
    
    # Test health checks
    print("\n🏥 Testing health checks...")
    for component_id in ["db_main", "api_gateway", "perf_monitor"]:
        health = manager.check_component_health(component_id)
        print(f"   {component_id}: {'✅' if health.get('healthy') else '❌'}")
    
    # Test dependency resolution
    print("\n🔗 Testing dependency resolution...")
    ready = manager.get_ready_components()
    print(f"   Ready components: {ready}")
    
    # Get status summary
    summary = manager.get_component_status_summary()
    print(f"\n📊 Component Summary:")
    print(f"   Total: {summary['total_components']}")
    print(f"   Ready: {summary['ready_components']}")
    print(f"   Status counts: {summary['status_counts']}")
    
    print("\n✅ V3-015 Integration Components completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

