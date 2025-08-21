"""
Automation Orchestrator for Agent_Cellphone_V2_Repository
Coordinates web automation, website generation, and testing operations
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .web_automation_engine import WebAutomationEngine, AutomationConfig
from .website_generator import WebsiteGenerator, WebsiteConfig, PageConfig, ComponentConfig
from .automation_test_suite import AutomationTestSuite

@dataclass
class OrchestrationConfig:
    """Configuration for automation orchestration"""
    max_concurrent_automations: int = 3
    automation_timeout: int = 300  # 5 minutes
    screenshot_interval: int = 30   # Take screenshots every 30 seconds
    log_level: str = "INFO"
    enable_monitoring: bool = True
    save_artifacts: bool = True
    artifacts_dir: str = "automation_artifacts"

class AutomationOrchestrator:
    """Main automation orchestrator coordinating all automation operations"""
    
    def __init__(self, config: Optional[OrchestrationConfig] = None):
        self.config = config or OrchestrationConfig()
        self.logger = self._setup_logging()
        
        # Initialize components
        self.automation_engine = None
        self.website_generator = None
        self.test_suite = None
        
        # State management
        self.active_automations = {}
        self.automation_history = []
        self.artifacts_dir = Path(self.config.artifacts_dir)
        self.artifacts_dir.mkdir(exist_ok=True)
        
        self.logger.info(f"Automation Orchestrator initialized with config: {self.config}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("AutomationOrchestrator")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def initialize_components(self):
        """Initialize all automation components"""
        try:
            self.logger.info("Initializing automation components...")
            
            # Initialize automation engine
            engine_config = AutomationConfig(
                headless=True,
                timeout=30,
                screenshot_dir=str(self.artifacts_dir / "screenshots")
            )
            self.automation_engine = WebAutomationEngine(engine_config)
            
            # Initialize website generator
            self.website_generator = WebsiteGenerator()
            
            # Initialize test suite
            self.test_suite = AutomationTestSuite()
            
            self.logger.info("All components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    async def run_automation_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a complete automation pipeline"""
        pipeline_id = f"pipeline_{int(time.time())}"
        
        try:
            self.logger.info(f"Starting automation pipeline: {pipeline_id}")
            
            # Initialize components if not already done
            if not self.automation_engine:
                self.initialize_components()
            
            # Execute pipeline steps
            results = {
                'pipeline_id': pipeline_id,
                'start_time': time.time(),
                'steps': [],
                'status': 'running'
            }
            
            # Step 1: Website Generation
            if 'website_generation' in pipeline_config:
                website_result = await self._generate_website_step(
                    pipeline_config['website_generation']
                )
                results['steps'].append(website_result)
            
            # Step 2: Web Automation
            if 'web_automation' in pipeline_config:
                automation_result = await self._run_automation_step(
                    pipeline_config['web_automation']
                )
                results['steps'].append(automation_result)
            
            # Step 3: Testing
            if 'testing' in pipeline_config:
                testing_result = await self._run_testing_step(
                    pipeline_config['testing']
                )
                results['steps'].append(testing_result)
            
            # Step 4: Validation
            validation_result = await self._run_validation_step(results['steps'])
            results['steps'].append(validation_result)
            
            # Finalize results
            results['end_time'] = time.time()
            results['duration'] = results['end_time'] - results['start_time']
            results['status'] = 'completed'
            
            # Save artifacts
            if self.config.save_artifacts:
                self._save_pipeline_artifacts(pipeline_id, results)
            
            self.logger.info(f"Pipeline {pipeline_id} completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline {pipeline_id} failed: {e}")
            results['status'] = 'failed'
            results['error'] = str(e)
            results['end_time'] = time.time()
            results['duration'] = results['end_time'] - results['start_time']
            return results
    
    async def _generate_website_step(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute website generation step"""
        step_id = f"website_gen_{int(time.time())}"
        
        try:
            self.logger.info(f"Starting website generation step: {step_id}")
            
            # Create website configuration
            website_config = WebsiteConfig(
                name=config.get('name', 'generated_website'),
                title=config.get('title', 'Generated Website'),
                description=config.get('description', 'Automatically generated website'),
                author=config.get('author', 'Automation Orchestrator'),
                theme=config.get('theme', 'default')
            )
            
            # Generate pages
            pages = []
            for page_config in config.get('pages', []):
                page = PageConfig(
                    name=page_config['name'],
                    title=page_config['title'],
                    template=page_config.get('template', 'base/responsive_base.html'),
                    route=page_config['route'],
                    content=page_config.get('content', {})
                )
                pages.append(page)
            
            # Generate website
            website_path = self.website_generator.generate_website(website_config, pages)
            
            result = {
                'step_id': step_id,
                'step_type': 'website_generation',
                'status': 'completed',
                'website_path': str(website_path),
                'config': asdict(website_config),
                'pages_count': len(pages)
            }
            
            self.logger.info(f"Website generation step {step_id} completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Website generation step {step_id} failed: {e}")
            return {
                'step_id': step_id,
                'step_type': 'website_generation',
                'status': 'failed',
                'error': str(e)
            }
    
    async def _run_automation_step(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute web automation step"""
        step_id = f"automation_{int(time.time())}"
        
        try:
            self.logger.info(f"Starting automation step: {step_id}")
            
            # Create automation configuration
            automation_config = AutomationConfig(
                headless=config.get('headless', True),
                timeout=config.get('timeout', 30),
                browser_type=config.get('browser_type', 'chrome')
            )
            
            # Execute automation tasks
            tasks = config.get('tasks', [])
            results = []
            
            for task in tasks:
                task_result = await self._execute_automation_task(task, automation_config)
                results.append(task_result)
            
            result = {
                'step_id': step_id,
                'step_type': 'web_automation',
                'status': 'completed',
                'tasks_count': len(tasks),
                'task_results': results
            }
            
            self.logger.info(f"Automation step {step_id} completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Automation step {step_id} failed: {e}")
            return {
                'step_id': step_id,
                'step_type': 'web_automation',
                'status': 'failed',
                'error': str(e)
            }
    
    async def _execute_automation_task(self, task: Dict[str, Any], 
                                     config: AutomationConfig) -> Dict[str, Any]:
        """Execute a single automation task"""
        task_id = f"task_{int(time.time())}"
        
        try:
            task_type = task.get('type', 'navigation')
            
            if task_type == 'navigation':
                result = await self._execute_navigation_task(task, config)
            elif task_type == 'interaction':
                result = await self._execute_interaction_task(task, config)
            elif task_type == 'screenshot':
                result = await self._execute_screenshot_task(task, config)
            else:
                result = {'status': 'skipped', 'reason': f'Unknown task type: {task_type}'}
            
            result['task_id'] = task_id
            result['task_type'] = task_type
            return result
            
        except Exception as e:
            return {
                'task_id': task_id,
                'status': 'failed',
                'error': str(e)
            }
    
    async def _execute_navigation_task(self, task: Dict[str, Any], 
                                     config: AutomationConfig) -> Dict[str, Any]:
        """Execute navigation automation task"""
        url = task.get('url')
        if not url:
            return {'status': 'failed', 'error': 'No URL specified'}
        
        try:
            # Use ThreadPoolExecutor for synchronous operations
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self._run_navigation_sync, url, config
                )
                result = await asyncio.wrap_future(future)
                return result
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def _run_navigation_sync(self, url: str, config: AutomationConfig) -> Dict[str, Any]:
        """Run navigation synchronously (for ThreadPoolExecutor)"""
        try:
            with WebAutomationEngine(config) as engine:
                success = engine.navigate_to(url)
                if success:
                    title = engine.get_page_title()
                    return {
                        'status': 'completed',
                        'url': url,
                        'title': title,
                        'success': True
                    }
                else:
                    return {
                        'status': 'failed',
                        'url': url,
                        'error': 'Navigation failed'
                    }
        except Exception as e:
            return {
                'status': 'failed',
                'url': url,
                'error': str(e)
            }
    
    async def _execute_interaction_task(self, task: Dict[str, Any], 
                                      config: AutomationConfig) -> Dict[str, Any]:
        """Execute interaction automation task"""
        action = task.get('action')
        selector = task.get('selector')
        
        if not action or not selector:
            return {'status': 'failed', 'error': 'Missing action or selector'}
        
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self._run_interaction_sync, action, selector, task, config
                )
                result = await asyncio.wrap_future(future)
                return result
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def _run_interaction_sync(self, action: str, selector: str, 
                            task: Dict[str, Any], config: AutomationConfig) -> Dict[str, Any]:
        """Run interaction synchronously"""
        try:
            with WebAutomationEngine(config) as engine:
                if action == 'click':
                    success = engine.click_element(selector)
                elif action == 'input':
                    text = task.get('text', '')
                    success = engine.input_text(selector, text)
                elif action == 'wait':
                    timeout = task.get('timeout', 10)
                    success = engine.wait_for_element(selector, timeout=timeout)
                else:
                    return {'status': 'failed', 'error': f'Unknown action: {action}'}
                
                return {
                    'status': 'completed',
                    'action': action,
                    'selector': selector,
                    'success': success
                }
        except Exception as e:
            return {
                'status': 'failed',
                'action': action,
                'selector': selector,
                'error': str(e)
            }
    
    async def _execute_screenshot_task(self, task: Dict[str, Any], 
                                     config: AutomationConfig) -> Dict[str, Any]:
        """Execute screenshot automation task"""
        filename = task.get('filename', f'screenshot_{int(time.time())}')
        
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self._run_screenshot_sync, filename, config
                )
                result = await asyncio.wrap_future(future)
                return result
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def _run_screenshot_sync(self, filename: str, config: AutomationConfig) -> Dict[str, Any]:
        """Run screenshot synchronously"""
        try:
            with WebAutomationEngine(config) as engine:
                screenshot_path = engine.take_screenshot(filename)
                if screenshot_path:
                    return {
                        'status': 'completed',
                        'filename': filename,
                        'screenshot_path': screenshot_path,
                        'success': True
                    }
                else:
                    return {
                        'status': 'failed',
                        'filename': filename,
                        'error': 'Screenshot failed'
                    }
        except Exception as e:
            return {
                'status': 'failed',
                'filename': filename,
                'error': str(e)
            }
    
    async def _run_testing_step(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute testing step"""
        step_id = f"testing_{int(time.time())}"
        
        try:
            self.logger.info(f"Starting testing step: {step_id}")
            
            # Run automation tests
            test_results = self.test_suite.run_automation_tests()
            
            result = {
                'step_id': step_id,
                'step_type': 'testing',
                'status': 'completed',
                'test_results': test_results
            }
            
            self.logger.info(f"Testing step {step_id} completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Testing step {step_id} failed: {e}")
            return {
                'step_id': step_id,
                'step_type': 'testing',
                'status': 'failed',
                'error': str(e)
            }
    
    async def _run_validation_step(self, previous_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute validation step"""
        step_id = f"validation_{int(time.time())}"
        
        try:
            self.logger.info(f"Starting validation step: {step_id}")
            
            # Validate previous steps
            validation_results = []
            overall_success = True
            
            for step in previous_steps:
                if step.get('status') == 'failed':
                    overall_success = False
                    validation_results.append({
                        'step_id': step.get('step_id'),
                        'status': 'failed',
                        'error': step.get('error', 'Unknown error')
                    })
                else:
                    validation_results.append({
                        'step_id': step.get('step_id'),
                        'status': 'passed'
                    })
            
            result = {
                'step_id': step_id,
                'step_type': 'validation',
                'status': 'completed' if overall_success else 'failed',
                'overall_success': overall_success,
                'validation_results': validation_results
            }
            
            self.logger.info(f"Validation step {step_id} completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Validation step {step_id} failed: {e}")
            return {
                'step_id': step_id,
                'step_type': 'validation',
                'status': 'failed',
                'error': str(e)
            }
    
    def _save_pipeline_artifacts(self, pipeline_id: str, results: Dict[str, Any]):
        """Save pipeline artifacts for later analysis"""
        try:
            artifacts_file = self.artifacts_dir / f"{pipeline_id}_results.json"
            
            # Convert results to serializable format
            serializable_results = self._make_serializable(results)
            
            import json
            with open(artifacts_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Pipeline artifacts saved to {artifacts_file}")
            
        except Exception as e:
            self.logger.warning(f"Failed to save pipeline artifacts: {e}")
    
    def _make_serializable(self, obj: Any) -> Any:
        """Convert object to JSON serializable format"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, Path):
            return str(obj)
        elif hasattr(obj, '__dict__'):
            return self._make_serializable(obj.__dict__)
        else:
            return obj
    
    def get_pipeline_status(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific pipeline"""
        # Check active automations
        if pipeline_id in self.active_automations:
            return self.active_automations[pipeline_id]
        
        # Check artifacts for completed pipelines
        artifacts_file = self.artifacts_dir / f"{pipeline_id}_results.json"
        if artifacts_file.exists():
            try:
                import json
                with open(artifacts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load pipeline artifacts: {e}")
        
        return None
    
    def list_pipelines(self) -> List[Dict[str, Any]]:
        """List all pipelines (active and completed)"""
        pipelines = []
        
        # Add active pipelines
        for pipeline_id, status in self.active_automations.items():
            pipelines.append({
                'pipeline_id': pipeline_id,
                'status': 'active',
                'current_step': status.get('current_step', 'unknown')
            })
        
        # Add completed pipelines from artifacts
        for artifacts_file in self.artifacts_dir.glob("*_results.json"):
            try:
                pipeline_id = artifacts_file.stem.replace('_results', '')
                import json
                with open(artifacts_file, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                
                pipelines.append({
                    'pipeline_id': pipeline_id,
                    'status': results.get('status', 'unknown'),
                    'duration': results.get('duration', 0),
                    'completed_at': results.get('end_time', 0)
                })
            except Exception as e:
                self.logger.warning(f"Failed to load pipeline {artifacts_file}: {e}")
        
        return sorted(pipelines, key=lambda x: x.get('completed_at', 0), reverse=True)
    
    def cleanup_artifacts(self, older_than_days: int = 7):
        """Clean up old pipeline artifacts"""
        try:
            cutoff_time = time.time() - (older_than_days * 24 * 60 * 60)
            
            for artifacts_file in self.artifacts_dir.glob("*_results.json"):
                if artifacts_file.stat().st_mtime < cutoff_time:
                    artifacts_file.unlink()
                    self.logger.info(f"Cleaned up old artifact: {artifacts_file}")
            
        except Exception as e:
            self.logger.warning(f"Failed to cleanup artifacts: {e}")

# Convenience functions
def create_automation_orchestrator(config: Optional[OrchestrationConfig] = None) -> AutomationOrchestrator:
    """Create a new automation orchestrator instance"""
    return AutomationOrchestrator(config)

async def run_automation_pipeline(pipeline_config: Dict[str, Any], 
                                orchestrator: Optional[AutomationOrchestrator] = None) -> Dict[str, Any]:
    """Run an automation pipeline with the specified configuration"""
    if not orchestrator:
        orchestrator = create_automation_orchestrator()
    
    return await orchestrator.run_automation_pipeline(pipeline_config)

# Example pipeline configurations
EXAMPLE_PIPELINES = {
    'basic_website': {
        'website_generation': {
            'name': 'example_site',
            'title': 'Example Website',
            'description': 'A basic example website',
            'pages': [
                {
                    'name': 'home',
                    'title': 'Home',
                    'route': '/',
                    'content': {'heading': 'Welcome', 'description': 'Welcome to our site'}
                }
            ]
        },
        'testing': {}
    },
    
    'automation_demo': {
        'web_automation': {
            'headless': True,
            'browser_type': 'chrome',
            'tasks': [
                {
                    'type': 'navigation',
                    'url': 'https://example.com'
                },
                {
                    'type': 'screenshot',
                    'filename': 'example_site'
                }
            ]
        },
        'testing': {}
    }
}
