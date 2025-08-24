#!/usr/bin/env python3
"""
FastAPI Portal App - V2 Core Web Integration

FastAPI-based web application for the unified portal.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from .portal_core import UnifiedPortal
from .data_models import PortalConfig, AgentPortalInfo, PortalSection


class SessionRequest(BaseModel):
    """Session creation request model"""
    user_id: str = Field(..., description="User identifier")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Session metadata")


class FastAPIPortalApp:
    """
    FastAPI-based portal web application
    
    Single responsibility: FastAPI web interface for portal.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """

    def __init__(self, portal: UnifiedPortal, config: Optional[PortalConfig] = None):
        """Initialize FastAPI portal app"""
        self.portal = portal
        self.config = config or portal.config
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title=self.config.title,
            version=self.config.version,
            description="Unified Portal API"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.logger = logging.getLogger(f"{__name__}.FastAPIPortalApp")
        self._setup_routes()
        self.logger.info("FastAPI portal app initialized")

    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def index():
            """Main portal page"""
            return f"""
            <html>
                <head>
                    <title>{self.config.title}</title>
                </head>
                <body>
                    <h1>{self.config.title}</h1>
                    <p>Version: {self.config.version}</p>
                    <p>Welcome to the Unified Portal</p>
                </body>
            </html>
            """

        @self.app.get("/api/status")
        async def api_status():
            """Get portal status"""
            return self.portal.get_portal_status()

        @self.app.get("/api/agents")
        async def api_agents():
            """Get all agents"""
            agents = [agent.to_dict() for agent in self.portal.agents.values()]
            return {"agents": agents}

        @self.app.get("/api/agents/{agent_id}")
        async def api_agent_detail(agent_id: str):
            """Get specific agent details"""
            agent = self.portal.get_agent_info(agent_id)
            if agent:
                return agent.to_dict()
            raise HTTPException(status_code=404, detail="Agent not found")

        @self.app.get("/api/navigation")
        async def api_navigation():
            """Get navigation state"""
            return self.portal.get_navigation_state()

        @self.app.post("/api/navigation/{section}")
        async def api_navigate_to(section: str):
            """Navigate to specific section"""
            try:
                portal_section = PortalSection(section)
                self.portal.navigate_to_section(portal_section)
                return {"success": True, "section": section}
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid section")

        @self.app.post("/api/sessions")
        async def api_create_session(session_request: SessionRequest):
            """Create new session"""
            try:
                session_id = self.portal.create_session(
                    session_request.user_id, 
                    session_request.metadata
                )
                return {"session_id": session_id, "success": True}
            except Exception as e:
                self.logger.error(f"Session creation failed: {e}")
                raise HTTPException(status_code=500, detail="Session creation failed")

        @self.app.get("/api/sessions/{session_id}")
        async def api_session_status(session_id: str):
            """Get session status"""
            is_valid = self.portal.validate_session(session_id)
            return {"valid": is_valid, "session_id": session_id}

        @self.app.delete("/api/sessions/{session_id}")
        async def api_terminate_session(session_id: str):
            """Terminate session"""
            success = self.portal.terminate_session(session_id)
            return {"success": success, "session_id": session_id}

        @self.app.get("/api/statistics")
        async def api_statistics():
            """Get portal statistics"""
            return self.portal.get_agent_statistics()

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "service": "unified_portal"}

    def _setup_websocket_handlers(self):
        """Setup WebSocket handlers"""
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time communication"""
            await websocket.accept()
            connection_id = str(id(websocket))
            
            try:
                self.portal.add_connection(connection_id)
                self.logger.info(f"WebSocket client connected: {connection_id}")
                
                # Send welcome message
                await websocket.send_json({
                    "type": "connected",
                    "connection_id": connection_id,
                    "status": "connected"
                })
                
                # Handle incoming messages
                while True:
                    try:
                        data = await websocket.receive_json()
                        message_type = data.get("type")
                        
                        if message_type == "portal_update":
                            update_type = data.get("update_type")
                            if update_type == "status":
                                await websocket.send_json({
                                    "type": "portal_status",
                                    "data": self.portal.get_portal_status()
                                })
                            elif update_type == "agents":
                                agents = [agent.to_dict() for agent in self.portal.agents.values()]
                                await websocket.send_json({
                                    "type": "agents_update",
                                    "data": {"agents": agents}
                                })
                        
                        elif message_type == "ping":
                            await websocket.send_json({"type": "pong"})
                            
                    except Exception as e:
                        self.logger.error(f"WebSocket message handling error: {e}")
                        await websocket.send_json({
                            "type": "error",
                            "message": "Message processing failed"
                        })
                        
            except WebSocketDisconnect:
                self.logger.info(f"WebSocket client disconnected: {connection_id}")
            except Exception as e:
                self.logger.error(f"WebSocket error: {e}")
            finally:
                self.portal.remove_connection(connection_id)

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the FastAPI portal app"""
        import uvicorn
        
        if self.config.enable_websockets:
            self._setup_websocket_handlers()
        
        uvicorn.run(self.app, host=host, port=port)

    def get_app(self) -> FastAPI:
        """Get the FastAPI app instance"""
        return self.app
