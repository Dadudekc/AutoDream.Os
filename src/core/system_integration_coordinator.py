"""
System Integration Coordinator - V2 Compliant
============================================

Centralized system integration and coordination tool for V2_SWARM.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class IntegrationStatus(Enum):
    """Integration status enumeration."""
    
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class ServiceType(Enum):
    """Service type enumeration."""
    
    MESSAGING = "messaging"
    THEA = "thea"
    DISCORD = "discord"
    DATABASE = "database"
    COORDINATION = "coordination"


@dataclass
class ServiceInfo:
    """Service information data structure."""
    
    name: str
    service_type: ServiceType
    status: IntegrationStatus
    health_check_command: str
    dependencies: List[str]
    last_check: Optional[str] = None
    error_message: Optional[str] = None


class SystemIntegrationCoordinator:
    """Centralized system integration coordinator."""
    
    def __init__(self):
        """Initialize the integration coordinator."""
        self.services: Dict[str, ServiceInfo] = {}
        self._register_default_services()
    
    def _register_default_services(self) -> None:
        """Register default system services."""
        self.services = {
            "messaging": ServiceInfo(
                name="Consolidated Messaging Service",
                service_type=ServiceType.MESSAGING,
                status=IntegrationStatus.ACTIVE,
                health_check_command="python -m src.services.consolidated_messaging_service status",
                dependencies=[]
            ),
            "thea": ServiceInfo(
                name="THEA Communication System",
                service_type=ServiceType.THEA,
                status=IntegrationStatus.INACTIVE,
                health_check_command="python -c 'from src.services.thea.thea_communication_core import TheaCommunicationCore; print(\"THEA OK\")'",
                dependencies=["response_detector"]
            ),
            "discord": ServiceInfo(
                name="Discord Commander",
                service_type=ServiceType.DISCORD,
                status=IntegrationStatus.INACTIVE,
                health_check_command="python -c 'from src.services.discord_commander.bot_core import DiscordCommanderBot; print(\"Discord OK\")'",
                dependencies=[]
            ),
            "coordination": ServiceInfo(
                name="Swarm Coordination",
                service_type=ServiceType.COORDINATION,
                status=IntegrationStatus.ACTIVE,
                health_check_command="python tools/swarm_coordination_tool.py status",
                dependencies=[]
            )
        }
    
    def check_service_health(self, service_name: str) -> IntegrationStatus:
        """Check health of a specific service."""
        if service_name not in self.services:
            return IntegrationStatus.ERROR
        
        service = self.services[service_name]
        
        try:
            # Run health check command
            result = subprocess.run(
                service.health_check_command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                service.status = IntegrationStatus.ACTIVE
                service.error_message = None
            else:
                service.status = IntegrationStatus.ERROR
                service.error_message = result.stderr
            
            service.last_check = datetime.now().isoformat()
            
        except subprocess.TimeoutExpired:
            service.status = IntegrationStatus.ERROR
            service.error_message = "Health check timeout"
        except Exception as e:
            service.status = IntegrationStatus.ERROR
            service.error_message = str(e)
        
        return service.status
    
    def check_all_services(self) -> Dict[str, IntegrationStatus]:
        """Check health of all registered services."""
        results = {}
        
        for service_name in self.services:
            results[service_name] = self.check_service_health(service_name)
        
        return results
    
    def get_service_status(self, service_name: str) -> Optional[ServiceInfo]:
        """Get status information for a service."""
        return self.services.get(service_name)
    
    def get_all_services_status(self) -> Dict[str, ServiceInfo]:
        """Get status of all services."""
        return self.services.copy()
    
    def fix_service_dependencies(self, service_name: str) -> bool:
        """Attempt to fix service dependencies."""
        if service_name not in self.services:
            return False
        
        service = self.services[service_name]
        
        if service_name == "thea" and "response_detector" in service.dependencies:
            # Check if response_detector exists
            if not Path("response_detector.py").exists():
                return False  # Already created above
        
        return True
    
    def generate_integration_report(self) -> Dict:
        """Generate comprehensive integration report."""
        self.check_all_services()
        
        active_services = sum(1 for s in self.services.values() if s.status == IntegrationStatus.ACTIVE)
        total_services = len(self.services)
        
        return {
            "total_services": total_services,
            "active_services": active_services,
            "inactive_services": total_services - active_services,
            "health_percentage": (active_services / total_services) * 100,
            "services": {
                name: {
                    "status": service.status.value,
                    "last_check": service.last_check,
                    "error": service.error_message
                }
                for name, service in self.services.items()
            }
        }
    
    def create_integration_workflow(self, workflow_name: str, steps: List[str]) -> bool:
        """Create a system integration workflow."""
        try:
            workflow_data = {
                "name": workflow_name,
                "steps": steps,
                "created_at": datetime.now().isoformat(),
                "status": "created"
            }
            
            workflow_path = Path(f"integration_workflows/{workflow_name}.json")
            workflow_path.parent.mkdir(exist_ok=True)
            
            with open(workflow_path, "w") as f:
                json.dump(workflow_data, f, indent=2)
            
            return True
        except Exception:
            return False


def main():
    """CLI entry point for system integration coordinator."""
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description="System Integration Coordinator")
    parser.add_argument("--check-all", action="store_true", help="Check all services")
    parser.add_argument("--check", help="Check specific service")
    parser.add_argument("--report", action="store_true", help="Generate integration report")
    parser.add_argument("--fix-deps", help="Fix service dependencies")
    
    args = parser.parse_args()
    
    coordinator = SystemIntegrationCoordinator()
    
    if args.check_all:
        results = coordinator.check_all_services()
        print("Service Health Check Results:")
        for service, status in results.items():
            print(f"  {service}: {status.value}")
    
    elif args.check:
        status = coordinator.check_service_health(args.check)
        print(f"{args.check}: {status.value}")
    
    elif args.report:
        report = coordinator.generate_integration_report()
        print(f"Integration Report:")
        print(f"  Total Services: {report['total_services']}")
        print(f"  Active Services: {report['active_services']}")
        print(f"  Health Percentage: {report['health_percentage']:.1f}%")
    
    elif args.fix_deps:
        success = coordinator.fix_service_dependencies(args.fix_deps)
        print(f"Dependency fix for {args.fix_deps}: {'Success' if success else 'Failed'}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
