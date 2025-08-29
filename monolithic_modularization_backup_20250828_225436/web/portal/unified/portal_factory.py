#!/usr/bin/env python3
"""
Portal Factory - V2 Core Web Integration

Factory for creating different types of portal applications.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Optional, Literal
from enum import Enum

from .portal_core import UnifiedPortal
from .data_models import PortalConfig
from .flask_app import FlaskPortalApp
from .fastapi_app import FastAPIPortalApp


class PortalType(Enum):
    """Supported portal types"""
    FLASK = "flask"
    FASTAPI = "fastapi"


class PortalFactory:
    """
    Factory for creating portal applications
    
    Single responsibility: Portal application creation.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """

    def __init__(self):
        """Initialize portal factory"""
        self.logger = logging.getLogger(f"{__name__}.PortalFactory")
        self.logger.info("Portal factory initialized")

    def create_portal(self, config: Optional[PortalConfig] = None) -> UnifiedPortal:
        """Create a new unified portal instance"""
        try:
            portal = UnifiedPortal(config)
            self.logger.info("Unified portal created successfully")
            return portal
        except Exception as e:
            self.logger.error(f"Portal creation failed: {e}")
            raise

    def create_flask_app(self, portal: UnifiedPortal, 
                        config: Optional[PortalConfig] = None) -> FlaskPortalApp:
        """Create a Flask-based portal application"""
        try:
            flask_app = FlaskPortalApp(portal, config)
            self.logger.info("Flask portal app created successfully")
            return flask_app
        except Exception as e:
            self.logger.error(f"Flask app creation failed: {e}")
            raise

    def create_fastapi_app(self, portal: UnifiedPortal, 
                          config: Optional[PortalConfig] = None) -> FastAPIPortalApp:
        """Create a FastAPI-based portal application"""
        try:
            fastapi_app = FastAPIPortalApp(portal, config)
            self.logger.info("FastAPI portal app created successfully")
            return fastapi_app
        except Exception as e:
            self.logger.error(f"FastAPI app creation failed: {e}")
            raise

    def create_portal_with_app(self, portal_type: PortalType, 
                              config: Optional[PortalConfig] = None):
        """Create a portal with the specified application type"""
        try:
            # Create the core portal
            portal = self.create_portal(config)
            
            # Create the appropriate app type
            if portal_type == PortalType.FLASK:
                app = self.create_flask_app(portal, config)
                return portal, app
            elif portal_type == PortalType.FASTAPI:
                app = self.create_fastapi_app(portal, config)
                return portal, app
            else:
                raise ValueError(f"Unsupported portal type: {portal_type}")
                
        except Exception as e:
            self.logger.error(f"Portal with app creation failed: {e}")
            raise

    def create_default_portal(self) -> tuple[UnifiedPortal, FlaskPortalApp]:
        """Create a default portal with Flask app"""
        try:
            config = PortalConfig()
            portal, app = self.create_portal_with_app(PortalType.FLASK, config)
            self.logger.info("Default portal (Flask) created successfully")
            return portal, app
        except Exception as e:
            self.logger.error(f"Default portal creation failed: {e}")
            raise

    def create_production_portal(self) -> tuple[UnifiedPortal, FastAPIPortalApp]:
        """Create a production-ready portal with FastAPI app"""
        try:
            config = PortalConfig(
                enable_real_time=True,
                enable_websockets=True,
                enable_agent_integration=True,
                debug_mode=False,
                session_timeout=7200  # 2 hours for production
            )
            portal, app = self.create_portal_with_app(PortalType.FASTAPI, config)
            self.logger.info("Production portal (FastAPI) created successfully")
            return portal, app
        except Exception as e:
            self.logger.error(f"Production portal creation failed: {e}")
            raise

    def create_development_portal(self) -> tuple[UnifiedPortal, FlaskPortalApp]:
        """Create a development portal with Flask app"""
        try:
            config = PortalConfig(
                enable_real_time=True,
                enable_websockets=True,
                enable_agent_integration=True,
                debug_mode=True,
                session_timeout=1800  # 30 minutes for development
            )
            portal, app = self.create_portal_with_app(PortalType.FLASK, config)
            self.logger.info("Development portal (Flask) created successfully")
            return portal, app
        except Exception as e:
            self.logger.error(f"Development portal creation failed: {e}")
            raise

    def get_supported_types(self) -> list[str]:
        """Get list of supported portal types"""
        return [portal_type.value for portal_type in PortalType]

    def validate_portal_type(self, portal_type: str) -> bool:
        """Validate if a portal type is supported"""
        try:
            PortalType(portal_type)
            return True
        except ValueError:
            return False

    def get_portal_info(self, portal: UnifiedPortal) -> dict:
        """Get information about a portal instance"""
        try:
            return {
                'portal_id': id(portal),
                'config': portal.config.to_dict(),
                'status': portal.get_portal_status(),
                'statistics': portal.get_agent_statistics(),
                'navigation': portal.get_navigation_state()
            }
        except Exception as e:
            self.logger.error(f"Failed to get portal info: {e}")
            return {'error': str(e)}

