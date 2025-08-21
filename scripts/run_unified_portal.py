#!/usr/bin/env python3
"""
Unified Portal Launcher Script
Agent_Cellphone_V2_Repository - Multi-Agent Web Integration

This script provides a command-line interface for launching and managing
the unified web portal with support for both Flask and FastAPI backends.
"""

import os
import sys
import json
import yaml
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.web.portal import (
    create_unified_portal,
    create_portal_with_agents,
    setup_portal_integration
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PortalLauncher:
    """Portal launcher with configuration management"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/portal_config.yaml"
        self.config = self.load_config()
        self.portal = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load portal configuration from file"""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            logger.warning(f"Configuration file not found: {config_file}")
            return self.get_default_config()
        
        try:
            with open(config_file, 'r') as f:
                if config_file.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default portal configuration"""
        return {
            'portal': {
                'title': 'Agent_Cellphone_V2 Unified Portal',
                'version': '1.0.0',
                'theme': 'default',
                'enable_real_time': True,
                'enable_websockets': True,
                'enable_agent_integration': True,
                'max_agents': 8,
                'session_timeout': 3600,
                'debug_mode': False
            },
            'server': {
                'host': '0.0.0.0',
                'port': 5000,
                'reload': True,
                'debug': False
            },
            'agents': [
                {
                    'agent_id': 'agent-1',
                    'name': 'Project Management Agent',
                    'description': 'Manages project coordination and task tracking',
                    'dashboard_type': 'project_management',
                    'capabilities': ['project_planning', 'task_management', 'coordination'],
                    'status': 'online',
                    'integration_status': 'active'
                },
                {
                    'agent_id': 'agent-2',
                    'name': 'Web Development Agent',
                    'description': 'Handles web development and UI framework tasks',
                    'dashboard_type': 'web_development',
                    'capabilities': ['frontend_development', 'backend_development', 'ui_framework'],
                    'status': 'online',
                    'integration_status': 'active'
                },
                {
                    'agent_id': 'agent-3',
                    'name': 'Automation Agent',
                    'description': 'Manages automation and testing workflows',
                    'dashboard_type': 'automation',
                    'capabilities': ['test_automation', 'workflow_automation', 'ci_cd'],
                    'status': 'online',
                    'integration_status': 'active'
                },
                {
                    'agent_id': 'agent-4',
                    'name': 'Data Analysis Agent',
                    'description': 'Handles data processing and analysis tasks',
                    'dashboard_type': 'data_analysis',
                    'capabilities': ['data_processing', 'analytics', 'reporting'],
                    'status': 'online',
                    'integration_status': 'active'
                },
                {
                    'agent_id': 'agent-5',
                    'name': 'System Administration Agent',
                    'description': 'Manages system infrastructure and monitoring',
                    'dashboard_type': 'system_admin',
                    'capabilities': ['infrastructure', 'monitoring', 'security'],
                    'status': 'online',
                    'integration_status': 'active'
                },
                {
                    'agent_id': 'agent-6',
                    'name': 'User Interface Agent',
                    'description': 'Handles user experience and interface design',
                    'dashboard_type': 'user_interface',
                    'capabilities': ['ux_design', 'interface_design', 'accessibility'],
                    'status': 'online',
                    'integration_status': 'active'
                },
                {
                    'agent_id': 'agent-7',
                    'name': 'Integration Agent',
                    'description': 'Coordinates cross-agent communication and integration',
                    'dashboard_type': 'integration',
                    'capabilities': ['communication', 'integration', 'coordination'],
                    'status': 'online',
                    'integration_status': 'active'
                },
                {
                    'agent_id': 'agent-8',
                    'name': 'Quality Assurance Agent',
                    'description': 'Ensures quality and testing standards',
                    'dashboard_type': 'coordination',
                    'capabilities': ['quality_assurance', 'testing', 'standards'],
                    'status': 'online',
                    'integration_status': 'active'
                }
            ]
        }
    
    def create_portal(self, backend_type: str = 'flask') -> Any:
        """Create portal with specified backend"""
        try:
            logger.info(f"Creating {backend_type.upper()} portal...")
            
            # Create portal with agents
            self.portal = create_portal_with_agents(
                agent_configs=self.config['agents'],
                backend_type=backend_type,
                config=self.config
            )
            
            logger.info(f"Portal created successfully with {len(self.config['agents'])} agents")
            return self.portal
            
        except Exception as e:
            logger.error(f"Error creating portal: {e}")
            raise
    
    def launch_portal(self, backend_type: str = 'flask', host: str = None, port: int = None, reload: bool = None):
        """Launch the portal with specified settings"""
        try:
            # Create portal
            portal = self.create_portal(backend_type)
            
            # Get server configuration
            server_config = self.config.get('server', {})
            host = host or server_config.get('host', '0.0.0.0')
            port = port or server_config.get('port', 5000)
            reload = reload if reload is not None else server_config.get('reload', True)
            
            logger.info(f"Launching {backend_type.upper()} portal on {host}:{port}")
            logger.info(f"Portal URL: http://{host}:{port}")
            logger.info(f"Agent Dashboard: http://{host}:{port}/dashboard")
            logger.info(f"API Documentation: http://{host}:{port}/docs")
            
            # Launch portal
            if hasattr(portal, 'run'):
                portal.run(host=host, port=port, reload=reload)
            else:
                logger.error(f"Portal object does not have a 'run' method: {type(portal)}")
                
        except Exception as e:
            logger.error(f"Error launching portal: {e}")
            raise
    
    def show_status(self):
        """Show portal and agent status"""
        if not self.portal:
            logger.info("Portal not created yet. Use 'launch' command first.")
            return
        
        try:
            # Get portal stats
            if hasattr(self.portal, 'portal') and hasattr(self.portal.portal, 'get_portal_stats'):
                stats = self.portal.portal.get_portal_stats()
                logger.info("Portal Statistics:")
                logger.info(f"  Total Agents: {stats.get('total_agents', 0)}")
                logger.info(f"  Online Agents: {stats.get('online_agents', 0)}")
                logger.info(f"  Active Integrations: {stats.get('active_integrations', 0)}")
            
            # Get agent list
            if hasattr(self.portal, 'portal') and hasattr(self.portal.portal, 'get_all_agents'):
                agents = self.portal.portal.get_all_agents()
                logger.info(f"\nAgent Status ({len(agents)} agents):")
                for agent in agents:
                    status_icon = "🟢" if agent.status == "online" else "🔴"
                    logger.info(f"  {status_icon} {agent.name} ({agent.agent_id}) - {agent.status}")
                    
        except Exception as e:
            logger.error(f"Error getting portal status: {e}")
    
    def test_integration(self):
        """Test portal integration"""
        if not self.portal:
            logger.info("Portal not created yet. Use 'launch' command first.")
            return
        
        try:
            logger.info("Testing portal integration...")
            
            # Test basic functionality
            if hasattr(self.portal, 'portal'):
                logger.info("✅ Portal core accessible")
                
                if hasattr(self.portal.portal, 'get_all_agents'):
                    agents = self.portal.portal.get_all_agents()
                    logger.info(f"✅ Agent management: {len(agents)} agents registered")
                
                if hasattr(self.portal.portal, 'get_portal_stats'):
                    stats = self.portal.portal.get_portal_stats()
                    logger.info("✅ Portal statistics accessible")
                
                logger.info("✅ Portal integration test completed successfully")
            else:
                logger.error("❌ Portal core not accessible")
                
        except Exception as e:
            logger.error(f"❌ Portal integration test failed: {e}")

def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(
        description="Unified Portal Launcher for Agent_Cellphone_V2_Repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch Flask portal with default settings
  python run_unified_portal.py launch flask
  
  # Launch FastAPI portal on custom host/port
  python run_unified_portal.py launch fastapi --host 127.0.0.1 --port 8000
  
  # Show portal status
  python run_unified_portal.py status
  
  # Test portal integration
  python run_unified_portal.py test
  
  # Launch with custom config
  python run_unified_portal.py launch flask --config config/custom_portal.yaml
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Launch command
    launch_parser = subparsers.add_parser('launch', help='Launch the portal')
    launch_parser.add_argument('backend', choices=['flask', 'fastapi'], help='Backend type')
    launch_parser.add_argument('--host', help='Host to bind to')
    launch_parser.add_argument('--port', type=int, help='Port to bind to')
    launch_parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    launch_parser.add_argument('--no-reload', action='store_true', help='Disable auto-reload')
    launch_parser.add_argument('--config', help='Configuration file path')
    
    # Status command
    subparsers.add_parser('status', help='Show portal status')
    
    # Test command
    subparsers.add_parser('test', help='Test portal integration')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Create launcher
        config_path = args.config if hasattr(args, 'config') and args.config else None
        launcher = PortalLauncher(config_path)
        
        if args.command == 'launch':
            # Determine reload setting
            reload = None
            if args.reload:
                reload = True
            elif args.no_reload:
                reload = False
            
            launcher.launch_portal(
                backend_type=args.backend,
                host=args.host,
                port=args.port,
                reload=reload
            )
            
        elif args.command == 'status':
            launcher.show_status()
            
        elif args.command == 'test':
            launcher.test_integration()
            
    except KeyboardInterrupt:
        logger.info("Portal launch interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
