"""
Agent Entity - V2 Compliant Main Interface
==========================================

Main interface for agent entity system.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from typing import Any, Dict, List, Optional

from .agent_core import AgentCore, AgentManager
from .agent_models import (
    AgentCapability,
    AgentConfig,
    AgentMetrics,
    AgentStatus,
    AgentType,
)


class Agent:
    """Main agent interface."""
    
    def __init__(self, config: AgentConfig):
        """Initialize agent."""
        self.core = AgentCore(config)
    
    def manage_agent_operations(self, operation: str, **kwargs) -> Any:
        """Manage agent operations."""
        if operation == "activate":
            return self.core.activate()
        elif operation == "deactivate":
            return self.core.deactivate()
        elif operation == "set_busy":
            return self.core.set_busy()
        elif operation == "set_error":
            error_message = kwargs.get("error_message", "Unknown error")
            return self.core.set_error(error_message)
        elif operation == "has_capability":
            capability = kwargs.get("capability")
            return self.core.has_capability(capability) if capability else False
        elif operation == "get_status":
            return self.core.get_status()
        elif operation == "get_uptime":
            return self.core.get_uptime()
        elif operation == "update_metrics":
            metrics = kwargs.get("metrics")
            if metrics:
                self.core.update_metrics(metrics)
            return True
        else:
            return None
    
    def get_config(self) -> AgentConfig:
        """Get agent configuration."""
        return self.core.config
    
    def get_metrics(self) -> AgentMetrics:
        """Get agent metrics."""
        return self.core.config.metrics


# Global agent manager instance
agent_manager = AgentManager()


def main():
    """Main function for testing."""
    # Create a test agent
    test_agent = create_agent(
        agent_id="test-agent-1",
        name="Test Agent",
        agent_type=AgentType.CORE,
        capabilities=[AgentCapability.MESSAGING, AgentCapability.COORDINATION]
    )
    
    # Register the agent
    register_agent(test_agent)
    
    # Activate the agent
    test_agent.activate()
    
    print(f"Agent created and activated: {test_agent.get_config().agent_id}")
    print(f"Agent status: {test_agent.get_status()}")
    print(f"Agent capabilities: {[cap.value for cap in test_agent.get_config().capabilities]}")
    print(f"Total agents: {get_agent_count()}")
    print(f"Status summary: {get_status_summary()}")


if __name__ == "__main__":
    main()