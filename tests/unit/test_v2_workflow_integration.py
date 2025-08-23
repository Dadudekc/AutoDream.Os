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


def test_v2_workflow_engine_import():
    """Test V2 workflow engine import."""
    print("🧪 Testing V2 workflow engine import...")

    try:
        from services.v2_workflow_engine import (
            V2WorkflowEngine,
            V2Workflow,
            V2WorkflowStep,
        )

        print("✅ V2WorkflowEngine import successful")
        print("✅ V2Workflow import successful")
        print("✅ V2WorkflowStep import successful")
        return True
    except ImportError as e:
        print(f"❌ V2 workflow engine import failed: {e}")
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
    except ImportError as e:
        print(f"❌ V2 AI code review service import failed: {e}")
        return False


def test_v2_workflow_engine_instantiation():
    """Test V2 workflow engine instantiation."""
    print("\n🧪 Testing V2 workflow engine instantiation...")

    try:
        from services.v2_workflow_engine import V2WorkflowEngine

        # Create mock dependencies
        class MockFSMOrchestrator:
            def create_task(self, title, description, assigned_agent, priority):
                return f"TASK-{hash(title)}"

            def update_task_status(self, task_id, status):
                return True

        class MockAgentManager:
            pass

        class MockResponseCaptureService:
            pass

        # Test instantiation
        engine = V2WorkflowEngine(
            MockFSMOrchestrator(), MockAgentManager(), MockResponseCaptureService()
        )

        print("✅ V2WorkflowEngine instantiation successful")
        print(f"✅ Workflow data path: {engine.workflow_data_path}")
        print(f"✅ Monitoring status: {engine.monitoring}")
        return True

    except Exception as e:
        print(f"❌ V2 workflow engine instantiation failed: {e}")
        return False


def test_v2_workflow_creation():
    """Test V2 workflow creation."""
    print("\n🧪 Testing V2 workflow creation...")

    try:
        from services.v2_workflow_engine import V2WorkflowEngine

        # Create mock dependencies
        class MockFSMOrchestrator:
            def create_task(self, title, description, assigned_agent, priority):
                return f"TASK-{hash(title)}"

            def update_task_status(self, task_id, status):
                return True

        class MockAgentManager:
            pass

        class MockResponseCaptureService:
            pass

        engine = V2WorkflowEngine(
            MockFSMOrchestrator(), MockAgentManager(), MockResponseCaptureService()
        )

        # Test workflow creation
        test_steps = [
            {
                "id": "step1",
                "name": "Test Step 1",
                "description": "First test step",
                "agent_target": "Agent-1",
                "prompt_template": "Execute step 1",
                "expected_response_type": "text",
            },
            {
                "id": "step2",
                "name": "Test Step 2",
                "description": "Second test step",
                "agent_target": "Agent-2",
                "prompt_template": "Execute step 2",
                "expected_response_type": "text",
                "dependencies": ["step1"],
            },
        ]

        workflow_id = engine.create_workflow(
            name="Test Workflow",
            description="Test workflow for integration testing",
            steps=test_steps,
        )

        if workflow_id:
            print(f"✅ Workflow creation successful: {workflow_id}")

            # Test workflow retrieval
            workflow = engine.workflows.get(workflow_id)
            if workflow:
                print(f"✅ Workflow retrieval successful: {workflow.name}")
                print(f"✅ Workflow steps: {len(workflow.steps)}")
                return True
            else:
                print("❌ Workflow retrieval failed")
                return False
        else:
            print("❌ Workflow creation failed")
            return False

    except Exception as e:
        print(f"❌ V2 workflow creation test failed: {e}")
        return False


def test_v2_ai_code_review_instantiation():
    """Test V2 AI code review service instantiation."""
    print("\n🧪 Testing V2 AI code review service instantiation...")

    try:
        from services.v2_ai_code_review import V2AICodeReviewService

        # Create mock dependencies
        class MockWorkflowEngine:
            pass

        class MockAgentManager:
            pass

        # Test instantiation
        service = V2AICodeReviewService(MockWorkflowEngine(), MockAgentManager())

        print("✅ V2AICodeReviewService instantiation successful")
        print(f"✅ Focus areas: {service.focus_areas}")
        print(f"✅ Workflow templates: {len(service.workflow_templates)}")
        return True

    except Exception as e:
        print(f"❌ V2 AI code review service instantiation failed: {e}")
        return False


def test_v2_workflow_system_summary():
    """Test V2 workflow system summary."""
    print("\n🧪 Testing V2 workflow system summary...")

    try:
        from services.v2_workflow_engine import V2WorkflowEngine

        # Create mock dependencies
        class MockFSMOrchestrator:
            def create_task(self, title, description, assigned_agent, priority):
                return f"TASK-{hash(title)}"

            def update_task_status(self, task_id, status):
                return True

        class MockAgentManager:
            pass

        class MockResponseCaptureService:
            pass

        engine = V2WorkflowEngine(
            MockFSMOrchestrator(), MockAgentManager(), MockResponseCaptureService()
        )

        # Get system summary
        summary = engine.get_system_summary()

        if summary:
            print("✅ System summary retrieval successful")
            print(f"✅ Total workflows: {summary['total_workflows']}")
            print(f"✅ Active workflows: {summary['active_workflows']}")
            print(f"✅ Monitoring active: {summary['monitoring_active']}")
            return True
        else:
            print("❌ System summary retrieval failed")
            return False

    except Exception as e:
        print(f"❌ V2 workflow system summary test failed: {e}")
        return False


def test_v2_ai_code_review_system_summary():
    """Test V2 AI code review system summary."""
    print("\n🧪 Testing V2 AI code review system summary...")

    try:
        from services.v2_ai_code_review import V2AICodeReviewService

        # Create mock dependencies
        class MockWorkflowEngine:
            pass

        class MockAgentManager:
            pass

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
