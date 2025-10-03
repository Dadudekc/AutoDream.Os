#!/usr/bin/env python3
"""
Proper Agent Workflow Example
============================

Example of how agents should coordinate using messaging and workflows
instead of creating complex coordination files.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

from src.services.messaging_service import ConsolidatedMessagingService
from src.services.workflow_system import WorkflowManager, PredefinedWorkflows


def example_simple_messaging():
    """Example: Simple messaging between agents."""
    print("=== SIMPLE MESSAGING EXAMPLE ===")
    
    messaging = ConsolidatedMessagingService()
    
    # Simple task assignment
    messaging.send_message("Agent-7", "Please implement testing validation", "normal")
    messaging.send_message("Agent-8", "Please review Agent-7's implementation", "normal")
    messaging.send_message("Agent-4", "Please approve the final implementation", "normal")
    
    print("✅ Messages sent using simple messaging system")


def example_workflow_chain():
    """Example: Workflow chain for multi-step process."""
    print("\n=== WORKFLOW CHAIN EXAMPLE ===")
    
    messaging = ConsolidatedMessagingService()
    workflow_manager = WorkflowManager()
    
    # Create testing workflow
    testing_workflow = workflow_manager.create_workflow("testing_validation")
    testing_workflow.add_step("Agent-7", "Implement testing validation", "normal")
    testing_workflow.add_step("Agent-8", "Review testing implementation", "normal")
    testing_workflow.add_step("Agent-4", "Approve testing implementation", "normal")
    
    # Execute workflow
    testing_workflow.execute_all()
    
    print("✅ Workflow executed using workflow chain")


def example_predefined_workflow():
    """Example: Using predefined workflows."""
    print("\n=== PREDEFINED WORKFLOW EXAMPLE ===")
    
    messaging = ConsolidatedMessagingService()
    
    # Use predefined QA workflow
    qa_workflow = PredefinedWorkflows.qa_coordination(messaging)
    qa_workflow.execute_all()
    
    print("✅ Predefined QA workflow executed")


def example_status_updates():
    """Example: Simple status updates."""
    print("\n=== STATUS UPDATES EXAMPLE ===")
    
    messaging = ConsolidatedMessagingService()
    
    # Simple status updates
    messaging.update_status("Agent-7", "Working on testing validation")
    messaging.update_status("Agent-8", "Waiting for Agent-7 to complete")
    messaging.update_status("Agent-4", "Monitoring progress")
    
    print("✅ Status updates sent")


def main():
    """Run all examples."""
    print("🚀 PROPER AGENT WORKFLOW EXAMPLES")
    print("=" * 50)
    
    try:
        example_simple_messaging()
        example_workflow_chain()
        example_predefined_workflow()
        example_status_updates()
        
        print("\n🎉 ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("\n📋 KEY PRINCIPLES:")
        print("✅ Use messaging system for communication")
        print("✅ Use workflow chains for multi-step processes")
        print("✅ Use simple status updates for progress")
        print("❌ Don't create complex coordination files")
        print("❌ Don't create spinoff implementations")
        print("❌ Don't overengineer simple tasks")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()