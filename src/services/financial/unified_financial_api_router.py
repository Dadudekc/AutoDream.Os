import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AgentRegistration, CrossAgentRequest

logger = logging.getLogger(__name__)


class UnifiedFinancialAPIRouterMixin:
    """Agent registration and request routing helpers."""

    def register_agent(
        self,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        required_services: List[str],
        api_token: str = "",
    ) -> bool:
        """Register a new agent with the unified API."""
        try:
            available_services = [
                "portfolio_management",
                "risk_management",
                "market_data",
                "trading_intelligence",
                "options_trading",
                "financial_analytics",
                "market_sentiment",
                "portfolio_optimization",
            ]
            for service in required_services:
                if service not in available_services:
                    logger.error(f"Invalid service requested: {service}")
                    return False

            agent_reg = AgentRegistration(
                agent_id=agent_id,
                agent_name=agent_name,
                agent_type=agent_type,
                required_services=required_services,
                registration_time=datetime.now(),
                last_heartbeat=datetime.now(),
                status="ACTIVE",
            )
            self.registered_agents[agent_id] = agent_reg
            if hasattr(self.auth_service, "register_agent"):
                self.auth_service.register_agent(agent_id, api_token)

            self.performance_metrics[agent_id] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0.0,
                "last_updated": datetime.now().isoformat(),
            }
            logger.info(f"Agent {agent_id} registered successfully")
            self.persistence.save(
                self.registered_agents, self.request_history, self.performance_metrics
            )
            return True
        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {e}")
            return False

    def update_agent_heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat."""
        try:
            if agent_id in self.registered_agents:
                self.registered_agents[agent_id].last_heartbeat = datetime.now()
                self.registered_agents[agent_id].status = "ACTIVE"
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating heartbeat for agent {agent_id}: {e}")
            return False

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of an agent."""
        try:
            if agent_id in self.registered_agents:
                agent = self.registered_agents[agent_id]
                return {
                    "agent_id": agent.agent_id,
                    "agent_name": agent.agent_name,
                    "agent_type": agent.agent_type,
                    "status": agent.status,
                    "required_services": agent.required_services,
                    "registration_time": agent.registration_time.isoformat(),
                    "last_heartbeat": agent.last_heartbeat.isoformat(),
                    "performance_metrics": self.performance_metrics.get(agent_id, {}),
                }
            return None
        except Exception as e:
            logger.error(f"Error getting agent status for {agent_id}: {e}")
            return None

    def get_all_agents_status(self) -> List[Dict[str, Any]]:
        """Get status of all registered agents."""
        try:
            return [
                self.get_agent_status(agent_id)
                for agent_id in self.registered_agents.keys()
            ]
        except Exception as e:
            logger.error(f"Error getting all agents status: {e}")
            return []

    def request_service(
        self,
        source_agent: str,
        target_service: str,
        request_type: str,
        request_data: Dict[str, Any],
        priority: str = "MEDIUM",
        api_token: str = "",
    ) -> str:
        """Request a financial service through the unified API."""
        try:
            if source_agent not in self.registered_agents:
                raise ValueError(f"Agent {source_agent} not registered")

            if hasattr(self.auth_service, "authorize"):
                self.auth_service.authorize(
                    source_agent, target_service, self.registered_agents
                )
            else:
                if not self.auth_service.authenticate(source_agent, api_token):
                    raise PermissionError("Authentication failed")
                if (
                    target_service
                    not in self.registered_agents[source_agent].required_services
                ):
                    raise ValueError(
                        f"Service {target_service} not available for agent {source_agent}"
                    )

            request_id = str(uuid.uuid4())
            request = CrossAgentRequest(
                request_id=request_id,
                source_agent=source_agent,
                target_service=target_service,
                request_type=request_type,
                request_data=request_data,
                timestamp=datetime.now(),
                priority=priority,
                status="PENDING",
            )
            self.active_requests[request_id] = request
            self.request_history.append(request)
            self.performance_metrics[source_agent]["total_requests"] += 1
            logger.info(f"Service request {request_id} created for {source_agent}")
            return request_id
        except Exception as e:
            logger.error(f"Error creating service request: {e}")
            raise
