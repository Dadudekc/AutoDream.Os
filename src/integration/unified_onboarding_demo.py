#!/usr/bin/env python3
"""
Unified Onboarding System Demo - V2 Compliant
============================================

Demonstrates the unified onboarding system integration with Discord Commander.

Features:
- Unified onboarding service demonstration
- Discord Commander integration
- Agent state management
- Contract system demonstration
- V2 compliance (≤400 lines)

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.unified_onboarding_service import UnifiedOnboardingService
from discord_commander.discord_commander import DiscordCommander
from discord_commander.onboarding_integration import integrate_onboarding_with_discord_commander

logger = logging.getLogger(__name__)

async def demo_unified_onboarding():
    """Demonstrate the unified onboarding system."""
    print("🚀 Unified Onboarding System Demo")
    print("=" * 50)
    
    # Initialize services
    print("\n📋 Initializing services...")
    onboarding_service = UnifiedOnboardingService()
    discord_commander = DiscordCommander()
    
    # Setup integration
    print("🔗 Setting up Discord Commander integration...")
    success = discord_commander.setup_onboarding_integration(onboarding_service)
    if success:
        print("✅ Integration setup successful")
    else:
        print("❌ Integration setup failed")
        return
    
    # Load existing state
    print("\n📂 Loading existing onboarding state...")
    onboarding_service.load_onboarding_state()
    
    # Demonstrate agent state management
    print("\n🤖 Agent State Management Demo:")
    for agent_id in onboarding_service.agent_roles.keys():
        state = onboarding_service.get_agent_state(agent_id)
        contract = onboarding_service.get_agent_contract(agent_id)
        print(f"  {agent_id}: {state.value if state else 'unknown'} (Contract: {contract.status if contract else 'none'})")
    
    # Demonstrate onboarding commands
    print("\n💬 Discord Command Demo:")
    
    # Test onboarding status command
    status_result = await discord_commander.handle_discord_command("onboarding_status")
    print(f"Status Command Result:\n{status_result}")
    
    # Test individual agent onboarding
    print("\n🚀 Testing individual agent onboarding...")
    onboard_result = await discord_commander.handle_discord_command("onboard Agent-3")
    print(f"Onboard Command Result: {onboard_result}")
    
    # Test agent state command
    print("\n🔍 Testing agent state query...")
    state_result = await discord_commander.handle_discord_command("agent_state Agent-3")
    print(f"Agent State Result:\n{state_result}")
    
    # Test contracts command
    print("\n📋 Testing contracts overview...")
    contracts_result = await discord_commander.handle_discord_command("contracts")
    print(f"Contracts Result:\n{contracts_result}")
    
    # Demonstrate bulk onboarding
    print("\n🎯 Testing bulk onboarding...")
    bulk_result = await discord_commander.handle_discord_command("onboard_all")
    print(f"Bulk Onboarding Result: {bulk_result}")
    
    # Save state
    print("\n💾 Saving onboarding state...")
    onboarding_service.save_onboarding_state()
    
    # Test help command
    print("\n❓ Testing help command...")
    help_result = await discord_commander.handle_discord_command("help")
    print(f"Help Result:\n{help_result}")
    
    print("\n✅ Demo completed successfully!")
    print("\n📊 Summary:")
    print(f"  - Agents managed: {len(onboarding_service.agent_roles)}")
    print(f"  - Active contracts: {len([c for c in onboarding_service.contracts.values() if c.status == 'active'])}")
    print(f"  - Integration status: {'✅ Active' if discord_commander.onboarding_integration else '❌ Inactive'}")

async def demo_contract_management():
    """Demonstrate contract management features."""
    print("\n📋 Contract Management Demo")
    print("=" * 30)
    
    onboarding_service = UnifiedOnboardingService()
    
    # Create sample contracts
    print("📝 Creating sample contracts...")
    for agent_id in ["Agent-1", "Agent-2", "Agent-3"]:
        contract = onboarding_service.create_onboarding_contract(agent_id)
        contract.status = "active"
        contract.progress_percentage = 75
        onboarding_service.contracts[agent_id] = contract
        print(f"  ✅ Created contract for {agent_id}")
    
    # Demonstrate contract queries
    print("\n🔍 Contract Status:")
    for agent_id, contract in onboarding_service.contracts.items():
        if contract:
            print(f"  {agent_id}: {contract.contract_type.value} - {contract.status} ({contract.progress_percentage}%)")
    
    # Save and load state
    print("\n💾 Testing state persistence...")
    onboarding_service.save_onboarding_state("demo_state.json")
    
    # Create new service instance and load state
    new_service = UnifiedOnboardingService()
    new_service.load_onboarding_state("demo_state.json")
    
    print("📂 Loaded state verification:")
    for agent_id in ["Agent-1", "Agent-2", "Agent-3"]:
        contract = new_service.get_agent_contract(agent_id)
        if contract:
            print(f"  {agent_id}: {contract.status} ({contract.progress_percentage}%)")
    
    # Cleanup
    Path("demo_state.json").unlink(missing_ok=True)
    print("🧹 Demo state file cleaned up")

async def main():
    """Main demo function."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Run demos
        await demo_unified_onboarding()
        await demo_contract_management()
        
        print("\n🎉 All demos completed successfully!")
        print("\n📚 Available Discord Commands:")
        print("  • onboard <agent_id> - Onboard specific agent")
        print("  • onboard_all - Onboard all agents")
        print("  • onboarding_status - Get status of all agents")
        print("  • agent_state <agent_id> - Get detailed agent state")
        print("  • contracts - Show active contracts")
        print("  • reset_agent <agent_id> - Reset agent state")
        print("  • help - Show help message")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
