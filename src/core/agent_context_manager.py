"""
Agent Context Manager

Manages agent-specific context and preferences for personalized documentation access.
"""


logger = logging.getLogger(__name__)

class AgentContextManager:
    """
    Manages context information for different agents.
    """

    def __init__(self):
        self.agent_contexts: Dict[str, Dict[str, Any]] = {}

    def set_agent_context(self, agent_id: str, context: Dict[str, Any]) -> None:
        """
        Set or update context for a specific agent.

        Args:
            agent_id: Unique identifier for the agent
            context: Context information (role, domain, current_task, etc.)
        """
        self.agent_contexts[agent_id] = {
            **context,
            "last_updated": datetime.now().isoformat()
        }
        get_logger(__name__).info(f"Set context for agent {agent_id}: {context}")

    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """
        Get context for a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent context dictionary
        """
        return self.agent_contexts.get(agent_id, {})

    def update_agent_task(self, agent_id: str, task: str) -> None:
        """
        Update the current task for an agent.

        Args:
            agent_id: Agent identifier
            task: New current task
        """
        if agent_id in self.agent_contexts:
            self.agent_contexts[agent_id]["current_task"] = task
            self.agent_contexts[agent_id]["last_updated"] = datetime.now().isoformat()
            get_logger(__name__).info(f"Updated task for agent {agent_id}: {task}")

    def get_agent_role(self, agent_id: str) -> str:
        """
        Get the role of a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent role string
        """
        context = self.get_agent_context(agent_id)
        return context.get('role', 'Unknown')

    def get_agent_domain(self, agent_id: str) -> str:
        """
        Get the domain of a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent domain string
        """
        context = self.get_agent_context(agent_id)
        return context.get('domain', 'General')

    def get_all_agents(self) -> List[str]:
        """
        Get list of all agent IDs with context.

        Returns:
            List of agent IDs
        """
        return list(self.agent_contexts.keys())

    def get_agents_by_role(self, role: str) -> List[str]:
        """
        Get agents that have a specific role.

        Args:
            role: Role to search for

        Returns:
            List of agent IDs with the specified role
        """
        return [
            agent_id for agent_id, context in self.agent_contexts.items()
            if context.get('role', '').lower() == role.lower()
        ]

    def get_agents_by_domain(self, domain: str) -> List[str]:
        """
        Get agents that work in a specific domain.

        Args:
            domain: Domain to search for

        Returns:
            List of agent IDs working in the specified domain
        """
        return [
            agent_id for agent_id, context in self.agent_contexts.items()
            if domain.lower() in context.get('domain', '').lower()
        ]

    def remove_agent_context(self, agent_id: str) -> bool:
        """
        Remove context for a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            True if removed, False if not found
        """
        if agent_id in self.agent_contexts:
            del self.agent_contexts[agent_id]
            get_logger(__name__).info(f"Removed context for agent {agent_id}")
            return True
        return False

    def clear_all_contexts(self) -> None:
        """
        Clear all agent contexts.
        """
        self.agent_contexts = {}
        get_logger(__name__).info("Cleared all agent contexts")

    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all agent contexts.

        Returns:
            Dictionary with context summary
        """
        summary = {
            'total_agents': len(self.agent_contexts),
            'roles': {},
            'domains': {},
            'agents': {}
        }

        for agent_id, context in self.agent_contexts.items():
            role = context.get('role', 'Unknown')
            domain = context.get('domain', 'General')

            # Count roles
            summary['roles'][role] = summary['roles'].get(role, 0) + 1

            # Count domains
            summary['domains'][domain] = summary['domains'].get(domain, 0) + 1

            # Agent details
            summary['agents'][agent_id] = {
                'role': role,
                'domain': domain,
                'current_task': context.get('current_task', ''),
                'last_updated': context.get('last_updated', '')
            }

        return summary

    def export_contexts(self, file_path: str) -> bool:
        """
        Export all agent contexts to a file.

        Args:
            file_path: Path to save the contexts

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                write_json(self.agent_contexts, f, indent=2, ensure_ascii=False)
            get_logger(__name__).info(f"Exported agent contexts to {file_path}")
            return True
        except Exception as e:
            get_logger(__name__).error(f"Error exporting contexts: {e}")
            return False

    def import_contexts(self, file_path: str) -> bool:
        """
        Import agent contexts from a file.

        Args:
            file_path: Path to load contexts from

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.agent_contexts = read_json(f)
            get_logger(__name__).info(f"Imported agent contexts from {file_path}")
            return True
        except Exception as e:
            get_logger(__name__).error(f"Error importing contexts: {e}")
            return False

