#!/usr/bin/env python3
"""
Multimedia Integration Coordinator
Coordinates multimedia services with other agents across all systems
"""

import logging
import json
import time
import asyncio
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from datetime import datetime
import threading

# Import multimedia services
try:
    from .multimedia.media_processor_service import MediaProcessorService
    from .multimedia.content_management_service import ContentManagementService
    from .multimedia.streaming_service import StreamingService
except ImportError:
    # Fallback for standalone usage
    import sys
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    from multimedia.media_processor_service import MediaProcessorService
    from multimedia.content_management_service import ContentManagementService
    from multimedia.streaming_service import StreamingService

logger = logging.getLogger(__name__)


class MultimediaIntegrationCoordinator:
    """
    Multimedia Integration Coordinator
    Coordinates multimedia services with other agents and systems
    """

    def __init__(self):
        self.multimedia_services = {}
        self.agent_connections = {}
        self.integration_status = {}
        self.coordination_events = {}

        # Initialize multimedia services
        self._initialize_multimedia_services()

        # Initialize agent coordination
        self._initialize_agent_coordination()

        # Setup coordination monitoring
        self._setup_coordination_monitoring()

    def _initialize_multimedia_services(self):
        """Initialize all multimedia services"""
        try:
            logger.info("🎬 Initializing multimedia services for agent coordination...")

            # Media processor service
            self.multimedia_services["media_processor"] = MediaProcessorService()
            logger.info("✅ MediaProcessorService initialized")

            # Content management service
            self.multimedia_services["content_manager"] = ContentManagementService()
            logger.info("✅ ContentManagementService initialized")

            # Streaming service
            self.multimedia_services["streaming"] = StreamingService()
            logger.info("✅ StreamingService initialized")

            logger.info("🎬 All multimedia services initialized successfully")

        except Exception as e:
            logger.error(f"❌ Error initializing multimedia services: {e}")
            raise

    def _initialize_agent_coordination(self):
        """Initialize coordination with other agents"""
        try:
            logger.info("🤝 Initializing agent coordination...")

            # Define agent coordination channels
            self.agent_connections = {
                "agent_1": {
                    "role": "Repository Development Specialist",
                    "multimedia_needs": ["content_generation", "documentation_videos"],
                    "status": "active",
                    "last_communication": time.time(),
                },
                "agent_2": {
                    "role": "Enhanced Collaborative System Specialist",
                    "multimedia_needs": ["collaboration_streams", "team_meetings"],
                    "status": "active",
                    "last_communication": time.time(),
                },
                "agent_3": {
                    "role": "Multimedia & Content Specialist (SELF)",
                    "multimedia_needs": ["core_multimedia_services"],
                    "status": "active",
                    "last_communication": time.time(),
                },
                "agent_4": {
                    "role": "Quality Assurance & Testing Specialist",
                    "multimedia_needs": ["test_videos", "quality_demos"],
                    "status": "active",
                    "last_communication": time.time(),
                },
                "agent_5": {
                    "role": "Captain & Coordination Specialist",
                    "multimedia_needs": ["coordination_streams", "status_reports"],
                    "status": "active",
                    "last_communication": time.time(),
                },
                "agent_6": {
                    "role": "Performance & Optimization Specialist",
                    "multimedia_needs": ["performance_metrics", "optimization_demos"],
                    "status": "active",
                    "last_communication": time.time(),
                },
                "agent_7": {
                    "role": "Integration & API Specialist",
                    "multimedia_needs": ["api_demos", "integration_tutorials"],
                    "status": "active",
                    "last_communication": time.time(),
                },
                "agent_8": {
                    "role": "Workflow & Automation Specialist",
                    "multimedia_needs": ["workflow_demos", "automation_videos"],
                    "status": "active",
                    "last_communication": time.time(),
                },
            }

            logger.info(
                f"✅ Agent coordination initialized for {len(self.agent_connections)} agents"
            )

        except Exception as e:
            logger.error(f"❌ Error initializing agent coordination: {e}")
            raise

    def _setup_coordination_monitoring(self):
        """Setup monitoring for agent coordination"""
        try:
            logger.info("📊 Setting up coordination monitoring...")

            # Initialize integration status
            self.integration_status = {
                "overall_status": "active",
                "multimedia_services_healthy": True,
                "agent_communications_active": True,
                "last_coordination_check": time.time(),
                "total_coordination_events": 0,
            }

            # Start coordination monitoring thread
            self.coordination_thread = threading.Thread(
                target=self._coordination_monitoring_loop, daemon=True
            )
            self.coordination_thread.start()

            logger.info("✅ Coordination monitoring setup complete")

        except Exception as e:
            logger.error(f"❌ Error setting up coordination monitoring: {e}")
            raise

    def _coordination_monitoring_loop(self):
        """Continuous monitoring loop for agent coordination"""
        while True:
            try:
                # Check agent communication status
                self._check_agent_communication_status()

                # Monitor multimedia service health
                self._monitor_multimedia_services()

                # Update coordination metrics
                self._update_coordination_metrics()

                # Sleep for monitoring interval
                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"❌ Error in coordination monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error

    def _check_agent_communication_status(self):
        """Check communication status with all agents"""
        try:
            current_time = time.time()

            for agent_id, agent_info in self.agent_connections.items():
                # Check if agent is responsive
                time_since_last_comm = current_time - agent_info["last_communication"]

                if time_since_last_comm > 300:  # 5 minutes
                    agent_info["status"] = "inactive"
                    logger.warning(
                        f"⚠️ Agent {agent_id} ({agent_info['role']}) appears inactive"
                    )
                else:
                    agent_info["status"] = "active"

            # Update overall status
            active_agents = sum(
                1
                for agent in self.agent_connections.values()
                if agent["status"] == "active"
            )
            total_agents = len(self.agent_connections)

            if active_agents == total_agents:
                self.integration_status["agent_communications_active"] = True
            else:
                self.integration_status["agent_communications_active"] = False
                logger.warning(f"⚠️ {total_agents - active_agents} agents are inactive")

        except Exception as e:
            logger.error(f"❌ Error checking agent communication status: {e}")

    def _monitor_multimedia_services(self):
        """Monitor health of multimedia services"""
        try:
            services_healthy = True

            for service_name, service in self.multimedia_services.items():
                try:
                    # Check service health (basic check)
                    if hasattr(service, "get_system_status"):
                        status = service.get_system_status()
                        if status.get("status") == "error":
                            services_healthy = False
                            logger.error(
                                f"❌ Service {service_name} reports error status"
                            )
                    else:
                        # Basic health check for services without status method
                        if not service:
                            services_healthy = False
                            logger.error(f"❌ Service {service_name} is None")

                except Exception as e:
                    services_healthy = False
                    logger.error(f"❌ Error checking service {service_name}: {e}")

            self.integration_status["multimedia_services_healthy"] = services_healthy

            if not services_healthy:
                logger.warning("⚠️ Some multimedia services are unhealthy")

        except Exception as e:
            logger.error(f"❌ Error monitoring multimedia services: {e}")

    def _update_coordination_metrics(self):
        """Update coordination metrics"""
        try:
            current_time = time.time()

            # Update last coordination check
            self.integration_status["last_coordination_check"] = current_time

            # Update overall status
            if (
                self.integration_status["multimedia_services_healthy"]
                and self.integration_status["agent_communications_active"]
            ):
                self.integration_status["overall_status"] = "healthy"
            else:
                self.integration_status["overall_status"] = "degraded"

        except Exception as e:
            logger.error(f"❌ Error updating coordination metrics: {e}")

    def coordinate_with_agent(
        self, agent_id: str, multimedia_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Coordinate multimedia services with a specific agent

        Args:
            agent_id: ID of the agent to coordinate with
            multimedia_request: Request for multimedia services

        Returns:
            Dict containing coordination response
        """
        try:
            if agent_id not in self.agent_connections:
                return {"error": f"Agent {agent_id} not found"}

            agent_info = self.agent_connections[agent_id]
            current_time = time.time()

            # Update last communication time
            agent_info["last_communication"] = current_time

            # Process multimedia request based on agent needs
            response = self._process_agent_multimedia_request(
                agent_id, multimedia_request
            )

            # Log coordination event
            self._log_coordination_event(agent_id, multimedia_request, response)

            logger.info(f"🤝 Coordinated with {agent_id} ({agent_info['role']})")
            return response

        except Exception as e:
            logger.error(f"❌ Error coordinating with agent {agent_id}: {e}")
            return {"error": str(e)}

    def _process_agent_multimedia_request(
        self, agent_id: str, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process multimedia request from specific agent"""
        try:
            request_type = request.get("type", "unknown")

            if request_type == "content_generation":
                return self._handle_content_generation_request(agent_id, request)
            elif request_type == "streaming_setup":
                return self._handle_streaming_setup_request(agent_id, request)
            elif request_type == "media_processing":
                return self._handle_media_processing_request(agent_id, request)
            elif request_type == "status_report":
                return self._handle_status_report_request(agent_id, request)
            elif request_type == "multimedia_update":
                return self._handle_multimedia_update_request(agent_id, request)
            else:
                return {"error": f"Unknown request type: {request_type}"}

        except Exception as e:
            logger.error(f"❌ Error processing multimedia request: {e}")
            return {"error": str(e)}

    def _handle_content_generation_request(
        self, agent_id: str, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle content generation request from agent"""
        try:
            content_manager = self.multimedia_services["content_manager"]

            # Extract request parameters
            pipeline_name = request.get("pipeline_name", f"{agent_id}_pipeline")
            content_type = request.get("content_type", "blog")
            source_data = request.get("source_data", {})

            # Create content pipeline
            pipeline_config = {
                "name": pipeline_name,
                "type": content_type,
                "source": agent_id,
                "output_format": request.get("output_format", "markdown"),
            }

            # Create and start pipeline
            if content_manager.create_content_pipeline(pipeline_name, pipeline_config):
                if content_manager.start_content_generation(pipeline_name, source_data):
                    return {
                        "status": "success",
                        "pipeline_name": pipeline_name,
                        "message": f"Content generation started for {agent_id}",
                        "pipeline_status": content_manager.get_pipeline_status(
                            pipeline_name
                        ),
                    }
                else:
                    return {"error": "Failed to start content generation"}
            else:
                return {"error": "Failed to create content pipeline"}

        except Exception as e:
            logger.error(f"❌ Error handling content generation request: {e}")
            return {"error": str(e)}

    def _handle_streaming_setup_request(
        self, agent_id: str, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle streaming setup request from agent"""
        try:
            streaming_service = self.multimedia_services["streaming"]

            # Extract request parameters
            stream_name = request.get("stream_name", f"{agent_id}_stream")
            stream_config = {
                "name": stream_name,
                "source": request.get("source", "webcam"),
                "platforms": request.get("platforms", ["youtube"]),
                "quality": request.get("quality", "720p"),
                "fps": request.get("fps", 30),
            }

            # Start streaming
            if streaming_service.start_live_stream(stream_name, stream_config):
                return {
                    "status": "success",
                    "stream_name": stream_name,
                    "message": f"Streaming started for {agent_id}",
                    "stream_status": streaming_service.get_streaming_status(
                        stream_name
                    ),
                }
            else:
                return {"error": "Failed to start streaming"}

        except Exception as e:
            logger.error(f"❌ Error handling streaming setup request: {e}")
            return {"error": str(e)}

    def _handle_media_processing_request(
        self, agent_id: str, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle media processing request from agent"""
        try:
            media_processor = self.multimedia_services["media_processor"]

            # Extract request parameters
            pipeline_name = request.get("pipeline_name", f"{agent_id}_media_pipeline")
            pipeline_config = {
                "name": pipeline_name,
                "type": "multimedia",
                "enable_video": request.get("enable_video", True),
                "enable_audio": request.get("enable_audio", True),
                "video": request.get("video", {}),
                "audio": request.get("audio", {}),
                "video_effects": request.get("video_effects", []),
                "audio_effects": request.get("audio_effects", []),
            }

            # Start multimedia pipeline
            if media_processor.start_multimedia_pipeline(
                pipeline_name, pipeline_config
            ):
                return {
                    "status": "success",
                    "pipeline_name": pipeline_name,
                    "message": f"Media processing pipeline started for {agent_id}",
                    "pipeline_status": media_processor.get_pipeline_status(
                        pipeline_name
                    ),
                }
            else:
                return {"error": "Failed to start media processing pipeline"}

        except Exception as e:
            logger.error(f"❌ Error handling media processing request: {e}")
            return {"error": str(e)}

    def _handle_status_report_request(
        self, agent_id: str, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle status report request from agent"""
        try:
            return {
                "status": "success",
                "agent_id": agent_id,
                "multimedia_services_status": {
                    "media_processor": self.multimedia_services[
                        "media_processor"
                    ].get_system_status(),
                    "content_manager": self.multimedia_services[
                        "content_manager"
                    ].get_pipeline_status(),
                    "streaming": self.multimedia_services[
                        "streaming"
                    ].get_streaming_status(),
                },
                "integration_status": self.integration_status,
                "agent_connections": self.agent_connections,
            }

        except Exception as e:
            logger.error(f"❌ Error handling status report request: {e}")
            return {"error": str(e)}

    def _handle_multimedia_update_request(
        self, agent_id: str, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle multimedia update request from agent"""
        try:
            update_type = request.get("update_type", "general")
            update_data = request.get("update_data", {})

            # Process the update based on type
            if update_type == "general_update":
                return {
                    "status": "success",
                    "agent_id": agent_id,
                    "message": f'Multimedia update received: {update_data.get("message", "No message")}',
                    "update_type": update_type,
                    "timestamp": time.time(),
                    "multimedia_services_available": list(
                        self.multimedia_services.keys()
                    ),
                }
            else:
                return {
                    "status": "success",
                    "agent_id": agent_id,
                    "message": f"Multimedia update of type {update_type} received",
                    "update_type": update_type,
                    "timestamp": time.time(),
                }

        except Exception as e:
            logger.error(f"❌ Error handling multimedia update request: {e}")
            return {"error": str(e)}

    def _log_coordination_event(
        self, agent_id: str, request: Dict[str, Any], response: Dict[str, Any]
    ):
        """Log coordination event for monitoring"""
        try:
            event = {
                "timestamp": time.time(),
                "agent_id": agent_id,
                "request_type": request.get("type", "unknown"),
                "request_data": request,
                "response": response,
                "status": response.get("status", "error"),
            }

            # Store event
            if "coordination_events" not in self.coordination_events:
                self.coordination_events = {}

            event_id = f"{agent_id}_{int(time.time())}"
            self.coordination_events[event_id] = event

            # Update metrics
            self.integration_status["total_coordination_events"] += 1

            # Clean up old events (keep last 100)
            if len(self.coordination_events) > 100:
                oldest_events = sorted(
                    self.coordination_events.keys(),
                    key=lambda k: self.coordination_events[k]["timestamp"],
                )[:50]
                for old_event in oldest_events:
                    del self.coordination_events[old_event]

        except Exception as e:
            logger.error(f"❌ Error logging coordination event: {e}")

    def get_coordination_status(self) -> Dict[str, Any]:
        """Get overall coordination status"""
        try:
            return {
                "integration_status": self.integration_status,
                "agent_connections": self.agent_connections,
                "multimedia_services": {
                    name: "healthy" if service else "unhealthy"
                    for name, service in self.multimedia_services.items()
                },
                "recent_coordination_events": len(self.coordination_events),
                "timestamp": time.time(),
            }

        except Exception as e:
            logger.error(f"❌ Error getting coordination status: {e}")
            return {"error": str(e)}

    def broadcast_multimedia_update(
        self, update_type: str, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Broadcast multimedia update to all agents"""
        try:
            logger.info(f"📢 Broadcasting multimedia update: {update_type}")

            broadcast_results = {}

            for agent_id, agent_info in self.agent_connections.items():
                if agent_info["status"] == "active":
                    try:
                        # Send update to agent
                        result = self.coordinate_with_agent(
                            agent_id,
                            {
                                "type": "multimedia_update",
                                "update_type": update_type,
                                "update_data": update_data,
                            },
                        )
                        broadcast_results[agent_id] = result

                    except Exception as e:
                        broadcast_results[agent_id] = {"error": str(e)}
                        logger.error(f"❌ Error broadcasting to {agent_id}: {e}")
                else:
                    broadcast_results[agent_id] = {"status": "inactive"}

            logger.info(f"📢 Broadcast complete. Results: {broadcast_results}")
            return {
                "status": "success",
                "broadcast_results": broadcast_results,
                "total_agents": len(self.agent_connections),
                "active_agents": sum(
                    1
                    for agent in self.agent_connections.values()
                    if agent["status"] == "active"
                ),
            }

        except Exception as e:
            logger.error(f"❌ Error broadcasting multimedia update: {e}")
            return {"error": str(e)}


# CLI interface for coordination
def main():
    """CLI interface for Multimedia Integration Coordinator"""
    import argparse

    parser = argparse.ArgumentParser(description="Multimedia Integration Coordinator")
    parser.add_argument(
        "--status", action="store_true", help="Show coordination status"
    )
    parser.add_argument("--coordinate", type=str, help="Coordinate with specific agent")
    parser.add_argument("--broadcast", type=str, help="Broadcast update to all agents")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring mode")

    args = parser.parse_args()

    try:
        coordinator = MultimediaIntegrationCoordinator()

        if args.status:
            status = coordinator.get_coordination_status()
            print(json.dumps(status, indent=2, default=str))

        elif args.coordinate:
            # Example coordination request
            request = {
                "type": "content_generation",
                "content_type": "blog",
                "source_data": {
                    "title": "Test Content",
                    "description": "Test Description",
                },
            }
            result = coordinator.coordinate_with_agent(args.coordinate, request)
            print(json.dumps(result, indent=2, default=str))

        elif args.broadcast:
            # Example broadcast
            update_data = {"message": args.broadcast, "timestamp": time.time()}
            result = coordinator.broadcast_multimedia_update(
                "general_update", update_data
            )
            print(json.dumps(result, indent=2, default=str))

        elif args.monitor:
            print("🔍 Starting coordination monitoring...")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    status = coordinator.get_coordination_status()
                    print(
                        f"\n📊 Status Update: {status['integration_status']['overall_status']}"
                    )
                    print(f"Active Agents: {status['agent_connections']}")
                    time.sleep(30)
            except KeyboardInterrupt:
                print("\n👋 Monitoring stopped")

        else:
            print("🎬 Multimedia Integration Coordinator ready")
            print("Use --help for available commands")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
