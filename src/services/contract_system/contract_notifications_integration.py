#!/usr/bin/env python3
"""
Contract System → Discord Notifications Integration
Hooks ContractNotifier into contract lifecycle events.

Author: Agent-7
Date: 2025-10-15
Mission: Discord Contract Notifications - Week 1 Quick Win
"""

import logging
from typing import Optional
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.discord_commander.contract_notifications import ContractNotifier

logger = logging.getLogger(__name__)


class ContractNotificationHooks:
    """
    Integrates Discord notifications into contract lifecycle.
    
    Automatically sends Discord notifications when:
    - Contract assigned to agent
    - Agent starts contract work  
    - Agent completes contract
    - Agent is blocked on contract
    """
    
    def __init__(self):
        """Initialize notification hooks."""
        self.notifier = ContractNotifier()
        logger.info("✅ Contract notification hooks initialized")
    
    def on_contract_assigned(
        self,
        contract_id: str,
        agent_id: str,
        contract_data: dict
    ) -> bool:
        """
        Hook: Called when contract is assigned to agent.
        
        Args:
            contract_id: Contract identifier
            agent_id: Agent receiving contract
            contract_data: Contract details (name, priority, estimated_hours)
            
        Returns:
            True if notification sent successfully
        """
        try:
            success = self.notifier.notify_contract_assigned(
                contract_id=contract_id,
                agent_id=agent_id,
                contract_name=contract_data.get('name', 'Unnamed Contract'),
                priority=contract_data.get('priority', 'MEDIUM'),
                estimated_hours=contract_data.get('estimated_hours', 0)
            )
            
            if success:
                logger.info(f"✅ Discord notified: {contract_id} assigned to {agent_id}")
            else:
                logger.warning(f"⚠️ Discord notification failed for assignment: {contract_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error in assignment hook: {e}")
            return False
    
    def on_contract_started(
        self,
        contract_id: str,
        agent_id: str,
        contract_name: str
    ) -> bool:
        """
        Hook: Called when agent starts working on contract.
        
        Args:
            contract_id: Contract identifier
            agent_id: Agent starting work
            contract_name: Contract name
            
        Returns:
            True if notification sent successfully
        """
        try:
            success = self.notifier.notify_contract_started(
                contract_id=contract_id,
                agent_id=agent_id,
                contract_name=contract_name
            )
            
            if success:
                logger.info(f"✅ Discord notified: {agent_id} started {contract_id}")
            else:
                logger.warning(f"⚠️ Discord notification failed for start: {contract_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error in start hook: {e}")
            return False
    
    def on_contract_completed(
        self,
        contract_id: str,
        agent_id: str,
        contract_data: dict,
        metrics: dict
    ) -> bool:
        """
        Hook: Called when agent completes contract.
        
        Args:
            contract_id: Contract identifier
            agent_id: Agent completing contract
            contract_data: Contract details (name)
            metrics: Completion metrics (points, hours, quality)
            
        Returns:
            True if notification sent successfully
        """
        try:
            success = self.notifier.notify_contract_completed(
                contract_id=contract_id,
                agent_id=agent_id,
                contract_name=contract_data.get('name', 'Unnamed Contract'),
                points_earned=metrics.get('points', 0),
                actual_hours=metrics.get('hours', 0.0)
            )
            
            if success:
                logger.info(f"✅ Discord notified: {agent_id} completed {contract_id}")
            else:
                logger.warning(f"⚠️ Discord notification failed for completion: {contract_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error in completion hook: {e}")
            return False
    
    def on_contract_blocked(
        self,
        contract_id: str,
        agent_id: str,
        contract_name: str,
        blocker: str
    ) -> bool:
        """
        Hook: Called when agent is blocked on contract.
        
        Args:
            contract_id: Contract identifier
            agent_id: Blocked agent
            contract_name: Contract name
            blocker: Description of what's blocking
            
        Returns:
            True if notification sent successfully
        """
        try:
            success = self.notifier.notify_contract_blocked(
                contract_id=contract_id,
                agent_id=agent_id,
                contract_name=contract_name,
                blocker=blocker
            )
            
            if success:
                logger.info(f"✅ Discord notified: {agent_id} blocked on {contract_id}")
            else:
                logger.warning(f"⚠️ Discord notification failed for blocker: {contract_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error in blocker hook: {e}")
            return False


# Global instance for easy access
_notification_hooks: Optional[ContractNotificationHooks] = None


def get_notification_hooks() -> ContractNotificationHooks:
    """Get or create global notification hooks instance."""
    global _notification_hooks
    if _notification_hooks is None:
        _notification_hooks = ContractNotificationHooks()
    return _notification_hooks


# Convenience functions for contract system to call
def notify_assigned(contract_id: str, agent_id: str, contract_data: dict) -> bool:
    """Notify Discord when contract assigned."""
    return get_notification_hooks().on_contract_assigned(contract_id, agent_id, contract_data)


def notify_started(contract_id: str, agent_id: str, contract_name: str) -> bool:
    """Notify Discord when contract started."""
    return get_notification_hooks().on_contract_started(contract_id, agent_id, contract_name)


def notify_completed(contract_id: str, agent_id: str, contract_data: dict, metrics: dict) -> bool:
    """Notify Discord when contract completed."""
    return get_notification_hooks().on_contract_completed(contract_id, agent_id, contract_data, metrics)


def notify_blocked(contract_id: str, agent_id: str, contract_name: str, blocker: str) -> bool:
    """Notify Discord when contract blocked."""
    return get_notification_hooks().on_contract_blocked(contract_id, agent_id, contract_name, blocker)


if __name__ == "__main__":
    # Test the hooks
    print("🧪 Testing Contract Notification Hooks...\n")
    
    hooks = ContractNotificationHooks()
    
    # Test assignment
    print("Test 1: Assignment Hook")
    hooks.on_contract_assigned(
        "C-TEST-001",
        "Agent-7",
        {"name": "Test Contract", "priority": "HIGH", "estimated_hours": 25}
    )
    
    # Test started
    print("\nTest 2: Started Hook")
    hooks.on_contract_started("C-TEST-001", "Agent-7", "Test Contract")
    
    # Test completed
    print("\nTest 3: Completed Hook")
    hooks.on_contract_completed(
        "C-TEST-001",
        "Agent-7",
        {"name": "Test Contract"},
        {"points": 500, "hours": 22.5, "quality": 9.5}
    )
    
    # Test blocked
    print("\nTest 4: Blocked Hook")
    hooks.on_contract_blocked(
        "C-TEST-001",
        "Agent-7",
        "Test Contract",
        "Waiting for Captain approval"
    )
    
    print("\n✅ All hooks tested!")

