"""
Discord Commander Web Routes
V2 Compliant web routes functionality
"""

import logging

from flask import Flask, jsonify, request

from .web_controller_models import AgentStatus, MessageData, SystemHealth

logger = logging.getLogger(__name__)


class WebRoutes:
    """Web routes handler for Discord Commander"""

    def __init__(self, app: Flask):
        """Initialize web routes"""
        self.app = app
        self._register_routes()

    def _register_routes(self):
        """Register all web routes"""
        self.app.route("/")(self.index)
        self.app.route("/api/agents")(self.get_agents)
        self.app.route("/api/agents/<agent_id>")(self.get_agent)
        self.app.route("/api/messages", methods=["POST"])(self.send_message)
        self.app.route("/api/health")(self.get_health)
        self.app.route("/api/status")(self.get_status)

    def index(self):
        """Serve main dashboard page"""
        return self.app.send_static_file("index.html")

    def get_agents(self):
        """Get all agents status"""
        try:
            # Mock data for now
            agents = [
                AgentStatus(
                    agent_id="Agent-1",
                    status="active",
                    last_seen=datetime.now(),
                    current_task="testing",
                    performance_score=95.5,
                ),
                AgentStatus(
                    agent_id="Agent-2",
                    status="idle",
                    last_seen=datetime.now(),
                    current_task=None,
                    performance_score=88.2,
                ),
            ]
            return jsonify([agent.__dict__ for agent in agents])
        except Exception as e:
            logger.error(f"Error getting agents: {e}")
            return jsonify({"error": str(e)}), 500

    def get_agent(self, agent_id: str):
        """Get specific agent status"""
        try:
            # Mock data for now
            agent = AgentStatus(
                agent_id=agent_id,
                status="active",
                last_seen=datetime.now(),
                current_task="processing",
                performance_score=92.1,
            )
            return jsonify(agent.__dict__)
        except Exception as e:
            logger.error(f"Error getting agent {agent_id}: {e}")
            return jsonify({"error": str(e)}), 500

    def send_message(self):
        """Send message to agent"""
        try:
            data = request.get_json()
            message = MessageData(
                content=data.get("content", ""),
                target_agent=data.get("target_agent", ""),
                priority=data.get("priority", "normal"),
                timestamp=datetime.now(),
            )

            # Process message here
            logger.info(f"Sending message to {message.target_agent}: {message.content}")

            return jsonify({"status": "success", "message": "Message sent"})
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return jsonify({"error": str(e)}), 500

    def get_health(self):
        """Get system health status"""
        try:
            health = SystemHealth(
                overall_status="healthy",
                active_agents=5,
                total_messages=1234,
                error_count=0,
                uptime=3600.0,
            )
            return jsonify(health.__dict__)
        except Exception as e:
            logger.error(f"Error getting health: {e}")
            return jsonify({"error": str(e)}), 500

    def get_status(self):
        """Get overall system status"""
        try:
            return jsonify(
                {
                    "status": "operational",
                    "timestamp": datetime.now().isoformat(),
                    "version": "2.0.0",
                }
            )
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return jsonify({"error": str(e)}), 500
