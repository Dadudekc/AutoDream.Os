#!/usr/bin/env python3
"""
Integration Framework Manager - V2 Modular Architecture
=====================================================

Unified integration framework management system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pathlib import Path
import json

from ..types.api_types import ServiceStatus, ServiceEndpoint
from src.services.config_utils import ConfigLoader

logger = logging.getLogger(__name__)


class IntegrationFrameworkManager:
    """
    Integration Framework Manager - Single responsibility: Manage integration framework
    
    Handles all integration framework operations including:
    - Service registration and coordination
    - Integration workflow management
    - Service health monitoring
    - Cross-service communication
    - Integration configuration management
    """

    def __init__(self, config_path: str = "config/system/integration.json"):
        """Initialize integration framework manager"""
        self.logger = logging.getLogger(f"{__name__}.IntegrationFrameworkManager")
        self.config_path = Path(config_path)
        
        # Service registry
        self._services: Dict[str, ServiceEndpoint] = {}
        self._service_handlers: Dict[str, Callable] = {}
        self._service_dependencies: Dict[str, List[str]] = {}
        
        # Integration state
        self._framework_initialized = False
        self._health_monitor_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()
        
        # Configuration
        self._config: Dict[str, Any] = ConfigLoader.load(self.config_path, {})

        # Performance tracking
        self._start_time = time.time()
        self._total_integrations = 0
        self._successful_integrations = 0
        self._failed_integrations = 0
        
        self.logger.info("✅ Integration Framework Manager initialized successfully")

    def register_service(
        self,
        service_id: str,
        service_name: str,
        version: str = "1.0.0",
        base_url: Optional[str] = None,
        endpoints: Optional[List[str]] = None,
        health_check_url: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Register a service with the integration framework"""
        try:
            if service_id in self._services:
                self.logger.warning(f"Service {service_id} already registered")
                return False
            
            # Create service endpoint
            service = ServiceEndpoint(
                service_id=service_id,
                name=service_name,
                version=version,
                base_url=base_url or "",
                health_check_url=health_check_url,
                status=ServiceStatus.UNKNOWN,
                metadata=metadata or {}
            )
            
            self._services[service_id] = service
            self._service_dependencies[service_id] = dependencies or []
            
            self.logger.info(f"Service registered: {service_id} ({service_name} v{version})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register service {service_id}: {e}")
            return False

    def unregister_service(self, service_id: str) -> bool:
        """Unregister a service from the integration framework"""
        try:
            if service_id not in self._services:
                self.logger.warning(f"Service {service_id} not found")
                return False
            
            # Check if other services depend on this one
            dependent_services = [
                sid for sid, deps in self._service_dependencies.items()
                if service_id in deps
            ]
            
            if dependent_services:
                self.logger.warning(f"Service {service_id} has dependent services: {dependent_services}")
                return False
            
            # Remove service
            del self._services[service_id]
            del self._service_dependencies[service_id]
            
            if service_id in self._service_handlers:
                del self._service_handlers[service_id]
            
            self.logger.info(f"Service unregistered: {service_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister service {service_id}: {e}")
            return False

    def register_service_handler(self, service_id: str, handler: Callable) -> bool:
        """Register a handler function for a service"""
        try:
            if service_id not in self._services:
                self.logger.error(f"Service {service_id} not registered")
                return False
            
            self._service_handlers[service_id] = handler
            self.logger.info(f"Handler registered for service: {service_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register handler for {service_id}: {e}")
            return False

    def get_service(self, service_id: str) -> Optional[ServiceEndpoint]:
        """Get a specific service"""
        return self._services.get(service_id)

    def get_all_services(self) -> List[ServiceEndpoint]:
        """Get all registered services"""
        return list(self._services.values())

    def get_services_by_status(self, status: ServiceStatus) -> List[ServiceEndpoint]:
        """Get services by status"""
        return [service for service in self._services.values() if service.status == status]

    def get_service_dependencies(self, service_id: str) -> List[str]:
        """Get dependencies for a service"""
        return self._service_dependencies.get(service_id, [])

    def check_service_health(self, service_id: str) -> bool:
        """Check health of a specific service"""
        try:
            service = self._services.get(service_id)
            if not service:
                return False
            
            # In production, implement actual health check
            # For now, just update timestamp and assume healthy
            service.last_health_check = datetime.now()
            service.status = ServiceStatus.HEALTHY
            
            return True
            
        except Exception as e:
            self.logger.error(f"Health check failed for {service_id}: {e}")
            return False

    def start_health_monitoring(self, interval: int = 60):
        """Start health monitoring for all services"""
        try:
            if self._health_monitor_thread and self._health_monitor_thread.is_alive():
                self.logger.info("Health monitoring already active")
                return
            
            self._stop_monitoring.clear()
            self._health_monitor_thread = threading.Thread(
                target=self._health_monitoring_loop,
                args=(interval,),
                daemon=True
            )
            self._health_monitor_thread.start()
            
            self.logger.info(f"✅ Health monitoring started with {interval}s interval")
            
        except Exception as e:
            self.logger.error(f"Failed to start health monitoring: {e}")

    def stop_health_monitoring(self):
        """Stop health monitoring"""
        try:
            self._stop_monitoring.set()
            
            if self._health_monitor_thread:
                self._health_monitor_thread.join(timeout=5.0)
            
            self.logger.info("✅ Health monitoring stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop health monitoring: {e}")

    def _health_monitoring_loop(self, interval: int):
        """Health monitoring loop"""
        while not self._stop_monitoring.is_set():
            try:
                self._monitor_all_services()
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(5)

    def _monitor_all_services(self):
        """Monitor health of all services"""
        try:
            for service_id in self._services:
                self.check_service_health(service_id)
                
        except Exception as e:
            self.logger.error(f"Service monitoring error: {e}")

    def execute_integration_workflow(
        self,
        workflow_name: str,
        workflow_data: Dict[str, Any],
        target_services: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Execute an integration workflow"""
        try:
            self._total_integrations += 1
            start_time = time.time()
            
            # Determine target services
            if not target_services:
                target_services = list(self._services.keys())
            
            # Execute workflow for each target service
            results = {}
            for service_id in target_services:
                if service_id in self._services:
                    try:
                        result = self._execute_service_workflow(
                            service_id, workflow_name, workflow_data
                        )
                        results[service_id] = result
                        self._successful_integrations += 1
                    except Exception as e:
                        self.logger.error(f"Workflow execution failed for {service_id}: {e}")
                        results[service_id] = {"error": str(e)}
                        self._failed_integrations += 1
                else:
                    results[service_id] = {"error": "Service not found"}
                    self._failed_integrations += 1
            
            execution_time = time.time() - start_time
            
            workflow_result = {
                "workflow_name": workflow_name,
                "execution_time": execution_time,
                "target_services": target_services,
                "results": results,
                "success_count": len([r for r in results.values() if "error" not in r]),
                "error_count": len([r for r in results.values() if "error" in r])
            }
            
            self.logger.info(f"Integration workflow completed: {workflow_name} ({execution_time:.3f}s)")
            return workflow_result
            
        except Exception as e:
            self.logger.error(f"Integration workflow execution failed: {e}")
            return {"error": str(e)}

    def _execute_service_workflow(
        self, service_id: str, workflow_name: str, workflow_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute workflow for a specific service"""
        try:
            handler = self._service_handlers.get(service_id)
            if not handler:
                return {"error": "No handler registered for service"}
            
            # Execute handler
            result = handler(workflow_name, workflow_data)
            return {"success": True, "result": result}
            
        except Exception as e:
            return {"error": str(e)}

    def get_framework_status(self) -> Dict[str, Any]:
        """Get integration framework status"""
        try:
            uptime = time.time() - self._start_time
            
            return {
                "framework_initialized": self._framework_initialized,
                "uptime_seconds": uptime,
                "total_services": len(self._services),
                "total_integrations": self._total_integrations,
                "successful_integrations": self._successful_integrations,
                "failed_integrations": self._failed_integrations,
                "success_rate": self._successful_integrations / self._total_integrations if self._total_integrations > 0 else 0.0,
                "health_monitoring_active": self._health_monitor_thread and self._health_monitor_thread.is_alive(),
                "start_time": datetime.fromtimestamp(self._start_time).isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get framework status: {e}")
            return {"error": str(e)}

    def get_service_health_summary(self) -> Dict[str, Any]:
        """Get summary of all service health"""
        try:
            health_summary = {}
            
            for service_id, service in self._services.items():
                health_summary[service_id] = {
                    "name": service.name,
                    "version": service.version,
                    "status": service.status.value,
                    "last_health_check": service.last_health_check.isoformat() if service.last_health_check else None,
                    "has_handler": service_id in self._service_handlers,
                    "dependencies": self._service_dependencies.get(service_id, [])
                }
            
            return health_summary
            
        except Exception as e:
            self.logger.error(f"Failed to get service health summary: {e}")
            return {"error": str(e)}

    def update_configuration(self, new_config: Dict[str, Any]) -> bool:
        """Update integration configuration"""
        try:
            self._config.update(new_config)
            
            # Save to file
            if self.config_path.exists():
                with open(self.config_path, "w") as f:
                    json.dump(self._config, f, indent=2)
            
            self.logger.info("Configuration updated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.stop_health_monitoring()
            self.logger.info("✅ Integration Framework Manager cleanup completed")
        except Exception as e:
            self.logger.error(f"Integration Framework Manager cleanup failed: {e}")


