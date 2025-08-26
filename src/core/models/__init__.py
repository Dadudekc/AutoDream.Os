#!/usr/bin/env python3
"""
Unified Models Package - Agent Cellphone V2

Consolidated model framework with V2 standards compliance.
All modules ≤400 LOC for optimal maintainability.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation (V2 Compliance Refactoring)
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

# ============================================================================
# UNIFIED ENUMS - Consolidated enum system
# ============================================================================
from .unified_enums import (
    UnifiedStatus,
    UnifiedPriority,
    UnifiedSeverity,
    UnifiedType,
    UnifiedFormat,
    get_all_enum_values,
    validate_enum_value,
    get_enum_by_value
)

# ============================================================================
# BASE MODELS - Foundation classes
# ============================================================================
from .base_models import (
    BaseModel,
    StatusModel,
    TypedModel,
    ConfigurableModel,
    create_base_model,
    create_status_model,
    create_typed_model,
    create_configurable_model,
    validate_model_data
)

# ============================================================================
# HEALTH & PERFORMANCE MODELS - Domain-specific implementations
# ============================================================================
from .health_performance_models import (
    HealthModel,
    PerformanceModel,
    create_health_model,
    create_performance_model
)

# ============================================================================
# TASK & WORKFLOW MODELS - Domain-specific implementations
# ============================================================================
from .task_workflow_models import (
    TaskModel,
    WorkflowModel,
    create_task_model,
    create_workflow_model
)

# ============================================================================
# MESSAGE MODELS - Communication implementations
# ============================================================================
from .message_models import (
    MessageModel,
    NotificationModel,
    create_message_model,
    create_notification_model
)

# ============================================================================
# UNIFIED FRAMEWORK - Main entry point
# ============================================================================
from .unified_framework import (
    UnifiedModelFramework,
    ModelRegistry,
    UnifiedModelFactory,
    create_unified_model,
    get_unified_enums
)

# ============================================================================
# PACKAGE EXPORTS
# ============================================================================
__all__ = [
    # Unified Enums
    'UnifiedStatus',
    'UnifiedPriority',
    'UnifiedSeverity',
    'UnifiedType',
    'UnifiedFormat',
    'get_all_enum_values',
    'validate_enum_value',
    'get_enum_by_value',
    
    # Base Models
    'BaseModel',
    'StatusModel',
    'TypedModel',
    'ConfigurableModel',
    'create_base_model',
    'create_status_model',
    'create_typed_model',
    'create_configurable_model',
    'validate_model_data',
    
    # Health & Performance Models
    'HealthModel',
    'PerformanceModel',
    'create_health_model',
    'create_performance_model',
    
    # Task & Workflow Models
    'TaskModel',
    'WorkflowModel',
    'create_task_model',
    'create_workflow_model',
    
    # Message Models
    'MessageModel',
    'NotificationModel',
    'create_message_model',
    'create_notification_model',
    
    # Unified Framework
    'UnifiedModelFramework',
    'ModelRegistry',
    'UnifiedModelFactory',
    'create_unified_model',
    'get_unified_enums'
]

# ============================================================================
# PACKAGE METADATA
# ============================================================================
__version__ = "2.0.0"
__author__ = "Agent-3 Integration & Testing Specialist"
__description__ = "Unified Model Framework - V2 Standards Compliant"
__v2_compliant__ = True
__max_loc_per_module__ = 400

# ============================================================================
# QUICK ACCESS FUNCTIONS
# ============================================================================

def get_framework_info() -> dict:
    """Get comprehensive framework information"""
    framework = UnifiedModelFramework()
    return framework.get_model_info()

def create_model(model_type: str, **kwargs):
    """Quick function to create any model type"""
    return create_unified_model(model_type, **kwargs)

def get_available_model_types() -> list:
    """Get list of available model types"""
    return ["health", "performance", "task", "workflow", "message"]

def validate_v2_compliance() -> dict:
    """Validate V2 standards compliance"""
    import os
    
    compliance_report = {
        "v2_compliant": True,
        "modules": {},
        "total_modules": 0,
        "compliant_modules": 0
    }
    
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            filepath = os.path.join(current_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                
                module_name = filename[:-3]
                is_compliant = lines <= 400
                
                compliance_report["modules"][module_name] = {
                    "lines": lines,
                    "compliant": is_compliant
                }
                
                compliance_report["total_modules"] += 1
                if is_compliant:
                    compliance_report["compliant_modules"] += 1
                else:
                    compliance_report["v2_compliant"] = False
                    
            except Exception as e:
                compliance_report["modules"][filename] = {
                    "error": str(e),
                    "compliant": False
                }
                compliance_report["v2_compliant"] = False
    
    return compliance_report

