#!/usr/bin/env python3
"""
JavaScript V2 Testing Coordinator - Agent Cellphone V2
====================================================

Advanced testing coordination system for JavaScript V2 compliance validation.
Provides comprehensive testing protocols, parallel processing, caching mechanisms,
and custom validator registration for JavaScript-specific validation rules.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
import concurrent.futures
import time
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import os

from .validation_models import ValidationIssue, ValidationSeverity
from .javascript_v2_compliance_validator import JavaScriptV2ComplianceValidator, JavaScriptFileMetrics


class TestingStrategy(Enum):
    """JavaScript V2 testing strategies."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CACHED = "cached"
    PIPELINE = "pipeline"
    HYBRID = "hybrid"


@dataclass
class ValidationCache:
    """Validation result cache."""
    file_hash: str
    validation_results: List[ValidationIssue]
    timestamp: datetime
    file_size: int
    last_modified: float


@dataclass
class ComponentValidationProfile:
    """Component validation profile."""
    component_name: str
    file_path: str
    original_lines: int
    refactored_lines: int
    reduction_percent: float
    priority_score: float
    validation_status: str = "pending"
    validation_results: List[ValidationIssue] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)


class JavaScriptV2TestingCoordinator:
    """
    Advanced JavaScript V2 testing coordination system.
    
    Provides comprehensive testing capabilities for:
    - Modular architecture validation patterns
    - Parallel processing for component validation
    - Caching mechanisms for performance optimization
    - Custom validator registration for JavaScript-specific rules
    - Comprehensive metrics collection and reporting
    """

    def __init__(self, max_workers: int = 4, cache_size: int = 1000):
        """Initialize the JavaScript V2 testing coordinator."""
        self.validator = JavaScriptV2ComplianceValidator()
        self.max_workers = max_workers
        self.cache_size = cache_size
        self.validation_cache: Dict[str, ValidationCache] = {}
        self.component_profiles: Dict[str, ComponentValidationProfile] = {}
        self.custom_validators: Dict[str, Callable[[str, str], List[ValidationIssue]]] = {}
        self.testing_metrics: Dict[str, Any] = {
            "total_validations": 0,
            "cache_hits": 0,
            "parallel_validations": 0,
            "validation_times": [],
            "components_validated": 0
        }

    def register_custom_validator(
        self,
        name: str,
        validator_func: Callable[[str, str], List[ValidationIssue]]
    ) -> None:
        """
        Register a custom JavaScript validator.
        
        Args:
            name: Name of the custom validator
            validator_func: Function that takes (file_path, content) and returns validation issues
        """
        if not callable(validator_func):
            raise ValueError("Custom validator must be a callable function")
        
        self.custom_validators[name] = validator_func
        print(f"Custom validator '{name}' registered for JavaScript V2 compliance testing")

    async def coordinate_v2_compliance_testing(
        self,
        component_files: List[Dict[str, Any]],
        testing_strategy: TestingStrategy = TestingStrategy.HYBRID,
        enable_caching: bool = True,
        enable_parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Coordinate comprehensive V2 compliance testing for JavaScript components.
        
        Args:
            component_files: List of component file information
            testing_strategy: Testing strategy to use
            enable_caching: Enable validation result caching
            enable_parallel: Enable parallel processing
            
        Returns:
            Comprehensive testing results and metrics
        """
        start_time = time.time()
        testing_results = {
            "timestamp": datetime.now().isoformat(),
            "testing_strategy": testing_strategy.value,
            "components_tested": len(component_files),
            "validation_results": {},
            "performance_metrics": {},
            "recommendations": [],
            "summary": {}
        }

        try:
            # Initialize component profiles
            await self._initialize_component_profiles(component_files)

            # Execute testing based on strategy
            if testing_strategy == TestingStrategy.SEQUENTIAL:
                await self._execute_sequential_testing(component_files, enable_caching)
            elif testing_strategy == TestingStrategy.PARALLEL:
                await self._execute_parallel_testing(component_files, enable_caching)
            elif testing_strategy == TestingStrategy.CACHED:
                await self._execute_cached_testing(component_files)
            elif testing_strategy == TestingStrategy.PIPELINE:
                await self._execute_pipeline_testing(component_files, enable_caching)
            elif testing_strategy == TestingStrategy.HYBRID:
                await self._execute_hybrid_testing(component_files, enable_caching, enable_parallel)

            # Collect validation results
            testing_results["validation_results"] = await self._collect_validation_results()

            # Generate performance metrics
            testing_results["performance_metrics"] = await self._generate_performance_metrics()

            # Generate recommendations
            testing_results["recommendations"] = await self._generate_testing_recommendations()

            # Generate summary
            testing_results["summary"] = await self._generate_testing_summary()

        except Exception as e:
            testing_results["error"] = f"V2 compliance testing coordination failed: {str(e)}"

        end_time = time.time()
        testing_results["total_execution_time_ms"] = (end_time - start_time) * 1000

        return testing_results

    async def _initialize_component_profiles(self, component_files: List[Dict[str, Any]]) -> None:
        """Initialize component validation profiles."""
        for component in component_files:
            component_name = component.get("name", "unknown")
            file_path = component.get("file_path", "")
            original_lines = component.get("original_lines", 0)
            refactored_lines = component.get("refactored_lines", 0)
            
            reduction_percent = 0.0
            if original_lines > 0:
                reduction_percent = ((original_lines - refactored_lines) / original_lines) * 100
            
            # Calculate priority score based on reduction and file size
            priority_score = reduction_percent + (refactored_lines / 10.0)
            
            self.component_profiles[component_name] = ComponentValidationProfile(
                component_name=component_name,
                file_path=file_path,
                original_lines=original_lines,
                refactored_lines=refactored_lines,
                reduction_percent=reduction_percent,
                priority_score=priority_score
            )

    async def _execute_sequential_testing(
        self,
        component_files: List[Dict[str, Any]],
        enable_caching: bool
    ) -> None:
        """Execute sequential validation testing."""
        for component in component_files:
            file_path = component.get("file_path", "")
            component_name = component.get("name", "unknown")
            
            if file_path and os.path.exists(file_path):
                await self._validate_component(file_path, component_name, enable_caching)

    async def _execute_parallel_testing(
        self,
        component_files: List[Dict[str, Any]],
        enable_caching: bool
    ) -> None:
        """Execute parallel validation testing."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for component in component_files:
                file_path = component.get("file_path", "")
                component_name = component.get("name", "unknown")
                
                if file_path and os.path.exists(file_path):
                    future = executor.submit(
                        asyncio.run,
                        self._validate_component(file_path, component_name, enable_caching)
                    )
                    futures.append(future)
            
            # Wait for all validations to complete
            concurrent.futures.wait(futures)
            self.testing_metrics["parallel_validations"] += len(futures)

    async def _execute_cached_testing(self, component_files: List[Dict[str, Any]]) -> None:
        """Execute cached validation testing."""
        for component in component_files:
            file_path = component.get("file_path", "")
            component_name = component.get("name", "unknown")
            
            if file_path and os.path.exists(file_path):
                await self._validate_component(file_path, component_name, enable_caching=True)

    async def _execute_pipeline_testing(
        self,
        component_files: List[Dict[str, Any]],
        enable_caching: bool
    ) -> None:
        """Execute pipeline validation testing."""
        # Pipeline: validate in batches with overlap for efficiency
        batch_size = max(1, len(component_files) // self.max_workers)
        
        for i in range(0, len(component_files), batch_size):
            batch = component_files[i:i + batch_size]
            batch_futures = []
            
            for component in batch:
                file_path = component.get("file_path", "")
                component_name = component.get("name", "unknown")
                
                if file_path and os.path.exists(file_path):
                    future = asyncio.create_task(
                        self._validate_component(file_path, component_name, enable_caching)
                    )
                    batch_futures.append(future)
            
            # Wait for batch to complete before starting next batch
            await asyncio.gather(*batch_futures)

    async def _execute_hybrid_testing(
        self,
        component_files: List[Dict[str, Any]],
        enable_caching: bool,
        enable_parallel: bool
    ) -> None:
        """Execute hybrid validation testing (combines multiple strategies)."""
        # Sort components by priority
        sorted_components = sorted(
            component_files,
            key=lambda x: self.component_profiles.get(x.get("name", ""), ComponentValidationProfile("", "", 0, 0, 0, 0)).priority_score,
            reverse=True
        )
        
        # High priority components: sequential for thoroughness
        high_priority = sorted_components[:len(sorted_components)//2]
        await self._execute_sequential_testing(high_priority, enable_caching)
        
        # Lower priority components: parallel for efficiency
        if enable_parallel and len(sorted_components) > 1:
            low_priority = sorted_components[len(sorted_components)//2:]
            await self._execute_parallel_testing(low_priority, enable_caching)

    async def _validate_component(
        self,
        file_path: str,
        component_name: str,
        enable_caching: bool
    ) -> None:
        """Validate a single component with caching support."""
        start_time = time.time()
        
        # Check cache first if enabled
        if enable_caching:
            file_hash = self._calculate_file_hash(file_path)
            if file_hash in self.validation_cache:
                cache_entry = self.validation_cache[file_hash]
                # Check if cache is still valid (file hasn't changed)
                if (os.path.getmtime(file_path) <= cache_entry.last_modified and
                    os.path.getsize(file_path) == cache_entry.file_size):
                    self.testing_metrics["cache_hits"] += 1
                    self.component_profiles[component_name].validation_results = cache_entry.validation_results
                    self.component_profiles[component_name].validation_status = "cached"
                    return

        # Perform validation
        validation_results = []
        
        # Standard V2 compliance validation
        standard_issues = self.validator.validate_javascript_file(file_path)
        validation_results.extend(standard_issues)
        
        # Custom validators
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for validator_name, validator_func in self.custom_validators.items():
                try:
                    custom_issues = validator_func(file_path, content)
                    validation_results.extend(custom_issues)
                except Exception as e:
                    validation_results.append(ValidationIssue(
                        rule_id=f"custom_validator_error_{validator_name}",
                        rule_name=f"Custom Validator Error: {validator_name}",
                        severity=ValidationSeverity.ERROR,
                        message=f"Custom validator '{validator_name}' failed: {str(e)}",
                        details={"validator_name": validator_name, "error": str(e)},
                        timestamp=datetime.now(),
                        component="javascript_v2_testing_coordinator"
                    ))
        except Exception as e:
            validation_results.append(ValidationIssue(
                rule_id="file_read_error",
                rule_name="File Read Error",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to read file {file_path}: {str(e)}",
                details={"file_path": file_path, "error": str(e)},
                timestamp=datetime.now(),
                component="javascript_v2_testing_coordinator"
            ))

        # Update component profile
        self.component_profiles[component_name].validation_results = validation_results
        self.component_profiles[component_name].validation_status = "completed"

        # Cache results if enabled
        if enable_caching:
            file_hash = self._calculate_file_hash(file_path)
            self.validation_cache[file_hash] = ValidationCache(
                file_hash=file_hash,
                validation_results=validation_results,
                timestamp=datetime.now(),
                file_size=os.path.getsize(file_path),
                last_modified=os.path.getmtime(file_path)
            )
            
            # Maintain cache size limit
            if len(self.validation_cache) > self.cache_size:
                # Remove oldest entries
                oldest_key = min(self.validation_cache.keys(), 
                               key=lambda k: self.validation_cache[k].timestamp)
                del self.validation_cache[oldest_key]

        # Update metrics
        end_time = time.time()
        validation_time = (end_time - start_time) * 1000
        self.testing_metrics["validation_times"].append(validation_time)
        self.testing_metrics["total_validations"] += 1
        self.testing_metrics["components_validated"] += 1

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate hash for file caching."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return hashlib.md5(file_path.encode()).hexdigest()

    async def _collect_validation_results(self) -> Dict[str, Any]:
        """Collect comprehensive validation results."""
        results = {
            "component_results": {},
            "summary_statistics": {
                "total_components": len(self.component_profiles),
                "completed_validations": 0,
                "cached_validations": 0,
                "total_issues": 0,
                "critical_issues": 0,
                "warning_issues": 0,
                "info_issues": 0
            }
        }

        for component_name, profile in self.component_profiles.items():
            component_result = {
                "file_path": profile.file_path,
                "original_lines": profile.original_lines,
                "refactored_lines": profile.refactored_lines,
                "reduction_percent": profile.reduction_percent,
                "priority_score": profile.priority_score,
                "validation_status": profile.validation_status,
                "issue_count": len(profile.validation_results),
                "issues": [
                    {
                        "rule_id": issue.rule_id,
                        "rule_name": issue.rule_name,
                        "severity": issue.severity.value,
                        "message": issue.message,
                        "details": issue.details
                    }
                    for issue in profile.validation_results
                ]
            }
            
            results["component_results"][component_name] = component_result
            
            # Update summary statistics
            if profile.validation_status in ["completed", "cached"]:
                results["summary_statistics"]["completed_validations"] += 1
                if profile.validation_status == "cached":
                    results["summary_statistics"]["cached_validations"] += 1
                
                results["summary_statistics"]["total_issues"] += len(profile.validation_results)
                
                for issue in profile.validation_results:
                    if issue.severity == ValidationSeverity.ERROR:
                        results["summary_statistics"]["critical_issues"] += 1
                    elif issue.severity == ValidationSeverity.WARNING:
                        results["summary_statistics"]["warning_issues"] += 1
                    else:
                        results["summary_statistics"]["info_issues"] += 1

        return results

    async def _generate_performance_metrics(self) -> Dict[str, Any]:
        """Generate comprehensive performance metrics."""
        metrics = self.testing_metrics.copy()
        
        if metrics["validation_times"]:
            metrics["avg_validation_time_ms"] = sum(metrics["validation_times"]) / len(metrics["validation_times"])
            metrics["min_validation_time_ms"] = min(metrics["validation_times"])
            metrics["max_validation_time_ms"] = max(metrics["validation_times"])
        else:
            metrics["avg_validation_time_ms"] = 0
            metrics["min_validation_time_ms"] = 0
            metrics["max_validation_time_ms"] = 0
        
        metrics["cache_hit_rate"] = (
            (metrics["cache_hits"] / metrics["total_validations"] * 100)
            if metrics["total_validations"] > 0 else 0
        )
        
        metrics["parallel_efficiency"] = (
            (metrics["parallel_validations"] / metrics["total_validations"] * 100)
            if metrics["total_validations"] > 0 else 0
        )
        
        return metrics

    async def _generate_testing_recommendations(self) -> List[str]:
        """Generate testing recommendations based on results."""
        recommendations = []
        
        # Check for high-priority components with issues
        high_priority_components = [
            name for name, profile in self.component_profiles.items()
            if profile.priority_score > 50 and len(profile.validation_results) > 0
        ]
        
        if high_priority_components:
            recommendations.append(
                f"Focus on resolving issues in high-priority components: {', '.join(high_priority_components)}"
            )
        
        # Check cache performance
        cache_hit_rate = self.testing_metrics.get("cache_hit_rate", 0)
        if cache_hit_rate < 30:
            recommendations.append("Consider optimizing caching strategy to improve validation performance")
        
        # Check parallel processing efficiency
        parallel_efficiency = self.testing_metrics.get("parallel_efficiency", 0)
        if parallel_efficiency < 50:
            recommendations.append("Increase parallel processing utilization for better performance")
        
        # General recommendations
        recommendations.append("Implement continuous validation in CI/CD pipeline")
        recommendations.append("Establish validation baselines and regression detection")
        recommendations.append("Regular validation performance reviews and optimization")
        
        return recommendations

    async def _generate_testing_summary(self) -> Dict[str, Any]:
        """Generate comprehensive testing summary."""
        total_components = len(self.component_profiles)
        completed_components = sum(1 for p in self.component_profiles.values() 
                                 if p.validation_status in ["completed", "cached"])
        
        total_issues = sum(len(p.validation_results) for p in self.component_profiles.values())
        critical_issues = sum(
            len([i for i in p.validation_results if i.severity == ValidationSeverity.ERROR])
            for p in self.component_profiles.values()
        )
        
        compliance_rate = ((total_components - critical_issues) / total_components * 100) if total_components > 0 else 0
        
        return {
            "total_components": total_components,
            "completed_components": completed_components,
            "completion_rate": (completed_components / total_components * 100) if total_components > 0 else 0,
            "total_issues": total_issues,
            "critical_issues": critical_issues,
            "v2_compliance_rate": compliance_rate,
            "testing_efficiency": self.testing_metrics.get("cache_hit_rate", 0),
            "performance_score": self._calculate_performance_score()
        }

    def _calculate_performance_score(self) -> float:
        """Calculate overall testing performance score."""
        score = 0.0
        
        # Cache hit rate contribution (30%)
        cache_hit_rate = self.testing_metrics.get("cache_hit_rate", 0)
        score += (cache_hit_rate / 100) * 30
        
        # Parallel efficiency contribution (25%)
        parallel_efficiency = self.testing_metrics.get("parallel_efficiency", 0)
        score += (parallel_efficiency / 100) * 25
        
        # Validation speed contribution (25%)
        avg_time = self.testing_metrics.get("avg_validation_time_ms", 0)
        if avg_time > 0:
            speed_score = max(0, 100 - (avg_time / 10))  # Penalty for slow validation
            score += (speed_score / 100) * 25
        
        # Component coverage contribution (20%)
        total_components = len(self.component_profiles)
        completed_components = sum(1 for p in self.component_profiles.values() 
                                 if p.validation_status in ["completed", "cached"])
        coverage_rate = (completed_components / total_components * 100) if total_components > 0 else 0
        score += (coverage_rate / 100) * 20
        
        return min(100.0, score)

    def get_testing_coordination_summary(self) -> str:
        """Get human-readable testing coordination summary."""
        summary = f"JavaScript V2 Testing Coordination Summary:\n"
        summary += f"Components Profiled: {len(self.component_profiles)}\n"
        summary += f"Total Validations: {self.testing_metrics['total_validations']}\n"
        summary += f"Cache Hits: {self.testing_metrics['cache_hits']}\n"
        summary += f"Cache Hit Rate: {self.testing_metrics.get('cache_hit_rate', 0):.1f}%\n"
        summary += f"Parallel Validations: {self.testing_metrics['parallel_validations']}\n"
        summary += f"Average Validation Time: {self.testing_metrics.get('avg_validation_time_ms', 0):.2f}ms\n"
        summary += f"Custom Validators: {len(self.custom_validators)}\n"
        summary += f"Performance Score: {self._calculate_performance_score():.1f}/100\n"
        
        return summary
