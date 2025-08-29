#!/usr/bin/env python3
"""
Refactoring Performance Benchmark - Agent Cellphone V2
=====================================================

Performance benchmarking and efficiency measurement tools for refactoring operations.
Follows V2 standards: OOP, SRP, clean code.

Author: Agent-5 (REFACTORING TOOL PREPARATION MANAGER)
License: MIT
"""

import logging
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

from src.core.base_manager import BaseManager


@dataclass
class BenchmarkResult:
    """Result of a performance benchmark"""
    benchmark_id: str
    operation_name: str
    file_path: str
    execution_time: float  # seconds
    memory_usage: float  # MB
    cpu_usage: float  # percentage
    lines_processed: int
    efficiency_score: float  # 0-100
    improvement_percentage: float
    timestamp: datetime
    metadata: Dict[str, Any] = None


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics"""
    total_benchmarks: int = 0
    average_execution_time: float = 0.0
    average_memory_usage: float = 0.0
    average_cpu_usage: float = 0.0
    average_efficiency_score: float = 0.0
    total_improvement: float = 0.0
    fastest_operation: Optional[str] = None
    slowest_operation: Optional[str] = None
    most_efficient_operation: Optional[str] = None


@dataclass
class BenchmarkSuite:
    """Collection of related benchmarks"""
    suite_id: str
    name: str
    description: str
    benchmarks: List[Dict[str, Any]]
    target_files: List[str]
    expected_improvements: Dict[str, float]
    created_at: datetime
    execution_count: int = 0
    average_suite_score: float = 0.0


class RefactoringPerformanceBenchmark(BaseManager):
    """
    Refactoring Performance Benchmark - Measures efficiency gains and performance
    
    This benchmark system provides:
    - Performance measurement for refactoring operations
    - Efficiency gain calculations
    - Memory and CPU usage monitoring
    - Comparative analysis between before/after states
    - Automated benchmarking suites
    """
    
    def __init__(self, workspace_path: str = None):
        super().__init__()
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.benchmark_results: Dict[str, BenchmarkResult] = {}
        self.benchmark_suites: Dict[str, BenchmarkSuite] = {}
        self.metrics = PerformanceMetrics()
        self.execution_pool = ThreadPoolExecutor(max_workers=4)
        self.is_monitoring = False
        
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Load existing benchmark data
        self._load_benchmark_data()
    
    def _load_benchmark_data(self):
        """Load benchmark data from storage"""
        try:
            # Load benchmark results
            results_file = self.workspace_path / "data" / "benchmark_results.json"
            if results_file.exists():
                with open(results_file, 'r') as f:
                    data = json.load(f)
                    # Convert back to BenchmarkResult objects
                    for result_data in data.get("benchmark_results", []):
                        result = BenchmarkResult(**result_data)
                        self.benchmark_results[result.benchmark_id] = result
            
            # Load benchmark suites
            suites_file = self.workspace_path / "data" / "benchmark_suites.json"
            if suites_file.exists():
                with open(suites_file, 'r') as f:
                    data = json.load(f)
                    # Convert back to BenchmarkSuite objects
                    for suite_data in data.get("benchmark_suites", []):
                        suite = BenchmarkSuite(**suite_data)
                        self.benchmark_suites[suite.suite_id] = suite
                        
        except Exception as e:
            self.logger.warning(f"Could not load benchmark data: {e}")
    
    def _save_benchmark_data(self):
        """Save benchmark data to storage"""
        try:
            # Save benchmark results
            results_file = self.workspace_path / "data" / "benchmark_results.json"
            results_file.parent.mkdir(parents=True, exist_ok=True)
            
            results_data = {
                "benchmark_results": [
                    asdict(result) for result in self.benchmark_results.values()
                ]
            }
            
            with open(results_file, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            # Save benchmark suites
            suites_file = self.workspace_path / "data" / "benchmark_suites.json"
            suites_file.parent.mkdir(parents=True, exist_ok=True)
            
            suites_data = {
                "benchmark_suites": [
                    asdict(suite) for suite in self.benchmark_suites.values()
                ]
            }
            
            with open(suites_file, 'w') as f:
                json.dump(suites_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Could not save benchmark data: {e}")
    
    def create_benchmark_suite(self, name: str, description: str, 
                              benchmarks: List[Dict[str, Any]], 
                              target_files: List[str],
                              expected_improvements: Dict[str, float]) -> str:
        """Create a new benchmark suite"""
        suite_id = f"SUITE_{int(time.time())}_{hash(name) % 10000}"
        
        suite = BenchmarkSuite(
            suite_id=suite_id,
            name=name,
            description=description,
            benchmarks=benchmarks,
            target_files=target_files,
            expected_improvements=expected_improvements,
            created_at=datetime.now()
        )
        
        self.benchmark_suites[suite_id] = suite
        self._save_benchmark_data()
        
        self.logger.info(f"Created benchmark suite {suite_id}: {name}")
        return suite_id
    
    def run_single_benchmark(self, operation_name: str, file_path: str, 
                            operation_func: Callable, 
                            before_state: Dict[str, Any] = None,
                            after_state: Dict[str, Any] = None) -> BenchmarkResult:
        """Run a single performance benchmark"""
        benchmark_id = f"BENCH_{int(time.time())}_{hash(operation_name) % 10000}"
        
        # Start monitoring
        start_time = time.time()
        start_memory = self._get_memory_usage()
        start_cpu = self._get_cpu_usage()
        
        try:
            # Execute operation
            result = operation_func()
            
            # End monitoring
            end_time = time.time()
            end_memory = self._get_memory_usage()
            end_cpu = self._get_cpu_usage()
            
            # Calculate metrics
            execution_time = end_time - start_time
            memory_usage = end_memory - start_memory
            cpu_usage = (start_cpu + end_cpu) / 2  # Average
            
            # Calculate efficiency score
            efficiency_score = self._calculate_efficiency_score(
                execution_time, memory_usage, cpu_usage, before_state, after_state
            )
            
            # Calculate improvement percentage
            improvement_percentage = self._calculate_improvement_percentage(
                before_state, after_state
            )
            
            # Create benchmark result
            benchmark_result = BenchmarkResult(
                benchmark_id=benchmark_id,
                operation_name=operation_name,
                file_path=file_path,
                execution_time=execution_time,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                lines_processed=result.get("lines_processed", 0),
                efficiency_score=efficiency_score,
                improvement_percentage=improvement_percentage,
                timestamp=datetime.now(),
                metadata=result
            )
            
            # Store result
            self.benchmark_results[benchmark_id] = benchmark_result
            self._save_benchmark_data()
            
            # Update metrics
            self._update_performance_metrics(benchmark_result)
            
            self.logger.info(f"Benchmark {benchmark_id} completed: {operation_name}")
            return benchmark_result
            
        except Exception as e:
            self.logger.error(f"Benchmark {benchmark_id} failed: {e}")
            # Create failed result
            failed_result = BenchmarkResult(
                benchmark_id=benchmark_id,
                operation_name=operation_name,
                file_path=file_path,
                execution_time=0.0,
                memory_usage=0.0,
                cpu_usage=0.0,
                lines_processed=0,
                efficiency_score=0.0,
                improvement_percentage=0.0,
                timestamp=datetime.now(),
                metadata={"error": str(e)}
            )
            
            self.benchmark_results[benchmark_id] = failed_result
            self._save_benchmark_data()
            return failed_result
    
    def run_benchmark_suite(self, suite_id: str) -> Dict[str, Any]:
        """Run a complete benchmark suite"""
        if suite_id not in self.benchmark_suites:
            return {"error": f"Benchmark suite {suite_id} not found"}
        
        suite = self.benchmark_suites[suite_id]
        suite.execution_count += 1
        
        self.logger.info(f"Running benchmark suite: {suite.name}")
        
        results = []
        total_score = 0.0
        
        for benchmark in suite.benchmarks:
            try:
                # Extract benchmark parameters
                operation_name = benchmark.get("operation_name")
                file_path = benchmark.get("file_path")
                operation_type = benchmark.get("operation_type")
                
                if not all([operation_name, file_path, operation_type]):
                    self.logger.warning(f"Incomplete benchmark config: {benchmark}")
                    continue
                
                # Create operation function based on type
                operation_func = self._create_operation_function(operation_type, benchmark)
                
                # Get before state
                before_state = self._capture_file_state(file_path)
                
                # Run benchmark
                result = self.run_single_benchmark(
                    operation_name, file_path, operation_func, before_state
                )
                
                results.append(result)
                total_score += result.efficiency_score
                
            except Exception as e:
                self.logger.error(f"Benchmark execution failed: {e}")
                results.append({
                    "error": str(e),
                    "benchmark": benchmark
                })
        
        # Calculate suite score
        if results and all(hasattr(r, 'efficiency_score') for r in results):
            suite.average_suite_score = total_score / len(results)
        
        self._save_benchmark_data()
        
        return {
            "suite_id": suite_id,
            "suite_name": suite.name,
            "execution_count": suite.execution_count,
            "results": results,
            "average_score": suite.average_suite_score,
            "total_benchmarks": len(results)
        }
    
    def _create_operation_function(self, operation_type: str, 
                                  benchmark_config: Dict[str, Any]) -> Callable:
        """Create operation function based on benchmark configuration"""
        if operation_type == "file_analysis":
            return lambda: self._benchmark_file_analysis(benchmark_config)
        elif operation_type == "module_extraction":
            return lambda: self._benchmark_module_extraction(benchmark_config)
        elif operation_type == "duplicate_consolidation":
            return lambda: self._benchmark_duplicate_consolidation(benchmark_config)
        elif operation_type == "architecture_optimization":
            return lambda: self._benchmark_architecture_optimization(benchmark_config)
        else:
            return lambda: {"error": f"Unknown operation type: {operation_type}"}
    
    def _benchmark_file_analysis(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Benchmark file analysis operation"""
        file_path = config.get("file_path")
        if not file_path:
            return {"error": "Missing file_path"}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Perform analysis
            analysis = {
                "line_count": len(lines),
                "class_count": content.count('class '),
                "function_count": content.count('def '),
                "import_count": content.count('import '),
                "complexity_score": self._calculate_complexity_score(content)
            }
            
            return {
                "lines_processed": len(lines),
                "analysis_result": analysis,
                "success": True
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _benchmark_module_extraction(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Benchmark module extraction operation"""
        file_path = config.get("file_path")
        if not file_path:
            return {"error": "Missing file_path"}
        
        try:
            # Simulate module extraction
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Create extraction plan
            extraction_plan = self._create_extraction_plan_simulation(lines)
            
            # Simulate extraction
            extracted_modules = []
            for module_info in extraction_plan["modules"]:
                extracted_modules.append({
                    "name": module_info["name"],
                    "lines": module_info["estimated_lines"],
                    "type": module_info["type"]
                })
            
            return {
                "lines_processed": len(lines),
                "extraction_plan": extraction_plan,
                "extracted_modules": extracted_modules,
                "success": True
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _benchmark_duplicate_consolidation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Benchmark duplicate consolidation operation"""
        # Simulate duplicate consolidation
        duplicates = [
            {"pattern": "api_key_manager.py", "files": ["file1.py", "file2.py"]},
            {"pattern": "workflow_manager.py", "files": ["file3.py", "file4.py"]}
        ]
        
        consolidation_plan = {
            "targets": len(duplicates),
            "estimated_effort": len(duplicates) * 0.5,
            "expected_reduction": len(duplicates) * 100
        }
        
        return {
            "lines_processed": len(duplicates) * 100,  # Estimate
            "duplicates_found": len(duplicates),
            "consolidation_plan": consolidation_plan,
            "success": True
        }
    
    def _benchmark_architecture_optimization(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Benchmark architecture optimization operation"""
        # Simulate architecture optimization
        patterns = [
            {"name": "BaseManager Inheritance", "quality": 85},
            {"name": "Module Extraction", "quality": 90},
            {"name": "Single Responsibility", "quality": 88}
        ]
        
        optimization_plan = {
            "patterns_analyzed": len(patterns),
            "optimization_targets": len([p for p in patterns if p["quality"] < 90]),
            "expected_improvement": sum(95 - p["quality"] for p in patterns if p["quality"] < 90)
        }
        
        return {
            "lines_processed": len(patterns) * 50,  # Estimate
            "patterns_analyzed": patterns,
            "optimization_plan": optimization_plan,
            "success": True
        }
    
    def _create_extraction_plan_simulation(self, lines: List[str]) -> Dict[str, Any]:
        """Create extraction plan simulation for benchmarking"""
        line_count = len(lines)
        
        if line_count < 300:
            return {"modules": [], "estimated_effort": 0.0}
        
        modules = []
        estimated_effort = 0.0
        
        if line_count > 500:
            modules.append({
                "name": "core_logic",
                "type": "core_functionality",
                "estimated_lines": 150,
                "estimated_effort": 2.0
            })
            estimated_effort += 2.0
        
        if line_count > 400:
            modules.append({
                "name": "utilities",
                "type": "helper_functions",
                "estimated_lines": 100,
                "estimated_effort": 1.5
            })
            estimated_effort += 1.5
        
        if line_count > 600:
            modules.append({
                "name": "configuration",
                "type": "config_management",
                "estimated_lines": 80,
                "estimated_effort": 1.0
            })
            estimated_effort += 1.0
        
        return {
            "modules": modules,
            "estimated_effort": estimated_effort
        }
    
    def _calculate_complexity_score(self, content: str) -> float:
        """Calculate complexity score for content"""
        # Simple complexity calculation
        complexity_factors = {
            'if ': 1,
            'for ': 1,
            'while ': 1,
            'try:': 1,
            'except': 1,
            'class ': 2,
            'def ': 1,
            'import ': 0.5,
            'from ': 0.5
        }
        
        score = 0
        for factor, weight in complexity_factors.items():
            score += content.count(factor) * weight
        
        return min(score / 10, 10.0)  # Normalize to 0-10
    
    def _capture_file_state(self, file_path: str) -> Dict[str, Any]:
        """Capture current state of a file for comparison"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {"error": "File not found"}
            
            stat = file_path_obj.stat()
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            return {
                "file_size": stat.st_size,
                "line_count": len(lines),
                "class_count": content.count('class '),
                "function_count": content.count('def '),
                "import_count": content.count('import '),
                "complexity_score": self._calculate_complexity_score(content),
                "last_modified": stat.st_mtime
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_efficiency_score(self, execution_time: float, memory_usage: float,
                                  cpu_usage: float, before_state: Dict[str, Any],
                                  after_state: Dict[str, Any]) -> float:
        """Calculate efficiency score based on performance metrics"""
        # Base score starts at 100
        score = 100.0
        
        # Penalize slow execution
        if execution_time > 5.0:  # More than 5 seconds
            score -= min(execution_time - 5.0, 30)  # Max 30 point penalty
        
        # Penalize high memory usage
        if memory_usage > 100:  # More than 100MB
            score -= min(memory_usage / 10, 20)  # Max 20 point penalty
        
        # Penalize high CPU usage
        if cpu_usage > 80:  # More than 80%
            score -= min(cpu_usage - 80, 20)  # Max 20 point penalty
        
        # Bonus for improvements
        if before_state and after_state:
            if "line_count" in before_state and "line_count" in after_state:
                reduction = before_state["line_count"] - after_state["line_count"]
                if reduction > 0:
                    score += min(reduction / 10, 20)  # Max 20 point bonus
        
        return max(0.0, min(100.0, score))
    
    def _calculate_improvement_percentage(self, before_state: Dict[str, Any],
                                        after_state: Dict[str, Any]) -> float:
        """Calculate improvement percentage between before/after states"""
        if not before_state or not after_state:
            return 0.0
        
        if "line_count" in before_state and "line_count" in after_state:
            before_lines = before_state["line_count"]
            after_lines = after_state["line_count"]
            
            if before_lines > 0:
                return ((before_lines - after_lines) / before_lines) * 100
        
        return 0.0
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage (simplified)"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0  # psutil not available
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage (simplified)"""
        try:
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0.0  # psutil not available
    
    def _update_performance_metrics(self, result: BenchmarkResult):
        """Update aggregated performance metrics"""
        self.metrics.total_benchmarks += 1
        
        # Update averages
        if self.metrics.total_benchmarks == 1:
            self.metrics.average_execution_time = result.execution_time
            self.metrics.average_memory_usage = result.memory_usage
            self.metrics.average_cpu_usage = result.cpu_usage
            self.metrics.average_efficiency_score = result.efficiency_score
        else:
            # Calculate running averages
            n = self.metrics.total_benchmarks
            self.metrics.average_execution_time = (
                (self.metrics.average_execution_time * (n-1) + result.execution_time) / n
            )
            self.metrics.average_memory_usage = (
                (self.metrics.average_memory_usage * (n-1) + result.memory_usage) / n
            )
            self.metrics.average_cpu_usage = (
                (self.metrics.average_cpu_usage * (n-1) + result.cpu_usage) / n
            )
            self.metrics.average_efficiency_score = (
                (self.metrics.average_efficiency_score * (n-1) + result.efficiency_score) / n
            )
        
        # Update totals
        self.metrics.total_improvement += result.improvement_percentage
        
        # Update fastest/slowest
        if (not self.metrics.fastest_operation or 
            result.execution_time < self.benchmark_results[self.metrics.fastest_operation].execution_time):
            self.metrics.fastest_operation = result.benchmark_id
        
        if (not self.metrics.slowest_operation or 
            result.execution_time > self.benchmark_results[self.metrics.slowest_operation].execution_time):
            self.metrics.slowest_operation = result.benchmark_id
        
        # Update most efficient
        if (not self.metrics.most_efficient_operation or 
            result.efficiency_score > self.benchmark_results[self.metrics.most_efficient_operation].efficiency_score):
            self.metrics.most_efficient_operation = result.benchmark_id
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        return {
            "performance_metrics": asdict(self.metrics),
            "recent_benchmarks": [
                asdict(result) for result in 
                sorted(self.benchmark_results.values(), 
                       key=lambda x: x.timestamp, reverse=True)[:10]
            ],
            "benchmark_suites": len(self.benchmark_suites),
            "total_results": len(self.benchmark_results),
            "system_status": "operational" if not self.is_monitoring else "monitoring"
        }
    
    def start_performance_monitoring(self):
        """Start continuous performance monitoring"""
        if self.is_monitoring:
            return {"error": "Performance monitoring already active"}
        
        self.is_monitoring = True
        self.logger.info("Starting performance monitoring...")
        
        # Start monitoring thread
        monitoring_thread = threading.Thread(target=self._performance_monitor_loop, daemon=True)
        monitoring_thread.start()
        
        return {"success": True, "message": "Performance monitoring started"}
    
    def stop_performance_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        self.logger.info("Stopping performance monitoring...")
        return {"success": True, "message": "Performance monitoring stopped"}
    
    def _performance_monitor_loop(self):
        """Main performance monitoring loop"""
        while self.is_monitoring:
            try:
                # Perform system health check
                system_health = self._check_system_health()
                
                # Log if issues detected
                if system_health["status"] != "healthy":
                    self.logger.warning(f"System health issue: {system_health}")
                
                # Sleep before next check
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Performance monitor error: {e}")
                time.sleep(120)  # Wait longer on error
    
    def _check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        try:
            # Check memory usage
            memory_usage = self._get_memory_usage()
            memory_status = "healthy" if memory_usage < 1000 else "warning"  # 1GB threshold
            
            # Check CPU usage
            cpu_usage = self._get_cpu_usage()
            cpu_status = "healthy" if cpu_usage < 80 else "warning"  # 80% threshold
            
            # Overall status
            overall_status = "healthy"
            if memory_status == "warning" or cpu_status == "warning":
                overall_status = "warning"
            
            return {
                "status": overall_status,
                "memory": {"usage": memory_usage, "status": memory_status},
                "cpu": {"usage": cpu_usage, "status": cpu_status},
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now()
            }
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_performance_monitoring()
        self.execution_pool.shutdown(wait=True)
        self._save_benchmark_data()
        super().cleanup()
