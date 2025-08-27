"""
Validation Manager - Unified Validation Framework

This module provides a central manager for coordinating all validators in the unified
validation system. It acts as a facade for the entire validation framework.
"""

import logging
from typing import Dict, List, Any, Optional, Type
from .base_validator import BaseValidator, ValidationResult, ValidationSeverity, ValidationStatus
from .contract_validator import ContractValidator
from .config_validator import ConfigValidator
from ..workflow.validation.workflow_validator import WorkflowValidator
from .message_validator import MessageValidator
from .quality_validator import QualityValidator
from .security_validator import SecurityValidator
from .storage_validator import StorageValidator
from .onboarding_validator import OnboardingValidator
from .task_validator import TaskValidator
from .code_validator import CodeValidator


class ValidationManager:
    """Central manager for coordinating all validators in the unified framework"""
    
    def __init__(self):
        """Initialize validation manager"""
        self.logger = logging.getLogger(f"{__name__}.ValidationManager")
        self.validators: Dict[str, BaseValidator] = {}
        self.validation_history: List[ValidationResult] = []
        self._initialize_default_validators()
    
    def _initialize_default_validators(self) -> None:
        """Initialize default validators"""
        try:
            # Initialize core validators
            self.validators["contract"] = ContractValidator()
            self.validators["config"] = ConfigValidator()
            self.validators["workflow"] = WorkflowValidator()
            self.validators["message"] = MessageValidator()
            self.validators["quality"] = QualityValidator()
            self.validators["security"] = SecurityValidator()
            self.validators["storage"] = StorageValidator()
            self.validators["onboarding"] = OnboardingValidator()
            self.validators["task"] = TaskValidator()
            self.validators["code"] = CodeValidator()
            
            self.logger.info("Default validators initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default validators: {e}")
    
    def register_validator(self, name: str, validator: BaseValidator) -> bool:
        """Register a new validator"""
        try:
            if not isinstance(validator, BaseValidator):
                self.logger.error(f"Validator must inherit from BaseValidator: {type(validator)}")
                return False
            
            self.validators[name] = validator
            self.logger.info(f"Validator registered: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register validator {name}: {e}")
            return False
    
    def unregister_validator(self, name: str) -> bool:
        """Unregister a validator"""
        try:
            if name in self.validators:
                del self.validators[name]
                self.logger.info(f"Validator unregistered: {name}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to unregister validator {name}: {e}")
            return False
    
    def get_validator(self, name: str) -> Optional[BaseValidator]:
        """Get a validator by name"""
        return self.validators.get(name)
    
    def list_validators(self) -> List[str]:
        """List all registered validators"""
        return list(self.validators.keys())
    
    def validate_with_validator(
        self, 
        validator_name: str, 
        data: Any, 
        **kwargs
    ) -> List[ValidationResult]:
        """Validate data using a specific validator"""
        try:
            validator = self.validators.get(validator_name)
            if not validator:
                error_result = ValidationResult(
                    rule_id="validator_not_found",
                    rule_name="Validator Not Found",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Validator '{validator_name}' not found",
                    details={"available_validators": self.list_validators()}
                )
                return [error_result]
            
            results = validator.validate(data, **kwargs)
            
            # Store results in manager history
            self.validation_history.extend(results)
            
            # Keep history manageable
            if len(self.validation_history) > 10000:
                self.validation_history = self.validation_history[-10000:]
            
            return results
            
        except Exception as e:
            error_result = ValidationResult(
                rule_id="validation_manager_error",
                rule_name="Validation Manager Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Validation error: {str(e)}",
                details={"error_type": type(e).__name__, "validator": validator_name}
            )
            return [error_result]
    
    def validate_all(self, data: Dict[str, Any], **kwargs) -> Dict[str, List[ValidationResult]]:
        """Validate data using all applicable validators"""
        results = {}
        
        try:
            for validator_name, validator in self.validators.items():
                # Check if validator should be used for this data
                if self._should_use_validator(validator_name, data, **kwargs):
                    validator_results = validator.validate(data, **kwargs)
                    results[validator_name] = validator_results
                    
                    # Store results in manager history
                    self.validation_history.extend(validator_results)
                else:
                    results[validator_name] = []
            
            # Keep history manageable
            if len(self.validation_history) > 10000:
                self.validation_history = self.validation_history[-10000:]
            
        except Exception as e:
            self.logger.error(f"Error in validate_all: {e}")
            error_result = ValidationResult(
                rule_id="validation_manager_error",
                rule_name="Validation Manager Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Validation error: {str(e)}",
                details={"error_type": type(e).__name__}
            )
            results["error"] = [error_result]
        
        return results
    
    def _should_use_validator(self, validator_name: str, data: Any, **kwargs) -> bool:
        """Determine if a validator should be used for the given data"""
        # This is a simple heuristic - could be made more sophisticated
        if validator_name == "contract":
            return isinstance(data, dict) and "title" in data and "description" in data
        elif validator_name == "config":
            return isinstance(data, dict) and len(data) > 0
        elif validator_name == "workflow":
            return isinstance(data, dict) and "steps" in data and "transitions" in data
        elif validator_name == "message":
            return isinstance(data, dict) and "type" in data and "content" in data
        elif validator_name == "quality":
            return isinstance(data, dict) and "metrics" in data
        elif validator_name == "security":
            return isinstance(data, dict) and "security_level" in data
        elif validator_name == "storage":
            return isinstance(data, dict) and "type" in data and "configuration" in data
        elif validator_name == "onboarding":
            return isinstance(data, dict) and "stage" in data and "status" in data
        elif validator_name == "task":
            return isinstance(data, dict) and "status" in data and "priority" in data
        elif validator_name == "code":
            return isinstance(data, dict) and "content" in data and "language" in data
        else:
            # For custom validators, assume they should be used
            return True
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get overall validation summary across all validators"""
        summary = {
            "total_validators": len(self.validators),
            "validator_names": self.list_validators(),
            "total_validations": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "success_rate": 0.0,
            "validator_details": {}
        }
        
        # Aggregate results from all validators
        for validator_name, validator in self.validators.items():
            validator_summary = validator.get_validation_summary()
            summary["validator_details"][validator_name] = validator_summary
            
            summary["total_validations"] += validator_summary["total_validations"]
            summary["passed"] += validator_summary["passed"]
            summary["failed"] += validator_summary["failed"]
            summary["warnings"] += validator_summary["warnings"]
        
        # Calculate overall success rate
        if summary["total_validations"] > 0:
            summary["success_rate"] = (summary["passed"] / summary["total_validations"]) * 100
        
        return summary
    
    def get_validation_history(self, limit: int = 1000) -> List[ValidationResult]:
        """Get validation history from all validators"""
        return self.validation_history[-limit:] if limit > 0 else self.validation_history.copy()
    
    def clear_validation_history(self) -> None:
        """Clear validation history from all validators"""
        for validator in self.validators.values():
            validator.clear_validation_history()
        self.validation_history.clear()
        self.logger.info("All validation history cleared")
    
    def get_validator_statistics(self, validator_name: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a specific validator"""
        validator = self.validators.get(validator_name)
        if validator:
            return validator.get_validation_summary()
        return None
    
    def run_validation_pipeline(
        self, 
        data: Any, 
        pipeline: List[str], 
        **kwargs
    ) -> Dict[str, List[ValidationResult]]:
        """Run validation through a specific pipeline of validators"""
        results = {}
        
        try:
            for validator_name in pipeline:
                if validator_name in self.validators:
                    validator_results = self.validators[validator_name].validate(data, **kwargs)
                    results[validator_name] = validator_results
                    
                    # Store results in manager history
                    self.validation_history.extend(validator_results)
                else:
                    self.logger.warning(f"Validator '{validator_name}' not found in pipeline")
                    results[validator_name] = []
            
            # Keep history manageable
            if len(self.validation_history) > 10000:
                self.validation_history = self.validation_history[-10000:]
            
        except Exception as e:
            self.logger.error(f"Error in validation pipeline: {e}")
            error_result = ValidationResult(
                rule_id="validation_pipeline_error",
                rule_name="Validation Pipeline Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Validation pipeline error: {str(e)}",
                details={"error_type": type(e).__name__, "pipeline": pipeline}
            )
            results["pipeline_error"] = [error_result]
        
        return results

    # SPECIALIZED VALIDATION CAPABILITIES - ENHANCED FOR V2
    def create_validation_strategy(self, strategy_type: str, parameters: Dict[str, Any]) -> str:
        """Create a specialized validation strategy"""
        try:
            strategy_id = f"strategy_{strategy_type}_{len(self.validation_history)}"
            
            if strategy_type == "cascading":
                strategy = {
                    "id": strategy_id,
                    "type": "cascading",
                    "description": "Sequential validation with early termination on failure",
                    "parameters": {
                        **parameters,
                        "stop_on_first_failure": parameters.get("stop_on_first_failure", True),
                        "validation_order": parameters.get("validation_order", ["security", "quality", "config"]),
                        "max_failures": parameters.get("max_failures", 3)
                    }
                }
            elif strategy_type == "parallel":
                strategy = {
                    "id": strategy_id,
                    "type": "parallel",
                    "description": "Parallel validation for improved performance",
                    "parameters": {
                        **parameters,
                        "max_concurrent_validators": parameters.get("max_concurrent_validators", 5),
                        "timeout_seconds": parameters.get("timeout_seconds", 30),
                        "fail_fast": parameters.get("fail_fast", False)
                    }
                }
            elif strategy_type == "adaptive":
                strategy = {
                    "id": strategy_id,
                    "type": "adaptive",
                    "description": "Adaptive validation based on data characteristics",
                    "parameters": {
                        **parameters,
                        "complexity_threshold": parameters.get("complexity_threshold", 0.7),
                        "performance_mode": parameters.get("performance_mode", "balanced"),
                        "quality_priority": parameters.get("quality_priority", "high")
                    }
                }
            else:
                raise ValueError(f"Unknown validation strategy type: {strategy_type}")
            
            # Store strategy
            if not hasattr(self, 'validation_strategies'):
                self.validation_strategies = {}
            self.validation_strategies[strategy_id] = strategy
            
            self.logger.info(f"Created validation strategy: {strategy_id}")
            return strategy_id
            
        except Exception as e:
            self.logger.error(f"Failed to create validation strategy: {e}")
            raise
    
    def execute_validation_strategy(self, strategy_id: str, data: Dict[str, Any], **kwargs) -> Dict[str, List[ValidationResult]]:
        """Execute a specific validation strategy"""
        try:
            if not hasattr(self, 'validation_strategies') or strategy_id not in self.validation_strategies:
                raise ValueError(f"Validation strategy not found: {strategy_id}")
            
            strategy = self.validation_strategies[strategy_id]
            strategy_type = strategy["type"]
            
            if strategy_type == "cascading":
                return self._execute_cascading_validation(data, strategy["parameters"], **kwargs)
            elif strategy_type == "parallel":
                return self._execute_parallel_validation(data, strategy["parameters"], **kwargs)
            elif strategy_type == "adaptive":
                return self._execute_adaptive_validation(data, strategy["parameters"], **kwargs)
            else:
                raise ValueError(f"Unknown strategy type: {strategy_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to execute validation strategy: {e}")
            raise
    
    def _execute_cascading_validation(self, data: Dict[str, Any], parameters: Dict[str, Any], **kwargs) -> Dict[str, List[ValidationResult]]:
        """Execute cascading validation strategy"""
        try:
            results = {}
            validation_order = parameters.get("validation_order", ["security", "quality", "config"])
            stop_on_first_failure = parameters.get("stop_on_first_failure", True)
            max_failures = parameters.get("max_failures", 3)
            
            failure_count = 0
            
            for validator_name in validation_order:
                if validator_name in self.validators:
                    validator_results = self.validators[validator_name].validate(data, **kwargs)
                    results[validator_name] = validator_results
                    
                    # Check for failures
                    failures = [r for r in validator_results if r.status == ValidationStatus.FAILED]
                    if failures:
                        failure_count += len(failures)
                        
                        if stop_on_first_failure or failure_count >= max_failures:
                            self.logger.info(f"Cascading validation stopped at {validator_name} due to failures")
                            break
                else:
                    self.logger.warning(f"Validator not found for cascading validation: {validator_name}")
                    results[validator_name] = []
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to execute cascading validation: {e}")
            raise
    
    def _execute_parallel_validation(self, data: Dict[str, Any], parameters: Dict[str, Any], **kwargs) -> Dict[str, List[ValidationResult]]:
        """Execute parallel validation strategy"""
        try:
            import concurrent.futures
            import time
            
            results = {}
            max_concurrent = parameters.get("max_concurrent_validators", 5)
            timeout_seconds = parameters.get("timeout_seconds", 30)
            fail_fast = parameters.get("fail_fast", False)
            
            # Prepare validation tasks
            validation_tasks = {}
            for validator_name, validator in self.validators.items():
                if self._should_use_validator(validator_name, data, **kwargs):
                    validation_tasks[validator_name] = validator
            
            # Execute parallel validation
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
                future_to_validator = {
                    executor.submit(validator.validate, data, **kwargs): validator_name
                    for validator_name, validator in validation_tasks.items()
                }
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(future_to_validator, timeout=timeout_seconds):
                    validator_name = future_to_validator[future]
                    try:
                        validator_results = future.result()
                        results[validator_name] = validator_results
                        
                        # Check for failures if fail_fast is enabled
                        if fail_fast:
                            failures = [r for r in validator_results if r.status == ValidationStatus.FAILED]
                            if failures:
                                self.logger.info(f"Parallel validation stopped due to failure in {validator_name}")
                                break
                                
                    except concurrent.futures.TimeoutError:
                        self.logger.warning(f"Validation timeout for {validator_name}")
                        results[validator_name] = []
                    except Exception as e:
                        self.logger.error(f"Validation error for {validator_name}: {e}")
                        results[validator_name] = []
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to execute parallel validation: {e}")
            raise
    
    def _execute_adaptive_validation(self, data: Dict[str, Any], parameters: Dict[str, Any], **kwargs) -> Dict[str, List[ValidationResult]]:
        """Execute adaptive validation strategy based on data characteristics"""
        try:
            complexity_threshold = parameters.get("complexity_threshold", 0.7)
            performance_mode = parameters.get("performance_mode", "balanced")
            quality_priority = parameters.get("quality_priority", "high")
            
            # Analyze data complexity
            data_complexity = self._assess_data_complexity(data)
            
            # Select validation approach based on complexity and performance mode
            if data_complexity > complexity_threshold:
                if performance_mode == "fast":
                    # Use minimal validation for complex data in fast mode
                    selected_validators = ["security", "config"]
                elif performance_mode == "balanced":
                    # Use balanced validation
                    selected_validators = ["security", "quality", "config", "workflow"]
                else:  # quality mode
                    # Use comprehensive validation
                    selected_validators = list(self.validators.keys())
            else:
                # Simple data - use standard validation
                selected_validators = ["security", "quality", "config"]
            
            # Execute validation with selected validators
            results = {}
            for validator_name in selected_validators:
                if validator_name in self.validators:
                    validator_results = self.validators[validator_name].validate(data, **kwargs)
                    results[validator_name] = validator_results
                else:
                    results[validator_name] = []
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to execute adaptive validation: {e}")
            raise
    
    def _assess_data_complexity(self, data: Any) -> float:
        """Assess the complexity of data for adaptive validation"""
        try:
            complexity_score = 0.0
            
            if isinstance(data, dict):
                # Assess dictionary complexity
                complexity_score += min(len(data) * 0.1, 0.3)  # Size factor
                
                # Assess nested structure complexity
                for value in data.values():
                    if isinstance(value, (list, dict)):
                        complexity_score += 0.2
                    elif isinstance(value, str) and len(value) > 100:
                        complexity_score += 0.1
                        
            elif isinstance(data, list):
                # Assess list complexity
                complexity_score += min(len(data) * 0.05, 0.2)  # Size factor
                
                # Assess item complexity
                for item in data[:10]:  # Sample first 10 items
                    if isinstance(item, (dict, list)):
                        complexity_score += 0.1
                        
            elif isinstance(data, str):
                # Assess string complexity
                complexity_score += min(len(data) * 0.001, 0.2)  # Length factor
                
                # Assess content complexity
                if any(char in data for char in ['{', '[', '<', '>']):
                    complexity_score += 0.2  # Structured content
            
            return min(complexity_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Failed to assess data complexity: {e}")
            return 0.5  # Default to medium complexity
    
    def analyze_validation_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze validation patterns for optimization insights"""
        try:
            import time
            from datetime import datetime, timedelta
            
            cutoff_time = datetime.now() - timedelta(hours=time_range_hours)
            
            # Filter recent validation results
            recent_results = [
                result for result in self.validation_history
                if hasattr(result, 'timestamp') and result.timestamp
            ]
            
            # Analyze patterns
            pattern_analysis = {
                "total_validations": len(recent_results),
                "success_rate": 0.0,
                "failure_patterns": {},
                "performance_metrics": {},
                "optimization_opportunities": []
            }
            
            if recent_results:
                # Calculate success rate
                successful_validations = [
                    r for r in recent_results
                    if r.status == ValidationStatus.PASSED
                ]
                pattern_analysis["success_rate"] = len(successful_validations) / len(recent_results)
                
                # Analyze failure patterns
                failed_validations = [
                    r for r in recent_results
                    if r.status == ValidationStatus.FAILED
                ]
                
                for failure in failed_validations:
                    rule_name = failure.rule_name
                    if rule_name not in pattern_analysis["failure_patterns"]:
                        pattern_analysis["failure_patterns"][rule_name] = 0
                    pattern_analysis["failure_patterns"][rule_name] += 1
                
                # Performance metrics
                pattern_analysis["performance_metrics"] = {
                    "average_validation_time": 0.0,  # Would need timing data
                    "validator_usage": {},
                    "data_complexity_distribution": {}
                }
                
                # Identify optimization opportunities
                if pattern_analysis["success_rate"] < 0.8:
                    pattern_analysis["optimization_opportunities"].append("Low success rate - review validation rules")
                
                if len(pattern_analysis["failure_patterns"]) > 5:
                    pattern_analysis["optimization_opportunities"].append("Many failure patterns - consider rule consolidation")
                
                # High failure validators
                high_failure_validators = [
                    name for name, count in pattern_analysis["failure_patterns"].items()
                    if count > 10
                ]
                if high_failure_validators:
                    pattern_analysis["optimization_opportunities"].append(
                        f"High failure validators: {', '.join(high_failure_validators)}"
                    )
            
            self.logger.info(f"Validation pattern analysis completed")
            return pattern_analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze validation patterns: {e}")
            return {}
    
    def optimize_validation_performance(self) -> Dict[str, Any]:
        """Optimize validation performance based on pattern analysis"""
        try:
            # Get pattern analysis
            patterns = self.analyze_validation_patterns()
            
            optimization_plan = {
                "current_performance": patterns.get("success_rate", 0.0),
                "recommended_strategies": [],
                "validator_optimizations": [],
                "rule_consolidations": []
            }
            
            # Recommend strategies based on patterns
            if patterns.get("success_rate", 0.0) < 0.7:
                optimization_plan["recommended_strategies"].append("cascading")
                optimization_plan["recommended_strategies"].append("adaptive")
            elif patterns.get("success_rate", 0.0) > 0.9:
                optimization_plan["recommended_strategies"].append("parallel")
            
            # Validator-specific optimizations
            high_failure_validators = patterns.get("failure_patterns", {})
            for validator_name, failure_count in high_failure_validators.items():
                if failure_count > 10:
                    optimization_plan["validator_optimizations"].append({
                        "validator": validator_name,
                        "action": "review_rules",
                        "priority": "high"
                    })
            
            # Rule consolidation opportunities
            if len(high_failure_validators) > 3:
                optimization_plan["rule_consolidations"].append({
                    "action": "consolidate_similar_rules",
                    "target_validators": list(high_failure_validators.keys()),
                    "expected_benefit": "reduced_failures"
                })
            
            self.logger.info(f"Validation performance optimization completed")
            return optimization_plan
            
        except Exception as e:
            self.logger.error(f"Failed to optimize validation performance: {e}")
            return {}
