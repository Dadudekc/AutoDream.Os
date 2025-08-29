#!/usr/bin/env python3
"""
Learning Module Interfaces - Agent Cellphone V2
=============================================

Clean interfaces for all modularized learning components.
Follows V2 standards: modular design, clean APIs, unified access.

**Author:** Captain Agent-3 (MODULAR-007 Contract)
**Created:** Current Sprint
**Status:** ACTIVE - MODULARIZATION IN PROGRESS
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from .learning_algorithms import LearningAlgorithmsModule
from .data_processing import DataProcessingModule, DataProcessingResult
from .model_management import ModelManagementModule, ModelType, ModelStatus


class LearningModuleInterface(ABC):
    """Abstract base class for learning module interfaces"""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the module"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get module status"""
        pass
    
    @abstractmethod
    def run_health_check(self) -> bool:
        """Run module health check"""
        pass


class UnifiedLearningInterface:
    """
    Unified interface for all learning modules
    
    This interface provides:
    - Single point of access to all learning functionality
    - Consistent API across all modules
    - Error handling and logging
    - Performance monitoring
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Initialize all modules
        self.algorithms_module = LearningAlgorithmsModule()
        self.data_processing_module = DataProcessingModule()
        self.model_management_module = ModelManagementModule()
        
        # Module status tracking
        self.module_status = {
            "algorithms": "initializing",
            "data_processing": "initializing",
            "model_management": "initializing"
        }
        
        # Performance metrics
        self.interface_metrics = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "last_operation": None
        }
        
        self.logger.info("UnifiedLearningInterface initialized")
        self._initialize_all_modules()
    
    def _initialize_all_modules(self):
        """Initialize all learning modules"""
        try:
            # Initialize algorithms module
            if self.algorithms_module:
                self.module_status["algorithms"] = "active"
                self.logger.info("✅ Learning algorithms module initialized")
            
            # Initialize data processing module
            if self.data_processing_module:
                self.module_status["data_processing"] = "active"
                self.logger.info("✅ Data processing module initialized")
            
            # Initialize model management module
            if self.model_management_module:
                self.module_status["model_management"] = "active"
                self.logger.info("✅ Model management module initialized")
            
            self.logger.info("🎉 All learning modules initialized successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize modules: {e}")
            raise
    
    def _record_operation(self, success: bool):
        """Record operation metrics"""
        self.interface_metrics["total_operations"] += 1
        if success:
            self.interface_metrics["successful_operations"] += 1
        else:
            self.interface_metrics["failed_operations"] += 1
        
        self.interface_metrics["last_operation"] = datetime.now().isoformat()
    
    # ============================================================================
    # LEARNING ALGORITHMS INTERFACE
    # ============================================================================
    
    def register_learning_strategy(self, strategy: Any) -> str:
        """Register a new learning strategy"""
        try:
            result = self.algorithms_module.register_learning_strategy(strategy)
            self._record_operation(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to register learning strategy: {e}")
            self._record_operation(False)
            return ""
    
    def execute_learning_strategy(
        self,
        strategy_id: str,
        input_data: Dict[str, Any],
        context: str = "general"
    ) -> Optional[Dict[str, Any]]:
        """Execute a learning strategy"""
        try:
            result = self.algorithms_module.execute_learning_strategy(strategy_id, input_data, context)
            self._record_operation(result is not None)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to execute learning strategy: {e}")
            self._record_operation(False)
            return None
    
    def get_algorithm_performance(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for an algorithm"""
        try:
            result = self.algorithms_module.get_algorithm_performance(strategy_id)
            self._record_operation(True)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get algorithm performance: {e}")
            self._record_operation(False)
            return None
    
    def optimize_algorithm_parameters(self, strategy_id: str) -> bool:
        """Optimize algorithm parameters"""
        try:
            result = self.algorithms_module.optimize_algorithm_parameters(strategy_id)
            self._record_operation(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to optimize algorithm parameters: {e}")
            self._record_operation(False)
            return False
    
    # ============================================================================
    # DATA PROCESSING INTERFACE
    # ============================================================================
    
    def process_learning_data(
        self,
        raw_data: Dict[str, Any],
        context: str = "general",
        validation_level: str = "standard"
    ) -> DataProcessingResult:
        """Process learning data"""
        try:
            result = self.data_processing_module.process_learning_data(raw_data, context, validation_level)
            self._record_operation(result.success)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to process learning data: {e}")
            self._record_operation(False)
            return DataProcessingResult(
                success=False,
                error_message=str(e),
                data_quality_score=0.0
            )
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get data processing statistics"""
        try:
            result = self.data_processing_module.get_processing_statistics()
            self._record_operation(True)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get processing statistics: {e}")
            self._record_operation(False)
            return {}
    
    def get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached processed data"""
        try:
            result = self.data_processing_module.get_cached_data(cache_key)
            self._record_operation(True)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get cached data: {e}")
            self._record_operation(False)
            return None
    
    def clear_data_cache(self, older_than_hours: int = 24) -> int:
        """Clear old cached data"""
        try:
            result = self.data_processing_module.clear_cache(older_than_hours)
            self._record_operation(True)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to clear data cache: {e}")
            self._record_operation(False)
            return 0
    
    # ============================================================================
    # MODEL MANAGEMENT INTERFACE
    # ============================================================================
    
    def register_model(
        self,
        model: Any,
        model_type: ModelType,
        name: str,
        description: str,
        version: str = "1.0.0"
    ) -> str:
        """Register a new model"""
        try:
            result = self.model_management_module.register_model(model, model_type, name, description, version)
            self._record_operation(bool(result))
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to register model: {e}")
            self._record_operation(False)
            return ""
    
    def activate_model(self, model_id: str) -> bool:
        """Activate a model"""
        try:
            result = self.model_management_module.activate_model(model_id)
            self._record_operation(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to activate model: {e}")
            self._record_operation(False)
            return False
    
    def deactivate_model(self, model_id: str) -> bool:
        """Deactivate a model"""
        try:
            result = self.model_management_module.deactivate_model(model_id)
            self._record_operation(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to deactivate model: {e}")
            self._record_operation(False)
            return False
    
    def update_model_performance(self, model_id: str, performance_score: float) -> bool:
        """Update model performance"""
        try:
            result = self.model_management_module.update_model_performance(model_id, performance_score)
            self._record_operation(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to update model performance: {e}")
            self._record_operation(False)
            return False
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get model information"""
        try:
            result = self.model_management_module.get_model_info(model_id)
            self._record_operation(True)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get model info: {e}")
            self._record_operation(False)
            return None
    
    def get_all_models_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all models"""
        try:
            result = self.model_management_module.get_all_models_info()
            self._record_operation(True)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get all models info: {e}")
            self._record_operation(False)
            return {}
    
    def cleanup_deprecated_models(self, older_than_days: Optional[int] = None) -> int:
        """Clean up deprecated models"""
        try:
            result = self.model_management_module.cleanup_deprecated_models(older_than_days)
            self._record_operation(True)
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup deprecated models: {e}")
            self._record_operation(False)
            return 0
    
    # ============================================================================
    # UNIFIED OPERATIONS INTERFACE
    # ============================================================================
    
    def execute_learning_workflow(
        self,
        strategy_id: str,
        input_data: Dict[str, Any],
        context: str = "general"
    ) -> Dict[str, Any]:
        """Execute a complete learning workflow"""
        try:
            workflow_result = {
                "workflow_id": f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "strategy_id": strategy_id,
                "context": context,
                "start_time": datetime.now().isoformat(),
                "steps": [],
                "success": False,
                "final_result": None
            }
            
            # Step 1: Process input data
            self.logger.info("🔄 Step 1: Processing input data...")
            data_result = self.process_learning_data(input_data, context, "standard")
            workflow_result["steps"].append({
                "step": "data_processing",
                "success": data_result.success,
                "quality_score": data_result.data_quality_score,
                "processing_time_ms": data_result.processing_time_ms
            })
            
            if not data_result.success:
                workflow_result["error"] = data_result.error_message
                return workflow_result
            
            # Step 2: Execute learning strategy
            self.logger.info("🔄 Step 2: Executing learning strategy...")
            strategy_result = self.execute_learning_strategy(strategy_id, data_result.processed_data, context)
            workflow_result["steps"].append({
                "step": "strategy_execution",
                "success": strategy_result is not None,
                "performance_score": strategy_result.get("performance_score", 0.0) if strategy_result else 0.0
            })
            
            if not strategy_result:
                workflow_result["error"] = "Strategy execution failed"
                return workflow_result
            
            # Step 3: Update model performance
            self.logger.info("🔄 Step 3: Updating model performance...")
            if "performance_score" in strategy_result:
                performance_updated = self.update_model_performance(strategy_id, strategy_result["performance_score"])
                workflow_result["steps"].append({
                    "step": "performance_update",
                    "success": performance_updated
                })
            
            # Step 4: Record model usage
            self.logger.info("🔄 Step 4: Recording model usage...")
            usage_recorded = self.model_management_module.record_model_usage(strategy_id)
            workflow_result["steps"].append({
                "step": "usage_recording",
                "success": usage_recorded
            })
            
            # Workflow completed successfully
            workflow_result["success"] = True
            workflow_result["final_result"] = strategy_result
            workflow_result["end_time"] = datetime.now().isoformat()
            
            self.logger.info("✅ Learning workflow completed successfully!")
            return workflow_result
            
        except Exception as e:
            self.logger.error(f"❌ Learning workflow failed: {e}")
            workflow_result["error"] = str(e)
            workflow_result["end_time"] = datetime.now().isoformat()
            return workflow_result
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all modules and interface"""
        try:
            # Get individual module statuses
            algorithms_status = self.algorithms_module.get_all_algorithm_performance() if self.algorithms_module else {}
            data_processing_status = self.data_processing_module.get_processing_statistics() if self.data_processing_module else {}
            model_management_status = self.model_management_module.get_all_models_info() if self.model_management_module else {}
            
            # Calculate overall health score
            total_operations = self.interface_metrics["total_operations"]
            success_rate = (self.interface_metrics["successful_operations"] / max(1, total_operations)) * 100.0
            
            # Module health assessment
            active_modules = sum(1 for status in self.module_status.values() if status == "active")
            total_modules = len(self.module_status)
            module_health = (active_modules / total_modules) * 100.0
            
            return {
                "interface_status": {
                    "status": "healthy" if module_health > 80 and success_rate > 90 else "degraded",
                    "module_health_percent": round(module_health, 2),
                    "success_rate_percent": round(success_rate, 2),
                    "total_operations": total_operations,
                    "last_operation": self.interface_metrics["last_operation"]
                },
                "module_status": self.module_status.copy(),
                "algorithms_module": {
                    "status": "active" if self.module_status["algorithms"] == "active" else "inactive",
                    "registered_strategies": len(algorithms_status),
                    "performance_summary": algorithms_status
                },
                "data_processing_module": {
                    "status": "active" if self.module_status["data_processing"] == "active" else "inactive",
                    "processing_stats": data_processing_status
                },
                "model_management_module": {
                    "status": "active" if self.module_status["model_management"] == "active" else "inactive",
                    "total_models": len(model_management_status),
                    "active_models": len([m for m in model_management_status.values() if m.get("status") == "active"])
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get comprehensive status: {e}")
            return {"error": str(e)}
    
    def run_health_check(self) -> bool:
        """Run comprehensive health check of all modules"""
        try:
            self.logger.info("🔍 Running comprehensive health check...")
            
            # Test algorithms module
            algorithms_healthy = self.algorithms_module.run_module_test() if self.algorithms_module else False
            
            # Test data processing module
            data_processing_healthy = self.data_processing_module.run_module_test() if self.data_processing_module else False
            
            # Test model management module
            model_management_healthy = self.model_management_module.run_module_test() if self.model_management_module else False
            
            # Overall health assessment
            all_healthy = algorithms_healthy and data_processing_healthy and model_management_healthy
            
            if all_healthy:
                self.logger.info("✅ All modules passed health check!")
            else:
                self.logger.warning("⚠️ Some modules failed health check")
                if not algorithms_healthy:
                    self.logger.warning("❌ Algorithms module health check failed")
                if not data_processing_healthy:
                    self.logger.warning("❌ Data processing module health check failed")
                if not model_management_healthy:
                    self.logger.warning("❌ Model management module health check failed")
            
            return all_healthy
            
        except Exception as e:
            self.logger.error(f"❌ Health check failed: {e}")
            return False
    
    def run_module_test(self) -> bool:
        """Run basic functionality test for the unified interface"""
        try:
            # Test basic operations
            test_data = {
                "input_data": {"test": "value"},
                "output_data": {"result": "success"},
                "performance_score": 0.9
            }
            
            # Test data processing
            data_result = self.process_learning_data(test_data, "test")
            if not data_result.success:
                return False
            
            # Test status retrieval
            status = self.get_comprehensive_status()
            if "error" in status:
                return False
            
            # Test health check
            if not self.run_health_check():
                return False
            
            self.logger.info("✅ Unified learning interface test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Unified learning interface test failed: {e}")
            return False
