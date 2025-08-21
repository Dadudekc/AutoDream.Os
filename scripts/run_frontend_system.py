#!/usr/bin/env python3
"""
Frontend System Launcher
Agent_Cellphone_V2_Repository TDD Integration Project

This script provides a unified interface for running the frontend system:
- Launch Flask frontend application
- Launch FastAPI frontend application
- Run frontend tests
- Component development tools
- Routing configuration tools

Author: Web Development & UI Framework Specialist
License: MIT
"""

import os
import sys
import json
import argparse
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

# Add src directory to Python path
repo_root = Path(__file__).parent.parent
src_dir = repo_root / "src"
sys.path.insert(0, str(src_dir))

# Import frontend modules
try:
    from web.frontend import (
        create_flask_frontend,
        create_fastapi_frontend,
        create_frontend_router,
        run_frontend_tests,
        FrontendAppFactory,
        FrontendRouter
    )
    FRONTEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Frontend modules not available: {e}")
    print("Please ensure the frontend package is properly installed.")
    FRONTEND_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FrontendSystemLauncher:
    """Main launcher for the frontend system"""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.config_path = self.repo_root / "config" / "web_development_config.yaml"
        self.config = self._load_config()
        
        if FRONTEND_AVAILABLE:
            self.flask_app = None
            self.fastapi_app = None
            self.router = None
            logger.info("Frontend system launcher initialized")
        else:
            logger.warning("Frontend system launcher initialized with limited functionality")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration file"""
        try:
            if self.config_path.exists():
                import yaml
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'flask': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': True
            },
            'fastapi': {
                'host': '0.0.0.0',
                'port': 8000,
                'reload': True
            },
            'frontend': {
                'theme': 'light',
                'language': 'en',
                'debug': True
            }
        }
    
    def launch_flask_frontend(self, host: str = None, port: int = None, debug: bool = None):
        """Launch Flask frontend application"""
        if not FRONTEND_AVAILABLE:
            print("❌ Frontend modules not available")
            return False
        
        try:
            # Get configuration
            config = self.config.get('flask', {})
            host = host or config.get('host', '0.0.0.0')
            port = port or config.get('port', 5000)
            debug = debug if debug is not None else config.get('debug', True)
            
            print(f"🚀 Launching Flask Frontend Application...")
            print(f"   Host: {host}")
            print(f"   Port: {port}")
            print(f"   Debug: {debug}")
            print(f"   URL: http://{host}:{port}")
            
            # Create and launch Flask app
            self.flask_app = create_flask_frontend({
                'debug': debug,
                'secret_key': 'frontend-secret-key'
            })
            
            print("✅ Flask Frontend Application launched successfully!")
            print("   Press Ctrl+C to stop")
            
            # Run the application
            self.flask_app.run(host=host, port=port, debug=debug)
            
            return True
            
        except Exception as e:
            logger.error(f"Error launching Flask frontend: {e}")
            print(f"❌ Failed to launch Flask frontend: {e}")
            return False
    
    def launch_fastapi_frontend(self, host: str = None, port: int = None, reload: bool = None):
        """Launch FastAPI frontend application"""
        if not FRONTEND_AVAILABLE:
            print("❌ Frontend modules not available")
            return False
        
        try:
            # Get configuration
            config = self.config.get('fastapi', {})
            host = host or config.get('host', '0.0.0.0')
            port = port or config.get('port', 8000)
            reload = reload if reload is not None else config.get('reload', True)
            
            print(f"🚀 Launching FastAPI Frontend Application...")
            print(f"   Host: {host}")
            print(f"   Port: {port}")
            print(f"   Reload: {reload}")
            print(f"   URL: http://{host}:{port}")
            print(f"   API Docs: http://{host}:{port}/docs")
            
            # Create FastAPI app
            self.fastapi_app = create_fastapi_frontend({
                'title': 'Agent_Cellphone_V2 Frontend API',
                'description': 'Modern Frontend API with WebSocket Support',
                'version': '2.0.0'
            })
            
            print("✅ FastAPI Frontend Application created successfully!")
            print("   Starting server...")
            
            # Import uvicorn for running FastAPI
            try:
                import uvicorn
                uvicorn.run(
                    "scripts.run_frontend_system:FrontendSystemLauncher().fastapi_app.app",
                    host=host,
                    port=port,
                    reload=reload
                )
            except ImportError:
                print("❌ uvicorn not available. Please install with: pip install uvicorn[standard]")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error launching FastAPI frontend: {e}")
            print(f"❌ Failed to launch FastAPI frontend: {e}")
            return False
    
    def run_frontend_tests(self, test_type: str = None):
        """Run frontend tests"""
        if not FRONTEND_AVAILABLE:
            print("❌ Frontend modules not available")
            return False
        
        try:
            print("🧪 Running Frontend Tests...")
            
            if test_type:
                print(f"   Test Type: {test_type}")
            
            # Run tests
            results = run_frontend_tests()
            
            print("✅ Frontend Tests Completed!")
            print("\n📊 Test Results Summary:")
            
            for suite_name, suite in results.items():
                print(f"   {suite_name.upper()}: {suite.passed_tests}/{suite.total_tests} passed")
                print(f"   Duration: {suite.total_duration:.2f}s")
            
            return True
            
        except Exception as e:
            logger.error(f"Error running frontend tests: {e}")
            print(f"❌ Failed to run frontend tests: {e}")
            return False
    
    def show_component_info(self):
        """Show information about available components"""
        if not FRONTEND_AVAILABLE:
            print("❌ Frontend modules not available")
            return False
        
        try:
            print("🔧 Frontend Component Information")
            print("=" * 50)
            
            # Create a sample app to get component info
            flask_app = create_flask_frontend()
            
            # Show registered components
            registry = flask_app.component_registry
            components = registry.list_components()
            
            print(f"📦 Registered Components: {len(components)}")
            for component in components:
                print(f"   • {component}")
            
            # Show templates
            templates = list(registry.templates.keys())
            print(f"\n📝 Available Templates: {len(templates)}")
            for template in templates:
                print(f"   • {template}")
            
            # Show styles
            styles = list(registry.styles.keys())
            print(f"\n🎨 Available Styles: {len(styles)}")
            for style in styles:
                print(f"   • {style}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error showing component info: {e}")
            print(f"❌ Failed to show component info: {e}")
            return False
    
    def show_routing_info(self):
        """Show information about routing configuration"""
        if not FRONTEND_AVAILABLE:
            print("❌ Frontend modules not available")
            return False
        
        try:
            print("🗺️  Frontend Routing Information")
            print("=" * 50)
            
            # Create router with default routes
            router = create_frontend_router()
            
            print(f"🛣️  Configured Routes: {len(router.routes)}")
            print("\nRoute Details:")
            
            for route in router.routes:
                print(f"   📍 {route.path}")
                print(f"      Component: {route.component}")
                print(f"      Name: {route.name}")
                print(f"      Guards: {', '.join(route.guards) if route.guards else 'None'}")
                print(f"      Children: {len(route.children)}")
                print()
            
            # Show current navigation state
            nav_state = router.get_navigation_state()
            print(f"📍 Current Route: {nav_state.current_route}")
            print(f"📚 Navigation History: {len(nav_state.navigation_history)} routes")
            
            return True
            
        except Exception as e:
            logger.error(f"Error showing routing info: {e}")
            print(f"❌ Failed to show routing info: {e}")
            return False
    
    def create_component(self, component_name: str, component_type: str = "basic"):
        """Create a new component"""
        if not FRONTEND_AVAILABLE:
            print("❌ Frontend modules not available")
            return False
        
        try:
            print(f"🔧 Creating Component: {component_name}")
            print(f"   Type: {component_type}")
            
            # Create component
            component = create_component(component_name, {
                'type': component_type,
                'created_by': 'FrontendSystemLauncher'
            })
            
            print("✅ Component Created Successfully!")
            print(f"   ID: {component.id}")
            print(f"   Type: {component.type}")
            print(f"   Props: {component.props}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating component: {e}")
            print(f"❌ Failed to create component: {e}")
            return False
    
    def show_system_status(self):
        """Show overall system status"""
        print("📊 Frontend System Status")
        print("=" * 50)
        
        # Check frontend availability
        if FRONTEND_AVAILABLE:
            print("✅ Frontend modules: Available")
        else:
            print("❌ Frontend modules: Not available")
            return False
        
        # Check configuration
        if self.config:
            print("✅ Configuration: Loaded")
            print(f"   Flask: {self.config.get('flask', {}).get('port', 'N/A')}")
            print(f"   FastAPI: {self.config.get('fastapi', {}).get('port', 'N/A')}")
        else:
            print("❌ Configuration: Not loaded")
        
        # Check if apps are running
        if self.flask_app:
            print("✅ Flask App: Running")
        else:
            print("⏸️  Flask App: Not running")
        
        if self.fastapi_app:
            print("✅ FastAPI App: Running")
        else:
            print("⏸️  FastAPI App: Not running")
        
        return True
    
    def show_help(self):
        """Show help information"""
        print("🌐 Frontend System Launcher - Help")
        print("=" * 50)
        print("Available Commands:")
        print("  flask          - Launch Flask frontend application")
        print("  fastapi        - Launch FastAPI frontend application")
        print("  test           - Run frontend tests")
        print("  components     - Show component information")
        print("  routes         - Show routing information")
        print("  create         - Create a new component")
        print("  status         - Show system status")
        print("  help           - Show this help message")
        print("\nExamples:")
        print("  python scripts/run_frontend_system.py flask")
        print("  python scripts/run_frontend_system.py fastapi --port 8001")
        print("  python scripts/run_frontend_system.py test")
        print("  python scripts/run_frontend_system.py components")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Frontend System Launcher")
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('--host', help='Host to bind to')
    parser.add_argument('--port', type=int, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload (FastAPI)')
    parser.add_argument('--component-name', help='Component name for create command')
    parser.add_argument('--component-type', default='basic', help='Component type for create command')
    
    args = parser.parse_args()
    
    # Create launcher
    launcher = FrontendSystemLauncher()
    
    # Execute command
    if not args.command:
        launcher.show_help()
        return
    
    command = args.command.lower()
    
    try:
        if command == 'flask':
            launcher.launch_flask_frontend(
                host=args.host,
                port=args.port,
                debug=args.debug
            )
        elif command == 'fastapi':
            launcher.launch_fastapi_frontend(
                host=args.host,
                port=args.port,
                reload=args.reload
            )
        elif command == 'test':
            launcher.run_frontend_tests()
        elif command == 'components':
            launcher.show_component_info()
        elif command == 'routes':
            launcher.show_routing_info()
        elif command == 'create':
            if not args.component_name:
                print("❌ Component name is required. Use --component-name")
                return
            launcher.create_component(args.component_name, args.component_type)
        elif command == 'status':
            launcher.show_system_status()
        elif command == 'help':
            launcher.show_help()
        else:
            print(f"❌ Unknown command: {command}")
            launcher.show_help()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
