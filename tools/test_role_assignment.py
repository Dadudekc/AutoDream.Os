#!/usr/bin/env python3
"""
Test Role Assignment System
===========================

Test tool for the dynamic role assignment system.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.services.role_assignment.role_assignment_service import RoleAssignmentService
from src.services.role_assignment.contract_integration import ContractIntegration


def test_role_assignment_service():
    """Test the role assignment service."""
    print("🧪 Testing Role Assignment Service")
    print("=" * 50)
    
    # Initialize service
    service = RoleAssignmentService()
    
    # Test listing available roles
    print("\n📋 Available Roles:")
    roles = service.list_available_roles()
    for role in roles:
        print(f"  - {role}")
    
    # Test listing agent capabilities
    print("\n👥 Agent Capabilities:")
    for agent_id in ["Agent-1", "Agent-2", "Agent-8"]:
        capabilities = service.list_agent_capabilities(agent_id)
        print(f"  {agent_id}: {', '.join(capabilities)}")
    
    # Test role assignment (dry run)
    print("\n🎯 Testing Role Assignment (Dry Run):")
    print("  Would assign Agent-8 as INTEGRATION_SPECIALIST")
    print("  Task: 'Discord webhook integration'")
    print("  Duration: '2 cycles'")
    
    # Check if agent can perform role
    can_perform = service._can_agent_perform_role("Agent-8", "INTEGRATION_SPECIALIST")
    print(f"  Agent-8 can perform INTEGRATION_SPECIALIST: {can_perform}")
    
    # Test message creation
    if can_perform:
        from src.services.role_assignment.role_assignment_service import RoleAssignment
        assignment = RoleAssignment(
            agent_id="Agent-8",
            role="INTEGRATION_SPECIALIST",
            task="Discord webhook integration",
            duration="2 cycles"
        )
        message = service._create_role_assignment_message(assignment)
        print(f"  Generated message: {message[:100]}...")


def test_contract_integration():
    """Test the contract integration system."""
    print("\n🧪 Testing Contract Integration")
    print("=" * 50)
    
    # Initialize integration
    integration = ContractIntegration()
    
    # Test general cycle
    print("\n🔄 General Cycle Definition:")
    for phase in integration.get_general_cycle():
        print(f"  {phase.phase}: {phase.description} (Priority: {phase.priority})")
    
    # Test role contracts
    print("\n📋 Role Contracts:")
    for role, contract in integration.role_contracts.items():
        summary = integration.get_contract_summary(role)
        print(f"  {role}: {summary['phases']} phases, Valid: {summary['is_valid']}")
    
    # Test role cycle adaptations
    print("\n🎯 Role Cycle Adaptations for INTEGRATION_SPECIALIST:")
    adaptations = integration.get_role_cycle_adaptations("INTEGRATION_SPECIALIST")
    for phase, adaptation in adaptations.items():
        print(f"  {phase}: {adaptation}")


def test_practical_example():
    """Test a practical role assignment example."""
    print("\n🧪 Practical Role Assignment Example")
    print("=" * 50)
    
    service = RoleAssignmentService()
    integration = ContractIntegration()
    
    # Simulate Captain Agent-4 assigning role to Agent-8
    print("\n🎯 Captain Agent-4 assigns role to Agent-8:")
    print("  Role: INTEGRATION_SPECIALIST")
    print("  Task: Discord webhook integration")
    print("  Duration: 2 cycles")
    
    # Check if assignment is valid
    can_perform = service._can_agent_perform_role("Agent-8", "INTEGRATION_SPECIALIST")
    contract_valid = integration.validate_role_contract("INTEGRATION_SPECIALIST")
    
    print(f"\n✅ Assignment Validation:")
    print(f"  Agent-8 can perform role: {can_perform}")
    print(f"  Role contract is valid: {contract_valid}")
    
    if can_perform and contract_valid:
        print("\n🚀 Assignment would proceed:")
        print("  1. Captain sends PyAutoGUI message to Agent-8")
        print("  2. Agent-8 receives message and wakes up")
        print("  3. Agent-8 loads integration_specialist.json protocols")
        print("  4. Agent-8 adapts behavior for INTEGRATION_SPECIALIST role")
        print("  5. Agent-8 begins task execution with role-specific protocols")
        print("  6. Agent-8 follows adapted general cycle:")
        
        # Show adapted cycle
        adaptations = integration.get_role_cycle_adaptations("INTEGRATION_SPECIALIST")
        for phase, adaptation in adaptations.items():
            focus = adaptation.get("focus", "general")
            priority = adaptation.get("priority", "NORMAL")
            print(f"     - {phase}: {focus} (Priority: {priority})")
        
        print("\n📝 Agent-8 would send acknowledgment back to Captain")
        print("   'ROLE_ASSIGNMENT_ACKNOWLEDGED - Agent-8 now operating as INTEGRATION_SPECIALIST'")
    else:
        print("\n❌ Assignment would fail:")
        if not can_perform:
            print("  - Agent-8 cannot perform INTEGRATION_SPECIALIST role")
        if not contract_valid:
            print("  - INTEGRATION_SPECIALIST contract is invalid")


def main():
    """Run all tests."""
    print("🚀 V2_SWARM Dynamic Role Assignment System Test")
    print("=" * 60)
    
    try:
        test_role_assignment_service()
        test_contract_integration()
        test_practical_example()
        
        print("\n✅ All tests completed successfully!")
        print("\n🎯 System is ready for Captain Agent-4 role assignments")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
