"""
Deployment Executor - V2 Compliant Module
========================================

Handles execution of deployment tasks and concurrent processing.
Extracted from deployment_coordinator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List
import logging

from ..deployment_models import MassDeploymentTarget


class DeploymentExecutor:
    """
    Executor for deployment tasks with concurrent processing.
    
    Manages thread pool execution, deployment coordination, and result collection.
    """
    
    def __init__(self, config):
        """Initialize deployment executor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Execution state
        self.is_running = False
        self.deployment_lock = threading.Lock()
        self.active_deployments = 0
        
        # Thread pool for concurrent deployments
        self.executor = ThreadPoolExecutor(max_workers=config.max_concurrent_deployments)
    
    def execute_deployment_batch(self, targets: List[MassDeploymentTarget]) -> Dict[str, Any]:
        """Execute a batch of deployment targets."""
        if self.is_running:
            return {"success": False, "error": "Deployment already in progress"}
        
        self.is_running = True
        self.active_deployments = 0
        
        try:
            self.logger.info(f"Starting deployment batch with {len(targets)} targets")
            
            # Execute deployments concurrently
            results = self._execute_concurrent_deployments(targets)
            
            # Calculate success rate
            successful = sum(1 for r in results if r.get("success", False))
            success_rate = (successful / len(results)) * 100 if results else 0
            
            self.logger.info(f"Deployment batch completed: {successful}/{len(results)} successful ({success_rate:.1f}%)")
            
            return {
                "success": True,
                "results": results,
                "success_rate": success_rate,
                "total_targets": len(targets),
                "successful_deployments": successful,
                "failed_deployments": len(results) - successful
            }
            
        except Exception as e:
            self.logger.error(f"Error executing deployment batch: {e}")
            return {"success": False, "error": str(e)}
        finally:
            self.is_running = False
    
    def _execute_concurrent_deployments(self, targets: List[MassDeploymentTarget]) -> List[Dict[str, Any]]:
        """Execute deployments concurrently using thread pool."""
        results = []
        futures = []
        
        # Submit deployment tasks
        for target in targets:
            future = self.executor.submit(self._deploy_target, target)
            futures.append((future, target))
        
        # Collect results as they complete
        for future, target in futures:
            try:
                result = future.result(timeout=self.config.deployment_timeout_seconds)
                results.append(result)
                
            except Exception as e:
                self.logger.error(f"Deployment failed for {target.file_path}: {e}")
                error_result = {
                    "success": False,
                    "target_path": target.file_path,
                    "error": str(e)
                }
                results.append(error_result)
        
        return results
    
    def _deploy_target(self, target: MassDeploymentTarget) -> Dict[str, Any]:
        """Deploy individual target."""
        start_time = time.time()
        
        try:
            with self.deployment_lock:
                self.active_deployments += 1
            
            self.logger.debug(f"Deploying target: {target.file_path}")
            
            # Simulate deployment process
            deployment_result = self._perform_deployment(target)
            
            # Calculate deployment time
            deployment_time = time.time() - start_time
            
            result = {
                "success": deployment_result["success"],
                "target_path": target.file_path,
                "deployment_time": deployment_time,
                "details": deployment_result.get("details", {})
            }
            
            if not deployment_result["success"]:
                result["error"] = deployment_result.get("error", "Unknown deployment error")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error deploying target {target.file_path}: {e}")
            return {
                "success": False,
                "target_path": target.file_path,
                "error": str(e),
                "deployment_time": time.time() - start_time
            }
        finally:
            with self.deployment_lock:
                self.active_deployments -= 1
    
    def _perform_deployment(self, target: MassDeploymentTarget) -> Dict[str, Any]:
        """Perform actual deployment for target."""
        try:
            # Simulate deployment based on pattern type
            if target.pattern_type == "logging":
                return self._deploy_logging_target(target)
            elif target.pattern_type == "manager":
                return self._deploy_manager_target(target)
            elif target.pattern_type == "config":
                return self._deploy_config_target(target)
            else:
                return self._deploy_generic_target(target)
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _deploy_logging_target(self, target: MassDeploymentTarget) -> Dict[str, Any]:
        """Deploy logging target."""
        # Simulate logging deployment
        time.sleep(0.1)  # Simulate processing time
        return {
            "success": True,
            "details": {"type": "logging", "action": "deployed"}
        }
    
    def _deploy_manager_target(self, target: MassDeploymentTarget) -> Dict[str, Any]:
        """Deploy manager target."""
        # Simulate manager deployment
        time.sleep(0.2)  # Simulate processing time
        return {
            "success": True,
            "details": {"type": "manager", "action": "deployed"}
        }
    
    def _deploy_config_target(self, target: MassDeploymentTarget) -> Dict[str, Any]:
        """Deploy config target."""
        # Simulate config deployment
        time.sleep(0.05)  # Simulate processing time
        return {
            "success": True,
            "details": {"type": "config", "action": "deployed"}
        }
    
    def _deploy_generic_target(self, target: MassDeploymentTarget) -> Dict[str, Any]:
        """Deploy generic target."""
        # Simulate generic deployment
        time.sleep(0.1)  # Simulate processing time
        return {
            "success": True,
            "details": {"type": "generic", "action": "deployed"}
        }
    
    def get_execution_status(self) -> Dict[str, Any]:
        """Get current execution status."""
        return {
            "is_running": self.is_running,
            "active_deployments": self.active_deployments,
            "max_concurrent": self.config.max_concurrent_deployments,
            "thread_pool_size": self.executor._max_workers
        }
    
    def shutdown(self):
        """Shutdown deployment executor."""
        self.logger.info("Shutting down deployment executor...")
        self.executor.shutdown(wait=True)
        self.is_running = False
        self.logger.info("Deployment executor shutdown complete")
