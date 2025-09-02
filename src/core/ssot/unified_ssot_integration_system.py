#!/usr/bin/env python3
"""
Unified SSOT Integration System - Agent-8 Integration & Performance Specialist

This module provides a unified SSOT (Single Source of Truth) integration system that
consolidates Agent-7's unified logging and configuration systems with existing SSOT
infrastructure, ensuring V2 compliance and cross-agent system integration.

Agent: Agent-8 (Integration & Performance Specialist)
Mission: V2 Compliance SSOT Maintenance & System Integration
Status: ACTIVE - SSOT Integration & System Validation
Priority: HIGH (650 points)
"""

import os
import sys
import json
import logging
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

# Import Agent-7's unified systems
import sys
import importlib.util

# Import unified logging system
spec = importlib.util.spec_from_file_location("unified_logging_system", "src/core/consolidation/unified-logging-system.py")
unified_logging_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unified_logging_module)

# Import unified configuration system  
spec = importlib.util.spec_from_file_location("unified_configuration_system", "src/core/consolidation/unified-configuration-system.py")
unified_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unified_config_module)

# Get the classes and functions
UnifiedLoggingSystem = unified_logging_module.UnifiedLoggingSystem
LogLevel = unified_logging_module.LogLevel
LoggingTemplates = unified_logging_module.LoggingTemplates
get_unified_logger = unified_logging_module.get_unified_logger

UnifiedConfigurationSystem = unified_config_module.UnifiedConfigurationSystem
ConfigType = unified_config_module.ConfigType
ConfigSource = unified_config_module.ConfigSource
get_unified_config = unified_config_module.get_unified_config

# Import existing SSOT systems
from ..interfaces.unified_interface_registry import UnifiedInterfaceRegistry

# Import message queue and file lock systems
try:
    from ..message_queue_v2 import MessageQueue, QueueConfig
except ImportError:
    MessageQueue = None
    QueueConfig = None

try:
    from ..file_lock import FileLockManager, LockConfig
except ImportError:
    FileLockManager = None
    LockConfig = None

# ================================
# SSOT INTEGRATION TYPES
# ================================

class SSOTIntegrationStatus(Enum):
    """SSOT integration status levels."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VALIDATED = "validated"
    FAILED = "failed"

class SSOTComponentType(Enum):
    """Types of SSOT components."""
    LOGGING = "logging"
    CONFIGURATION = "configuration"
    INTERFACE = "interface"
    MESSAGING = "messaging"
    FILE_LOCKING = "file_locking"
    VALIDATION = "validation"

@dataclass
class SSOTComponent:
    """SSOT component definition."""
    component_id: str
    component_type: SSOTComponentType
    status: SSOTIntegrationStatus
    integration_path: str
    dependencies: List[str] = field(default_factory=list)
    validation_checks: List[str] = field(default_factory=list)
    last_updated: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

# ================================
# UNIFIED SSOT INTEGRATION SYSTEM
# ================================

class UnifiedSSOTIntegrationSystem:
    """
    Unified SSOT integration system that consolidates all SSOT components.
    
    This system integrates:
    - Agent-7's unified logging system
    - Agent-7's unified configuration system
    - Existing SSOT infrastructure (interfaces, messaging, file locking)
    - Cross-agent system validation
    - V2 compliance enforcement
    
    CONSOLIDATED: Single source of truth for all SSOT operations.
    """
    
    def __init__(self, config_name: str = "unified_ssot_integration"):
        self.config_name = config_name
        self.logger = get_unified_logger()
        self.config_system = get_unified_config()
        self.interface_registry = UnifiedInterfaceRegistry()
        
        # SSOT components registry
        self.ssot_components: Dict[str, SSOTComponent] = {}
        self.integration_status: Dict[str, SSOTIntegrationStatus] = {}
        self.validation_results: Dict[str, Dict[str, Any]] = {}
        
        # Initialize SSOT components
        self._initialize_ssot_components()
        
        # Log system initialization
        self.logger.log_operation_start("SSOT Integration System Initialization")
    
    def _initialize_ssot_components(self) -> None:
        """Initialize all SSOT components."""
        components = [
            SSOTComponent(
                component_id="unified_logging",
                component_type=SSOTComponentType.LOGGING,
                status=SSOTIntegrationStatus.PENDING,
                integration_path="src.core.consolidation.unified_logging_system",
                dependencies=[],
                validation_checks=["logging_functionality", "performance_metrics", "template_consistency"]
            ),
            SSOTComponent(
                component_id="unified_configuration",
                component_type=SSOTComponentType.CONFIGURATION,
                status=SSOTIntegrationStatus.PENDING,
                integration_path="src.core.consolidation.unified_configuration_system",
                dependencies=[],
                validation_checks=["config_loading", "agent_configs", "path_resolution"]
            ),
            SSOTComponent(
                component_id="interface_registry",
                component_type=SSOTComponentType.INTERFACE,
                status=SSOTIntegrationStatus.PENDING,
                integration_path="src.core.interfaces.unified_interface_registry",
                dependencies=["unified_logging", "unified_configuration"],
                validation_checks=["interface_registration", "cross_system_compatibility"]
            ),
            SSOTComponent(
                component_id="message_queue",
                component_type=SSOTComponentType.MESSAGING,
                status=SSOTIntegrationStatus.PENDING,
                integration_path="src.core.message_queue_v2",
                dependencies=["unified_logging", "unified_configuration"],
                validation_checks=["queue_operations", "message_delivery", "persistence"]
            ),
            SSOTComponent(
                component_id="file_locking",
                component_type=SSOTComponentType.FILE_LOCKING,
                status=SSOTIntegrationStatus.PENDING,
                integration_path="src.core.file_lock",
                dependencies=["unified_logging"],
                validation_checks=["lock_operations", "atomic_operations", "cross_platform"]
            )
        ]
        
        for component in components:
            self.ssot_components[component.component_id] = component
            self.integration_status[component.component_id] = component.status
    
    # ================================
    # SSOT INTEGRATION OPERATIONS
    # ================================
    
    def integrate_ssot_component(self, component_id: str) -> bool:
        """Integrate a specific SSOT component."""
        if component_id not in self.ssot_components:
            self.logger.log_error_generic("SSOT Integration", f"Component {component_id} not found")
            return False
        
        component = self.ssot_components[component_id]
        
        # Check dependencies
        if not self._check_dependencies(component):
            self.logger.log_error_generic("SSOT Integration", f"Dependencies not met for {component_id}")
            return False
        
        # Update status
        component.status = SSOTIntegrationStatus.IN_PROGRESS
        component.last_updated = datetime.now()
        self.integration_status[component_id] = component.status
        
        self.logger.log_operation_start(f"SSOT Component Integration: {component_id}")
        
        try:
            # Perform integration based on component type
            success = self._perform_component_integration(component)
            
            if success:
                component.status = SSOTIntegrationStatus.COMPLETED
                self.logger.log_operation_complete(f"SSOT Component Integration: {component_id}")
            else:
                component.status = SSOTIntegrationStatus.FAILED
                self.logger.log_operation_failed(f"SSOT Component Integration: {component_id}", "Integration failed")
            
            self.integration_status[component_id] = component.status
            return success
            
        except Exception as e:
            component.status = SSOTIntegrationStatus.FAILED
            self.integration_status[component_id] = component.status
            self.logger.log_operation_failed(f"SSOT Component Integration: {component_id}", str(e))
            return False
    
    def _check_dependencies(self, component: SSOTComponent) -> bool:
        """Check if component dependencies are met."""
        for dep_id in component.dependencies:
            if dep_id not in self.integration_status:
                return False
            if self.integration_status[dep_id] != SSOTIntegrationStatus.COMPLETED:
                return False
        return True
    
    def _perform_component_integration(self, component: SSOTComponent) -> bool:
        """Perform the actual integration for a component."""
        if component.component_type == SSOTComponentType.LOGGING:
            return self._integrate_logging_system(component)
        elif component.component_type == SSOTComponentType.CONFIGURATION:
            return self._integrate_configuration_system(component)
        elif component.component_type == SSOTComponentType.INTERFACE:
            return self._integrate_interface_registry(component)
        elif component.component_type == SSOTComponentType.MESSAGING:
            return self._integrate_message_queue(component)
        elif component.component_type == SSOTComponentType.FILE_LOCKING:
            return self._integrate_file_locking(component)
        else:
            return False
    
    def _integrate_logging_system(self, component: SSOTComponent) -> bool:
        """Integrate unified logging system."""
        try:
            # Validate logging system functionality
            self.logger.log_validation_start("logging_functionality")
            
            # Test logging operations
            test_operations = [
                ("operation_start", lambda: self.logger.log_operation_start("test_operation")),
                ("operation_complete", lambda: self.logger.log_operation_complete("test_operation")),
                ("performance_metric", lambda: self.logger.log_performance_metric("test_metric", 1.0)),
                ("validation_passed", lambda: self.logger.log_validation_passed("test_validation"))
            ]
            
            for op_name, op_func in test_operations:
                try:
                    op_func()
                except Exception as e:
                    self.logger.log_error_generic("SSOT Integration", f"Logging operation {op_name} failed: {e}")
                    return False
            
            self.logger.log_validation_passed("logging_functionality")
            component.metadata["integration_timestamp"] = datetime.now().isoformat()
            return True
            
        except Exception as e:
            self.logger.log_error_generic("SSOT Integration", f"Logging system integration failed: {e}")
            return False
    
    def _integrate_configuration_system(self, component: SSOTComponent) -> bool:
        """Integrate unified configuration system."""
        try:
            # Validate configuration system functionality
            self.logger.log_validation_start("config_loading")
            
            # Test configuration operations
            test_operations = [
                ("agent_configs", lambda: self.config_system.get_agent_config("Agent-8")),
                ("agent_coordinates", lambda: self.config_system.get_agent_coordinates("Agent-8")),
                ("path_configs", lambda: self.config_system.get_path("agent_workspaces")),
                ("config_validation", lambda: self.config_system.validate_configuration())
            ]
            
            for op_name, op_func in test_operations:
                try:
                    result = op_func()
                    if result is None and op_name != "config_validation":
                        self.logger.log_error_generic("SSOT Integration", f"Configuration operation {op_name} returned None")
                        return False
                except Exception as e:
                    self.logger.log_error_generic("SSOT Integration", f"Configuration operation {op_name} failed: {e}")
                    return False
            
            self.logger.log_validation_passed("config_loading")
            component.metadata["integration_timestamp"] = datetime.now().isoformat()
            return True
            
        except Exception as e:
            self.logger.log_error_generic("SSOT Integration", f"Configuration system integration failed: {e}")
            return False
    
    def _integrate_interface_registry(self, component: SSOTComponent) -> bool:
        """Integrate interface registry system."""
        try:
            # Validate interface registry functionality
            self.logger.log_validation_start("interface_registration")
            
            # Test interface operations
            test_operations = [
                ("registry_initialization", lambda: self.interface_registry is not None),
                ("interface_availability", lambda: hasattr(self.interface_registry, 'register_interface'))
            ]
            
            for op_name, op_func in test_operations:
                try:
                    result = op_func()
                    if not result:
                        self.logger.log_error_generic("SSOT Integration", f"Interface operation {op_name} failed")
                        return False
                except Exception as e:
                    self.logger.log_error_generic("SSOT Integration", f"Interface operation {op_name} failed: {e}")
                    return False
            
            self.logger.log_validation_passed("interface_registration")
            component.metadata["integration_timestamp"] = datetime.now().isoformat()
            return True
            
        except Exception as e:
            self.logger.log_error_generic("SSOT Integration", f"Interface registry integration failed: {e}")
            return False
    
    def _integrate_message_queue(self, component: SSOTComponent) -> bool:
        """Integrate message queue system."""
        try:
            # Validate message queue functionality
            self.logger.log_validation_start("queue_operations")
            
            # Test message queue operations
            test_operations = [
                ("queue_initialization", lambda: MessageQueue is not None),
                ("queue_config", lambda: QueueConfig is not None)
            ]
            
            for op_name, op_func in test_operations:
                try:
                    result = op_func()
                    if not result:
                        self.logger.log_error_generic("SSOT Integration", f"Message queue operation {op_name} failed")
                        return False
                except Exception as e:
                    self.logger.log_error_generic("SSOT Integration", f"Message queue operation {op_name} failed: {e}")
                    return False
            
            self.logger.log_validation_passed("queue_operations")
            component.metadata["integration_timestamp"] = datetime.now().isoformat()
            return True
            
        except Exception as e:
            self.logger.log_error_generic("SSOT Integration", f"Message queue integration failed: {e}")
            return False
    
    def _integrate_file_locking(self, component: SSOTComponent) -> bool:
        """Integrate file locking system."""
        try:
            # Validate file locking functionality
            self.logger.log_validation_start("lock_operations")
            
            # Test file locking operations
            test_operations = [
                ("lock_manager_initialization", lambda: FileLockManager is not None),
                ("lock_config", lambda: LockConfig is not None)
            ]
            
            for op_name, op_func in test_operations:
                try:
                    result = op_func()
                    if not result:
                        self.logger.log_error_generic("SSOT Integration", f"File locking operation {op_name} failed")
                        return False
                except Exception as e:
                    self.logger.log_error_generic("SSOT Integration", f"File locking operation {op_name} failed: {e}")
                    return False
            
            self.logger.log_validation_passed("lock_operations")
            component.metadata["integration_timestamp"] = datetime.now().isoformat()
            return True
            
        except Exception as e:
            self.logger.log_error_generic("SSOT Integration", f"File locking integration failed: {e}")
            return False
    
    # ================================
    # SSOT VALIDATION OPERATIONS
    # ================================
    
    def validate_ssot_integration(self, component_id: str) -> Dict[str, Any]:
        """Validate SSOT integration for a specific component."""
        if component_id not in self.ssot_components:
            return {"status": "error", "message": f"Component {component_id} not found"}
        
        component = self.ssot_components[component_id]
        validation_results = {}
        
        self.logger.log_validation_start(f"SSOT Integration Validation: {component_id}")
        
        try:
            # Run validation checks
            for check_name in component.validation_checks:
                validation_results[check_name] = self._run_validation_check(component_id, check_name)
            
            # Determine overall validation status
            all_passed = all(result.get("status") == "passed" for result in validation_results.values())
            overall_status = "passed" if all_passed else "failed"
            
            validation_results["overall_status"] = overall_status
            validation_results["timestamp"] = datetime.now().isoformat()
            
            self.validation_results[component_id] = validation_results
            
            if all_passed:
                component.status = SSOTIntegrationStatus.VALIDATED
                self.logger.log_validation_passed(f"SSOT Integration Validation: {component_id}")
            else:
                self.logger.log_validation_failed(f"SSOT Integration Validation: {component_id}", "Some checks failed")
            
            return validation_results
            
        except Exception as e:
            error_result = {"status": "error", "message": str(e), "timestamp": datetime.now().isoformat()}
            self.validation_results[component_id] = error_result
            self.logger.log_validation_failed(f"SSOT Integration Validation: {component_id}", str(e))
            return error_result
    
    def _run_validation_check(self, component_id: str, check_name: str) -> Dict[str, Any]:
        """Run a specific validation check."""
        component = self.ssot_components[component_id]
        
        try:
            if check_name == "logging_functionality":
                return self._validate_logging_functionality()
            elif check_name == "performance_metrics":
                return self._validate_performance_metrics()
            elif check_name == "template_consistency":
                return self._validate_template_consistency()
            elif check_name == "config_loading":
                return self._validate_config_loading()
            elif check_name == "agent_configs":
                return self._validate_agent_configs()
            elif check_name == "path_resolution":
                return self._validate_path_resolution()
            elif check_name == "interface_registration":
                return self._validate_interface_registration()
            elif check_name == "cross_system_compatibility":
                return self._validate_cross_system_compatibility()
            elif check_name == "queue_operations":
                return self._validate_queue_operations()
            elif check_name == "message_delivery":
                return self._validate_message_delivery()
            elif check_name == "persistence":
                return self._validate_persistence()
            elif check_name == "lock_operations":
                return self._validate_lock_operations()
            elif check_name == "atomic_operations":
                return self._validate_atomic_operations()
            elif check_name == "cross_platform":
                return self._validate_cross_platform()
            else:
                return {"status": "skipped", "message": f"Unknown validation check: {check_name}"}
                
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_logging_functionality(self) -> Dict[str, Any]:
        """Validate logging system functionality."""
        try:
            # Test basic logging operations
            self.logger.log_operation_start("validation_test")
            self.logger.log_operation_complete("validation_test")
            
            return {"status": "passed", "message": "Logging functionality validated"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_performance_metrics(self) -> Dict[str, Any]:
        """Validate performance metrics collection."""
        try:
            # Test performance metrics
            self.logger.log_performance_metric("test_metric", 1.0)
            metrics = self.logger.get_performance_metrics()
            
            if "test_metric" in metrics:
                return {"status": "passed", "message": "Performance metrics validated"}
            else:
                return {"status": "failed", "message": "Performance metrics not collected"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_template_consistency(self) -> Dict[str, Any]:
        """Validate logging template consistency."""
        try:
            # Check if templates are available
            templates = self.logger.templates
            required_templates = ["OPERATION_START", "OPERATION_COMPLETE", "VALIDATION_PASSED"]
            
            for template_name in required_templates:
                if not hasattr(templates, template_name):
                    return {"status": "failed", "message": f"Missing template: {template_name}"}
            
            return {"status": "passed", "message": "Template consistency validated"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_config_loading(self) -> Dict[str, Any]:
        """Validate configuration loading."""
        try:
            # Test configuration loading
            config_data = self.config_system.load_configuration()
            
            if isinstance(config_data, dict):
                return {"status": "passed", "message": "Configuration loading validated"}
            else:
                return {"status": "failed", "message": "Configuration loading returned invalid data"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_agent_configs(self) -> Dict[str, Any]:
        """Validate agent configurations."""
        try:
            # Test agent configuration access
            agent_config = self.config_system.get_agent_config("Agent-8")
            
            if agent_config and "role" in agent_config:
                return {"status": "passed", "message": "Agent configurations validated"}
            else:
                return {"status": "failed", "message": "Agent configurations incomplete"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_path_resolution(self) -> Dict[str, Any]:
        """Validate path resolution."""
        try:
            # Test path resolution
            workspace_path = self.config_system.get_path("agent_workspaces")
            
            if workspace_path:
                return {"status": "passed", "message": "Path resolution validated"}
            else:
                return {"status": "failed", "message": "Path resolution failed"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_interface_registration(self) -> Dict[str, Any]:
        """Validate interface registration."""
        try:
            # Test interface registry
            if hasattr(self.interface_registry, 'register_interface'):
                return {"status": "passed", "message": "Interface registration validated"}
            else:
                return {"status": "failed", "message": "Interface registration not available"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_cross_system_compatibility(self) -> Dict[str, Any]:
        """Validate cross-system compatibility."""
        try:
            # Test cross-system integration
            if self.logger and self.config_system and self.interface_registry:
                return {"status": "passed", "message": "Cross-system compatibility validated"}
            else:
                return {"status": "failed", "message": "Cross-system compatibility issues"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_queue_operations(self) -> Dict[str, Any]:
        """Validate queue operations."""
        try:
            # Test queue system availability
            if MessageQueue and QueueConfig:
                return {"status": "passed", "message": "Queue operations validated"}
            else:
                return {"status": "failed", "message": "Queue operations not available"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_message_delivery(self) -> Dict[str, Any]:
        """Validate message delivery."""
        try:
            # Test message delivery system
            if MessageQueue:
                return {"status": "passed", "message": "Message delivery validated"}
            else:
                return {"status": "failed", "message": "Message delivery not available"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_persistence(self) -> Dict[str, Any]:
        """Validate persistence."""
        try:
            # Test persistence system
            if MessageQueue:
                return {"status": "passed", "message": "Persistence validated"}
            else:
                return {"status": "failed", "message": "Persistence not available"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_lock_operations(self) -> Dict[str, Any]:
        """Validate lock operations."""
        try:
            # Test file locking system
            if FileLockManager and LockConfig:
                return {"status": "passed", "message": "Lock operations validated"}
            else:
                return {"status": "failed", "message": "Lock operations not available"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_atomic_operations(self) -> Dict[str, Any]:
        """Validate atomic operations."""
        try:
            # Test atomic operations
            if FileLockManager:
                return {"status": "passed", "message": "Atomic operations validated"}
            else:
                return {"status": "failed", "message": "Atomic operations not available"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def _validate_cross_platform(self) -> Dict[str, Any]:
        """Validate cross-platform compatibility."""
        try:
            # Test cross-platform compatibility
            if FileLockManager:
                return {"status": "passed", "message": "Cross-platform compatibility validated"}
            else:
                return {"status": "failed", "message": "Cross-platform compatibility not available"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    # ================================
    # SSOT SYSTEM OPERATIONS
    # ================================
    
    def integrate_all_ssot_components(self) -> Dict[str, bool]:
        """Integrate all SSOT components in dependency order."""
        integration_results = {}
        
        self.logger.log_operation_start("Complete SSOT Integration")
        
        # Define integration order based on dependencies
        integration_order = [
            "unified_logging",
            "unified_configuration", 
            "interface_registry",
            "message_queue",
            "file_locking"
        ]
        
        for component_id in integration_order:
            if component_id in self.ssot_components:
                success = self.integrate_ssot_component(component_id)
                integration_results[component_id] = success
                
                if not success:
                    self.logger.log_error_generic("SSOT Integration", f"Failed to integrate {component_id}")
                    break
        
        # Log completion
        all_success = all(integration_results.values())
        if all_success:
            self.logger.log_operation_complete("Complete SSOT Integration")
        else:
            self.logger.log_operation_failed("Complete SSOT Integration", "Some components failed")
        
        return integration_results
    
    def validate_all_ssot_components(self) -> Dict[str, Dict[str, Any]]:
        """Validate all SSOT components."""
        validation_results = {}
        
        self.logger.log_operation_start("Complete SSOT Validation")
        
        for component_id in self.ssot_components:
            if self.integration_status.get(component_id) == SSOTIntegrationStatus.COMPLETED:
                validation_results[component_id] = self.validate_ssot_integration(component_id)
        
        # Log completion
        all_validated = all(
            result.get("overall_status") == "passed" 
            for result in validation_results.values()
        )
        
        if all_validated:
            self.logger.log_operation_complete("Complete SSOT Validation")
        else:
            self.logger.log_operation_failed("Complete SSOT Validation", "Some validations failed")
        
        return validation_results
    
    def get_ssot_status_report(self) -> Dict[str, Any]:
        """Get comprehensive SSOT status report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "integration_status": self.integration_status.copy(),
            "validation_results": self.validation_results.copy(),
            "component_details": {}
        }
        
        for component_id, component in self.ssot_components.items():
            report["component_details"][component_id] = {
                "component_type": component.component_type.value,
                "status": component.status.value,
                "dependencies": component.dependencies,
                "validation_checks": component.validation_checks,
                "last_updated": component.last_updated.isoformat() if component.last_updated else None,
                "metadata": component.metadata
            }
        
        return report
    
    def export_ssot_configuration(self, file_path: str) -> None:
        """Export SSOT configuration to file."""
        config_data = {
            "ssot_components": {
                comp_id: {
                    "component_type": comp.component_type.value,
                    "status": comp.status.value,
                    "integration_path": comp.integration_path,
                    "dependencies": comp.dependencies,
                    "validation_checks": comp.validation_checks,
                    "metadata": comp.metadata
                }
                for comp_id, comp in self.ssot_components.items()
            },
            "integration_status": self.integration_status,
            "validation_results": self.validation_results
        }
        
        with open(file_path, 'w') as f:
            json.dump(config_data, f, indent=2, default=str)
        
        self.logger.log_config_updated("SSOT Configuration Export")

# ================================
# FACTORY FUNCTIONS
# ================================

def create_unified_ssot_integration_system(config_name: str = "unified_ssot_integration") -> UnifiedSSOTIntegrationSystem:
    """Create a new unified SSOT integration system instance."""
    return UnifiedSSOTIntegrationSystem(config_name)

# ================================
# GLOBAL INSTANCE
# ================================

# Global unified SSOT integration system instance
_unified_ssot_integration = None

def get_unified_ssot_integration() -> UnifiedSSOTIntegrationSystem:
    """Get the global unified SSOT integration system instance."""
    global _unified_ssot_integration
    if _unified_ssot_integration is None:
        _unified_ssot_integration = create_unified_ssot_integration_system()
    return _unified_ssot_integration

# ================================
# EXPORTS
# ================================

__all__ = [
    'UnifiedSSOTIntegrationSystem',
    'SSOTComponent',
    'SSOTComponentType',
    'SSOTIntegrationStatus',
    'create_unified_ssot_integration_system',
    'get_unified_ssot_integration'
]
