#!/usr/bin/env python3
"""
Discord Commander Web Controller V2 - V2 Compliant
================================================

V2 compliant version of Discord Commander Web Controller using modular architecture.
Maintains all functionality while achieving V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import threading
from pathlib import Path

try:
    from flask import Flask
    from flask_socketio import SocketIO

    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from .bot import DiscordCommanderBot
from .web_models import WebControllerConfig
from .web_routes import WebRoutes

logger = logging.getLogger(__name__)


class DiscordCommanderControllerV2:
    """V2 compliant web controller for Discord Commander system."""

    def __init__(self, host: str = "localhost", port: int = 8080, debug: bool = False):
        """Initialize the V2 compliant web controller."""
        self.config = WebControllerConfig(
            host=host,
            port=port,
            debug=debug,
            flask_available=FLASK_AVAILABLE,
            socketio_enabled=True,
            auto_start=True,
            template_dir="templates",
            static_dir="static",
        )

        self.bot = None
        self.app = None
        self.socketio = None
        self.routes = None
        self.server_thread = None

        if not FLASK_AVAILABLE:
            logger.error(
                "Flask and Flask-SocketIO not available. Install: pip install flask flask-socketio"
            )
            return

        self._setup_flask_app()
        self._create_default_templates()

    def _setup_flask_app(self):
        """Setup Flask application."""
        if not FLASK_AVAILABLE:
            return

        self.app = Flask(
            __name__, template_folder=self.config.template_dir, static_folder=self.config.static_dir
        )

        self.app.config["SECRET_KEY"] = "discord_commander_secret_key"
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        logger.info("Flask application initialized")

    def _create_default_templates(self):
        """Create default HTML templates."""
        if not FLASK_AVAILABLE:
            return

        templates_dir = Path(self.config.template_dir)
        templates_dir.mkdir(exist_ok=True)

        # Create basic dashboard template
        dashboard_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Discord Commander</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel { border: 1px solid #ccc; padding: 15px; border-radius: 5px; }
        .agent-status { margin: 10px 0; padding: 10px; background: #f5f5f5; }
        .system-health { font-weight: bold; }
        .health-excellent { color: green; }
        .health-good { color: blue; }
        .health-fair { color: orange; }
        .health-poor { color: red; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <div class="dashboard">
        <div class="panel">
            <h2>System Status</h2>
            <p>Total Agents: {{ system_status.total_agents }}</p>
            <p>Active Agents: {{ system_status.active_agents }}</p>
            <p>System Health: <span class="system-health health-{{ system_status.system_health.lower() }}">{{ system_status.system_health }}</span></p>
        </div>
        
        <div class="panel">
            <h2>Agent Status</h2>
            {% for agent in agents %}
            <div class="agent-status">
                <strong>{{ agent.agent_id }}</strong> - {{ agent.status }}
                <br>Mission: {{ agent.current_mission }}
                <br>Tasks: {{ agent.current_tasks|length }} active, {{ agent.completed_tasks|length }} completed
            </div>
            {% endfor %}
        </div>
        
        <div class="panel">
            <h2>Quality Metrics</h2>
            <p>V2 Compliance: {{ (quality_metrics.compliance_rate * 100)|round(1) }}%</p>
            <p>Total Files: {{ quality_metrics.total_files }}</p>
            <p>Critical Violations: {{ quality_metrics.critical_violations }}</p>
        </div>
        
        <div class="panel">
            <h2>Social Media</h2>
            {% for platform in social_media_status %}
            <p>{{ platform.platform }}: {{ platform.status }} 
               {% if platform.is_active %}({{ platform.posts_today }} posts today){% endif %}</p>
            {% endfor %}
        </div>
    </div>

    <script>
        const socket = io();
        
        socket.on('connect', function() {
            console.log('Connected to Discord Commander');
        });
        
        socket.on('agent_status_update', function(data) {
            console.log('Agent status update:', data);
            // Refresh page or update specific elements
            location.reload();
        });
        
        socket.on('system_status_update', function(data) {
            console.log('System status update:', data);
            // Update system status display
        });
        
        // Request periodic updates
        setInterval(function() {
            socket.emit('update_dashboard');
        }, 30000); // Every 30 seconds
    </script>
</body>
</html>
        """

        with open(templates_dir / "dashboard.html", "w") as f:
            f.write(dashboard_template)

        logger.info("Default templates created")

    def set_bot(self, bot: DiscordCommanderBot):
        """Set the Discord bot instance."""
        self.bot = bot
        logger.info("Discord bot instance set")

    def start(self):
        """Start the web controller."""
        if not FLASK_AVAILABLE:
            logger.error("Cannot start web controller: Flask not available")
            return False

        try:
            # Initialize routes with messaging service
            messaging_service = None
            if self.bot:
                messaging_service = getattr(self.bot, "messaging_service", None)

            self.routes = WebRoutes(self.app, self.socketio, messaging_service)

            # Start server in separate thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()

            logger.info(f"Web controller started on http://{self.config.host}:{self.config.port}")
            return True

        except Exception as e:
            logger.error(f"Error starting web controller: {e}")
            return False

    def _run_server(self):
        """Run the Flask server."""
        try:
            self.socketio.run(
                self.app,
                host=self.config.host,
                port=self.config.port,
                debug=self.config.debug,
                allow_unsafe_werkzeug=True,
            )
        except Exception as e:
            logger.error(f"Error running web server: {e}")

    def stop(self):
        """Stop the web controller."""
        logger.info("Web controller stopped")

    def broadcast_update(self, update_type: str, data: dict):
        """Broadcast update to all connected clients."""
        if self.routes and self.socketio:
            if update_type == "agent_status":
                self.routes.broadcast_agent_update(data.get("agent_id"), data)
            elif update_type == "system_status":
                self.routes.broadcast_system_update(data)
            elif update_type == "message":
                self.routes.broadcast_message_notification(data)

    def get_status(self) -> dict:
        """Get web controller status."""
        return {
            "running": self.server_thread is not None and self.server_thread.is_alive(),
            "flask_available": FLASK_AVAILABLE,
            "host": self.config.host,
            "port": self.config.port,
            "debug": self.config.debug,
            "bot_connected": self.bot is not None,
        }


def create_web_controller(
    host: str = "localhost", port: int = 8080
) -> DiscordCommanderControllerV2:
    """Create and return a web controller instance."""
    return DiscordCommanderControllerV2(host, port)


if __name__ == "__main__":
    # Test the web controller
    controller = create_web_controller()
    if controller.start():
        try:
            import time

            time.sleep(60)  # Run for 1 minute for testing
        except KeyboardInterrupt:
            pass
        finally:
            controller.stop()
    else:
        print("Failed to start web controller")
