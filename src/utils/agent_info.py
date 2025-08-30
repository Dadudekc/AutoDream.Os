from typing import Dict, List, Any
import os
import sys

    import argparse
from ..core.agent_models import AgentRole, AgentStatus, AgentCapability
from base_manager import BaseManager
from dataclasses import dataclass
import time

"""
Agent Information Module - Agent Role Definitions

This module contains agent role definitions and information structures.
Follows Single Responsibility Principle - only manages agent metadata.
Now inherits from BaseManager for unified functionality.

Architecture: Single Responsibility Principle - agent information only
LOC: 150 lines (under 200 limit)
"""



# Import BaseManager with relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))


# AgentRole now imported from unified agent_models


@dataclass
class AgentResponsibilities:
    """Agent responsibilities structure"""

    role: str
    emoji: str
    key_responsibilities: List[str]
    leadership: str
    onboarding_path: str
    priority_docs: List[str]


class AgentInfoManager(BaseManager):
    """
    Manages agent information and role definitions.

    Responsibilities:
    - Provide agent role information
    - Manage agent metadata
    - Support agent lookup operations
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self):
        super().__init__(
            manager_id="agent_info_manager",
            name="Agent Info Manager",
            description="Manages agent information and role definitions"
        )
        
        # Agent information tracking
        self.agent_info_operations: List[Dict[str, Any]] = []
        self.agent_lookups = 0
        self.role_queries = 0
        self.emoji_queries = 0
        self.failed_operations: List[Dict[str, Any]] = []
        
        self.logger.info("Agent Info Manager initialized")
        self.agent_info = {
            "Agent-1": AgentResponsibilities(
                role=AgentRole.SYSTEM_COORDINATOR.value,
                emoji="🎯",
                key_responsibilities=[
                    "Project coordination and task assignment",
                    "Progress monitoring and bottleneck identification",
                    "Conflict resolution and team leadership",
                    "Quality assurance and strategic planning",
                ],
                leadership="You are the team leader and coordinator.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/protocols/agent_protocols.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/onboarding_checklist.md",
                ],
            ),
            "Agent-2": AgentResponsibilities(
                role=AgentRole.TECHNICAL_ARCHITECT.value,
                emoji="🏗️",
                key_responsibilities=[
                    "System architecture and technical design",
                    "Code development and implementation",
                    "Technical problem-solving and optimization",
                    "Code review and quality assurance",
                ],
                leadership="You are the technical lead and architect.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/tools_and_technologies.md",
                ],
            ),
            "Agent-3": AgentResponsibilities(
                role=AgentRole.DATA_ENGINEER.value,
                emoji="📊",
                key_responsibilities=[
                    "Data pipeline development and maintenance",
                    "Data analysis and insights generation",
                    "Database design and optimization",
                    "Data quality assurance and governance",
                ],
                leadership="You are the data and analytics expert.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
                    "D:/repos/Dadudekc/onboarding/protocols/workflow_protocols.md",
                ],
            ),
            "Agent-4": AgentResponsibilities(
                role=AgentRole.DEVOPS_ENGINEER.value,
                emoji="⚙️",
                key_responsibilities=[
                    "Infrastructure automation and deployment",
                    "System monitoring and reliability",
                    "Security implementation and compliance",
                    "Performance optimization and scaling",
                ],
                leadership="You are the infrastructure and operations expert.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/tools_and_technologies.md",
                    "D:/repos/Dadudekc/onboarding/protocols/command_reference.md",
                ],
            ),
            "Agent-5": AgentResponsibilities(
                role=AgentRole.AI_ML_ENGINEER.value,
                emoji="🤖",
                key_responsibilities=[
                    "Machine learning model development",
                    "AI algorithm implementation and optimization",
                    "Data preprocessing and feature engineering",
                    "Model evaluation and deployment",
                ],
                leadership="You are the AI and machine learning expert.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/best_practices.md",
                ],
            ),
        }

    def get_agent_info(self, agent_name: str) -> AgentResponsibilities:
        """Get agent information for the specified agent"""
        start_time = time.time()
        try:
            agent_info = self.agent_info.get(
                agent_name,
                AgentResponsibilities(
                    role="Team Member",
                    emoji="👤",
                    key_responsibilities=["General team support and collaboration"],
                    leadership="You are a valuable team member.",
                    onboarding_path="docs/onboarding/README.md",
                    priority_docs=[
                        "docs/onboarding/agent_roles_and_responsibilities.md",
                        "docs/onboarding/development_standards.md",
                        "docs/onboarding/best_practices.md",
                    ],
                ),
            )
            
            # Record successful operation
            self.agent_lookups += 1
            self.record_operation("get_agent_info", True, time.time() - start_time)
            
            return agent_info
            
        except Exception as e:
            self.logger.error(f"Failed to get agent info for {agent_name}: {e}")
            self.record_operation("get_agent_info", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "get_agent_info",
                "agent_name": agent_name,
                "error": str(e),
                "timestamp": time.time()
            })
            raise

    def get_all_agents(self) -> Dict[str, AgentResponsibilities]:
        """Get all agent information"""
        start_time = time.time()
        try:
            agents = self.agent_info.copy()
            
            # Record successful operation
            self.record_operation("get_all_agents", True, time.time() - start_time)
            
            return agents
            
        except Exception as e:
            self.logger.error(f"Failed to get all agents: {e}")
            self.record_operation("get_all_agents", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "get_all_agents",
                "error": str(e),
                "timestamp": time.time()
            })
            raise

    def get_agent_role(self, agent_name: str) -> str:
        """Get the role of a specific agent"""
        start_time = time.time()
        try:
            agent = self.get_agent_info(agent_name)
            role = agent.role
            
            # Record successful operation
            self.role_queries += 1
            self.record_operation("get_agent_role", True, time.time() - start_time)
            
            return role
            
        except Exception as e:
            self.logger.error(f"Failed to get agent role for {agent_name}: {e}")
            self.record_operation("get_agent_role", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "get_agent_role",
                "agent_name": agent_name,
                "error": str(e),
                "timestamp": time.time()
            })
            raise

    def get_agent_emoji(self, agent_name: str) -> str:
        """Get the emoji of a specific agent"""
        start_time = time.time()
        try:
            agent = self.get_agent_info(agent_name)
            emoji = agent.emoji
            
            # Record successful operation
            self.emoji_queries += 1
            self.record_operation("get_agent_emoji", True, time.time() - start_time)
            
            return emoji
            
        except Exception as e:
            self.logger.error(f"Failed to get agent emoji for {agent_name}: {e}")
            self.record_operation("get_agent_emoji", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "get_agent_emoji",
                "agent_name": agent_name,
                "error": str(e),
                "timestamp": time.time()
            })
            raise

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize agent information management system"""
        try:
            self.logger.info("Starting Agent Info Manager...")
            
            # Clear tracking data
            self.agent_info_operations.clear()
            self.agent_lookups = 0
            self.role_queries = 0
            self.emoji_queries = 0
            self.failed_operations.clear()
            
            self.logger.info("Agent Info Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Agent Info Manager: {e}")
            return False
    
    def _on_stop(self) -> bool:
        """Cleanup agent information management system"""
        try:
            self.logger.info("Stopping Agent Info Manager...")
            
            # Save agent information management data
            self._save_agent_info_management_data()
            
            self.logger.info("Agent Info Manager stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop Agent Info Manager: {e}")
            return False
    
    def _on_heartbeat(self) -> bool:
        """Agent information management health check"""
        try:
            # Check agent information management health
            health_status = self._check_agent_info_management_health()
            
            # Update metrics
            self.metrics.update(
                operations_count=len(self.agent_info_operations),
                success_rate=self._calculate_success_rate(),
                average_response_time=self._calculate_average_response_time(),
                health_status=health_status
            )
            
            return health_status == "healthy"
            
        except Exception as e:
            self.logger.error(f"Agent Info Manager heartbeat failed: {e}")
            return False
    
    def _on_initialize_resources(self) -> bool:
        """Initialize agent information management resources"""
        try:
            # Initialize agent information tracking
            self.agent_info_operations = []
            self.agent_lookups = 0
            self.role_queries = 0
            self.emoji_queries = 0
            self.failed_operations = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Agent Info Manager resources: {e}")
            return False
    
    def _on_cleanup_resources(self) -> bool:
        """Cleanup agent information management resources"""
        try:
            # Save agent information management data
            self._save_agent_info_management_data()
            
            # Clear tracking data
            self.agent_info_operations.clear()
            self.agent_lookups = 0
            self.role_queries = 0
            self.emoji_queries = 0
            self.failed_operations.clear()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup Agent Info Manager resources: {e}")
            return False
    
    def _on_recovery_attempt(self) -> bool:
        """Attempt to recover from errors"""
        try:
            self.logger.info("Attempting Agent Info Manager recovery...")
            
            # Reinitialize agent information tracking
            self.agent_info_operations = []
            self.agent_lookups = 0
            self.role_queries = 0
            self.emoji_queries = 0
            self.failed_operations.clear()
            
            self.logger.info("Agent Info Manager recovery successful")
            return True
                
        except Exception as e:
            self.logger.error(f"Agent Info Manager recovery attempt failed: {e}")
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_agent_info_management_data(self):
        """Save agent information management data for persistence"""
        try:
            data = {
                "agent_lookups": self.agent_lookups,
                "role_queries": self.role_queries,
                "emoji_queries": self.emoji_queries,
                "failed_operations": self.failed_operations,
                "timestamp": time.time()
            }
            
            # Save to file or database as needed
            # For now, just log the data
            self.logger.info(f"Agent information management data: {data}")
            
        except Exception as e:
            self.logger.error(f"Failed to save agent information management data: {e}")
    
    def _check_agent_info_management_health(self) -> str:
        """Check agent information management system health"""
        try:
            # Check if we have agent information defined
            if len(self.agent_info) > 0:
                # Check if we have recent operations
                if len(self.agent_info_operations) > 0:
                    return "healthy"
                else:
                    return "idle"
            else:
                return "no_agents"
                
        except Exception as e:
            self.logger.error(f"Agent information management health check failed: {e}")
            return "unhealthy"
    
    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate"""
        try:
            if len(self.agent_info_operations) == 0:
                return 1.0
            
            successful_ops = sum(1 for op in self.agent_info_operations if op.get("success", False))
            return successful_ops / len(self.agent_info_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate success rate: {e}")
            return 0.0
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average operation response time"""
        try:
            if len(self.agent_info_operations) == 0:
                return 0.0
            
            total_time = sum(op.get("duration", 0.0) for op in self.agent_info_operations)
            return total_time / len(self.agent_info_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate average response time: {e}")
            return 0.0


def run_smoke_test():
    """Run basic functionality test for AgentInfoManager"""
    print("🧪 Running AgentInfoManager Smoke Test...")

    try:
        manager = AgentInfoManager()

        # Test getting agent info
        agent1 = manager.get_agent_info("Agent-1")
        assert agent1.role == "System Coordinator & Project Manager"
        assert agent1.emoji == "🎯"

        # Test getting unknown agent
        unknown = manager.get_agent_info("Unknown")
        assert unknown.role == "Team Member"

        # Test getting all agents
        all_agents = manager.get_all_agents()
        assert len(all_agents) == 5

        print("✅ AgentInfoManager Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ AgentInfoManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for AgentInfoManager testing"""

    parser = argparse.ArgumentParser(description="Agent Info Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--agent", help="Get info for specific agent")
    parser.add_argument("--list", action="store_true", help="List all agents")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    manager = AgentInfoManager()

    if args.agent:
        agent_info = manager.get_agent_info(args.agent)
        print(f"Agent: {args.agent}")
        print(f"Role: {agent_info.role}")
        print(f"Emoji: {agent_info.emoji}")
        print(f"Leadership: {agent_info.leadership}")
        print("Responsibilities:")
        for resp in agent_info.key_responsibilities:
            print(f"  • {resp}")
    elif args.list:
        agents = manager.get_all_agents()
        for name, info in agents.items():
            print(f"{name}: {info.emoji} {info.role}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
