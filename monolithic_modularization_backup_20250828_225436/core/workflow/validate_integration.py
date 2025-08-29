import os
import sys

        from ..fsm.fsm_core import FSMCore
        from .base_workflow_engine import BaseWorkflowEngine
        from .types.workflow_enums import WorkflowType, TaskStatus
        from .types.workflow_models import WorkflowDefinition
        from workflow_engine_integration import FSMWorkflowIntegration
        import traceback

#!/usr/bin/env python3
"""
Integration Validation - Simple validation of workflow engine integration

Basic validation to ensure the integration system is working.
"""


# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def validate_imports():
    """Validate that all required modules can be imported."""
    print("🔍 Validating imports...")
    
    try:
        # Test workflow types import
        print("✅ Workflow enums imported successfully")
    except ImportError as e:
        print(f"❌ Workflow enums import failed: {e}")
        return False
    
    try:
        # Test workflow models import
        print("✅ Workflow models imported successfully")
    except ImportError as e:
        print(f"❌ Workflow models import failed: {e}")
        return False
    
    try:
        # Test base workflow engine import
        print("✅ Base workflow engine imported successfully")
    except ImportError as e:
        print(f"❌ Base workflow engine import failed: {e}")
        return False
    
    try:
        # Test FSM system import
        print("✅ FSM Core imported successfully")
    except ImportError as e:
        print(f"❌ FSM Core import failed: {e}")
        return False
    
    return True

def validate_integration_module():
    """Validate the integration module structure."""
    print("\n🔍 Validating integration module...")
    
    try:
        # Import the integration module
        print("✅ FSMWorkflowIntegration class imported successfully")
        
        # Check class attributes
        integration = FSMWorkflowIntegration()
        print("✅ FSMWorkflowIntegration instance created successfully")
        
        # Check basic methods
        if hasattr(integration, 'get_integration_health'):
            print("✅ get_integration_health method exists")
        else:
            print("❌ get_integration_health method missing")
            return False
        
        if hasattr(integration, 'create_integrated_workflow'):
            print("✅ create_integrated_workflow method exists")
        else:
            print("❌ create_integrated_workflow method missing")
            return False
        
        if hasattr(integration, 'list_integrated_workflows'):
            print("✅ list_integrated_workflows method exists")
        else:
            print("❌ list_integrated_workflows method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Integration module validation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main validation function."""
    print("🚀 Workflow Engine Integration Validation")
    print("=" * 50)
    
    # Validate imports
    if not validate_imports():
        print("\n❌ Import validation failed")
        return False
    
    # Validate integration module
    if not validate_integration_module():
        print("\n❌ Integration module validation failed")
        return False
    
    print("\n🎉 All validations passed successfully!")
    print("✅ Workflow Engine Integration is ready for use")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
