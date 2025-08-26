"""Simple dependency management utilities with BaseManager inheritance."""
from __future__ import annotations

import importlib
import logging
from typing import Dict, Iterable, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json

from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority


class DependencyManager(BaseManager):
    """
    Dependency Manager - Manages Python module dependencies
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self):
        """Initialize dependency manager with BaseManager"""
        super().__init__(
            manager_id="dependency_manager",
            name="Dependency Manager",
            description="Manages Python module dependencies and availability checks"
        )
        
        # Dependency tracking
        self.dependency_cache: Dict[str, bool] = {}
        self.dependency_history: List[Dict[str, Any]] = []
        self.failed_dependencies: List[str] = []
        
        self.logger.info("Dependency Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize dependency management system"""
        try:
            self.logger.info("Starting Dependency Manager...")
            
            # Clear cache and history
            self.dependency_cache.clear()
            self.dependency_history.clear()
            self.failed_dependencies.clear()
            
            self.logger.info("Dependency Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Dependency Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup dependency management system"""
        try:
            self.logger.info("Stopping Dependency Manager...")
            
            # Save dependency history
            self._save_dependency_history()
            
            # Clear data
            self.dependency_cache.clear()
            self.dependency_history.clear()
            self.failed_dependencies.clear()
            
            self.logger.info("Dependency Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Dependency Manager: {e}")
    
    def _on_heartbeat(self):
        """Dependency manager heartbeat"""
        try:
            # Check critical dependencies
            self._check_critical_dependencies()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize dependency manager resources"""
        try:
            # Initialize data structures
            self.dependency_cache = {}
            self.dependency_history = []
            self.failed_dependencies = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup dependency manager resources"""
        try:
            # Clear data
            self.dependency_cache.clear()
            self.dependency_history.clear()
            self.failed_dependencies.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Clear cache and retry
            self.dependency_cache.clear()
            self.failed_dependencies.clear()
            
            # Recheck critical dependencies
            critical_deps = ["logging", "typing", "datetime"]
            for dep in critical_deps:
                if not self.check_dependency(dep):
                    self.logger.error(f"Critical dependency {dep} still missing")
                    return False
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Dependency Management Methods
    # ============================================================================
    
    @staticmethod
    def check_dependency(module_name: str) -> bool:
        """Return True if ``module_name`` can be imported."""
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False

    def ensure(self, modules: Iterable[str]) -> Dict[str, bool]:
        """Check multiple ``modules`` and return their availability."""
        try:
            results = {}
            
            for module in modules:
                # Check cache first
                if module in self.dependency_cache:
                    results[module] = self.dependency_cache[module]
                    continue
                
                # Check dependency
                available = self.check_dependency(module)
                results[module] = available
                
                # Cache result
                self.dependency_cache[module] = available
                
                # Track failed dependencies
                if not available:
                    self.failed_dependencies.append(module)
                
                # Record in history
                self._record_dependency_check(module, available)
            
            # Record operation
            self.record_operation("ensure_dependencies", True, 0.0)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to ensure dependencies: {e}")
            self.record_operation("ensure_dependencies", False, 0.0)
            return {}
    
    def check_dependency_with_retry(self, module_name: str, max_retries: int = 3) -> bool:
        """Check dependency with retry logic"""
        try:
            for attempt in range(max_retries):
                if self.check_dependency(module_name):
                    self.logger.debug(f"Dependency {module_name} available on attempt {attempt + 1}")
                    return True
                
                if attempt < max_retries - 1:
                    self.logger.debug(f"Dependency {module_name} not available, retrying...")
                    import time
                    time.sleep(0.1 * (attempt + 1))  # Exponential backoff
            
            self.logger.warning(f"Dependency {module_name} not available after {max_retries} attempts")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to check dependency {module_name} with retry: {e}")
            return False
    
    def get_dependency_status(self) -> Dict[str, Any]:
        """Get comprehensive dependency status"""
        try:
            status = {
                "total_dependencies_checked": len(self.dependency_cache),
                "available_dependencies": len([d for d in self.dependency_cache.values() if d]),
                "missing_dependencies": len([d for d in self.dependency_cache.values() if not d]),
                "failed_dependencies": self.failed_dependencies.copy(),
                "cache_size": len(self.dependency_cache),
                "history_size": len(self.dependency_history)
            }
            
            # Record operation
            self.record_operation("get_dependency_status", True, 0.0)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to get dependency status: {e}")
            self.record_operation("get_dependency_status", False, 0.0)
            return {"error": str(e)}
    
    def clear_cache(self) -> bool:
        """Clear dependency cache"""
        try:
            cache_size = len(self.dependency_cache)
            self.dependency_cache.clear()
            
            # Record operation
            self.record_operation("clear_cache", True, 0.0)
            
            self.logger.info(f"Cleared dependency cache ({cache_size} entries)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {e}")
            self.record_operation("clear_cache", False, 0.0)
            return False
    
    def get_missing_dependencies(self) -> List[str]:
        """Get list of missing dependencies"""
        try:
            missing = [module for module, available in self.dependency_cache.items() if not available]
            
            # Record operation
            self.record_operation("get_missing_dependencies", True, 0.0)
            
            return missing
            
        except Exception as e:
            self.logger.error(f"Failed to get missing dependencies: {e}")
            self.record_operation("get_missing_dependencies", False, 0.0)
            return []
    
    def get_available_dependencies(self) -> List[str]:
        """Get list of available dependencies"""
        try:
            available = [module for module, available in self.dependency_cache.items() if available]
            
            # Record operation
            self.record_operation("get_available_dependencies", True, 0.0)
            
            return available
            
        except Exception as e:
            self.logger.error(f"Failed to get available dependencies: {e}")
            self.record_operation("get_available_dependencies", False, 0.0)
            return []
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _record_dependency_check(self, module_name: str, available: bool):
        """Record dependency check in history"""
        try:
            record = {
                "module_name": module_name,
                "available": available,
                "timestamp": datetime.now().isoformat(),
                "cache_hit": module_name in self.dependency_cache
            }
            
            self.dependency_history.append(record)
            
            # Keep history manageable
            if len(self.dependency_history) > 1000:
                self.dependency_history = self.dependency_history[-500:]
                
        except Exception as e:
            self.logger.error(f"Failed to record dependency check: {e}")
    
    def _save_dependency_history(self):
        """Save dependency history to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            persistence_dir = Path("data/persistent/dependencies")
            persistence_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for persistence
            dependency_data = {
                "dependency_cache": self.dependency_cache,
                "dependency_history": self.dependency_history,
                "critical_dependencies": ["logging", "typing", "datetime", "importlib"],
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0"
            }
            
            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dependency_data_{timestamp}.json"
            filepath = persistence_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(dependency_data, f, indent=2, default=str)
            
            # Keep only the latest 5 backup files
            self._cleanup_old_backups(persistence_dir, "dependency_data_*.json", 5)
            
            self.logger.info(f"Dependency history saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save dependency history: {e}")
            # Fallback to basic logging if persistence fails
            self.logger.warning("Persistence failed, data only logged in memory")
    
    def _cleanup_old_backups(self, directory: Path, pattern: str, keep_count: int):
        """Clean up old backup files, keeping only the specified number"""
        try:
            files = list(directory.glob(pattern))
            if len(files) > keep_count:
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x.stat().st_mtime)
                # Remove oldest files
                for old_file in files[:-keep_count]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")
    
    def _check_critical_dependencies(self):
        """Check critical system dependencies"""
        try:
            critical_deps = ["logging", "typing", "datetime", "importlib"]
            
            for dep in critical_deps:
                if not self.check_dependency(dep):
                    self.logger.error(f"Critical dependency {dep} is missing!")
                    self.handle_error(Exception(f"Critical dependency {dep} missing"), "critical_dependency_check")
                    break
                    
        except Exception as e:
            self.logger.error(f"Failed to check critical dependencies: {e}")
