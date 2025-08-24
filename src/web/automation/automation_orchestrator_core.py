import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .automation_orchestrator_config import OrchestrationConfig
from .automation_orchestrator_executor import AutomationExecutorMixin
from .automation_orchestrator_monitor import AutomationMonitorMixin
from .web_automation_engine import WebAutomationEngine, AutomationConfig
from .website_generator import WebsiteGenerator
from .automation_test_suite import AutomationTestSuite


class AutomationOrchestrator(AutomationExecutorMixin, AutomationMonitorMixin):
    """Main automation orchestrator coordinating automation operations."""

    def __init__(self, config: Optional[OrchestrationConfig] = None):
        self.config = config or OrchestrationConfig()
        self.logger = self._setup_logging()
        self.automation_engine = None
        self.website_generator = None
        self.test_suite = None
        self.active_automations: Dict[str, Dict[str, Any]] = {}
        self.automation_history: List[Dict[str, Any]] = []
        self.artifacts_dir = Path(self.config.artifacts_dir)
        self.artifacts_dir.mkdir(exist_ok=True)
        self.logger.info(
            f"Automation Orchestrator initialized with config: {self.config}"
        )

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger("AutomationOrchestrator")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def initialize_components(self):
        """Initialize all automation components."""
        try:
            self.logger.info("Initializing automation components...")
            engine_config = AutomationConfig(
                headless=True,
                timeout=30,
                screenshot_dir=str(self.artifacts_dir / "screenshots"),
            )
            self.automation_engine = WebAutomationEngine(engine_config)
            self.website_generator = WebsiteGenerator()
            self.test_suite = AutomationTestSuite()
            self.logger.info("All components initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise

    async def run_automation_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a complete automation pipeline."""
        pipeline_id = f"pipeline_{int(time.time())}"
        try:
            self.logger.info(f"Starting automation pipeline: {pipeline_id}")
            if not self.automation_engine:
                self.initialize_components()
            results = {
                "pipeline_id": pipeline_id,
                "start_time": time.time(),
                "steps": [],
                "status": "running",
            }
            if "website_generation" in pipeline_config:
                website_result = await self._generate_website_step(
                    pipeline_config["website_generation"]
                )
                results["steps"].append(website_result)
            if "web_automation" in pipeline_config:
                automation_result = await self._run_automation_step(
                    pipeline_config["web_automation"]
                )
                results["steps"].append(automation_result)
            if "testing" in pipeline_config:
                testing_result = await self._run_testing_step(pipeline_config["testing"])
                results["steps"].append(testing_result)
            validation_result = await self._run_validation_step(results["steps"])
            results["steps"].append(validation_result)
            results["end_time"] = time.time()
            results["duration"] = results["end_time"] - results["start_time"]
            results["status"] = "completed"
            if self.config.save_artifacts:
                self._save_pipeline_artifacts(pipeline_id, results)
            self.logger.info(f"Pipeline {pipeline_id} completed successfully")
            return results
        except Exception as e:
            self.logger.error(f"Pipeline {pipeline_id} failed: {e}")
            results["status"] = "failed"
            results["error"] = str(e)
            results["end_time"] = time.time()
            results["duration"] = results["end_time"] - results["start_time"]
            return results


def create_automation_orchestrator(
    config: Optional[OrchestrationConfig] = None,
) -> AutomationOrchestrator:
    """Create a new automation orchestrator instance."""
    return AutomationOrchestrator(config)


async def run_automation_pipeline(
    pipeline_config: Dict[str, Any],
    orchestrator: Optional[AutomationOrchestrator] = None,
) -> Dict[str, Any]:
    """Run an automation pipeline with the specified configuration."""
    if not orchestrator:
        orchestrator = create_automation_orchestrator()
    return await orchestrator.run_automation_pipeline(pipeline_config)
