#!/usr/bin/env python3
"""
Discord Commander Web Controller
================================

Web-based interface for controlling the Discord Commander system.
Provides an interactive dashboard for managing agents and sending messages.

Features:
- Real-time agent status monitoring
- Interactive message sending interface
- Swarm coordination tools
- System health monitoring
- Rich web interface with real-time updates
"""

import asyncio
import logging
import threading
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, jsonify, render_template, request
    from flask_socketio import SocketIO, emit

    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from .bot import DiscordCommanderBot

logger = logging.getLogger(__name__)


class DiscordCommanderController:
    """Web controller for Discord Commander system."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize the web controller."""
        self.host = host
        self.port = port
        self.bot = None
        self.app = None
        self.socketio = None

        if not FLASK_AVAILABLE:
            logger.error(
                "Flask and Flask-SocketIO not available. Install: pip install flask flask-socketio"
            )
            return

        self._setup_flask_app()

    def _setup_flask_app(self):
        """Set up the Flask application."""
        self.app = Flask(
            __name__,
            template_folder=Path(__file__).parent / "templates",
            static_folder=Path(__file__).parent / "static",
        )
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        # Register routes
        self._register_routes()

        # Register socket events
        self._register_socket_events()

    def _register_routes(self):
        """Register Flask routes."""

        @self.app.route("/")
        def index():
            """Serve the main dashboard."""
            return render_template("discord_commander.html")

        @self.app.route("/api/agents")
        def get_agents():
            """Get agent status."""
            if not self.bot:
                return jsonify({"error": "Bot not initialized"}), 503

            agents = [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ]
            agent_status = {}

            for agent in agents:
                status = asyncio.run(self.bot._get_agent_status(agent))
                agent_status[agent] = {"status": status, "last_seen": "Unknown"}

            return jsonify({"agents": agent_status, "timestamp": datetime.now().isoformat()})

        @self.app.route("/api/send_message", methods=["POST"])
        def send_message():
            """Send a message to an agent."""
            if not self.bot:
                return jsonify({"error": "Bot not initialized"}), 503

            data = request.get_json()
            agent_id = data.get("agent_id")
            message = data.get("message")

            if not agent_id or not message:
                return jsonify({"error": "Missing agent_id or message"}), 400

            try:
                result = asyncio.run(
                    self.bot.messaging_service.send_message(
                        agent_id=agent_id, message=message, sender="Web-Controller"
                    )
                )

                return jsonify(
                    {
                        "success": result.get("success", False),
                        "message": result.get("message", "No response"),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/swarm_coordinate", methods=["POST"])
        def swarm_coordinate():
            """Send coordination message to all agents."""
            if not self.bot:
                return jsonify({"error": "Bot not initialized"}), 503

            data = request.get_json()
            message = data.get("message")

            if not message:
                return jsonify({"error": "Missing message"}), 400

            try:
                agents = [
                    "Agent-1",
                    "Agent-2",
                    "Agent-3",
                    "Agent-4",
                    "Agent-5",
                    "Agent-6",
                    "Agent-7",
                    "Agent-8",
                ]
                results = []

                for agent in agents:
                    result = asyncio.run(
                        self.bot.messaging_service.send_message(
                            agent_id=agent,
                            message=f"[SWARM COORDINATION] {message}",
                            sender="Web-Controller",
                        )
                    )
                    results.append({"agent": agent, "success": result.get("success", False)})

                return jsonify({"results": results, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                logger.error(f"Error in swarm coordination: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/system_status")
        def get_system_status():
            """Get system status."""
            if not self.bot:
                return jsonify({"error": "Bot not initialized"}), 503

            status = self.bot.get_status()
            return jsonify({"status": status, "timestamp": datetime.now().isoformat()})

    def _register_socket_events(self):
        """Register SocketIO events."""

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection."""
            logger.info("Client connected to Discord Commander Controller")
            emit("status", {"message": "Connected to Discord Commander Controller"})

        @self.socketio.on("get_agent_status")
        def handle_get_agent_status():
            """Handle request for agent status."""
            if not self.bot:
                emit("error", {"message": "Bot not initialized"})
                return

            agents = [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ]
            agent_status = {}

            for agent in agents:
                status = asyncio.run(self.bot._get_agent_status(agent))
                agent_status[agent] = status

            emit("agent_status", {"agents": agent_status, "timestamp": datetime.now().isoformat()})

        @self.socketio.on("send_message")
        def handle_send_message(data):
            """Handle message sending via socket."""
            if not self.bot:
                emit("error", {"message": "Bot not initialized"})
                return

            agent_id = data.get("agent_id")
            message = data.get("message")

            if not agent_id or not message:
                emit("error", {"message": "Missing agent_id or message"})
                return

            try:
                result = asyncio.run(
                    self.bot.messaging_service.send_message(
                        agent_id=agent_id, message=message, sender="Web-Controller-Socket"
                    )
                )

                emit(
                    "message_sent",
                    {
                        "agent_id": agent_id,
                        "success": result.get("success", False),
                        "message": result.get("message", "No response"),
                        "timestamp": datetime.now().isoformat(),
                    },
                )
            except Exception as e:
                emit("error", {"message": str(e)})

    def set_bot(self, bot: DiscordCommanderBot):
        """Set the Discord bot instance."""
        self.bot = bot

    def run(self):
        """Run the web controller."""
        if not FLASK_AVAILABLE:
            logger.error("Cannot run web controller: Flask not available")
            return

        if not self.app or not self.socketio:
            logger.error("Flask app not initialized")
            return

        logger.info(f"Starting Discord Commander Web Controller on {self.host}:{self.port}")
        logger.info("Open http://localhost:8080 in your browser to access the controller")

        # Start Flask app in a separate thread
        def run_app():
            self.socketio.run(self.app, host=self.host, port=self.port, debug=False)

        thread = threading.Thread(target=run_app, daemon=True)
        thread.start()

    def stop(self):
        """Stop the web controller."""
        logger.info("Stopping Discord Commander Web Controller")
        if self.socketio:
            self.socketio.stop()


def create_default_templates():
    """Create default HTML templates."""
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)

    # Create main dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Commander Controller</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .main-content {
            padding: 30px;
        }

        .section {
            margin-bottom: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .agent-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .agent-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #3498db;
        }

        .agent-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .agent-status {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 15px;
        }

        .status-active {
            background: #d4edda;
            color: #155724;
        }

        .status-inactive {
            background: #f8d7da;
            color: #721c24;
        }

        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .control-group {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .control-group h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #2c3e50;
            font-weight: bold;
        }

        input, select, textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }

        textarea {
            min-height: 100px;
            resize: vertical;
        }

        button {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: transform 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
        }

        .logs {
            background: #2c3e50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .log-entry {
            margin-bottom: 5px;
            padding: 2px 0;
        }

        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 10px;
        }

        .status-connected {
            background: #27ae60;
        }

        .status-disconnected {
            background: #e74c3c;
        }

        .footer {
            text-align: center;
            padding: 20px;
            background: #34495e;
            color: white;
        }

        @media (max-width: 768px) {
            .controls {
                grid-template-columns: 1fr;
            }

            .agent-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Discord Commander Controller</h1>
            <p>Interactive control interface for the Agent Swarm system</p>
            <div id="connection-status">
                <span class="status-indicator status-disconnected" id="status-indicator"></span>
                <span id="status-text">Disconnected</span>
            </div>
        </div>

        <div class="main-content">
            <div class="section">
                <h2>🐝 Agent Status</h2>
                <div class="agent-grid" id="agent-grid">
                    <!-- Agent cards will be populated here -->
                </div>
            </div>

            <div class="controls">
                <div class="control-group">
                    <h3>📤 Send Message</h3>
                    <form id="message-form">
                        <div class="form-group">
                            <label for="agent-select">Select Agent:</label>
                            <select id="agent-select" required>
                                <option value="">Choose an agent...</option>
                                <option value="Agent-1">Agent-1 (Captain)</option>
                                <option value="Agent-2">Agent-2 (Architect)</option>
                                <option value="Agent-3">Agent-3 (Database)</option>
                                <option value="Agent-4">Agent-4 (Captain)</option>
                                <option value="Agent-5">Agent-5 (Analytics)</option>
                                <option value="Agent-6">Agent-6 (Builder)</option>
                                <option value="Agent-7">Agent-7 (Frontend)</option>
                                <option value="Agent-8">Agent-8 (Operations)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="message-input">Message:</label>
                            <textarea id="message-input" placeholder="Enter your message here..." required></textarea>
                        </div>

                        <button type="submit">Send Message</button>
                    </form>
                </div>

                <div class="control-group">
                    <h3>🐝 Swarm Coordination</h3>
                    <form id="swarm-form">
                        <div class="form-group">
                            <label for="swarm-message">Coordination Message:</label>
                            <textarea id="swarm-message" placeholder="Enter coordination message for all agents..." required></textarea>
                        </div>

                        <button type="submit">Coordinate Swarm</button>
                    </form>
                </div>
            </div>

            <div class="section">
                <h2>📋 System Status</h2>
                <div id="system-status">
                    <!-- System status will be populated here -->
                </div>
            </div>

            <div class="section">
                <h2>📜 Activity Logs</h2>
                <div class="logs" id="logs">
                    <!-- Logs will be populated here -->
                </div>
            </div>
        </div>

        <div class="footer">
            <p>🐝 WE ARE SWARM - Discord Commander Controller</p>
        </div>
    </div>

    <script>
        const socket = io();
        const logsContainer = document.getElementById('logs');

        // Socket event handlers
        socket.on('connect', function() {
            document.getElementById('status-indicator').className = 'status-indicator status-connected';
            document.getElementById('status-text').textContent = 'Connected';
            addLog('Connected to Discord Commander Controller', 'info');
            requestAgentStatus();
            requestSystemStatus();
        });

        socket.on('disconnect', function() {
            document.getElementById('status-indicator').className = 'status-indicator status-disconnected';
            document.getElementById('status-text').textContent = 'Disconnected';
            addLog('Disconnected from Discord Commander Controller', 'error');
        });

        socket.on('agent_status', function(data) {
            updateAgentStatus(data.agents);
        });

        socket.on('message_sent', function(data) {
            if (data.success) {
                addLog(`Message sent to ${data.agent_id}: ${data.message}`, 'success');
                document.getElementById('message-form').reset();
            } else {
                addLog(`Failed to send message to ${data.agent_id}: ${data.message}`, 'error');
            }
        });

        socket.on('error', function(data) {
            addLog(`Error: ${data.message}`, 'error');
        });

        // Form handlers
        document.getElementById('message-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const agentId = document.getElementById('agent-select').value;
            const message = document.getElementById('message-input').value;

            if (agentId && message) {
                socket.emit('send_message', {
                    agent_id: agentId,
                    message: message
                });
                addLog(`Sending message to ${agentId}...`, 'info');
            }
        });

        document.getElementById('swarm-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const message = document.getElementById('swarm-message').value;

            if (message) {
                socket.emit('swarm_coordinate', { message: message });
                addLog(`Coordinating swarm with message: ${message}`, 'info');
                document.getElementById('swarm-form').reset();
            }
        });

        // Functions
        function requestAgentStatus() {
            socket.emit('get_agent_status');
        }

        function requestSystemStatus() {
            fetch('/api/system_status')
                .then(response => response.json())
                .then(data => {
                    if (data.status) {
                        document.getElementById('system-status').innerHTML =
                            `<p><strong>Bot Status:</strong> ${data.status.status || 'Unknown'}</p>
                             <p><strong>Uptime:</strong> ${data.status.uptime_formatted || 'Unknown'}</p>
                             <p><strong>Commands:</strong> ${data.status.command_count || 0}</p>`;
                    }
                })
                .catch(err => addLog(`Error fetching system status: ${err}`, 'error'));
        }

        function updateAgentStatus(agents) {
            const agentGrid = document.getElementById('agent-grid');
            agentGrid.innerHTML = '';

            Object.entries(agents).forEach(([agentId, status]) => {
                const card = document.createElement('div');
                card.className = 'agent-card';

                const statusClass = status.toLowerCase().includes('active') ? 'status-active' : 'status-inactive';
                card.innerHTML = `
                    <h3>${agentId}</h3>
                    <div class="agent-status ${statusClass}">${status}</div>
                `;

                agentGrid.appendChild(card);
            });
        }

        function addLog(message, type = 'info') {
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${type}`;
            logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;

            logsContainer.appendChild(logEntry);
            logsContainer.scrollTop = logsContainer.scrollHeight;

            // Keep only last 100 logs
            while (logsContainer.children.length > 100) {
                logsContainer.removeChild(logsContainer.firstChild);
            }
        }

        // Periodic updates
        setInterval(requestAgentStatus, 5000);
        setInterval(requestSystemStatus, 10000);
    </script>
</body>
</html>
    """

    with open(templates_dir / "discord_commander.html", "w") as f:
        f.write(dashboard_html)

    print(
        f"✅ Created Discord Commander web interface at {templates_dir / 'discord_commander.html'}"
    )


if __name__ == "__main__":
    # Create templates if they don't exist
    create_default_templates()

    # Start the controller
    controller = DiscordCommanderController()
    controller.run()
