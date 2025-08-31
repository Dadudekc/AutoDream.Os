"""
agentconfiguration.py
Module: agentconfiguration.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:07
"""

# AgentConfiguration - Extracted for SRP compliance

class AgentConfiguration:
    """Agent configuration data"""
    agent_id: str
    agent_name: str
    agent_type: str
    current_location: str
    capabilities: List[str]
    limitations: List[str]
    integration_status: str
    last_updated: datetime
    configuration_data: Dict[str, Any] = field(default_factory=dict)


@dataclass

