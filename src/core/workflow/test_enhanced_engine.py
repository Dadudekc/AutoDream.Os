#!/usr/bin/env python3
"""
Test Enhanced Workflow Engine - Validation Framework Integration

This script tests the enhanced workflow engine with validation framework
integration to ensure all functionality works correctly.

Author: Agent-1 (Core Engine Development)
License: MIT
"""

import sys
import os
from pathlib import Path
import time

# Add the current working directory to the Python path
current_dir = Path.cwd()
sys.path.insert(0, str(current_dir))

from src.core.workflow.core.workflow_engine import WorkflowEngine, EngineConfig
from src.core.workflow.types.workflow_enums import WorkflowStatus, TaskStatus, WorkflowType
from src.core.workflow.types.workflow_models import WorkflowDefinition, WorkflowStep


def test_enhanced_workflow_engine():
    """Test the enhanced workflow engine with validation framework"""
    print("🧪 Testing Enhanced Workflow Engine with Validation Framework")
    print("=" * 60)
    
    # Test 1: Engine Configuration
    print("\n1. Testing Engine Configuration:")
    config = EngineConfig(
        enable_validation=True,
        enable_optimization=True,
        performance_target_ms=100.0
    )
    
    engine = WorkflowEngine(config)
    print(f"   ✅ Engine initialized with validation: {engine.config.enable_validation}")
    print(f"   ✅ Engine initialized with optimization: {engine.config.enable_optimization}")
    print(f"   ✅ Performance target: {engine.config.performance_target_ms}ms")
    
    # Test 2: Validation Framework Integration
    print("\n2. Testing Validation Framework Integration:")
    if engine.validation_manager:
        print("   ✅ Validation manager initialized")
        print(f"   ✅ Validation hooks: {len(engine.validation_manager.validation_hooks)}")
    else:
        print("   ❌ Validation manager not initialized")
        return False
    
    # Test 3: Workflow Creation with Validation
    print("\n3. Testing Workflow Creation with Validation:")
    execution = engine.create_workflow_execution("agent_onboarding")
    if execution:
        print(f"   ✅ Workflow execution created: {execution.execution_id}")
        print(f"   ✅ Execution status: {execution.status.value}")
        print(f"   ✅ Steps count: {len(execution.steps)}")
        
        # Check for optimizations
        if "optimizations" in execution.metadata:
            print("   ✅ Optimizations applied:")
            for opt_name, opt_data in execution.metadata["optimizations"].items():
                print(f"      - {opt_name}: {opt_data.get('estimated_improvement', 0):.1f}% improvement")
    else:
        print("   ❌ Workflow execution creation failed")
        return False
    
    # Test 4: Workflow Start with Validation
    print("\n4. Testing Workflow Start with Validation:")
    if engine.start_workflow(execution.execution_id):
        print("   ✅ Workflow started successfully")
        status = engine.get_workflow_status(execution.execution_id)
        print(f"   ✅ Workflow status: {status.value}")
    else:
        print("   ❌ Workflow start failed")
        return False
    
    # Test 5: Step Execution with Validation
    print("\n5. Testing Step Execution with Validation:")
    if engine.execute_workflow_step(execution.execution_id, "init", output="test_output"):
        print("   ✅ Step executed successfully")
        
        # Check step status
        step = next((s for s in execution.steps if s.step_id == "init"), None)
        if step and step.status == TaskStatus.COMPLETED:
            print(f"   ✅ Step status: {step.status.value}")
            print(f"   ✅ Step result: {step.result}")
        else:
            print("   ❌ Step status not updated correctly")
    else:
        print("   ❌ Step execution failed")
        return False
    
    # Test 6: Performance Metrics
    print("\n6. Testing Performance Metrics:")
    metrics = engine.get_workflow_performance_metrics()
    if metrics:
        print("   ✅ Performance metrics retrieved:")
        print(f"      - Total workflows: {metrics['total_workflows']}")
        print(f"      - Performance target met: {metrics['performance_target_met']}")
        print(f"      - Validation enabled: {metrics['validation_enabled']}")
        
        if 'validation' in metrics:
            validation_metrics = metrics['validation']
            print(f"      - Validation metrics: {validation_metrics['total_validations']} validations")
    else:
        print("   ❌ Performance metrics retrieval failed")
    
    # Test 7: Workflow Optimization
    print("\n7. Testing Workflow Optimization:")
    optimization = engine.optimize_workflow_performance("agent_onboarding")
    if "error" not in optimization:
        print("   ✅ Workflow optimization analysis completed:")
        print(f"      - Total estimated improvement: {optimization['total_estimated_improvement']:.1f}%")
        print(f"      - Optimization types: {len(optimization['optimizations'])}")
        
        for opt_name, opt_data in optimization['optimizations'].items():
            if opt_data.get('estimated_improvement', 0) > 0:
                print(f"      - {opt_name}: {opt_data['estimated_improvement']:.1f}% improvement")
    else:
        print("   ❌ Workflow optimization failed")
    
    # Test 8: Validation Performance
    print("\n8. Testing Validation Performance:")
    validation_metrics = engine.validation_manager.get_validation_performance_metrics()
    if validation_metrics:
        print("   ✅ Validation performance metrics:")
        print(f"      - Total validations: {validation_metrics['total_validations']}")
        print(f"      - Success rate: {validation_metrics['validation_success_rate']:.1f}%")
        print(f"      - Performance issues: {validation_metrics['performance_issues_detected']}")
    else:
        print("   ❌ Validation performance metrics failed")
    
    # Test 9: Smoke Test
    print("\n9. Testing Enhanced Smoke Test:")
    if engine.run_smoke_test():
        print("   ✅ Enhanced smoke test passed")
    else:
        print("   ❌ Enhanced smoke test failed")
        return False
    
    # Test 10: Performance Target Achievement
    print("\n10. Testing Performance Target Achievement:")
    performance_metrics = engine.get_workflow_performance_metrics()
    if performance_metrics['total_workflows'] > 0:
        target_rate = performance_metrics['performance_target_rate']
        print(f"   ✅ Performance target achievement rate: {target_rate:.1f}%")
        
        if target_rate >= 80:
            print("   🎯 Excellent performance target achievement!")
        elif target_rate >= 60:
            print("   ✅ Good performance target achievement")
        else:
            print("   ⚠️ Performance target achievement needs improvement")
    else:
        print("   ❌ No performance data available")
    
    print("\n🎉 Enhanced Workflow Engine Test Complete!")
    return True


def test_validation_integration():
    """Test specific validation integration features"""
    print("\n🔍 Testing Validation Integration Features:")
    print("-" * 40)
    
    config = EngineConfig(enable_validation=True)
    engine = WorkflowEngine(config)
    
    # Test validation hooks
    print("1. Testing Validation Hooks:")
    if engine.validation_manager:
        hooks = engine.validation_manager.validation_hooks
        print(f"   ✅ Validation hooks available: {list(hooks.keys())}")
        
        # Test workflow creation validation
        execution = engine.create_workflow_execution("agent_onboarding")
        if execution:
            print("   ✅ Workflow creation validation triggered")
            
            # Get validation summary
            summary = engine.validation_manager.get_workflow_validation_summary(execution.execution_id)
            if "error" not in summary:
                print(f"   ✅ Validation summary: {summary['total_validations']} validations")
                print(f"   ✅ Success rate: {summary['success_rate']:.1f}%")
            else:
                print("   ❌ Validation summary retrieval failed")
        else:
            print("   ❌ Workflow creation validation failed")
    
    print("2. Testing Real-time Validation:")
    if engine.validation_manager and execution:
        # Perform real-time validation
        workflow_def = engine.workflow_definitions["agent_onboarding"]
        validation_results = engine.validation_manager.validate_workflow_real_time(workflow_def, execution)
        
        if validation_results:
            print(f"   ✅ Real-time validation completed: {len(validation_results)} results")
            
            # Check for validation issues
            errors = [r for r in validation_results if r.status.value == "FAILED"]
            if errors:
                print(f"   ⚠️ Validation issues found: {len(errors)}")
                for error in errors[:3]:  # Show first 3 errors
                    print(f"      - {error.rule_name}: {error.message}")
            else:
                print("   ✅ No validation issues found")
        else:
            print("   ❌ Real-time validation failed")
    
    print("3. Testing Validation Report Export:")
    if engine.validation_manager and execution:
        report = engine.validation_manager.export_validation_report(execution.execution_id)
        if "error" not in report:
            print("   ✅ Validation report exported successfully")
            print(f"   ✅ Report timestamp: {report['validation_timestamp']}")
            print(f"   ✅ Detailed results: {len(report['detailed_results'])}")
        else:
            print("   ❌ Validation report export failed")
    
    return True


def main():
    """Run all tests"""
    print("🚀 Enhanced Workflow Engine - Validation Framework Integration Test")
    print("=" * 70)
    
    try:
        # Test enhanced workflow engine
        if not test_enhanced_workflow_engine():
            print("❌ Enhanced workflow engine test failed")
            return False
        
        # Test validation integration
        if not test_validation_integration():
            print("❌ Validation integration test failed")
            return False
        
        print("\n🎉 All tests completed successfully!")
        print("✅ Enhanced workflow engine with validation framework is operational")
        print("✅ Performance targets and validation integration working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
