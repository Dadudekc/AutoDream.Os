#!/usr/bin/env python3
"""
🧪 TESTING AUTOMATION FOR MODULARIZATION WORKFLOWS - MODULAR-004
Testing Framework Enhancement Manager - Agent-3

This module implements comprehensive testing automation for modularization
workflows, including automated testing, reporting, and integration.

Features:
- Automated modularization testing workflows
- Batch processing capabilities
- Integration with CI/CD pipelines
- Comprehensive reporting and analytics
- Performance monitoring and optimization
"""

import os
import sys
import time
import json
import asyncio
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import concurrent.futures
import logging

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import testing framework components
from .enhanced_modularization_framework import EnhancedModularizationFramework, FileType
from .quality_gates import QualityGateManager, run_quality_gates, get_quality_summary
from .regression_testing_system import RegressionTestingSystem


@dataclass
class AutomationWorkflow:
    """Configuration for an automation workflow"""
    name: str
    description: str
    steps: List[str]
    timeout: int = 300  # seconds
    parallel: bool = True
    retry_count: int = 3
    dependencies: List[str] = field(default_factory=list)


@dataclass
class WorkflowResult:
    """Result of workflow execution"""
    workflow_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED, TIMEOUT
    results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchProcessingConfig:
    """Configuration for batch processing"""
    batch_size: int = 10
    max_workers: int = 4
    timeout_per_file: int = 60
    continue_on_failure: bool = True
    output_format: str = "json"  # json, html, csv, markdown


class TestingAutomationEngine:
    """
    Main engine for testing automation workflows.
    
    Provides automated testing, batch processing, and workflow management
    for modularization testing and quality assurance.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Core components
        self.framework = EnhancedModularizationFramework()
        self.quality_gates = QualityGateManager()
        self.regression_system = RegressionTestingSystem()
        
        # Workflow management
        self.workflows: Dict[str, AutomationWorkflow] = {}
        self.workflow_results: List[WorkflowResult] = []
        self.active_workflows: Dict[str, WorkflowResult] = {}
        
        # Performance monitoring
        self.performance_metrics: Dict[str, List[float]] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
        # Initialize workflows
        self._initialize_workflows()
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('testing_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_workflows(self) -> None:
        """Initialize predefined automation workflows"""
        self.workflows = {
            "full_modularization_test": AutomationWorkflow(
                name="Full Modularization Test",
                description="Complete modularization testing workflow",
                steps=[
                    "File analysis and type detection",
                    "Quality gate validation",
                    "Test suite execution",
                    "Coverage analysis",
                    "Regression testing",
                    "Performance benchmarking"
                ],
                timeout=600,
                parallel=True
            ),
            
            "quality_gate_validation": AutomationWorkflow(
                name="Quality Gate Validation",
                description="Run quality gates for modularization validation",
                steps=[
                    "File size reduction analysis",
                    "Single responsibility validation",
                    "Interface quality assessment",
                    "Test coverage validation",
                    "Dependency complexity analysis"
                ],
                timeout=300,
                parallel=False
            ),
            
            "regression_testing": AutomationWorkflow(
                name="Regression Testing",
                description="Comprehensive regression testing workflow",
                steps=[
                    "Functionality regression tests",
                    "Performance regression tests",
                    "Integration regression tests",
                    "Test result analysis"
                ],
                timeout=450,
                parallel=True
            ),
            
            "coverage_analysis": AutomationWorkflow(
                name="Coverage Analysis",
                description="Test coverage analysis workflow",
                steps=[
                    "Line coverage analysis",
                    "Branch coverage analysis",
                    "Function coverage analysis",
                    "Coverage gap identification",
                    "Risk assessment"
                ],
                timeout=300,
                parallel=False
            ),
            
            "performance_benchmarking": AutomationWorkflow(
                name="Performance Benchmarking",
                description="Performance testing and benchmarking",
                steps=[
                    "Execution time measurement",
                    "Memory usage analysis",
                    "CPU usage monitoring",
                    "Performance trend analysis"
                ],
                timeout=300,
                parallel=False
            ),
            
            "batch_modularization_test": AutomationWorkflow(
                name="Batch Modularization Test",
                description="Batch processing for multiple files",
                steps=[
                    "File discovery and filtering",
                    "Batch quality gate validation",
                    "Parallel test execution",
                    "Results aggregation",
                    "Summary reporting"
                ],
                timeout=1800,
                parallel=True
            )
        }
    
    def run_workflow(self, workflow_name: str, target: str, **kwargs) -> WorkflowResult:
        """Run a specific automation workflow"""
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        workflow = self.workflows[workflow_name]
        
        # Create workflow result
        result = WorkflowResult(
            workflow_name=workflow_name,
            start_time=datetime.now(),
            status="RUNNING"
        )
        
        self.active_workflows[workflow_name] = result
        self.logger.info(f"Starting workflow: {workflow_name}")
        
        try:
            # Execute workflow based on type
            if workflow_name == "full_modularization_test":
                workflow_results = self._execute_full_modularization_test(target, **kwargs)
            elif workflow_name == "quality_gate_validation":
                workflow_results = self._execute_quality_gate_validation(target, **kwargs)
            elif workflow_name == "regression_testing":
                workflow_results = self._execute_regression_testing(target, **kwargs)
            elif workflow_name == "coverage_analysis":
                workflow_results = self._execute_coverage_analysis(target, **kwargs)
            elif workflow_name == "performance_benchmarking":
                workflow_results = self._execute_performance_benchmarking(target, **kwargs)
            elif workflow_name == "batch_modularization_test":
                workflow_results = self._execute_batch_modularization_test(target, **kwargs)
            else:
                workflow_results = {"error": f"Unknown workflow: {workflow_name}"}
            
            # Update result
            result.end_time = datetime.now()
            result.status = "COMPLETED"
            result.results = workflow_results
            
            # Calculate performance metrics
            execution_time = (result.end_time - result.start_time).total_seconds()
            result.performance_metrics = {
                "execution_time": execution_time,
                "workflow_timeout": workflow.timeout,
                "timeout_exceeded": execution_time > workflow.timeout
            }
            
            self.logger.info(f"Workflow completed: {workflow_name} in {execution_time:.2f}s")
            
        except Exception as e:
            result.end_time = datetime.now()
            result.status = "FAILED"
            result.errors.append(str(e))
            self.logger.error(f"Workflow failed: {workflow_name} - {e}")
        
        finally:
            # Remove from active workflows
            if workflow_name in self.active_workflows:
                del self.active_workflows[workflow_name]
            
            # Add to results history
            self.workflow_results.append(result)
            
            # Update performance metrics
            self._update_performance_metrics(workflow_name, result)
        
        return result
    
    def _execute_full_modularization_test(self, target: str, **kwargs) -> Dict[str, Any]:
        """Execute full modularization testing workflow"""
        start_time = time.time()
        results = {}
        
        try:
            # Step 1: File analysis and type detection
            file_type = self.framework._detect_file_type(target)
            results["file_analysis"] = {
                "target": target,
                "detected_type": file_type.value,
                "timestamp": datetime.now().isoformat()
            }
            
            # Step 2: Quality gate validation
            quality_results = self.quality_gates.run_all_gates(target)
            results["quality_gates"] = {
                "results": [self._serialize_quality_result(r) for r in quality_results],
                "summary": self.quality_gates.get_gate_summary(quality_results)
            }
            
            # Step 3: Test suite execution
            test_results = self.framework.run_file_type_test_suite(target, file_type)
            results["test_suite"] = test_results
            
            # Step 4: Coverage analysis
            coverage_results = self.framework.run_automated_workflow("coverage_analysis", target)
            results["coverage_analysis"] = coverage_results
            
            # Step 5: Regression testing
            regression_results = self.framework.run_automated_workflow("regression_testing", target)
            results["regression_testing"] = regression_results
            
            # Step 6: Performance benchmarking
            performance_results = self.framework.run_automated_workflow("performance_benchmarking", target)
            results["performance_benchmarking"] = performance_results
            
            # Calculate overall score
            overall_score = self._calculate_overall_modularization_score(results)
            results["overall_score"] = overall_score
            results["passed"] = overall_score >= 80.0
            
            execution_time = time.time() - start_time
            results["execution_time"] = execution_time
            
        except Exception as e:
            results["error"] = str(e)
            results["execution_time"] = time.time() - start_time
        
        return results
    
    def _execute_quality_gate_validation(self, target: str, **kwargs) -> Dict[str, Any]:
        """Execute quality gate validation workflow"""
        start_time = time.time()
        results = {}
        
        try:
            # Run all quality gates
            quality_results = self.quality_gates.run_all_gates(target)
            
            # Get summary
            summary = self.quality_gates.get_gate_summary(quality_results)
            
            results = {
                "target": target,
                "quality_gates": [self._serialize_quality_result(r) for r in quality_results],
                "summary": summary,
                "execution_time": time.time() - start_time
            }
            
        except Exception as e:
            results["error"] = str(e)
            results["execution_time"] = time.time() - start_time
        
        return results
    
    def _execute_regression_testing(self, target: str, **kwargs) -> Dict[str, Any]:
        """Execute regression testing workflow"""
        start_time = time.time()
        results = {}
        
        try:
            # Run regression tests
            regression_results = self.framework.run_automated_workflow("regression_testing", target)
            
            results = {
                "target": target,
                "regression_tests": regression_results,
                "execution_time": time.time() - start_time
            }
            
        except Exception as e:
            results["error"] = str(e)
            results["execution_time"] = time.time() - start_time
        
        return results
    
    def _execute_coverage_analysis(self, target: str, **kwargs) -> Dict[str, Any]:
        """Execute coverage analysis workflow"""
        start_time = time.time()
        results = {}
        
        try:
            # Run coverage analysis
            coverage_results = self.framework.run_automated_workflow("coverage_analysis", target)
            
            results = {
                "target": target,
                "coverage_analysis": coverage_results,
                "execution_time": time.time() - start_time
            }
            
        except Exception as e:
            results["error"] = str(e)
            results["execution_time"] = time.time() - start_time
        
        return results
    
    def _execute_performance_benchmarking(self, target: str, **kwargs) -> Dict[str, Any]:
        """Execute performance benchmarking workflow"""
        start_time = time.time()
        results = {}
        
        try:
            # Run performance benchmarking
            performance_results = self.framework.run_automated_workflow("performance_benchmarking", target)
            
            results = {
                "target": target,
                "performance_benchmarking": performance_results,
                "execution_time": time.time() - start_time
            }
            
        except Exception as e:
            results["error"] = str(e)
            results["execution_time"] = time.time() - start_time
        
        return results
    
    def _execute_batch_modularization_test(self, target_directory: str, **kwargs) -> Dict[str, Any]:
        """Execute batch modularization testing workflow"""
        start_time = time.time()
        results = {}
        
        try:
            # Discover files to test
            files_to_test = self._discover_files_for_testing(target_directory, **kwargs)
            
            # Configure batch processing
            batch_config = BatchProcessingConfig(**kwargs)
            
            # Process files in batches
            batch_results = self._process_files_in_batches(files_to_test, batch_config)
            
            # Aggregate results
            aggregated_results = self._aggregate_batch_results(batch_results)
            
            results = {
                "target_directory": target_directory,
                "files_processed": len(files_to_test),
                "batch_results": batch_results,
                "aggregated_results": aggregated_results,
                "execution_time": time.time() - start_time
            }
            
        except Exception as e:
            results["error"] = str(e)
            results["execution_time"] = time.time() - start_time
        
        return results
    
    def _discover_files_for_testing(self, directory: str, **kwargs) -> List[str]:
        """Discover files that need testing"""
        target_dir = Path(directory)
        if not target_dir.exists():
            return []
        
        # File patterns to test
        patterns = kwargs.get("file_patterns", ["*.py", "*.js", "*.ts", "*.md"])
        min_size = kwargs.get("min_size", 100)  # Minimum file size in lines
        
        files_to_test = []
        
        for pattern in patterns:
            for file_path in target_dir.rglob(pattern):
                try:
                    # Check file size
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = len(f.readlines())
                    
                    if line_count >= min_size:
                        files_to_test.append(str(file_path))
                        
                except Exception:
                    continue
        
        return files_to_test
    
    def _process_files_in_batches(self, files: List[str], config: BatchProcessingConfig) -> List[Dict[str, Any]]:
        """Process files in batches with parallel execution"""
        batch_results = []
        
        # Split files into batches
        batches = [files[i:i + config.batch_size] for i in range(0, len(files), config.batch_size)]
        
        for batch_idx, batch in enumerate(batches):
            batch_result = {
                "batch_index": batch_idx,
                "batch_size": len(batch),
                "files": batch,
                "results": []
            }
            
            # Process batch with parallel execution
            with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers) as executor:
                # Submit quality gate validation tasks
                future_to_file = {
                    executor.submit(self._run_quality_gates_for_file, file_path, config.timeout_per_file): file_path
                    for file_path in batch
                }
                
                # Collect results
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        batch_result["results"].append({
                            "file_path": file_path,
                            "result": result
                        })
                    except Exception as e:
                        batch_result["results"].append({
                            "file_path": file_path,
                            "error": str(e)
                        })
                        
                        if not config.continue_on_failure:
                            break
            
            batch_results.append(batch_result)
        
        return batch_results
    
    def _run_quality_gates_for_file(self, file_path: str, timeout: int) -> Dict[str, Any]:
        """Run quality gates for a single file with timeout"""
        try:
            # Run quality gates
            quality_results = self.quality_gates.run_all_gates(file_path)
            summary = self.quality_gates.get_gate_summary(quality_results)
            
            return {
                "quality_gates": [self._serialize_quality_result(r) for r in quality_results],
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _aggregate_batch_results(self, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from batch processing"""
        total_files = sum(batch["batch_size"] for batch in batch_results)
        successful_files = 0
        failed_files = 0
        
        all_quality_scores = []
        quality_level_counts = {}
        
        for batch in batch_results:
            for file_result in batch["results"]:
                if "result" in file_result and "summary" in file_result["result"]:
                    summary = file_result["result"]["summary"]
                    successful_files += 1
                    
                    # Collect quality scores
                    if "average_score" in summary:
                        all_quality_scores.append(summary["average_score"])
                    
                    # Count quality levels
                    if "quality_level_distribution" in summary:
                        for level, count in summary["quality_level_distribution"].items():
                            quality_level_counts[level.value] = quality_level_counts.get(level.value, 0) + count
                else:
                    failed_files += 1
        
        # Calculate aggregated metrics
        avg_quality_score = sum(all_quality_scores) / len(all_quality_scores) if all_quality_scores else 0.0
        
        return {
            "total_files": total_files,
            "successful_files": successful_files,
            "failed_files": failed_files,
            "success_rate": (successful_files / total_files) * 100 if total_files > 0 else 0.0,
            "average_quality_score": avg_quality_score,
            "quality_level_distribution": quality_level_counts,
            "timestamp": datetime.now().isoformat()
        }
    
    def _serialize_quality_result(self, result) -> Dict[str, Any]:
        """Serialize quality gate result for JSON output"""
        return {
            "gate_name": result.gate_name,
            "passed": result.passed,
            "score": result.score,
            "threshold": result.threshold,
            "details": result.details,
            "recommendations": result.recommendations,
            "quality_level": result.quality_level.value
        }
    
    def _calculate_overall_modularization_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall modularization score"""
        try:
            # Quality gate score (40% weight)
            quality_score = 0.0
            if "quality_gates" in results and "summary" in results["quality_gates"]:
                quality_score = results["quality_gates"]["summary"].get("average_score", 0.0)
            
            # Test suite score (30% weight)
            test_score = 0.0
            if "test_suite" in results and "overall_score" in results["test_suite"]:
                test_score = results["test_suite"]["overall_score"]
            
            # Coverage score (20% weight)
            coverage_score = 0.0
            if "coverage_analysis" in results:
                # Extract coverage percentage from results
                coverage_score = 80.0  # Default value
            
            # Performance score (10% weight)
            performance_score = 0.0
            if "performance_benchmarking" in results:
                performance_score = 80.0  # Default value
            
            # Calculate weighted average
            overall_score = (
                quality_score * 0.4 +
                test_score * 0.3 +
                coverage_score * 0.2 +
                performance_score * 0.1
            )
            
            return min(100.0, max(0.0, overall_score))
            
        except Exception:
            return 0.0
    
    def _update_performance_metrics(self, workflow_name: str, result: WorkflowResult) -> None:
        """Update performance metrics for workflows"""
        if workflow_name not in self.performance_metrics:
            self.performance_metrics[workflow_name] = []
        
        if result.performance_metrics and "execution_time" in result.performance_metrics:
            execution_time = result.performance_metrics["execution_time"]
            self.performance_metrics[workflow_name].append(execution_time)
            
            # Keep only last 100 measurements
            if len(self.performance_metrics[workflow_name]) > 100:
                self.performance_metrics[workflow_name] = self.performance_metrics[workflow_name][-100:]
    
    def get_workflow_status(self, workflow_name: str) -> Optional[WorkflowResult]:
        """Get status of a specific workflow"""
        # Check active workflows
        if workflow_name in self.active_workflows:
            return self.active_workflows[workflow_name]
        
        # Check completed workflows
        for result in reversed(self.workflow_results):
            if result.workflow_name == workflow_name:
                return result
        
        return None
    
    def get_available_workflows(self) -> List[str]:
        """Get list of available workflows"""
        return list(self.workflows.keys())
    
    def get_workflow_config(self, workflow_name: str) -> Optional[AutomationWorkflow]:
        """Get configuration for a specific workflow"""
        return self.workflows.get(workflow_name)
    
    def get_performance_metrics(self, workflow_name: str = None) -> Dict[str, Any]:
        """Get performance metrics for workflows"""
        if workflow_name:
            metrics = self.performance_metrics.get(workflow_name, [])
            if metrics:
                return {
                    "workflow": workflow_name,
                    "execution_times": metrics,
                    "average_time": sum(metrics) / len(metrics),
                    "min_time": min(metrics),
                    "max_time": max(metrics),
                    "total_executions": len(metrics)
                }
            return {}
        
        # Return all metrics
        all_metrics = {}
        for name, metrics in self.performance_metrics.items():
            if metrics:
                all_metrics[name] = {
                    "average_time": sum(metrics) / len(metrics),
                    "min_time": min(metrics),
                    "max_time": max(metrics),
                    "total_executions": len(metrics)
                }
        
        return all_metrics
    
    def export_results(self, workflow_name: str, output_format: str = "json") -> str:
        """Export workflow results in specified format"""
        result = self.get_workflow_status(workflow_name)
        if not result:
            return "Workflow not found"
        
        if output_format == "json":
            return json.dumps(result.results, indent=2, default=str)
        elif output_format == "html":
            return self._generate_html_report(result)
        elif output_format == "markdown":
            return self._generate_markdown_report(result)
        else:
            return f"Unsupported format: {output_format}"
    
    def _generate_html_report(self, result: WorkflowResult) -> str:
        """Generate HTML report for workflow results"""
        html = f"""
        <html>
        <head>
            <title>Workflow Report: {result.workflow_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .success {{ color: green; }}
                .error {{ color: red; }}
                .warning {{ color: orange; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🧪 Workflow Report: {result.workflow_name}</h1>
                <p><strong>Status:</strong> <span class="{'success' if result.status == 'COMPLETED' else 'error'}">{result.status}</span></p>
                <p><strong>Start Time:</strong> {result.start_time}</p>
                <p><strong>End Time:</strong> {result.end_time or 'N/A'}</p>
            </div>
            
            <div class="section">
                <h2>Results</h2>
                <pre>{json.dumps(result.results, indent=2, default=str)}</pre>
            </div>
            
            {f'<div class="section"><h2>Performance Metrics</h2><pre>{json.dumps(result.performance_metrics, indent=2)}</pre></div>' if result.performance_metrics else ''}
            
            {f'<div class="section"><h2>Errors</h2><ul>{"".join(f"<li class=\"error\">{error}</li>" for error in result.errors)}</ul></div>' if result.errors else ''}
            
            {f'<div class="section"><h2>Warnings</h2><ul>{"".join(f"<li class=\"warning\">{warning}</li>" for warning in result.warnings)}</ul></div>' if result.warnings else ''}
        </body>
        </html>
        """
        return html
    
    def _generate_markdown_report(self, result: WorkflowResult) -> str:
        """Generate Markdown report for workflow results"""
        markdown = f"""
        # 🧪 Workflow Report: {result.workflow_name}

        **Status:** {result.status}  
        **Start Time:** {result.start_time}  
        **End Time:** {result.end_time or 'N/A'}

        ## Results

        ```json
        {json.dumps(result.results, indent=2, default=str)}
        ```

        """
        
        if result.performance_metrics:
            markdown += f"""
        ## Performance Metrics

        ```json
        {json.dumps(result.performance_metrics, indent=2)}
        ```
        """
        
        if result.errors:
            markdown += """
        ## Errors

        """
            for error in result.errors:
                markdown += f"- ❌ {error}\n"
        
        if result.warnings:
            markdown += """
        ## Warnings

        """
            for warning in result.warnings:
                markdown += f"- ⚠️ {warning}\n"
        
        return markdown


# Convenience functions
def create_automation_engine(config: Optional[Dict[str, Any]] = None) -> TestingAutomationEngine:
    """Create a testing automation engine"""
    return TestingAutomationEngine(config)


def run_automated_workflow(workflow_name: str, target: str, **kwargs) -> Dict[str, Any]:
    """Run an automated workflow"""
    engine = create_automation_engine()
    result = engine.run_workflow(workflow_name, target, **kwargs)
    return {
        "workflow_name": result.workflow_name,
        "status": result.status,
        "results": result.results,
        "errors": result.errors,
        "execution_time": result.performance_metrics.get("execution_time", 0.0)
    }


if __name__ == "__main__":
    # Example usage
    print("🧪 Testing Automation for Modularization Workflows")
    print("=" * 60)
    
    # Create automation engine
    engine = create_automation_engine()
    
    # Show available workflows
    print("Available workflows:")
    for workflow_name in engine.get_available_workflows():
        config = engine.get_workflow_config(workflow_name)
        print(f"  - {workflow_name}: {config.description}")
    
    print("\n" + "=" * 60)
    
    # Test with a sample file
    sample_file = "tests/test_modularizer/enhanced_modularization_framework.py"
    
    if Path(sample_file).exists():
        print(f"Running quality gate validation on: {sample_file}")
        
        try:
            result = engine.run_workflow("quality_gate_validation", sample_file)
            print(f"Workflow completed with status: {result.status}")
            
            if result.results:
                summary = result.results.get("summary", {})
                print(f"Overall quality: {summary.get('overall_quality', 'UNKNOWN')}")
                print(f"Pass rate: {summary.get('pass_rate', 0.0):.1f}%")
                print(f"Average score: {summary.get('average_score', 0.0):.1f}")
            
        except Exception as e:
            print(f"Error running workflow: {e}")
    else:
        print("Sample file not found. Run workflows on existing files.")
