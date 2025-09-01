#!/usr/bin/env python3
"""
Enhanced CLI Validation Framework - Agent Cellphone V2
====================================================

Advanced validation framework for enhanced CLI validation capabilities.
Provides comprehensive validation strategies, parallel processing, caching,
custom validator registration, and metrics collection for CLI components.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
import time
import hashlib
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from .validation_models import ValidationIssue, ValidationSeverity
from .cli_modular_refactoring_validator import CLIModularRefactoringValidator, CLIModuleProfile
from .javascript_v2_compliance_validator import JavaScriptV2ComplianceValidator
from .repository_pattern_validator import RepositoryPatternValidator


class ValidationStrategy(Enum):
    """Types of validation strategies."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CACHED = "cached"
    PIPELINE = "pipeline"
    HYBRID = "hybrid"


@dataclass
class ValidationCache:
    """Validation result cache for performance optimization."""
    file_hash: str
    validation_results: Dict[str, Any]
    timestamp: datetime
    ttl_seconds: int = 3600  # 1 hour default TTL


@dataclass
class ValidationMetrics:
    """Comprehensive validation metrics."""
    total_files: int = 0
    validated_files: int = 0
    cached_files: int = 0
    parallel_workers: int = 0
    total_execution_time: float = 0.0
    average_validation_time: float = 0.0
    cache_hit_rate: float = 0.0
    validation_success_rate: float = 0.0
    custom_validators_used: int = 0


@dataclass
class EnhancedValidationResult:
    """Enhanced validation execution result."""
    strategy: ValidationStrategy
    files_validated: List[str]
    validation_results: Dict[str, Any]
    metrics: ValidationMetrics
    achievements: List[str]
    recommendations: List[str]
    execution_time: float
    timestamp: datetime


class EnhancedCLIValidationFramework:
    """
    Enhanced CLI validation framework with advanced capabilities.
    
    Provides comprehensive validation features:
    - Modular architecture validation patterns
    - Parallel processing for component validation
    - Caching mechanisms for performance optimization
    - Custom validator registration for JavaScript-specific rules
    - Comprehensive metrics collection and reporting
    """

    def __init__(self, max_workers: int = 4, cache_size: int = 1000):
        """
        Initialize the enhanced CLI validation framework.
        
        Args:
            max_workers: Maximum number of parallel workers
            cache_size: Maximum cache size for validation results
        """
        self.cli_validator = CLIModularRefactoringValidator()
        self.javascript_validator = JavaScriptV2ComplianceValidator()
        self.repository_validator = RepositoryPatternValidator()
        
        self.max_workers = max_workers
        self.cache_size = cache_size
        self.validation_cache: Dict[str, ValidationCache] = {}
        self.custom_validators: Dict[str, Callable] = {}
        self.validation_metrics = ValidationMetrics()
        
        # Validation strategies configuration
        self.strategy_configs = {
            ValidationStrategy.SEQUENTIAL: {
                "description": "Sequential validation of files one by one",
                "use_case": "Small file sets, debugging, resource-constrained environments"
            },
            ValidationStrategy.PARALLEL: {
                "description": "Parallel validation using multiple workers",
                "use_case": "Large file sets, performance optimization, multi-core systems"
            },
            ValidationStrategy.CACHED: {
                "description": "Validation with caching for repeated files",
                "use_case": "Incremental validation, CI/CD pipelines, development workflows"
            },
            ValidationStrategy.PIPELINE: {
                "description": "Pipeline validation with staged processing",
                "use_case": "Complex validation workflows, multi-stage validation"
            },
            ValidationStrategy.HYBRID: {
                "description": "Combination of multiple strategies",
                "use_case": "Optimal performance across different scenarios"
            }
        }

    def register_custom_validator(self, name: str, validator_func: Callable) -> None:
        """
        Register a custom validator for JavaScript-specific rules.
        
        Args:
            name: Name of the custom validator
            validator_func: Validator function that takes file_path and returns validation results
        """
        self.custom_validators[name] = validator_func
        print(f"Custom validator '{name}' registered successfully")

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file content for caching."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.sha256(content).hexdigest()
        except Exception:
            return ""

    def _get_cached_result(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get cached validation result if available and not expired."""
        file_hash = self._calculate_file_hash(file_path)
        if file_hash in self.validation_cache:
            cache_entry = self.validation_cache[file_hash]
            if (datetime.now() - cache_entry.timestamp).total_seconds() < cache_entry.ttl_seconds:
                return cache_entry.validation_results
            else:
                # Remove expired cache entry
                del self.validation_cache[file_hash]
        return None

    def _cache_result(self, file_path: str, validation_results: Dict[str, Any], ttl_seconds: int = 3600) -> None:
        """Cache validation result for future use."""
        file_hash = self._calculate_file_hash(file_path)
        
        # Implement LRU cache eviction if cache is full
        if len(self.validation_cache) >= self.cache_size:
            # Remove oldest entry
            oldest_key = min(self.validation_cache.keys(), 
                           key=lambda k: self.validation_cache[k].timestamp)
            del self.validation_cache[oldest_key]
        
        self.validation_cache[file_hash] = ValidationCache(
            file_hash=file_hash,
            validation_results=validation_results,
            timestamp=datetime.now(),
            ttl_seconds=ttl_seconds
        )

    async def validate_file_enhanced(self, file_path: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Enhanced file validation with caching and custom validators.
        
        Args:
            file_path: Path to the file to validate
            use_cache: Whether to use cached results
            
        Returns:
            Comprehensive validation results
        """
        start_time = time.time()
        
        # Check cache first
        if use_cache:
            cached_result = self._get_cached_result(file_path)
            if cached_result:
                self.validation_metrics.cached_files += 1
                return cached_result
        
        validation_results = {
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "validation_results": {},
            "custom_validations": {},
            "metrics": {},
            "achievements": [],
            "recommendations": []
        }
        
        try:
            # CLI modular validation
            if file_path.endswith('.py'):
                cli_issues = self.cli_validator.validate_cli_modular_refactoring(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                module_profile = self.cli_validator._analyze_cli_module_profile(file_path, content)
                refactoring_score = self.cli_validator.calculate_refactoring_score(module_profile)
                
                validation_results["validation_results"]["cli_modular"] = {
                    "issues": len(cli_issues),
                    "refactoring_score": refactoring_score,
                    "v2_compliant": module_profile.v2_compliant,
                    "reduction_percent": module_profile.reduction_percent,
                    "extracted_components": len(module_profile.extracted_components),
                    "factory_implementations": len(module_profile.factory_implementations),
                    "service_layers": len(module_profile.service_layers),
                    "dependency_injections": len(module_profile.dependency_injections),
                    "modular_structures": len(module_profile.modular_structures)
                }
                
                # Check for exceptional achievements
                if module_profile.reduction_percent >= 80:
                    validation_results["achievements"].append(f"EXCEPTIONAL: {module_profile.reduction_percent:.1f}% reduction")
                elif module_profile.reduction_percent >= 50:
                    validation_results["achievements"].append(f"OUTSTANDING: {module_profile.reduction_percent:.1f}% reduction")
                elif module_profile.reduction_percent >= 30:
                    validation_results["achievements"].append(f"GOOD: {module_profile.reduction_percent:.1f}% reduction")
            
            # JavaScript V2 validation
            elif file_path.endswith('.js'):
                js_issues = self.javascript_validator.validate_javascript_file(file_path)
                js_metrics = self.javascript_validator.analyze_javascript_file(file_path)
                
                validation_results["validation_results"]["javascript_v2"] = {
                    "issues": len(js_issues),
                    "line_count": js_metrics.line_count,
                    "v2_compliant": js_metrics.line_count <= 300,
                    "modular_architecture": js_metrics.modular_architecture_score,
                    "es6_modules": js_metrics.es6_modules_score,
                    "dependency_injection": js_metrics.dependency_injection_score,
                    "performance_optimization": js_metrics.performance_optimization_score,
                    "error_handling": js_metrics.error_handling_score,
                    "documentation": js_metrics.documentation_score,
                    "overall_score": js_metrics.overall_score
                }
                
                # Check for achievements
                if js_metrics.overall_score >= 90:
                    validation_results["achievements"].append(f"EXCELLENT: {js_metrics.overall_score:.1f}/100 V2 compliance score")
                elif js_metrics.overall_score >= 80:
                    validation_results["achievements"].append(f"GOOD: {js_metrics.overall_score:.1f}/100 V2 compliance score")
            
            # Repository pattern validation
            repo_issues = self.repository_validator.validate_repository_pattern(file_path)
            validation_results["validation_results"]["repository_pattern"] = {
                "issues": len(repo_issues),
                "pattern_compliant": len(repo_issues) == 0
            }
            
            # Custom validators
            for validator_name, validator_func in self.custom_validators.items():
                try:
                    custom_result = validator_func(file_path)
                    validation_results["custom_validations"][validator_name] = custom_result
                    self.validation_metrics.custom_validators_used += 1
                except Exception as e:
                    validation_results["custom_validations"][validator_name] = {"error": str(e)}
            
            # Calculate execution metrics
            execution_time = time.time() - start_time
            validation_results["metrics"] = {
                "execution_time_ms": execution_time * 1000,
                "file_size_bytes": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                "validation_strategies_used": len(validation_results["validation_results"])
            }
            
            # Cache the result
            if use_cache:
                self._cache_result(file_path, validation_results)
            
            self.validation_metrics.validated_files += 1
            
        except Exception as e:
            validation_results["error"] = f"Enhanced validation failed: {str(e)}"
        
        return validation_results

    async def validate_files_parallel(self, file_paths: List[str], use_cache: bool = True) -> Dict[str, Any]:
        """
        Parallel validation of multiple files using ThreadPoolExecutor.
        
        Args:
            file_paths: List of file paths to validate
            use_cache: Whether to use cached results
            
        Returns:
            Comprehensive parallel validation results
        """
        start_time = time.time()
        
        results = {
            "strategy": ValidationStrategy.PARALLEL.value,
            "files_validated": [],
            "total_files": len(file_paths),
            "parallel_workers": min(self.max_workers, len(file_paths)),
            "validation_results": {},
            "metrics": ValidationMetrics(),
            "achievements": [],
            "recommendations": [],
            "execution_time": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Execute parallel validation
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all validation tasks
            future_to_file = {
                executor.submit(self.validate_file_enhanced, file_path, use_cache): file_path
                for file_path in file_paths
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    file_result = future.result()
                    results["files_validated"].append(file_path)
                    results["validation_results"][file_path] = file_result
                    
                    # Collect achievements
                    if "achievements" in file_result:
                        results["achievements"].extend(file_result["achievements"])
                    
                except Exception as e:
                    results["validation_results"][file_path] = {"error": str(e)}
        
        # Calculate metrics
        results["execution_time"] = time.time() - start_time
        results["metrics"].total_files = len(file_paths)
        results["metrics"].validated_files = len(results["files_validated"])
        results["metrics"].parallel_workers = self.max_workers
        results["metrics"].total_execution_time = results["execution_time"]
        results["metrics"].average_validation_time = results["execution_time"] / len(file_paths) if file_paths else 0
        results["metrics"].validation_success_rate = (len(results["files_validated"]) / len(file_paths) * 100) if file_paths else 0
        
        # Generate recommendations
        if results["metrics"].validation_success_rate < 100:
            results["recommendations"].append("Address validation failures for 100% success rate")
        if results["metrics"].average_validation_time > 1.0:
            results["recommendations"].append("Consider optimizing validation performance")
        
        return results

    async def validate_files_cached(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Cached validation of multiple files with cache optimization.
        
        Args:
            file_paths: List of file paths to validate
            
        Returns:
            Comprehensive cached validation results
        """
        start_time = time.time()
        
        results = {
            "strategy": ValidationStrategy.CACHED.value,
            "files_validated": [],
            "cached_files": [],
            "total_files": len(file_paths),
            "validation_results": {},
            "metrics": ValidationMetrics(),
            "achievements": [],
            "recommendations": [],
            "execution_time": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check cache for all files first
        for file_path in file_paths:
            cached_result = self._get_cached_result(file_path)
            if cached_result:
                results["cached_files"].append(file_path)
                results["validation_results"][file_path] = cached_result
                if "achievements" in cached_result:
                    results["achievements"].extend(cached_result["achievements"])
            else:
                # Validate file and cache result
                file_result = await self.validate_file_enhanced(file_path, use_cache=True)
                results["files_validated"].append(file_path)
                results["validation_results"][file_path] = file_result
                if "achievements" in file_result:
                    results["achievements"].extend(file_result["achievements"])
        
        # Calculate metrics
        results["execution_time"] = time.time() - start_time
        results["metrics"].total_files = len(file_paths)
        results["metrics"].validated_files = len(results["files_validated"])
        results["metrics"].cached_files = len(results["cached_files"])
        results["metrics"].total_execution_time = results["execution_time"]
        results["metrics"].cache_hit_rate = (len(results["cached_files"]) / len(file_paths) * 100) if file_paths else 0
        results["metrics"].validation_success_rate = 100.0  # All files processed
        
        # Generate recommendations
        if results["metrics"].cache_hit_rate < 50:
            results["recommendations"].append("Consider increasing cache TTL for better hit rate")
        if results["metrics"].cache_hit_rate > 80:
            results["achievements"].append(f"EXCELLENT: {results['metrics'].cache_hit_rate:.1f}% cache hit rate")
        
        return results

    async def validate_files_hybrid(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Hybrid validation combining multiple strategies for optimal performance.
        
        Args:
            file_paths: List of file paths to validate
            
        Returns:
            Comprehensive hybrid validation results
        """
        start_time = time.time()
        
        results = {
            "strategy": ValidationStrategy.HYBRID.value,
            "files_validated": [],
            "cached_files": [],
            "total_files": len(file_paths),
            "validation_results": {},
            "metrics": ValidationMetrics(),
            "achievements": [],
            "recommendations": [],
            "execution_time": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Phase 1: Check cache for all files
        files_to_validate = []
        for file_path in file_paths:
            cached_result = self._get_cached_result(file_path)
            if cached_result:
                results["cached_files"].append(file_path)
                results["validation_results"][file_path] = cached_result
                if "achievements" in cached_result:
                    results["achievements"].extend(cached_result["achievements"])
            else:
                files_to_validate.append(file_path)
        
        # Phase 2: Parallel validation for remaining files
        if files_to_validate:
            parallel_results = await self.validate_files_parallel(files_to_validate, use_cache=True)
            results["files_validated"].extend(parallel_results["files_validated"])
            results["validation_results"].update(parallel_results["validation_results"])
            results["achievements"].extend(parallel_results["achievements"])
        
        # Calculate metrics
        results["execution_time"] = time.time() - start_time
        results["metrics"].total_files = len(file_paths)
        results["metrics"].validated_files = len(results["files_validated"])
        results["metrics"].cached_files = len(results["cached_files"])
        results["metrics"].parallel_workers = self.max_workers
        results["metrics"].total_execution_time = results["execution_time"]
        results["metrics"].cache_hit_rate = (len(results["cached_files"]) / len(file_paths) * 100) if file_paths else 0
        results["metrics"].validation_success_rate = 100.0  # All files processed
        
        # Generate recommendations
        if results["metrics"].cache_hit_rate > 70:
            results["achievements"].append(f"OPTIMIZED: {results['metrics'].cache_hit_rate:.1f}% cache hit rate with parallel processing")
        if results["metrics"].total_execution_time < 5.0:
            results["achievements"].append(f"EFFICIENT: {results['metrics'].total_execution_time:.2f}s total execution time")
        
        return results

    def get_validation_summary(self) -> str:
        """Get comprehensive validation framework summary."""
        summary = f"Enhanced CLI Validation Framework Summary:\n"
        summary += f"Max Workers: {self.max_workers}\n"
        summary += f"Cache Size: {self.cache_size}\n"
        summary += f"Cached Entries: {len(self.validation_cache)}\n"
        summary += f"Custom Validators: {len(self.custom_validators)}\n"
        summary += f"Validation Metrics:\n"
        summary += f"  Total Files: {self.validation_metrics.total_files}\n"
        summary += f"  Validated Files: {self.validation_metrics.validated_files}\n"
        summary += f"  Cached Files: {self.validation_metrics.cached_files}\n"
        summary += f"  Custom Validators Used: {self.validation_metrics.custom_validators_used}\n"
        return summary

    def clear_cache(self) -> None:
        """Clear the validation cache."""
        self.validation_cache.clear()
        print("Validation cache cleared")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if not self.validation_cache:
            return {"cache_size": 0, "entries": 0}
        
        now = datetime.now()
        active_entries = sum(1 for cache in self.validation_cache.values() 
                           if (now - cache.timestamp).total_seconds() < cache.ttl_seconds)
        
        return {
            "cache_size": len(self.validation_cache),
            "active_entries": active_entries,
            "expired_entries": len(self.validation_cache) - active_entries,
            "max_cache_size": self.cache_size
        }
