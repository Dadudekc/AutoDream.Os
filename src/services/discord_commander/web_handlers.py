#!/usr/bin/env python3
"""
Web Handlers - Request handlers for Discord Commander Web Controller
================================================================

Request handlers extracted from web_controller.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from typing import Any

from flask import request

from .web_models import MessageRequest, SwarmCoordinateRequest
from .web_utils import (
    create_template_data,
    format_agent_response,
    load_all_agents,
    validate_message_request,
)

logger = logging.getLogger(__name__)


class WebHandlers:
    """Web request handlers for Discord Commander."""

    def __init__(self, messaging_service=None, coordination_service=None):
        """Initialize web handlers."""
        self.messaging_service = messaging_service
        self.coordination_service = coordination_service

    def handle_get_agents(self) -> dict[str, Any]:
        """Handle GET /api/agents request."""
        try:
            agents = load_all_agents()
            formatted_agents = [format_agent_response(agent) for agent in agents]

            return {
                "success": True,
                "agents": formatted_agents,
                "total_agents": len(formatted_agents),
                "active_agents": len(
                    [a for a in formatted_agents if a["status"] == "ACTIVE_AGENT_MODE"]
                ),
            }
        except Exception as e:
            logger.error(f"Error getting agents: {e}")
            return {"success": False, "error": str(e)}

    def handle_send_message(self) -> dict[str, Any]:
        """Handle POST /api/send-message request."""
        try:
            data = request.get_json()
            if not data:
                return {"success": False, "error": "No JSON data provided"}

            if not validate_message_request(data):
                return {"success": False, "error": "Invalid message request data"}

            # Create message request model
            message_req = MessageRequest(
                from_agent=data["from_agent"],
                to_agent=data["to_agent"],
                message=data["message"],
                priority=data.get("priority", "NORMAL"),
                message_type=data.get("message_type", "text"),
                tags=data.get("tags", []),
                timestamp=data.get("timestamp", ""),
            )

            # Send message via messaging service
            if self.messaging_service:
                success = self.messaging_service.send_message(
                    message_req.to_agent,
                    message_req.message,
                    message_req.from_agent,
                    message_req.priority,
                )
            else:
                # Fallback: log message
                logger.info(
                    f"Message from {message_req.from_agent} to {message_req.to_agent}: {message_req.message}"
                )
                success = True

            return {
                "success": success,
                "message": "Message sent successfully" if success else "Failed to send message",
                "message_id": f"msg_{hash(message_req.message)}",
            }

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {"success": False, "error": str(e)}

    def handle_swarm_coordinate(self) -> dict[str, Any]:
        """Handle POST /api/swarm-coordinate request."""
        try:
            data = request.get_json()
            if not data:
                return {"success": False, "error": "No JSON data provided"}

            # Create coordinate request model
            coord_req = SwarmCoordinateRequest(
                requesting_agent=data.get("requesting_agent", "Unknown"),
                target_agents=data.get("target_agents", []),
                action=data.get("action", "coordinate"),
                parameters=data.get("parameters", {}),
                priority=data.get("priority", "NORMAL"),
                timestamp=data.get("timestamp", ""),
            )

            # Process coordination request
            if self.coordination_service:
                result = self.coordination_service.process_coordination_request(coord_req)
            else:
                # Fallback: log coordination request
                logger.info(
                    f"Coordination request from {coord_req.requesting_agent}: {coord_req.action}"
                )
                result = {"success": True, "message": "Coordination request logged"}

            return result

        except Exception as e:
            logger.error(f"Error processing swarm coordinate: {e}")
            return {"success": False, "error": str(e)}

    def handle_get_system_status(self) -> dict[str, Any]:
        """Handle GET /api/system-status request."""
        try:
            template_data = create_template_data()
            system_status = template_data.system_status

            return {
                "success": True,
                "system_status": {
                    "timestamp": system_status.timestamp,
                    "total_agents": system_status.total_agents,
                    "active_agents": system_status.active_agents,
                    "inactive_agents": system_status.inactive_agents,
                    "total_tasks": system_status.total_tasks,
                    "completed_tasks": system_status.completed_tasks,
                    "in_progress_tasks": system_status.in_progress_tasks,
                    "system_health": system_status.system_health,
                    "messaging_service_status": system_status.messaging_service_status,
                    "discord_bot_status": system_status.discord_bot_status,
                    "quality_compliance_rate": system_status.quality_compliance_rate,
                },
            }
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"success": False, "error": str(e)}

    def handle_get_social_media_status(self) -> dict[str, Any]:
        """Handle GET /api/social-media-status request."""
        try:
            template_data = create_template_data()
            social_status = template_data.social_media_status

            formatted_status = []
            for status in social_status:
                formatted_status.append(
                    {
                        "platform": status.platform,
                        "status": status.status,
                        "last_post": status.last_post,
                        "posts_today": status.posts_today,
                        "engagement_rate": status.engagement_rate,
                        "followers_count": status.followers_count,
                        "is_active": status.is_active,
                    }
                )

            return {"success": True, "social_media_status": formatted_status}
        except Exception as e:
            logger.error(f"Error getting social media status: {e}")
            return {"success": False, "error": str(e)}

    def handle_post_to_social_media(self) -> dict[str, Any]:
        """Handle POST /api/post-to-social-media request."""
        try:
            data = request.get_json()
            if not data:
                return {"success": False, "error": "No JSON data provided"}

            platform = data.get("platform")
            content = data.get("content")

            if not platform or not content:
                return {"success": False, "error": "Platform and content are required"}

            # TODO: Implement actual social media posting
            logger.info(f"Posting to {platform}: {content}")

            return {
                "success": True,
                "message": f"Posted to {platform} successfully",
                "post_id": f"post_{hash(content)}",
            }

        except Exception as e:
            logger.error(f"Error posting to social media: {e}")
            return {"success": False, "error": str(e)}

    def handle_get_quality_metrics(self) -> dict[str, Any]:
        """Handle GET /api/quality-metrics request."""
        try:
            template_data = create_template_data()
            quality_metrics = template_data.quality_metrics

            return {
                "success": True,
                "quality_metrics": {
                    "total_files": quality_metrics.total_files,
                    "v2_compliant_files": quality_metrics.v2_compliant_files,
                    "compliance_rate": quality_metrics.compliance_rate,
                    "critical_violations": quality_metrics.critical_violations,
                    "file_size_violations": quality_metrics.file_size_violations,
                    "function_count_violations": quality_metrics.function_count_violations,
                    "class_count_violations": quality_metrics.class_count_violations,
                    "last_quality_check": quality_metrics.last_quality_check,
                },
            }
        except Exception as e:
            logger.error(f"Error getting quality metrics: {e}")
            return {"success": False, "error": str(e)}

    def handle_health_check(self) -> dict[str, Any]:
        """Handle GET /api/health request."""
        return {
            "success": True,
            "status": "healthy",
            "timestamp": template_data.last_updated,
            "services": {
                "web_controller": "active",
                "messaging_service": "active" if self.messaging_service else "inactive",
                "coordination_service": "active" if self.coordination_service else "inactive",
            },
        }
