#!/usr/bin/env python3
"""
Perpetual Motion Contract System Demo
====================================

Demonstrates how the perpetual motion contract system automatically generates
new contracts when agents complete existing ones, creating a self-sustaining work cycle.
"""

import sys
import os
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from services.perpetual_motion_contract_service import PerpetualMotionContractService


def demo_contract_completion_cycle():
    """Demonstrate the complete contract completion cycle."""
    print("🔄 PERPETUAL MOTION CONTRACT SYSTEM DEMO")
    print("=" * 60)

    # Initialize service
    service = PerpetualMotionContractService()

    print("\n🎯 **DEMO SCENARIO**: Agent-1 completes a contract")
    print(
        "📋 **EXPECTED RESULT**: 2 new contracts automatically generated + resume message"
    )

    # Show initial state
    print(f"\n📊 **INITIAL STATE**:")
    status = service.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Simulate contract completion
    print(f"\n🚀 **SIMULATING CONTRACT COMPLETION**...")
    completion_data = {
        "task_id": "DEMO-TASK-001",
        "summary": "Demo contract completed successfully",
        "evidence": ["demo_file.py", "test_results.txt"],
        "completion_time": "2025-08-19T10:00:00",
    }

    service.on_contract_completion("DEMO-CONTRACT-001", "Agent-1", completion_data)

    # Show results
    print(f"\n📊 **AFTER CONTRACT COMPLETION**:")
    status = service.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Show generated contracts
    contract_files = list(service.contracts_dir.glob("*.json"))
    print(f"\n📁 **GENERATED CONTRACTS** ({len(contract_files)} total):")
    for contract_file in contract_files:
        print(f"  📄 {contract_file.name}")

    # Show resume message
    inbox_dir = Path("agent_workspaces/Agent-1/inbox")
    if inbox_dir.exists():
        resume_files = list(inbox_dir.glob("resume_message_*.json"))
        print(f"\n📬 **RESUME MESSAGE CREATED** ({len(resume_files)} files):")
        for resume_file in resume_files:
            print(f"  📧 {resume_file.name}")

    print(f"\n✅ **DEMO COMPLETE**: Perpetual motion system working!")
    print(
        "🔄 **NEXT CYCLE**: When Agent-1 completes these new contracts, more will be generated!"
    )


def demo_contract_templates():
    """Demonstrate contract template system."""
    print("\n📋 **CONTRACT TEMPLATES DEMO**")
    print("=" * 40)

    service = PerpetualMotionContractService()

    print(f"📚 **AVAILABLE TEMPLATES** ({len(service.contract_templates)} total):")
    for i, template in enumerate(service.contract_templates, 1):
        print(f"\n{i}. **{template.title}**")
        print(f"   📝 {template.description}")
        print(f"   ⏰ Estimated: {template.estimated_hours} hours")
        print(f"   🎯 Priority: {template.priority}")
        print(f"   🏷️ Category: {template.category}")
        print(f"   🛠️ Skills: {', '.join(template.skills_required)}")
        print(f"   ✅ Criteria: {len(template.acceptance_criteria)} acceptance criteria")


def demo_auto_generation():
    """Demonstrate automatic contract generation."""
    print("\n🤖 **AUTO-GENERATION DEMO**")
    print("=" * 40)

    service = PerpetualMotionContractService()

    print("🎯 **GENERATING 5 TEST CONTRACTS**...")
    contracts = service._generate_new_contracts("Agent-2", 5)

    print(f"✅ **GENERATED {len(contracts)} CONTRACTS**:")
    for i, contract in enumerate(contracts, 1):
        print(f"\n{i}. **{contract.title}**")
        print(f"   🆔 Contract ID: {contract.contract_id}")
        print(f"   📝 Task ID: {contract.task_id}")
        print(f"   👤 Assignee: {contract.assignee}")
        print(f"   📊 State: {contract.state}")
        print(f"   🏷️ Source: {contract.template_source}")
        print(f"   ⏰ Created: {contract.created_at}")

    # Save contracts
    print(f"\n💾 **SAVING CONTRACTS**...")
    for contract in contracts:
        service._save_contract(contract)

    print(f"✅ **CONTRACTS SAVED**: Check {service.contracts_dir} directory")


def demo_monitoring():
    """Demonstrate monitoring system."""
    print("\n👁️ **MONITORING SYSTEM DEMO**")
    print("=" * 40)

    service = PerpetualMotionContractService()

    print("🚀 **STARTING MONITORING**...")
    service.start_monitoring()

    print("⏳ **MONITORING FOR 5 SECONDS**...")
    time.sleep(5)

    print("🛑 **STOPPING MONITORING**...")
    service.stop_monitoring()

    print("✅ **MONITORING DEMO COMPLETE**")


def main():
    """Run the complete demo."""
    print("🎬 PERPETUAL MOTION CONTRACT SYSTEM - COMPLETE DEMO")
    print("=" * 70)

    try:
        # Run all demo sections
        demo_contract_completion_cycle()
        demo_contract_templates()
        demo_auto_generation()
        demo_monitoring()

        print("\n🎉 **ALL DEMOS COMPLETED SUCCESSFULLY!**")
        print("\n💡 **KEY FEATURES DEMONSTRATED**:")
        print("  ✅ Automatic contract generation on completion")
        print("  ✅ Resume message creation for agents")
        print("  ✅ Contract template system")
        print("  ✅ Background monitoring")
        print("  ✅ Self-sustaining work cycle")

        print("\n🔄 **PERPETUAL MOTION ACHIEVED**:")
        print("  🎯 Agents complete contracts")
        print("  🤖 System generates new contracts automatically")
        print("  📬 Agents get resume messages with new assignments")
        print("  🔄 Cycle continues indefinitely!")

    except Exception as e:
        print(f"\n❌ **DEMO FAILED**: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
