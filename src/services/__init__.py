#!/usr/bin/env python3
"""
Services Module - Agent Cellphone V2
====================================

Service layer modules with strict OOP design and CLI testing interfaces.
Follows Single Responsibility Principle with 200 LOC limit per file.
"""

from .agent_cell_phone import AgentCellPhone
from .response_capture_service import ResponseCaptureService, CapturedResponse, CaptureStrategy
from .agent_onboarding_service import AgentOnboardingService, OnboardingStatus, AgentRole, TrainingModule
from .training_content_service import TrainingContentService
from .training_content_definitions import TrainingContent, ContentType, DifficultyLevel
from .role_assignment_service import RoleAssignmentService, Capability, PermissionLevel, CapabilityType
from .orientation_workflow_service import OrientationWorkflowService, WorkflowStep, WorkflowStatus
from .contract_lifecycle_service import ContractLifecycleService, ContractState, ContractType
from .contract_validation_service import ContractValidationService, ViolationType, ValidationSeverity
from .unified_contract_manager import UnifiedContractManager
from .perpetual_motion_contract_service import PerpetualMotionContractService

__all__ = [
    # Core Services
    "AgentCellPhone",
    "ResponseCaptureService",
    "CapturedResponse", 
    "CaptureStrategy",
    
    # Onboarding Services
    "AgentOnboardingService",
    "OnboardingStatus",
    "AgentRole",
    "TrainingModule",
    
    # Training Services
    "TrainingContentService",
    "TrainingContent",
    "ContentType",
    "DifficultyLevel",
    
    # Role Management
    "RoleAssignmentService",
    "Capability",
    "PermissionLevel",
    "CapabilityType",
    
    # Workflow Services
    "OrientationWorkflowService",
    "WorkflowStep",
    "WorkflowStatus",
    
    # Contract Management
    "ContractLifecycleService",
    "ContractState",
    "ContractType",
    "ContractValidationService",
    "ViolationType",
    "ValidationSeverity",
    "UnifiedContractManager",
    
    # Perpetual Motion
    "PerpetualMotionContractService"
]

def get_services_info():
    """Get services module information for CLI testing."""
    return {
        "module": "services",
        "components": __all__,
        "standards": [
            "Object-Oriented Design",
            "Single Responsibility Principle",
            "200 LOC limit per file",
            "CLI interface for testing"
        ]
    }

if __name__ == "__main__":
    """CLI interface for services module testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Services Module Testing Interface")
    parser.add_argument("--info", action="store_true", help="Show services module information")
    parser.add_argument("--test", action="store_true", help="Run services module tests")
    
    args = parser.parse_args()
    
    if args.info or not any([args.info, args.test]):
        info = get_services_info()
        print(f"🔧 Services Module - Agent Cellphone V2")
        print(f"Components: {', '.join(info['components'])}")
        print("Standards:")
        for standard in info['standards']:
            print(f"  ✅ {standard}")
    
    if args.test:
        print("🧪 Running services module tests...")
        try:
            # Import and test service components
            from .agent_cell_phone import AgentCellPhone
            from .response_capture_service import ResponseCaptureService
            from .agent_onboarding_service import AgentOnboardingService
            from .training_content_service import TrainingContentService
            from .role_assignment_service import RoleAssignmentService
            from .orientation_workflow_service import OrientationWorkflowService
            from .contract_lifecycle_service import ContractLifecycleService
            from .contract_validation_service import ContractValidationService
            from .unified_contract_manager import UnifiedContractManager
            
            service1 = AgentCellPhone()
            print("✅ AgentCellPhone imported and instantiated successfully")
            
            service2 = ResponseCaptureService()
            print("✅ ResponseCaptureService imported and instantiated successfully")
            
            service3 = AgentOnboardingService()
            print("✅ AgentOnboardingService imported and instantiated successfully")
            
            service4 = TrainingContentService()
            print("✅ TrainingContentService imported and instantiated successfully")
            
            service5 = RoleAssignmentService()
            print("✅ RoleAssignmentService imported and instantiated successfully")
            
            service6 = OrientationWorkflowService()
            print("✅ OrientationWorkflowService imported and instantiated successfully")
            
            service7 = ContractLifecycleService()
            print("✅ ContractLifecycleService imported and instantiated successfully")
            
            service8 = ContractValidationService()
            print("✅ ContractValidationService imported and instantiated successfully")
            
            service9 = UnifiedContractManager()
            print("✅ UnifiedContractManager imported and instantiated successfully")
            
        except Exception as e:
            print(f"❌ Services module test failed: {e}")
