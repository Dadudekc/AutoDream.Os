#!/usr/bin/env python3
"""
Core Manager - Agent Cellphone V2
=================================

Core business logic manager with strict OOP design and CLI testing interface.
Follows Single Responsibility Principle with 200 LOC limit.
Now inherits from BaseManager for unified functionality.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

from src.utils.stability_improvements import stability_manager, safe_import
from .base_manager import BaseManager, ManagerStatus, ManagerPriority


class CoreManager(BaseManager):
    """
    Core Manager - Single responsibility: Core system management and coordination.

    This class manages the core system functionality including:
    - System initialization
    - Configuration management
    - Component coordination
    - Health monitoring
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, config_path: str = "config"):
        """Initialize Core Manager with BaseManager"""
        super().__init__(
            manager_id="core_manager",
            name="Core Manager",
            description="Core system management and coordination"
        )
        
        self.config_path = Path(config_path)
        self.config = self._load_configuration()
        self.components = {}
        
        # Core management tracking
        self.component_registrations: List[Dict[str, Any]] = []
        self.configuration_operations: List[Dict[str, Any]] = []
        self.system_operations: List[Dict[str, Any]] = []
        
        self.logger.info("Core Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize core management system"""
        try:
            self.logger.info("Starting Core Manager...")
            
            # Clear tracking data
            self.component_registrations.clear()
            self.configuration_operations.clear()
            self.system_operations.clear()
            
            # Initialize system
            if not self.initialize_system():
                raise RuntimeError("Failed to initialize core system")
            
            self.logger.info("Core Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Core Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup core management system"""
        try:
            self.logger.info("Stopping Core Manager...")
            
            # Save tracking data
            self._save_core_management_data()
            
            # Shutdown system
            self.shutdown_system()
            
            # Clear data
            self.component_registrations.clear()
            self.configuration_operations.clear()
            self.system_operations.clear()
            
            self.logger.info("Core Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Core Manager: {e}")
    
    def _on_heartbeat(self):
        """Core manager heartbeat"""
        try:
            # Check core management health
            self._check_core_management_health()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize core management resources"""
        try:
            # Initialize data structures
            self.component_registrations = []
            self.configuration_operations = []
            self.system_operations = []
            
            # Ensure config directory exists
            self.config_path.mkdir(parents=True, exist_ok=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup core management resources"""
        try:
            # Clear data
            self.component_registrations.clear()
            self.configuration_operations.clear()
            self.system_operations.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reload configuration
            self.config = self._load_configuration()
            
            # Reset tracking
            self.component_registrations.clear()
            self.configuration_operations.clear()
            self.system_operations.clear()
            
            # Reinitialize system
            if self.initialize_system():
                self.logger.info("Recovery successful")
                return True
            else:
                self.logger.error("Recovery failed: system initialization failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Core Management Methods
    # ============================================================================
    
    def _load_configuration(self) -> Dict:
        """Load system configuration from config files."""
        try:
            start_time = datetime.now()
            
            config = {}

            # Load runtime modes
            modes_file = self.config_path / "modes_runtime.json"
            if modes_file.exists():
                with open(modes_file, "r") as f:
                    config["modes"] = json.load(f)
                    self.logger.info("Runtime modes configuration loaded")

            # Load agent coordinates
            coords_file = self.config_path / "cursor_agent_coords.json"
            if coords_file.exists():
                with open(coords_file, "r") as f:
                    config["coordinates"] = json.load(f)
                    self.logger.info("Agent coordinates configuration loaded")
            
            # Record configuration operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "load_configuration",
                "config_keys": list(config.keys()),
                "success": True
            }
            self.configuration_operations.append(operation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("load_configuration", True, operation_time)

        except Exception as e:
            self.logger.error(f"Configuration loading failed: {e}")
            config = {}
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "load_configuration",
                "error": str(e),
                "success": False
            }
            self.configuration_operations.append(operation_record)
            
            self.record_operation("load_configuration", False, 0.0)

        return config

    def initialize_system(self) -> bool:
        """Initialize the core system."""
        try:
            start_time = datetime.now()
            
            self.logger.info("Initializing core system...")

            # Verify configuration
            if not self.config:
                self.logger.error("No configuration loaded")
                self.record_operation("initialize_system", False, 0.0)
                return False

            # Set status
            self.status = ManagerStatus.RUNNING
            
            # Record system operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "initialize_system",
                "success": True
            }
            self.system_operations.append(operation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("initialize_system", True, operation_time)
            
            self.logger.info("Core system initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"System initialization failed: {e}")
            self.status = ManagerStatus.ERROR
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "initialize_system",
                "error": str(e),
                "success": False
            }
            self.system_operations.append(operation_record)
            
            self.record_operation("initialize_system", False, 0.0)
            return False

    def get_system_status(self) -> Dict:
        """Get current system status."""
        try:
            status = {
                "status": self.status.value,
                "config_loaded": bool(self.config),
                "components": len(self.components),
                "config_keys": list(self.config.keys()) if self.config else [],
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_system_status", True, 0.0)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            self.record_operation("get_system_status", False, 0.0)
            return {"error": str(e)}

    def register_component(self, name: str, component: object) -> bool:
        """Register a component with the core manager."""
        try:
            start_time = datetime.now()
            
            self.components[name] = component
            
            # Record component registration
            registration_record = {
                "timestamp": datetime.now().isoformat(),
                "component_name": name,
                "component_type": type(component).__name__,
                "success": True
            }
            self.component_registrations.append(registration_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("register_component", True, operation_time)
            
            self.logger.info(f"Component '{name}' registered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Component registration failed: {e}")
            
            # Record failed registration
            registration_record = {
                "timestamp": datetime.now().isoformat(),
                "component_name": name,
                "error": str(e),
                "success": False
            }
            self.component_registrations.append(registration_record)
            
            self.record_operation("register_component", False, 0.0)
            return False

    def get_component(self, name: str) -> Optional[object]:
        """Get a registered component by name."""
        try:
            component = self.components.get(name)
            
            # Record operation
            self.record_operation("get_component", component is not None, 0.0)
            
            return component
            
        except Exception as e:
            self.logger.error(f"Failed to get component {name}: {e}")
            self.record_operation("get_component", False, 0.0)
            return None

    def shutdown_system(self) -> bool:
        """Shutdown the core system."""
        try:
            start_time = datetime.now()
            
            self.logger.info("Shutting down core system...")
            self.status = ManagerStatus.STOPPED
            self.components.clear()
            
            # Record system operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "shutdown_system",
                "success": True
            }
            self.system_operations.append(operation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("shutdown_system", True, operation_time)
            
            self.logger.info("Core system shutdown complete")
            return True
            
        except Exception as e:
            self.logger.error(f"System shutdown failed: {e}")
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "shutdown_system",
                "error": str(e),
                "success": False
            }
            self.system_operations.append(operation_record)
            
            self.record_operation("shutdown_system", False, 0.0)
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_core_management_data(self):
        """Save core management data (placeholder for future persistence)"""
        try:
            # TODO: Implement persistence to database/file
            self.logger.debug("Core management data saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save core management data: {e}")
    
    def _check_core_management_health(self):
        """Check core management health status"""
        try:
            # Check for excessive component registrations
            if len(self.component_registrations) > 1000:
                self.logger.warning(f"High number of component registrations: {len(self.component_registrations)}")
            
            # Check system operations
            if len(self.system_operations) > 500:
                self.logger.info(f"Large system operations history: {len(self.system_operations)} records")
                
        except Exception as e:
            self.logger.error(f"Failed to check core management health: {e}")
    
    def get_core_management_stats(self) -> Dict[str, Any]:
        """Get core management statistics"""
        try:
            stats = {
                "total_components": len(self.components),
                "component_registrations_count": len(self.component_registrations),
                "configuration_operations_count": len(self.configuration_operations),
                "system_operations_count": len(self.system_operations),
                "config_loaded": bool(self.config),
                "config_keys": list(self.config.keys()) if self.config else [],
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_core_management_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get core management stats: {e}")
            self.record_operation("get_core_management_stats", False, 0.0)
            return {"error": str(e)}


def main():
    """CLI interface for Core Manager testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Core Manager Testing Interface")
    parser.add_argument("--init", action="store_true", help="Initialize core system")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--test", action="store_true", help="Run core manager tests")
    parser.add_argument("--shutdown", action="store_true", help="Shutdown core system")

    args = parser.parse_args()

    # Create core manager instance
    manager = CoreManager()

    if args.init or not any([args.init, args.status, args.test, args.shutdown]):
        print("🚀 Core Manager - Agent Cellphone V2")
        success = manager.initialize_system()
        print(f"System initialization: {'✅ Success' if success else '❌ Failed'}")

    if args.status:
        status = manager.get_system_status()
        print("📊 System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")

    if args.test:
        print("🧪 Running core manager tests...")
        try:
            # Test component registration
            test_component = {"name": "test", "type": "test"}
            success = manager.register_component("test", test_component)
            print(f"Component registration: {'✅ Success' if success else '❌ Failed'}")

            # Test component retrieval
            component = manager.get_component("test")
            print(f"Component retrieval: {'✅ Success' if component else '❌ Failed'}")

        except Exception as e:
            print(f"❌ Core manager test failed: {e}")

    if args.shutdown:
        success = manager.shutdown_system()
        print(f"System shutdown: {'✅ Success' if success else '❌ Failed'}")


if __name__ == "__main__":
    main()
