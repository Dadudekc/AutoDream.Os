#!/usr/bin/env python3
"""
FastAPI Development Server Script
Agent_Cellphone_V2_Repository TDD Integration Project

This script runs the FastAPI development server with:
- Hot reloading enabled
- Interactive API documentation
- Proper configuration loading
- Health monitoring integration

Author: Web Development & UI Framework Specialist
License: MIT
"""

import os
import sys
import json
import logging
import uvicorn
from pathlib import Path
from typing import Dict, Any, List

# Add src directory to Python path
repo_root = Path(__file__).parent.parent
src_dir = repo_root / "src"
sys.path.insert(0, str(src_dir))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import yaml

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for API
class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    environment: str = Field(..., description="Environment")

class AutomationRequest(BaseModel):
    action: str = Field(..., description="Automation action to perform")
    target_url: str = Field(None, description="Target URL for automation")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters")

class AutomationResponse(BaseModel):
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Operation status")
    data: Dict[str, Any] = Field(default_factory=dict, description="Response data")

class UIRequest(BaseModel):
    component: str = Field(..., description="UI component to interact with")
    action: str = Field(..., description="Action to perform")
    data: Dict[str, Any] = Field(default_factory=dict, description="Component data")

class UIResponse(BaseModel):
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Operation status")
    component_data: Dict[str, Any] = Field(default_factory=dict, description="Component response data")

class FastAPIDevelopmentServer:
    """FastAPI development server for TDD integration"""
    
    def __init__(self, config_path: str = None):
        self.repo_root = Path(__file__).parent.parent
        self.config_path = config_path or str(self.repo_root / "config" / "fastapi_config.json")
        self.config = self._load_config()
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title=self.config.get('app', {}).get('title', 'Agent_Cellphone_V2 API'),
            description=self.config.get('app', {}).get('description', 'TDD Integration Web API'),
            version=self.config.get('app', {}).get('version', '2.0.0'),
            docs_url=self.config.get('app', {}).get('docs_url', '/docs'),
            redoc_url=self.config.get('app', {}).get('redoc_url', '/redoc')
        )
        
        # Setup middleware
        self._setup_middleware()
        
        # Setup routes
        self._setup_routes()
        
        logger.info("FastAPI development server initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load FastAPI configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default FastAPI configuration"""
        return {
            "app": {
                "title": "Agent_Cellphone_V2 API",
                "description": "TDD Integration Web API",
                "version": "2.0.0",
                "docs_url": "/docs",
                "redoc_url": "/redoc"
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "reload": True
            },
            "database": {
                "url": "sqlite:///./fastapi.db",
                "echo": False
            },
            "cors": {
                "origins": ["*"],
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "headers": ["*"]
            }
        }
    
    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        # CORS middleware
        cors_config = self.config.get('cors', {})
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_config.get('origins', ["*"]),
            allow_credentials=True,
            allow_methods=cors_config.get('methods', ["GET", "POST", "PUT", "DELETE"]),
            allow_headers=cors_config.get('headers', ["*"])
        )
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def index():
            """Main application page"""
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Agent_Cellphone_V2 FastAPI</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    .method { font-weight: bold; color: #0066cc; }
                    .url { font-family: monospace; background: #e8e8e8; padding: 2px 6px; }
                    .docs-link { display: inline-block; margin: 20px 0; padding: 10px 20px; background: #0066cc; color: white; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 Agent_Cellphone_V2 FastAPI Server</h1>
                    <p>Welcome to the FastAPI development server for TDD integration!</p>
                    
                    <a href="/docs" class="docs-link">📚 Interactive API Documentation</a>
                    <a href="/redoc" class="docs-link">📖 Alternative API Documentation</a>
                    
                    <h2>Available Endpoints:</h2>
                    
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div class="url">/health</div>
                        <p>Health check endpoint</p>
                    </div>
                    
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div class="url">/api/status</div>
                        <p>API status and available endpoints</p>
                    </div>
                    
                    <div class="endpoint">
                        <div class="method">GET/POST</div>
                        <div class="url">/api/web/automation</div>
                        <p>Web automation capabilities and requests</p>
                    </div>
                    
                    <div class="endpoint">
                        <div class="method">GET/POST</div>
                        <div class="url">/api/web/ui</div>
                        <p>Web UI framework interactions</p>
                    </div>
                    
                    <h2>Development Information:</h2>
                    <ul>
                        <li><strong>Server:</strong> FastAPI with Uvicorn</li>
                        <li><strong>Environment:</strong> Development</li>
                        <li><strong>Hot Reload:</strong> Enabled</li>
                        <li><strong>Documentation:</strong> Auto-generated</li>
                    </ul>
                </div>
            </body>
            </html>
            """
        
        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            """Health check endpoint"""
            return HealthResponse(
                status="healthy",
                service="FastAPI Development Server",
                version="2.0.0",
                environment="development"
            )
        
        @self.app.get("/api/status")
        async def api_status():
            """API status endpoint"""
            return {
                "api_status": "operational",
                "server": "FastAPI",
                "version": "2.0.0",
                "endpoints": [
                    "/health",
                    "/api/status",
                    "/api/web/automation",
                    "/api/web/ui"
                ],
                "documentation": {
                    "swagger": "/docs",
                    "redoc": "/redoc"
                }
            }
        
        @self.app.get("/api/web/automation")
        async def get_automation_status():
            """Get web automation capabilities"""
            return {
                "automation_status": "ready",
                "capabilities": [
                    "selenium_webdriver",
                    "playwright",
                    "web_scraping",
                    "form_automation",
                    "browser_automation",
                    "headless_testing"
                ],
                "frameworks": {
                    "selenium": "4.15.0+",
                    "playwright": "1.40.0+",
                    "webdriver_manager": "4.0.0+"
                }
            }
        
        @self.app.post("/api/web/automation", response_model=AutomationResponse)
        async def post_automation_request(request: AutomationRequest):
            """Process web automation requests"""
            try:
                # Simulate automation processing
                result = {
                    "action": request.action,
                    "target_url": request.target_url,
                    "parameters": request.parameters,
                    "timestamp": "2024-01-01T00:00:00Z",
                    "status": "processing"
                }
                
                return AutomationResponse(
                    message=f"Automation request '{request.action}' received",
                    status="processing",
                    data=result
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/web/ui")
        async def get_ui_status():
            """Get web UI framework status"""
            return {
                "ui_framework_status": "active",
                "frameworks": [
                    "FastAPI",
                    "Flask",
                    "React (planned)",
                    "Vue.js (planned)",
                    "Tailwind CSS (planned)"
                ],
                "capabilities": [
                    "REST API",
                    "WebSocket support",
                    "Template rendering",
                    "Static file serving",
                    "Middleware support"
                ]
            }
        
        @self.app.post("/api/web/ui", response_model=UIResponse)
        async def post_ui_request(request: UIRequest):
            """Process web UI requests"""
            try:
                # Simulate UI processing
                result = {
                    "component": request.component,
                    "action": request.action,
                    "data": request.data,
                    "timestamp": "2024-01-01T00:00:00Z",
                    "status": "processing"
                }
                
                return UIResponse(
                    message=f"UI request for component '{request.component}' received",
                    status="processing",
                    component_data=result
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/test")
        async def test_endpoint():
            """Test endpoint for TDD development"""
            return {
                "message": "Test endpoint working!",
                "status": "success",
                "test_data": {
                    "string": "Hello World",
                    "number": 42,
                    "boolean": True,
                    "array": [1, 2, 3, 4, 5],
                    "object": {"key": "value"}
                }
            }
    
    def run(self):
        """Run the FastAPI development server"""
        try:
            # Get server configuration
            server_config = self.config.get('server', {})
            host = server_config.get('host', '0.0.0.0')
            port = server_config.get('port', 8000)
            reload = server_config.get('reload', True)
            
            logger.info(f"Starting FastAPI development server on {host}:{port}")
            logger.info(f"Hot reload: {reload}")
            logger.info(f"API Documentation: http://localhost:{port}/docs")
            logger.info(f"Alternative Docs: http://localhost:{port}/redoc")
            
            # Run the FastAPI app with Uvicorn
            uvicorn.run(
                "scripts.run_fastapi_dev:FastAPIDevelopmentServer().app",
                host=host,
                port=port,
                reload=reload,
                log_level="info"
            )
            
        except Exception as e:
            logger.error(f"Error running FastAPI server: {e}")
            sys.exit(1)

def main():
    """Main function to run FastAPI development server"""
    try:
        server = FastAPIDevelopmentServer()
        server.run()
    except KeyboardInterrupt:
        logger.info("FastAPI development server stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
