"""
Modularization Testing Automation Workflow

This module orchestrates the complete testing workflow for monolithic file
modularization, including analysis, quality gates, regression testing, and
comprehensive reporting.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse

from src.utils.logger import get_logger

# Import our testing framework components
from .modularization_testing_framework import (
    ModularizationTestFramework,
    create_modularization_test_suite
)
from .modularization_test_suites import (
    run_file_type_specific_tests,
    FileTypeTestSuiteFactory
)
from .quality_gates import (
    create_quality_gate_system,
    run_quality_gates
)
from .regression_testing_automation import (
    RegressionTestManager,
    run_regression_testing,
    run_regression_tests_for_file
)

logger = get_logger(__name__)


@dataclass
class ModularizationTestWorkflow:
    """Complete workflow for modularization testing."""
    
    source_directory: Path
    test_directories: List[Path]
    output_directory: Path
    config: Dict[str, Any]
    
    def __init__(self, source_dir: Path, test_dirs: List[Path], output_dir: Path = None, config: Dict[str, Any] = None):
        self.source_directory = Path(source_dir)
        self.test_directories = [Path(d) for d in test_dirs]
        self.output_directory = Path(output_dir) if output_dir else Path("reports")
        self.config = config or self._get_default_config()
        
        # Ensure output directory exists
        self.output_directory.mkdir(parents=True, exist_ok=True)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for the testing workflow."""
        return {
            "quality_gates": {
                "enabled": True,
                "strict_mode": False,
                "failure_threshold": 0.8  # 80% success rate required
            },
            "regression_testing": {
                "enabled": True,
                "max_workers": 4,
                "timeout": 300,
                "parallel_execution": True
            },
            "file_analysis": {
                "include_patterns": ["*.py"],
                "exclude_patterns": ["__pycache__/*", "*.pyc", "*.pyo"],
                "max_file_size_mb": 10
            },
            "reporting": {
                "generate_json": True,
                "generate_markdown": True,
                "generate_html": False,
                "include_performance_metrics": True,
                "include_recommendations": True
            }
        }
    
    def run_complete_workflow(self, target_files: List[Path] = None) -> Dict[str, Any]:
        """Run the complete modularization testing workflow."""
        logger.info("🚀 Starting Modularization Testing Workflow")
        workflow_start = datetime.now()
        
        # Step 1: File Discovery and Analysis
        logger.info("📁 Step 1: Discovering and analyzing target files...")
        if target_files is None:
            target_files = self._discover_target_files()
        
        if not target_files:
            logger.warning("No target files found for analysis")
            return {"status": "no_files", "message": "No target files found"}
        
        logger.info(f"📊 Found {len(target_files)} files for analysis")
        
        # Step 2: Run Modularization Analysis
        logger.info("🔍 Step 2: Running modularization analysis...")
        analysis_results = self._run_modularization_analysis(target_files)
        
        # Step 3: Run Quality Gates
        logger.info("🚪 Step 3: Executing quality gates...")
        quality_gate_results = self._run_quality_gates(target_files, analysis_results)
        
        # Step 4: Run File-Type Specific Tests
        logger.info("🧪 Step 4: Running file-type specific tests...")
        file_type_results = self._run_file_type_tests(target_files)
        
        # Step 5: Run Regression Testing
        logger.info("🔄 Step 5: Executing regression testing...")
        regression_results = self._run_regression_testing()
        
        # Step 6: Generate Comprehensive Report
        logger.info("📋 Step 6: Generating comprehensive report...")
        workflow_report = self._generate_workflow_report(
            target_files, analysis_results, quality_gate_results,
            file_type_results, regression_results, workflow_start
        )
        
        # Step 7: Save Results
        logger.info("💾 Step 7: Saving workflow results...")
        self._save_workflow_results(workflow_report)
        
        workflow_duration = (datetime.now() - workflow_start).total_seconds()
        logger.info(f"✅ Modularization Testing Workflow completed in {workflow_duration:.2f} seconds")
        
        return workflow_report
    
    def _discover_target_files(self) -> List[Path]:
        """Discover target files for modularization testing."""
        target_files = []
        
        for source_dir in [self.source_directory] + self.test_directories:
            if not source_dir.exists():
                continue
            
            for pattern in self.config["file_analysis"]["include_patterns"]:
                for file_path in source_dir.rglob(pattern):
                    # Apply exclude patterns
                    if self._should_exclude_file(file_path):
                        continue
                    
                    # Check file size
                    if file_path.stat().st_size > self.config["file_analysis"]["max_file_size_mb"] * 1024 * 1024:
                        logger.debug(f"Skipping large file: {file_path}")
                        continue
                    
                    target_files.append(file_path)
        
        return sorted(target_files, key=lambda x: x.stat().st_size, reverse=True)
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded from analysis."""
        file_str = str(file_path)
        
        for exclude_pattern in self.config["file_analysis"]["exclude_patterns"]:
            if exclude_pattern in file_str:
                return True
        
        return False
    
    def _run_modularization_analysis(self, target_files: List[Path]) -> Dict[str, Any]:
        """Run the main modularization analysis."""
        try:
            framework = ModularizationTestFramework(self.source_directory, self.test_directories[0] if self.test_directories else Path("tests"))
            analysis_results = framework.analyze_monolithic_files(target_files)
            
            # Save analysis results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analysis_file = self.output_directory / f"modularization_analysis_{timestamp}.json"
            framework.save_analysis_results(analysis_results, analysis_file)
            
            logger.info(f"📊 Modularization analysis completed. Results saved to {analysis_file}")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in modularization analysis: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _run_quality_gates(self, target_files: List[Path], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run quality gates for all target files."""
        if not self.config["quality_gates"]["enabled"]:
            logger.info("Quality gates disabled in configuration")
            return {"status": "disabled"}
        
        quality_gate_results = {
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": len(target_files),
            "files_passing_gates": 0,
            "files_failing_gates": 0,
            "overall_success_rate": 0.0,
            "file_results": []
        }
        
        total_success_rate = 0.0
        
        for file_path in target_files:
            try:
                # Get metrics for this file
                file_metrics = self._get_file_metrics(file_path, analysis_results)
                
                # Run quality gates
                gate_results, gate_summary = run_quality_gates(file_path, file_metrics)
                
                # Determine if file passes all gates
                critical_gates_passed = all(
                    gate.status.value == "PASSED" 
                    for gate in gate_results 
                    if gate.severity.value == "CRITICAL"
                )
                
                file_result = {
                    "file_path": str(file_path),
                    "gate_results": [asdict(gate) for gate in gate_results],
                    "gate_summary": asdict(gate_summary),
                    "passes_gates": critical_gates_passed,
                    "success_rate": gate_summary.weighted_score
                }
                
                quality_gate_results["file_results"].append(file_result)
                
                if critical_gates_passed:
                    quality_gate_results["files_passing_gates"] += 1
                else:
                    quality_gate_results["files_failing_gates"] += 1
                
                total_success_rate += gate_summary.weighted_score
                
            except Exception as e:
                logger.error(f"Error running quality gates for {file_path}: {e}")
                quality_gate_results["file_results"].append({
                    "file_path": str(file_path),
                    "error": str(e),
                    "passes_gates": False,
                    "success_rate": 0.0
                })
                quality_gate_results["files_failing_gates"] += 1
        
        # Calculate overall success rate
        if quality_gate_results["files_analyzed"] > 0:
            quality_gate_results["overall_success_rate"] = total_success_rate / quality_gate_results["files_analyzed"]
        
        # Save quality gate results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        quality_gate_file = self.output_directory / f"quality_gate_results_{timestamp}.json"
        with open(quality_gate_file, 'w', encoding='utf-8') as f:
            json.dump(quality_gate_results, f, indent=2, default=str)
        
        logger.info(f"🚪 Quality gates completed. Results saved to {quality_gate_file}")
        return quality_gate_results
    
    def _get_file_metrics(self, file_path: Path, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metrics for a specific file from analysis results."""
        for file_result in analysis_results.get("file_results", []):
            if file_result.get("file_path") == str(file_path):
                return file_result.get("metrics", {})
        
        # If not found in analysis results, return basic metrics
        return {
            "original_lines": len(file_path.read_text().splitlines()),
            "complexity_score": 0.0,
            "dependency_count": 0,
            "test_coverage": 0.0
        }
    
    def _run_file_type_tests(self, target_files: List[Path]) -> Dict[str, Any]:
        """Run file-type specific tests."""
        try:
            file_type_results = run_file_type_specific_tests(target_files)
            
            # Save file type results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_type_file = self.output_directory / f"file_type_analysis_{timestamp}.json"
            with open(file_type_file, 'w', encoding='utf-8') as f:
                json.dump(file_type_results, f, indent=2, default=str)
            
            logger.info(f"🧪 File-type specific tests completed. Results saved to {file_type_file}")
            return file_type_results
            
        except Exception as e:
            logger.error(f"Error in file-type specific tests: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _run_regression_testing(self) -> Dict[str, Any]:
        """Run regression testing."""
        if not self.config["regression_testing"]["enabled"]:
            logger.info("Regression testing disabled in configuration")
            return {"status": "disabled"}
        
        try:
            # Run regression testing on all test directories
            regression_report = run_regression_testing(
                self.test_directories,
                self.output_directory
            )
            
            logger.info("🔄 Regression testing completed")
            return {"status": "completed", "report": asdict(regression_report)}
            
        except Exception as e:
            logger.error(f"Error in regression testing: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _generate_workflow_report(self, target_files: List[Path], analysis_results: Dict[str, Any],
                                quality_gate_results: Dict[str, Any], file_type_results: Dict[str, Any],
                                regression_results: Dict[str, Any], workflow_start: datetime) -> Dict[str, Any]:
        """Generate a comprehensive workflow report."""
        workflow_duration = (datetime.now() - workflow_start).total_seconds()
        
        # Calculate overall statistics
        total_files = len(target_files)
        files_needing_modularization = analysis_results.get("files_needing_modularization", 0)
        files_passing_gates = quality_gate_results.get("files_passing_gates", 0)
        overall_quality_score = quality_gate_results.get("overall_success_rate", 0.0)
        
        # Determine workflow success
        workflow_success = (
            files_passing_gates >= total_files * self.config["quality_gates"]["failure_threshold"]
            and analysis_results.get("status") != "failed"
            and quality_gate_results.get("status") != "failed"
        )
        
        workflow_report = {
            "workflow_metadata": {
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": workflow_duration,
                "source_directory": str(self.source_directory),
                "test_directories": [str(d) for d in self.test_directories],
                "output_directory": str(self.output_directory),
                "configuration": self.config
            },
            "execution_summary": {
                "total_files_analyzed": total_files,
                "files_needing_modularization": files_needing_modularization,
                "files_passing_quality_gates": files_passing_gates,
                "overall_quality_score": overall_quality_score,
                "workflow_success": workflow_success
            },
            "component_results": {
                "modularization_analysis": analysis_results,
                "quality_gates": quality_gate_results,
                "file_type_tests": file_type_results,
                "regression_testing": regression_results
            },
            "recommendations": self._generate_workflow_recommendations(
                total_files, files_needing_modularization, files_passing_gates, overall_quality_score
            ),
            "next_steps": self._generate_next_steps(workflow_success, files_needing_modularization)
        }
        
        return workflow_report
    
    def _generate_workflow_recommendations(self, total_files: int, files_needing_modularization: int,
                                        files_passing_gates: int, overall_quality_score: float) -> List[str]:
        """Generate recommendations based on workflow results."""
        recommendations = []
        
        if files_needing_modularization > 0:
            recommendations.append(f"🚨 PRIORITY: {files_needing_modularization} files need immediate modularization")
            recommendations.append("Focus on files with highest line counts and complexity scores")
            recommendations.append("Use the quality gate results to prioritize modularization efforts")
        
        if overall_quality_score < 80:
            recommendations.append("⚠️ QUALITY: Overall quality score is below 80% - focus on improving code quality")
            recommendations.append("Address failed quality gates, especially critical ones")
        
        if files_passing_gates < total_files * 0.8:
            recommendations.append("🎯 TARGET: Aim for 80% of files to pass quality gates")
            recommendations.append("Review and fix quality gate failures systematically")
        
        if not recommendations:
            recommendations.append("✅ EXCELLENT: All files are meeting quality standards")
            recommendations.append("Maintain current code quality practices")
        
        return recommendations
    
    def _generate_next_steps(self, workflow_success: bool, files_needing_modularization: int) -> List[str]:
        """Generate next steps based on workflow results."""
        next_steps = []
        
        if workflow_success:
            next_steps.append("🎉 Workflow completed successfully!")
            next_steps.append("Review detailed reports for any areas of improvement")
            next_steps.append("Schedule regular testing cycles to maintain quality")
        else:
            next_steps.append("🔧 Workflow completed with issues that need attention")
            next_steps.append("Address quality gate failures before proceeding")
            next_steps.append("Fix critical issues identified in the analysis")
        
        if files_needing_modularization > 0:
            next_steps.append(f"📋 Begin modularization of {files_needing_modularization} identified files")
            next_steps.append("Start with highest priority files (highest line count, complexity)")
            next_steps.append("Run regression tests after each modularization step")
        
        next_steps.append("📊 Review all generated reports for detailed insights")
        next_steps.append("🔄 Schedule next testing cycle based on project timeline")
        
        return next_steps
    
    def _save_workflow_results(self, workflow_report: Dict[str, Any]):
        """Save the complete workflow results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        if self.config["reporting"]["generate_json"]:
            json_file = self.output_directory / f"modularization_workflow_report_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(workflow_report, f, indent=2, default=str)
            logger.info(f"💾 JSON workflow report saved to {json_file}")
        
        # Save Markdown report
        if self.config["reporting"]["generate_markdown"]:
            md_file = self.output_directory / f"modularization_workflow_report_{timestamp}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(self._generate_markdown_workflow_report(workflow_report))
            logger.info(f"💾 Markdown workflow report saved to {md_file}")
    
    def _generate_markdown_workflow_report(self, workflow_report: Dict[str, Any]) -> str:
        """Generate a human-readable markdown workflow report."""
        lines = []
        
        # Header
        lines.append("# 🚀 MODULARIZATION TESTING WORKFLOW REPORT")
        lines.append(f"**Generated:** {workflow_report['workflow_metadata']['timestamp']}")
        lines.append(f"**Duration:** {workflow_report['workflow_metadata']['duration_seconds']:.2f} seconds")
        lines.append(f"**Source Directory:** {workflow_report['workflow_metadata']['source_directory']}")
        lines.append("")
        
        # Execution Summary
        summary = workflow_report['execution_summary']
        lines.append("## 📊 EXECUTION SUMMARY")
        lines.append(f"- **Total Files Analyzed:** {summary['total_files_analyzed']}")
        lines.append(f"- **Files Needing Modularization:** {summary['files_needing_modularization']}")
        lines.append(f"- **Files Passing Quality Gates:** {summary['files_passing_quality_gates']}")
        lines.append(f"- **Overall Quality Score:** {summary['overall_quality_score']:.1f}%")
        lines.append(f"- **Workflow Success:** {'✅ YES' if summary['workflow_success'] else '❌ NO'}")
        lines.append("")
        
        # Component Results Summary
        lines.append("## 🔧 COMPONENT RESULTS")
        components = workflow_report['component_results']
        
        for component_name, component_result in components.items():
            if component_result.get('status') == 'disabled':
                lines.append(f"- **{component_name.replace('_', ' ').title()}:** 🔒 Disabled")
            elif component_result.get('status') == 'failed':
                lines.append(f"- **{component_name.replace('_', ' ').title()}:** ❌ Failed")
            else:
                lines.append(f"- **{component_name.replace('_', ' ').title()}:** ✅ Completed")
        lines.append("")
        
        # Recommendations
        lines.append("## 💡 RECOMMENDATIONS")
        for recommendation in workflow_report['recommendations']:
            lines.append(f"- {recommendation}")
        lines.append("")
        
        # Next Steps
        lines.append("## 🎯 NEXT STEPS")
        for step in workflow_report['next_steps']:
            lines.append(f"- {step}")
        lines.append("")
        
        # Configuration
        lines.append("## ⚙️ CONFIGURATION")
        config = workflow_report['workflow_metadata']['configuration']
        for section, settings in config.items():
            lines.append(f"### {section.replace('_', ' ').title()}")
            for key, value in settings.items():
                lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
            lines.append("")
        
        return "\n".join(lines)


def create_modularization_testing_workflow(source_dir: str, test_dirs: List[str], 
                                         output_dir: str = None, config_file: str = None) -> ModularizationTestWorkflow:
    """Create a modularization testing workflow with the specified configuration."""
    # Load configuration if provided
    config = None
    if config_file and Path(config_file).exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    
    # Create workflow
    workflow = ModularizationTestWorkflow(
        source_dir=Path(source_dir),
        test_dirs=test_dirs,
        output_dir=output_dir,
        config=config
    )
    
    return workflow


def main():
    """Main entry point for the modularization testing workflow."""
    parser = argparse.ArgumentParser(description="Run Modularization Testing Workflow")
    parser.add_argument("--source-dir", required=True, help="Source directory to analyze")
    parser.add_argument("--test-dirs", nargs="+", required=True, help="Test directories")
    parser.add_argument("--output-dir", help="Output directory for reports")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--target-files", nargs="+", help="Specific target files to analyze")
    
    args = parser.parse_args()
    
    try:
        # Create workflow
        workflow = create_modularization_testing_workflow(
            source_dir=args.source_dir,
            test_dirs=args.test_dirs,
            output_dir=args.output_dir,
            config_file=args.config
        )
        
        # Convert target files to Path objects if provided
        target_files = None
        if args.target_files:
            target_files = [Path(f) for f in args.target_files]
        
        # Run workflow
        results = workflow.run_complete_workflow(target_files)
        
        # Print summary
        if results.get("status") == "no_files":
            print("❌ No files found for analysis")
            sys.exit(1)
        
        summary = results.get("execution_summary", {})
        print(f"\n✅ Workflow completed successfully!")
        print(f"📊 Files analyzed: {summary.get('total_files_analyzed', 0)}")
        print(f"🚨 Files needing modularization: {summary.get('files_needing_modularization', 0)}")
        print(f"🚪 Files passing quality gates: {summary.get('files_passing_quality_gates', 0)}")
        print(f"📈 Overall quality score: {summary.get('overall_quality_score', 0):.1f}%")
        
        if not summary.get('workflow_success', False):
            print("\n⚠️ Workflow completed with issues that need attention")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        print(f"❌ Workflow failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
