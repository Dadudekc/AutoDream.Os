#!/usr/bin/env python3
"""
Web Automation Launcher for Agent_Cellphone_V2_Repository
Command-line interface for running automation pipelines, website generation, and testing
"""

import asyncio
import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from web.automation.automation_orchestrator import (
    AutomationOrchestrator, 
    OrchestrationConfig,
    run_automation_pipeline,
    EXAMPLE_PIPELINES
)
from web.automation.website_generator import (
    WebsiteGenerator, 
    WebsiteConfig, 
    PageConfig, 
    ComponentConfig
)
from web.automation.web_automation_engine import WebAutomationEngine, AutomationConfig
from web.automation.automation_test_suite import AutomationTestSuite

class WebAutomationLauncher:
    """Main launcher for web automation operations"""
    
    def __init__(self):
        self.orchestrator = None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup basic logging"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    async def run_automation_pipeline(self, pipeline_name: str, config: Dict[str, Any] = None):
        """Run a predefined automation pipeline"""
        try:
            print(f"🚀 Starting automation pipeline: {pipeline_name}")
            
            # Get pipeline configuration
            if pipeline_name in EXAMPLE_PIPELINES:
                pipeline_config = EXAMPLE_PIPELINES[pipeline_name]
                if config:
                    pipeline_config.update(config)
            else:
                print(f"❌ Unknown pipeline: {pipeline_name}")
                print(f"Available pipelines: {list(EXAMPLE_PIPELINES.keys())}")
                return None
            
            # Run the pipeline
            results = await run_automation_pipeline(pipeline_config)
            
            # Display results
            self._display_pipeline_results(results)
            
            return results
            
        except Exception as e:
            print(f"❌ Pipeline execution failed: {e}")
            return None
    
    async def generate_website(self, name: str, title: str, description: str, 
                             author: str = "Website Generator", theme: str = "default"):
        """Generate a basic website"""
        try:
            print(f"🌐 Generating website: {name}")
            
            generator = WebsiteGenerator()
            website_path = generator.create_basic_website(name, title, description)
            
            print(f"✅ Website generated successfully at: {website_path}")
            print(f"📁 Open {website_path}/pages/home/index.html in your browser")
            
            return website_path
            
        except Exception as e:
            print(f"❌ Website generation failed: {e}")
            return None
    
    async def run_automation_tests(self):
        """Run the automation test suite"""
        try:
            print("🧪 Running automation test suite...")
            
            test_suite = AutomationTestSuite()
            results = test_suite.run_automation_tests()
            
            self._display_test_results(results)
            
            return results
            
        except Exception as e:
            print(f"❌ Test suite execution failed: {e}")
            return None
    
    async def run_web_automation(self, url: str, headless: bool = True, 
                                browser_type: str = "chrome", take_screenshot: bool = False):
        """Run basic web automation"""
        try:
            print(f"🤖 Running web automation for: {url}")
            
            config = AutomationConfig(
                headless=headless,
                browser_type=browser_type,
                timeout=30
            )
            
            with WebAutomationEngine(config) as engine:
                # Navigate to URL
                success = engine.navigate_to(url)
                if not success:
                    print(f"❌ Failed to navigate to {url}")
                    return False
                
                # Get page information
                title = engine.get_page_title()
                print(f"📄 Page title: {title}")
                
                # Take screenshot if requested
                if take_screenshot:
                    screenshot_path = engine.take_screenshot(f"automation_{int(time.time())}")
                    if screenshot_path:
                        print(f"📸 Screenshot saved to: {screenshot_path}")
                
                print(f"✅ Web automation completed successfully")
                return True
                
        except Exception as e:
            print(f"❌ Web automation failed: {e}")
            return False
    
    def _display_pipeline_results(self, results: Dict[str, Any]):
        """Display pipeline execution results"""
        print("\n" + "="*60)
        print("PIPELINE EXECUTION RESULTS")
        print("="*60)
        
        print(f"Pipeline ID: {results.get('pipeline_id', 'N/A')}")
        print(f"Status: {results.get('status', 'N/A')}")
        print(f"Duration: {results.get('duration', 0):.2f} seconds")
        
        if results.get('error'):
            print(f"❌ Error: {results['error']}")
            return
        
        print(f"\nSteps executed: {len(results.get('steps', []))}")
        
        for i, step in enumerate(results.get('steps', []), 1):
            status_icon = "✅" if step.get('status') == 'completed' else "❌"
            print(f"{status_icon} Step {i}: {step.get('step_type', 'unknown')} - {step.get('status', 'unknown')}")
            
            if step.get('error'):
                print(f"   Error: {step['error']}")
    
    def _display_test_results(self, results: Dict[str, Any]):
        """Display test execution results"""
        print("\n" + "="*60)
        print("AUTOMATION TEST SUITE RESULTS")
        print("="*60)
        
        print(f"Total Tests: {results.get('total_tests', 0)}")
        print(f"Passed: {results.get('passed', 0)}")
        print(f"Failed: {results.get('failed', 0)}")
        print(f"Skipped: {results.get('skipped', 0)}")
        print(f"Duration: {results.get('duration', 0):.2f} seconds")
        
        if results.get('test_details'):
            print(f"\nTest Details:")
            for test in results['test_details']:
                status_icon = "✅" if test.get('status') == 'passed' else "❌" if test.get('status') == 'failed' else "⏭️"
                print(f"{status_icon} {test.get('test_name', 'Unknown')}: {test.get('message', 'No message')}")
        
        if results.get('error'):
            print(f"\n❌ Test Suite Error: {results['error']}")
    
    def show_help(self):
        """Show detailed help information"""
        help_text = """
🌐 Web Automation Launcher - Agent_Cellphone_V2_Repository

USAGE EXAMPLES:

1. Generate a basic website:
   python scripts/run_web_automation.py website --name "my_site" --title "My Website" --description "A personal website"

2. Run automation pipeline:
   python scripts/run_web_automation.py pipeline --name "basic_website"

3. Run web automation:
   python scripts/run_web_automation.py automate --url "https://example.com" --screenshot

4. Run automation tests:
   python scripts/run_web_automation.py test

5. Show available pipelines:
   python scripts/run_web_automation.py pipelines

AVAILABLE PIPELINES:
   - basic_website: Generate a basic website with home, about, and contact pages
   - automation_demo: Demonstrate web automation with navigation and screenshots

AVAILABLE COMMANDS:
   website     - Generate a new website
   pipeline    - Run an automation pipeline
   automate    - Run basic web automation
   test        - Run automation test suite
   pipelines   - List available pipelines
   help        - Show this help message

For more information, see the documentation in docs/WEB_AUTOMATION_README.md
"""
        print(help_text)
    
    def list_pipelines(self):
        """List available automation pipelines"""
        print("\n📋 Available Automation Pipelines:")
        print("="*40)
        
        for pipeline_name, pipeline_config in EXAMPLE_PIPELINES.items():
            print(f"\n🔹 {pipeline_name}")
            
            if 'website_generation' in pipeline_config:
                web_config = pipeline_config['website_generation']
                print(f"   📝 Website: {web_config.get('title', 'N/A')}")
                print(f"   📄 Pages: {len(web_config.get('pages', []))}")
            
            if 'web_automation' in pipeline_config:
                auto_config = pipeline_config['web_automation']
                print(f"   🤖 Automation: {len(auto_config.get('tasks', []))} tasks")
                print(f"   🌐 Browser: {auto_config.get('browser_type', 'chrome')}")
            
            if 'testing' in pipeline_config:
                print(f"   🧪 Testing: Enabled")

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Web Automation Launcher for Agent_Cellphone_V2_Repository",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Website generation command
    website_parser = subparsers.add_parser('website', help='Generate a new website')
    website_parser.add_argument('--name', required=True, help='Website name')
    website_parser.add_argument('--title', required=True, help='Website title')
    website_parser.add_argument('--description', required=True, help='Website description')
    website_parser.add_argument('--author', default='Website Generator', help='Website author')
    website_parser.add_argument('--theme', default='default', help='Website theme')
    
    # Pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Run an automation pipeline')
    pipeline_parser.add_argument('--name', required=True, help='Pipeline name')
    pipeline_parser.add_argument('--config', help='Additional configuration JSON file')
    
    # Automation command
    automate_parser = subparsers.add_parser('automate', help='Run basic web automation')
    automate_parser.add_argument('--url', required=True, help='URL to automate')
    automate_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    automate_parser.add_argument('--browser', default='chrome', help='Browser type')
    automate_parser.add_argument('--screenshot', action='store_true', help='Take screenshot')
    
    # Test command
    subparsers.add_parser('test', help='Run automation test suite')
    
    # Pipelines command
    subparsers.add_parser('pipelines', help='List available pipelines')
    
    # Help command
    subparsers.add_parser('help', help='Show detailed help')
    
    args = parser.parse_args()
    
    if not args.command or args.command == 'help':
        launcher = WebAutomationLauncher()
        launcher.show_help()
        return
    
    launcher = WebAutomationLauncher()
    
    try:
        if args.command == 'website':
            await launcher.generate_website(
                name=args.name,
                title=args.title,
                description=args.description,
                author=args.author,
                theme=args.theme
            )
        
        elif args.command == 'pipeline':
            config = None
            if args.config:
                with open(args.config, 'r') as f:
                    config = json.load(f)
            
            await launcher.run_automation_pipeline(args.name, config)
        
        elif args.command == 'automate':
            await launcher.run_web_automation(
                url=args.url,
                headless=args.headless,
                browser_type=args.browser,
                take_screenshot=args.screenshot
            )
        
        elif args.command == 'test':
            await launcher.run_automation_tests()
        
        elif args.command == 'pipelines':
            launcher.list_pipelines()
        
        else:
            print(f"❌ Unknown command: {args.command}")
            launcher.show_help()
    
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
