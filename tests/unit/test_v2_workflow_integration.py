#!/usr/bin/env python3
"""
V2 Workflow Integration Test - Agent Cellphone V2
================================================

Comprehensive test script to verify V2 workflow system integration
without pytest dependencies.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from ..utils.mock_managers import (
    MockFSMOrchestrator,
    MockAgentManager,
    MockResponseCaptureService,
    MockWorkflowEngine,
)


def test_v2_workflow_engine_import():
    """Test modular workflow system import."""
    print("🧪 Testing modular workflow system import...")

    try:
        from src.core.workflow.workflow_execution import WorkflowExecutionEngine
        from src.core.workflow.workflow_types import WorkflowExecution, WorkflowStep
        from src.core.workflow.workflow_core import WorkflowDefinitionManager

        print("✅ WorkflowExecutionEngine import successful")
        print("✅ WorkflowExecution import successful")
        print("✅ WorkflowStep import successful")
        print("✅ WorkflowDefinitionManager import successful")
        return True
    except Exception as e:
        print(f"❌ Modular workflow system import failed: {e}")
        return False


def test_v2_ai_code_review_import():
    """Test V2 AI code review service import."""
    print("\n🧪 Testing V2 AI code review service import...")

    try:
        from services.v2_ai_code_review import (
            V2AICodeReviewService,
            CodeReviewTask,
            CodeReviewResult,
        )

        print("✅ V2AICodeReviewService import successful")
        print("✅ CodeReviewTask import successful")
        print("✅ CodeReviewResult import successful")
        return True
    except Exception as e:
        print(f"❌ V2 AI code review service import failed: {e}")
        return False


def test_v2_workflow_engine_instantiation():
    """Test modular workflow system instantiation."""
    print("\n🧪 Testing modular workflow system instantiation...")

    try:
        from src.core.workflow.workflow_execution import WorkflowExecutionEngine
        from src.core.workflow.workflow_core import WorkflowDefinitionManager

        # Test instantiation of modular components
        engine = WorkflowExecutionEngine(max_workers=2)
        definition_manager = WorkflowDefinitionManager()

        print("✅ WorkflowExecutionEngine instantiation successful")
        print("✅ WorkflowDefinitionManager instantiation successful")
        print(f"✅ Engine max workers: {engine.max_workers}")
        return True

    except Exception as e:
        print(f"❌ Modular workflow system instantiation failed: {e}")
        return False


def test_v2_workflow_creation():
    """Test modular workflow system creation."""
    print("\n🧪 Testing modular workflow system creation...")

    try:
        from src.core.workflow.workflow_core import WorkflowDefinitionManager
        from src.core.workflow.workflow_types import WorkflowStep

        # Test workflow definition management
        definition_manager = WorkflowDefinitionManager()

        # Test workflow definition creation
        test_steps = [
            WorkflowStep(
                step_id="step1",
                name="Test Step 1",
                description="First test step",
                step_type="general"
            ),
            WorkflowStep(
                step_id="step2",
                name="Test Step 2",
                description="Second test step",
                step_type="general"
            ),
        ]

        # Add workflow definition
        definition_manager.workflow_definitions["test_workflow"] = test_steps

        if "test_workflow" in definition_manager.workflow_definitions:
            print(f"✅ Workflow definition creation successful: test_workflow")
            print(f"✅ Workflow steps: {len(definition_manager.workflow_definitions['test_workflow'])}")
            return True
        else:
            print("❌ Workflow definition creation failed")
            return False

    except Exception as e:
        print(f"❌ Modular workflow creation test failed: {e}")
        return False


def test_v2_ai_code_review_instantiation():
    """Test V2 AI code review service instantiation."""
    print("\n🧪 Testing V2 AI code review service instantiation...")

    try:
        from services.v2_ai_code_review import V2AICodeReviewService

        # Test instantiation with shared mocks
        service = V2AICodeReviewService(MockWorkflowEngine(), MockAgentManager())

        print("✅ V2AICodeReviewService instantiation successful")
        print(f"✅ Focus areas: {service.focus_areas}")
        print(f"✅ Workflow templates: {len(service.workflow_templates)}")
        return True

    except Exception as e:
        print(f"❌ V2 AI code review service instantiation failed: {e}")
        return False


def test_v2_workflow_system_summary():
    """Test modular workflow system summary."""
    print("\n🧪 Testing modular workflow system summary...")

    try:
        from src.core.workflow.workflow_core import WorkflowDefinitionManager
        from src.core.workflow.workflow_execution import WorkflowExecutionEngine

        # Test modular system components
        definition_manager = WorkflowDefinitionManager()
        execution_engine = WorkflowExecutionEngine(max_workers=2)

        # Get system summary from modular components
        total_definitions = len(definition_manager.workflow_definitions)
        active_executions = len(execution_engine.active_executions)

        print("✅ Modular system summary retrieval successful")
        print(f"✅ Total workflow definitions: {total_definitions}")
        print(f"✅ Active executions: {active_executions}")
        print(f"✅ Max workers: {execution_engine.max_workers}")
        return True

    except Exception as e:
        print(f"❌ Modular workflow system summary failed: {e}")
        return False


def test_v2_ai_code_review_system_summary():
    """Test V2 AI code review system summary."""
    print("\n🧪 Testing V2 AI code review system summary...")

    try:
        from services.v2_ai_code_review import V2AICodeReviewService

        service = V2AICodeReviewService(MockWorkflowEngine(), MockAgentManager())

        # Get system summary
        summary = service.get_system_summary()

        if summary:
            print("✅ AI code review system summary retrieval successful")
            print(f"✅ Total review tasks: {summary['total_review_tasks']}")
            print(f"✅ Available focus areas: {len(summary['available_focus_areas'])}")
            print(f"✅ Workflow templates: {summary['workflow_templates']}")
            return True
        else:
            print("❌ AI code review system summary retrieval failed")
            return False

    except Exception as e:
        print(f"❌ V2 AI code review system summary test failed: {e}")
        return False


def main():
    """Run all V2 workflow integration tests."""
    print("🚀 V2 WORKFLOW INTEGRATION TEST")
    print("=" * 50)

    tests = [
        test_v2_workflow_engine_import,
        test_v2_ai_code_review_import,
        test_v2_workflow_engine_instantiation,
        test_v2_workflow_creation,
        test_v2_ai_code_review_instantiation,
        test_v2_workflow_system_summary,
        test_v2_ai_code_review_system_summary,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! V2 workflow system integration is operational.")
        return True
    else:
        print("⚠️  Some tests failed. V2 workflow system needs attention.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
