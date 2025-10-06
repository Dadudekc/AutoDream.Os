#!/usr/bin/env python3
"""
Discord Commander Web Controller - Routes
==========================================

Flask routes and SocketIO events for Discord Commander web interface.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- REST API endpoints
- WebSocket event handlers
- Agent status monitoring
- Message sending interface

Extracted from main web controller module for V2 compliance.
"""

import asyncio
from datetime import datetime

try:
    from flask import Flask, jsonify, render_template, request
    from flask_socketio import SocketIO, emit

    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


def register_routes(app: Flask, bot):
    """Register Flask routes."""

    @app.route("/")
    def index():
        """Serve the main dashboard."""
        return render_template("discord_commander.html")

    @app.route("/api/agents")
    def get_agents():
        """Get agent status."""
        if not bot:
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
            status = asyncio.run(bot._get_agent_status(agent))
            agent_status[agent] = {"status": status, "last_seen": "Unknown"}

        return jsonify({"agents": agent_status, "timestamp": datetime.now().isoformat()})

    @app.route("/api/send_message", methods=["POST"])
    def send_message():
        """Send a message to an agent."""
        if not bot:
            return jsonify({"error": "Bot not initialized"}), 503

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        agent_id = data.get("agent_id")
        message = data.get("message")
        priority = data.get("priority", "NORMAL")

        if not agent_id or not message:
            return jsonify({"error": "agent_id and message are required"}), 400

        try:
            # Send message using bot
            success = asyncio.run(bot.send_message_to_agent(agent_id, message, priority))

            if success:
                return jsonify(
                    {
                        "success": True,
                        "message": f"Message sent to {agent_id}",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            else:
                return jsonify({"error": "Failed to send message"}), 500

        except Exception as e:
            return jsonify({"error": f"Error sending message: {str(e)}"}), 500

    @app.route("/api/broadcast_message", methods=["POST"])
    def broadcast_message():
        """Broadcast a message to all agents."""
        if not bot:
            return jsonify({"error": "Bot not initialized"}), 503

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        message = data.get("message")
        priority = data.get("priority", "NORMAL")

        if not message:
            return jsonify({"error": "message is required"}), 400

        try:
            # Broadcast message using bot
            success = asyncio.run(bot.broadcast_message(message, priority))

            if success:
                return jsonify(
                    {
                        "success": True,
                        "message": "Message broadcast to all agents",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            else:
                return jsonify({"error": "Failed to broadcast message"}), 500

        except Exception as e:
            return jsonify({"error": f"Error broadcasting message: {str(e)}"}), 500

    @app.route("/api/system_status")
    def system_status():
        """Get system status."""
        if not bot:
            return jsonify({"error": "Bot not initialized"}), 503

        try:
            status = asyncio.run(bot.get_system_status())
            return jsonify({"status": status, "timestamp": datetime.now().isoformat()})
        except Exception as e:
            return jsonify({"error": f"Error getting system status: {str(e)}"}), 500

    @app.route("/api/channels")
    def get_channels():
        """Get Discord channels."""
        if not bot:
            return jsonify({"error": "Bot not initialized"}), 503

        try:
            channels = asyncio.run(bot.get_channels())
            return jsonify({"channels": channels, "timestamp": datetime.now().isoformat()})
        except Exception as e:
            return jsonify({"error": f"Error getting channels: {str(e)}"}), 500

    @app.route("/api/send_to_channel", methods=["POST"])
    def send_to_channel():
        """Send a message to a Discord channel."""
        if not bot:
            return jsonify({"error": "Bot not initialized"}), 503

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        channel_id = data.get("channel_id")
        message = data.get("message")

        if not channel_id or not message:
            return jsonify({"error": "channel_id and message are required"}), 400

        try:
            success = asyncio.run(bot.send_to_channel(channel_id, message))

            if success:
                return jsonify(
                    {
                        "success": True,
                        "message": f"Message sent to channel {channel_id}",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            else:
                return jsonify({"error": "Failed to send message to channel"}), 500

        except Exception as e:
            return jsonify({"error": f"Error sending message to channel: {str(e)}"}), 500


def register_socket_events(socketio: SocketIO, bot):
    """Register SocketIO events."""

    @socketio.on("connect")
    def handle_connect():
        """Handle client connection."""
        emit("status", {"message": "Connected to Discord Commander"})

    @socketio.on("disconnect")
    def handle_disconnect():
        """Handle client disconnection."""
        pass

    @socketio.on("get_agent_status")
    def handle_get_agent_status():
        """Handle agent status request."""
        if not bot:
            emit("agent_status", {"error": "Bot not initialized"})
            return

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
            agent_status = {}

            for agent in agents:
                status = asyncio.run(bot._get_agent_status(agent))
                agent_status[agent] = {"status": status, "last_seen": "Unknown"}

            emit("agent_status", {"agents": agent_status, "timestamp": datetime.now().isoformat()})
        except Exception as e:
            emit("agent_status", {"error": f"Error getting agent status: {str(e)}"})

    @socketio.on("send_message")
    def handle_send_message(data):
        """Handle message sending request."""
        if not bot:
            emit("message_result", {"error": "Bot not initialized"})
            return

        agent_id = data.get("agent_id")
        message = data.get("message")
        priority = data.get("priority", "NORMAL")

        if not agent_id or not message:
            emit("message_result", {"error": "agent_id and message are required"})
            return

        try:
            success = asyncio.run(bot.send_message_to_agent(agent_id, message, priority))

            if success:
                emit(
                    "message_result",
                    {
                        "success": True,
                        "message": f"Message sent to {agent_id}",
                        "timestamp": datetime.now().isoformat(),
                    },
                )
            else:
                emit("message_result", {"error": "Failed to send message"})
        except Exception as e:
            emit("message_result", {"error": f"Error sending message: {str(e)}"})

    @socketio.on("broadcast_message")
    def handle_broadcast_message(data):
        """Handle broadcast message request."""
        if not bot:
            emit("broadcast_result", {"error": "Bot not initialized"})
            return

        message = data.get("message")
        priority = data.get("priority", "NORMAL")

        if not message:
            emit("broadcast_result", {"error": "message is required"})
            return

        try:
            success = asyncio.run(bot.broadcast_message(message, priority))

            if success:
                emit(
                    "broadcast_result",
                    {
                        "success": True,
                        "message": "Message broadcast to all agents",
                        "timestamp": datetime.now().isoformat(),
                    },
                )
            else:
                emit("broadcast_result", {"error": "Failed to broadcast message"})
        except Exception as e:
            emit("broadcast_result", {"error": f"Error broadcasting message: {str(e)}"})

    @socketio.on("get_system_status")
    def handle_get_system_status():
        """Handle system status request."""
        if not bot:
            emit("system_status", {"error": "Bot not initialized"})
            return

        try:
            status = asyncio.run(bot.get_system_status())
            emit("system_status", {"status": status, "timestamp": datetime.now().isoformat()})
        except Exception as e:
            emit("system_status", {"error": f"Error getting system status: {str(e)}"})

    @socketio.on("get_channels")
    def handle_get_channels():
        """Handle channels request."""
        if not bot:
            emit("channels", {"error": "Bot not initialized"})
            return

        try:
            channels = asyncio.run(bot.get_channels())
            emit("channels", {"channels": channels, "timestamp": datetime.now().isoformat()})
        except Exception as e:
            emit("channels", {"error": f"Error getting channels: {str(e)}"})
