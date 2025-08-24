import asyncio
import time
from dataclasses import asdict
from typing import Any, Dict
from concurrent.futures import ThreadPoolExecutor

from .web_automation_engine import WebAutomationEngine, AutomationConfig
from .website_generator import WebsiteConfig, PageConfig


class AutomationExecutorMixin:
    """Provides execution methods for automation orchestrator."""

    async def _generate_website_step(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute website generation step."""
        step_id = f"website_gen_{int(time.time())}"
        try:
            self.logger.info(f"Starting website generation step: {step_id}")
            website_config = WebsiteConfig(
                name=config.get("name", "generated_website"),
                title=config.get("title", "Generated Website"),
                description=config.get(
                    "description", "Automatically generated website"
                ),
                author=config.get("author", "Automation Orchestrator"),
                theme=config.get("theme", "default"),
            )
            pages = []
            for page_config in config.get("pages", []):
                page = PageConfig(
                    name=page_config["name"],
                    title=page_config["title"],
                    template=page_config.get("template", "base/responsive_base.html"),
                    route=page_config["route"],
                    content=page_config.get("content", {}),
                )
                pages.append(page)
            website_path = self.website_generator.generate_website(website_config, pages)
            result = {
                "step_id": step_id,
                "step_type": "website_generation",
                "status": "completed",
                "website_path": str(website_path),
                "config": asdict(website_config),
                "pages_count": len(pages),
            }
            self.logger.info(f"Website generation step {step_id} completed")
            return result
        except Exception as e:
            self.logger.error(f"Website generation step {step_id} failed: {e}")
            return {
                "step_id": step_id,
                "step_type": "website_generation",
                "status": "failed",
                "error": str(e),
            }

    async def _run_automation_step(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute web automation step."""
        step_id = f"automation_{int(time.time())}"
        try:
            self.logger.info(f"Starting automation step: {step_id}")
            automation_config = AutomationConfig(
                headless=config.get("headless", True),
                timeout=config.get("timeout", 30),
                browser_type=config.get("browser_type", "chrome"),
            )
            tasks = config.get("tasks", [])
            results = []
            for task in tasks:
                task_result = await self._execute_automation_task(task, automation_config)
                results.append(task_result)
            result = {
                "step_id": step_id,
                "step_type": "web_automation",
                "status": "completed",
                "tasks_count": len(tasks),
                "task_results": results,
            }
            self.logger.info(f"Automation step {step_id} completed")
            return result
        except Exception as e:
            self.logger.error(f"Automation step {step_id} failed: {e}")
            return {
                "step_id": step_id,
                "step_type": "web_automation",
                "status": "failed",
                "error": str(e),
            }

    async def _execute_automation_task(
        self, task: Dict[str, Any], config: AutomationConfig
    ) -> Dict[str, Any]:
        """Execute a single automation task."""
        task_id = f"task_{int(time.time())}"
        try:
            task_type = task.get("type", "navigation")
            if task_type == "navigation":
                result = await self._execute_navigation_task(task, config)
            elif task_type == "interaction":
                result = await self._execute_interaction_task(task, config)
            elif task_type == "screenshot":
                result = await self._execute_screenshot_task(task, config)
            else:
                result = {
                    "status": "skipped",
                    "reason": f"Unknown task type: {task_type}",
                }
            result["task_id"] = task_id
            result["task_type"] = task_type
            return result
        except Exception as e:
            return {"task_id": task_id, "status": "failed", "error": str(e)}

    async def _execute_navigation_task(
        self, task: Dict[str, Any], config: AutomationConfig
    ) -> Dict[str, Any]:
        """Execute navigation automation task."""
        url = task.get("url")
        if not url:
            return {"status": "failed", "error": "No URL specified"}
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._run_navigation_sync, url, config)
                result = await asyncio.wrap_future(future)
                return result
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def _run_navigation_sync(self, url: str, config: AutomationConfig) -> Dict[str, Any]:
        """Run navigation synchronously."""
        try:
            with WebAutomationEngine(config) as engine:
                success = engine.navigate_to(url)
                if success:
                    title = engine.get_page_title()
                    return {
                        "status": "completed",
                        "url": url,
                        "title": title,
                        "success": True,
                    }
                return {
                    "status": "failed",
                    "url": url,
                    "error": "Navigation failed",
                }
        except Exception as e:
            return {"status": "failed", "url": url, "error": str(e)}

    async def _execute_interaction_task(
        self, task: Dict[str, Any], config: AutomationConfig
    ) -> Dict[str, Any]:
        """Execute interaction automation task."""
        action = task.get("action")
        selector = task.get("selector")
        if not action or not selector:
            return {"status": "failed", "error": "Missing action or selector"}
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self._run_interaction_sync, action, selector, task, config
                )
                result = await asyncio.wrap_future(future)
                return result
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def _run_interaction_sync(
        self, action: str, selector: str, task: Dict[str, Any], config: AutomationConfig
    ) -> Dict[str, Any]:
        """Run interaction synchronously."""
        try:
            with WebAutomationEngine(config) as engine:
                if action == "click":
                    success = engine.click_element(selector)
                elif action == "input":
                    text = task.get("text", "")
                    success = engine.input_text(selector, text)
                elif action == "wait":
                    timeout = task.get("timeout", 10)
                    success = engine.wait_for_element(selector, timeout=timeout)
                else:
                    return {"status": "failed", "error": f"Unknown action: {action}"}
                return {
                    "status": "completed",
                    "action": action,
                    "selector": selector,
                    "success": success,
                }
        except Exception as e:
            return {
                "status": "failed",
                "action": action,
                "selector": selector,
                "error": str(e),
            }

    async def _execute_screenshot_task(
        self, task: Dict[str, Any], config: AutomationConfig
    ) -> Dict[str, Any]:
        """Execute screenshot automation task."""
        filename = task.get("filename", f"screenshot_{int(time.time())}")
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._run_screenshot_sync, filename, config)
                result = await asyncio.wrap_future(future)
                return result
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def _run_screenshot_sync(self, filename: str, config: AutomationConfig) -> Dict[str, Any]:
        """Run screenshot synchronously."""
        try:
            with WebAutomationEngine(config) as engine:
                screenshot_path = engine.take_screenshot(filename)
                if screenshot_path:
                    return {
                        "status": "completed",
                        "filename": filename,
                        "screenshot_path": screenshot_path,
                        "success": True,
                    }
                return {
                    "status": "failed",
                    "filename": filename,
                    "error": "Screenshot failed",
                }
        except Exception as e:
            return {"status": "failed", "filename": filename, "error": str(e)}

    async def _run_testing_step(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute testing step."""
        step_id = f"testing_{int(time.time())}"
        try:
            self.logger.info(f"Starting testing step: {step_id}")
            test_results = self.test_suite.run_automation_tests()
            result = {
                "step_id": step_id,
                "step_type": "testing",
                "status": "completed",
                "test_results": test_results,
            }
            self.logger.info(f"Testing step {step_id} completed")
            return result
        except Exception as e:
            self.logger.error(f"Testing step {step_id} failed: {e}")
            return {
                "step_id": step_id,
                "step_type": "testing",
                "status": "failed",
                "error": str(e),
            }

    async def _run_validation_step(self, previous_steps: list) -> Dict[str, Any]:
        """Execute validation step."""
        step_id = f"validation_{int(time.time())}"
        try:
            self.logger.info(f"Starting validation step: {step_id}")
            validation_results = []
            overall_success = True
            for step in previous_steps:
                if step.get("status") == "failed":
                    overall_success = False
                    validation_results.append(
                        {
                            "step_id": step.get("step_id"),
                            "status": "failed",
                            "error": step.get("error", "Unknown error"),
                        }
                    )
                else:
                    validation_results.append(
                        {"step_id": step.get("step_id"), "status": "passed"}
                    )
            result = {
                "step_id": step_id,
                "step_type": "validation",
                "status": "completed" if overall_success else "failed",
                "overall_success": overall_success,
                "validation_results": validation_results,
            }
            self.logger.info(f"Validation step {step_id} completed")
            return result
        except Exception as e:
            self.logger.error(f"Validation step {step_id} failed: {e}")
            return {
                "step_id": step_id,
                "step_type": "validation",
                "status": "failed",
                "error": str(e),
            }
