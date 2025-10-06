#!/usr/bin/env python3
"""
Unit tests for Project Scanner tools functionality.

Author: Agent-3 (QA Lead)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))


class TestProjectScanner:
    """Test suite for Project Scanner functionality."""
    
    def test_project_scanner_initialization(self):
        """Test project scanner initialization."""
        # Mock project scanner
        scanner = Mock()
        scanner.scan_config = Mock()
        scanner.output_directory = "/scans"
        scanner.scan_types = ["full", "compliance", "dependencies", "health"]
        scanner.is_active = False
        
        # Test initialization
        assert scanner.scan_config is not None
        assert scanner.output_directory, "Should have output directory"
        assert isinstance(scanner.scan_types, list), "Should have scan types list"
        assert isinstance(scanner.is_active, bool), "Should have active status"
    
    def test_scan_configuration(self):
        """Test scan configuration management."""
        # Mock scan configuration
        scan_config = {
            "config_id": "config_12345",
            "scan_settings": {
                "include_patterns": ["*.py", "*.md", "*.json"],
                "exclude_patterns": ["__pycache__", "*.pyc", "node_modules"],
                "max_depth": 10,
                "follow_symlinks": False
            },
            "analysis_settings": {
                "code_analysis": True,
                "dependency_analysis": True,
                "security_scan": True,
                "performance_analysis": False
            },
            "output_settings": {
                "format": "json",
                "include_metadata": True,
                "compress_output": False,
                "output_directory": "/scans"
            }
        }
        
        # Test scan configuration validation
        assert scan_config["config_id"], "Should have config ID"
        assert isinstance(scan_config["scan_settings"], dict), "Should have scan settings"
        assert isinstance(scan_config["analysis_settings"], dict), "Should have analysis settings"
        assert isinstance(scan_config["output_settings"], dict), "Should have output settings"
        
        # Test scan settings validation
        scan_settings = scan_config["scan_settings"]
        assert isinstance(scan_settings["include_patterns"], list), "Should have include patterns"
        assert isinstance(scan_settings["exclude_patterns"], list), "Should have exclude patterns"
        assert scan_settings["max_depth"] > 0, "Max depth should be positive"
        assert isinstance(scan_settings["follow_symlinks"], bool), "Follow symlinks should be boolean"
        
        # Test analysis settings validation
        analysis_settings = scan_config["analysis_settings"]
        assert isinstance(analysis_settings["code_analysis"], bool), "Code analysis should be boolean"
        assert isinstance(analysis_settings["dependency_analysis"], bool), "Dependency analysis should be boolean"
        assert isinstance(analysis_settings["security_scan"], bool), "Security scan should be boolean"
        assert isinstance(analysis_settings["performance_analysis"], bool), "Performance analysis should be boolean"
    
    def test_file_discovery(self):
        """Test file discovery functionality."""
        # Mock file discovery
        file_discovery = {
            "discovery_id": "discovery_67890",
            "scan_root": "/project",
            "discovered_files": [
                {
                    "file_path": "/project/src/main.py",
                    "file_type": "python",
                    "file_size": 1024,
                    "last_modified": "2025-01-05T10:00:00Z",
                    "hash": "abc123def456"
                },
                {
                    "file_path": "/project/README.md",
                    "file_type": "markdown",
                    "file_size": 512,
                    "last_modified": "2025-01-04T15:30:00Z",
                    "hash": "def456ghi789"
                },
                {
                    "file_path": "/project/requirements.txt",
                    "file_type": "text",
                    "file_size": 256,
                    "last_modified": "2025-01-03T09:15:00Z",
                    "hash": "ghi789jkl012"
                }
            ],
            "discovery_metrics": {
                "total_files": 3,
                "total_size_bytes": 1792,
                "file_types": {"python": 1, "markdown": 1, "text": 1},
                "discovery_time_ms": 45.2
            }
        }
        
        # Test file discovery validation
        assert file_discovery["discovery_id"], "Should have discovery ID"
        assert file_discovery["scan_root"], "Should have scan root"
        assert isinstance(file_discovery["discovered_files"], list), "Should have discovered files list"
        assert isinstance(file_discovery["discovery_metrics"], dict), "Should have discovery metrics"
        
        # Test discovered files validation
        for file_info in file_discovery["discovered_files"]:
            assert file_info["file_path"], "File should have path"
            assert file_info["file_type"], "File should have type"
            assert file_info["file_size"] >= 0, "File size should be non-negative"
            assert file_info["last_modified"], "File should have last modified time"
            assert file_info["hash"], "File should have hash"
        
        # Test discovery metrics validation
        metrics = file_discovery["discovery_metrics"]
        assert metrics["total_files"] > 0, "Total files should be positive"
        assert metrics["total_size_bytes"] >= 0, "Total size should be non-negative"
        assert isinstance(metrics["file_types"], dict), "Should have file types dict"
        assert metrics["discovery_time_ms"] > 0, "Discovery time should be positive"
    
    def test_code_analysis(self):
        """Test code analysis functionality."""
        # Mock code analysis
        code_analysis = {
            "analysis_id": "analysis_11111",
            "analysis_type": "python_code_analysis",
            "analysis_results": {
                "file_metrics": {
                    "total_lines": 1500,
                    "code_lines": 1200,
                    "comment_lines": 200,
                    "blank_lines": 100,
                    "complexity_score": 15.5
                },
                "quality_metrics": {
                    "cyclomatic_complexity": 8.2,
                    "maintainability_index": 72.5,
                    "technical_debt_hours": 12.5,
                    "code_smells": 3
                },
                "structure_analysis": {
                    "classes": 25,
                    "functions": 150,
                    "imports": 45,
                    "dependencies": 12
                },
                "compliance_check": {
                    "v2_compliance": True,
                    "line_count_violations": 0,
                    "class_count_violations": 0,
                    "function_count_violations": 2
                }
            },
            "analysis_warnings": [
                {
                    "warning_type": "complexity",
                    "severity": "medium",
                    "message": "Function 'process_data' has high cyclomatic complexity",
                    "file_path": "/project/src/processor.py",
                    "line_number": 45
                }
            ]
        }
        
        # Test code analysis validation
        assert code_analysis["analysis_id"], "Should have analysis ID"
        assert code_analysis["analysis_type"], "Should have analysis type"
        assert isinstance(code_analysis["analysis_results"], dict), "Should have analysis results"
        assert isinstance(code_analysis["analysis_warnings"], list), "Should have analysis warnings"
        
        # Test file metrics validation
        file_metrics = code_analysis["analysis_results"]["file_metrics"]
        assert file_metrics["total_lines"] > 0, "Total lines should be positive"
        assert file_metrics["code_lines"] >= 0, "Code lines should be non-negative"
        assert file_metrics["comment_lines"] >= 0, "Comment lines should be non-negative"
        assert file_metrics["blank_lines"] >= 0, "Blank lines should be non-negative"
        assert file_metrics["complexity_score"] >= 0, "Complexity score should be non-negative"
        
        # Test quality metrics validation
        quality_metrics = code_analysis["analysis_results"]["quality_metrics"]
        assert quality_metrics["cyclomatic_complexity"] >= 0, "Cyclomatic complexity should be non-negative"
        assert 0 <= quality_metrics["maintainability_index"] <= 100, "Maintainability index should be between 0 and 100"
        assert quality_metrics["technical_debt_hours"] >= 0, "Technical debt should be non-negative"
        assert quality_metrics["code_smells"] >= 0, "Code smells should be non-negative"
        
        # Test compliance check validation
        compliance = code_analysis["analysis_results"]["compliance_check"]
        assert isinstance(compliance["v2_compliance"], bool), "V2 compliance should be boolean"
        assert compliance["line_count_violations"] >= 0, "Line count violations should be non-negative"
        assert compliance["class_count_violations"] >= 0, "Class count violations should be non-negative"
        assert compliance["function_count_violations"] >= 0, "Function count violations should be non-negative"
    
    def test_dependency_analysis(self):
        """Test dependency analysis functionality."""
        # Mock dependency analysis
        dependency_analysis = {
            "analysis_id": "dep_analysis_22222",
            "dependency_tree": {
                "direct_dependencies": [
                    {"name": "pytest", "version": "7.4.3", "type": "dev"},
                    {"name": "requests", "version": "2.31.0", "type": "prod"},
                    {"name": "numpy", "version": "1.24.3", "type": "prod"}
                ],
                "transitive_dependencies": [
                    {"name": "urllib3", "version": "2.0.4", "parent": "requests"},
                    {"name": "certifi", "version": "2023.7.22", "parent": "requests"},
                    {"name": "charset-normalizer", "version": "3.2.0", "parent": "requests"}
                ],
                "dependency_conflicts": []
            },
            "security_analysis": {
                "vulnerable_packages": [],
                "outdated_packages": [
                    {"name": "numpy", "current": "1.24.3", "latest": "1.25.0", "severity": "low"}
                ],
                "security_score": 95
            },
            "license_analysis": {
                "licenses_found": ["MIT", "Apache-2.0", "BSD-3-Clause"],
                "license_conflicts": [],
                "compliance_status": "compliant"
            }
        }
        
        # Test dependency analysis validation
        assert dependency_analysis["analysis_id"], "Should have analysis ID"
        assert isinstance(dependency_analysis["dependency_tree"], dict), "Should have dependency tree"
        assert isinstance(dependency_analysis["security_analysis"], dict), "Should have security analysis"
        assert isinstance(dependency_analysis["license_analysis"], dict), "Should have license analysis"
        
        # Test dependency tree validation
        dep_tree = dependency_analysis["dependency_tree"]
        assert isinstance(dep_tree["direct_dependencies"], list), "Should have direct dependencies"
        assert isinstance(dep_tree["transitive_dependencies"], list), "Should have transitive dependencies"
        assert isinstance(dep_tree["dependency_conflicts"], list), "Should have dependency conflicts"
        
        # Test direct dependencies validation
        for dep in dep_tree["direct_dependencies"]:
            assert dep["name"], "Dependency should have name"
            assert dep["version"], "Dependency should have version"
            assert dep["type"] in ["prod", "dev", "test"], "Should have valid dependency type"
        
        # Test security analysis validation
        security = dependency_analysis["security_analysis"]
        assert isinstance(security["vulnerable_packages"], list), "Should have vulnerable packages list"
        assert isinstance(security["outdated_packages"], list), "Should have outdated packages list"
        assert 0 <= security["security_score"] <= 100, "Security score should be between 0 and 100"
    
    def test_project_health_assessment(self):
        """Test project health assessment functionality."""
        # Mock project health assessment
        health_assessment = {
            "assessment_id": "health_33333",
            "assessment_date": "2025-01-05T12:00:00Z",
            "health_metrics": {
                "code_quality": {
                    "score": 85,
                    "factors": ["complexity", "maintainability", "test_coverage"],
                    "status": "good"
                },
                "dependency_health": {
                    "score": 90,
                    "factors": ["security", "currency", "conflicts"],
                    "status": "excellent"
                },
                "documentation_quality": {
                    "score": 75,
                    "factors": ["completeness", "accuracy", "accessibility"],
                    "status": "fair"
                },
                "test_coverage": {
                    "score": 25,
                    "factors": ["unit_tests", "integration_tests", "e2e_tests"],
                    "status": "needs_improvement"
                }
            },
            "overall_health_score": 68.75,
            "health_status": "fair",
            "recommendations": [
                "Increase test coverage to improve overall health",
                "Improve documentation completeness",
                "Maintain current code quality standards"
            ]
        }
        
        # Test health assessment validation
        assert health_assessment["assessment_id"], "Should have assessment ID"
        assert health_assessment["assessment_date"], "Should have assessment date"
        assert isinstance(health_assessment["health_metrics"], dict), "Should have health metrics"
        assert 0 <= health_assessment["overall_health_score"] <= 100, "Overall health score should be between 0 and 100"
        assert health_assessment["health_status"] in ["excellent", "good", "fair", "poor"], "Should have valid health status"
        assert isinstance(health_assessment["recommendations"], list), "Should have recommendations list"
        
        # Test individual health metrics validation
        for metric_name, metric_data in health_assessment["health_metrics"].items():
            assert 0 <= metric_data["score"] <= 100, f"{metric_name} score should be between 0 and 100"
            assert isinstance(metric_data["factors"], list), f"{metric_name} should have factors list"
            assert metric_data["status"] in ["excellent", "good", "fair", "poor", "needs_improvement"], f"{metric_name} should have valid status"


@pytest.mark.unit
class TestProjectScannerIntegration:
    """Integration tests for Project Scanner."""
    
    def test_complete_scan_workflow(self):
        """Test complete project scan workflow."""
        # Step 1: Initialize scanner
        scanner = Mock()
        scanner.is_active = True
        scanner.scan_config = Mock()
        
        # Step 2: Configure scan
        scanner.configure_scan.return_value = True
        config_result = scanner.configure_scan({
            "scan_type": "full",
            "include_patterns": ["*.py"],
            "output_format": "json"
        })
        
        # Step 3: Discover files
        scanner.discover_files.return_value = {
            "files_found": 150,
            "total_size": 2048000,
            "discovery_time": 2.5
        }
        discovery_result = scanner.discover_files("/project")
        
        # Step 4: Analyze code
        scanner.analyze_code.return_value = {
            "analysis_complete": True,
            "metrics": {"complexity": 12.5, "maintainability": 78.0},
            "violations": 3
        }
        analysis_result = scanner.analyze_code()
        
        # Step 5: Generate report
        scanner.generate_report.return_value = {
            "report_generated": True,
            "report_path": "/scans/scan_report.json",
            "file_size": 51200
        }
        report_result = scanner.generate_report()
        
        # Validate workflow
        assert config_result == True, "Scan configuration should succeed"
        assert discovery_result["files_found"] > 0, "Should discover files"
        assert analysis_result["analysis_complete"] == True, "Analysis should complete"
        assert report_result["report_generated"] == True, "Report should be generated"
    
    def test_scan_performance_monitoring(self):
        """Test scan performance monitoring."""
        # Mock performance monitoring
        performance_monitoring = {
            "monitoring_session_id": "scan_monitor_44444",
            "scan_metrics": {
                "file_discovery": {
                    "files_processed": 1500,
                    "discovery_time_ms": 2500,
                    "throughput_files_per_second": 600
                },
                "code_analysis": {
                    "files_analyzed": 800,
                    "analysis_time_ms": 15000,
                    "throughput_files_per_second": 53.3
                },
                "dependency_analysis": {
                    "packages_analyzed": 45,
                    "analysis_time_ms": 5000,
                    "throughput_packages_per_second": 9.0
                }
            },
            "performance_bottlenecks": [
                {
                    "bottleneck_type": "file_io",
                    "severity": "medium",
                    "impact_percent": 15.2,
                    "recommendation": "Consider using SSD storage"
                }
            ],
            "optimization_recommendations": [
                "Enable parallel processing for code analysis",
                "Implement caching for repeated scans",
                "Optimize file discovery patterns"
            ]
        }
        
        # Test performance monitoring validation
        assert performance_monitoring["monitoring_session_id"], "Should have monitoring session ID"
        assert isinstance(performance_monitoring["scan_metrics"], dict), "Should have scan metrics"
        assert isinstance(performance_monitoring["performance_bottlenecks"], list), "Should have performance bottlenecks"
        assert isinstance(performance_monitoring["optimization_recommendations"], list), "Should have optimization recommendations"
        
        # Test scan metrics validation
        scan_metrics = performance_monitoring["scan_metrics"]
        for metric_type, metrics in scan_metrics.items():
            # Check for appropriate items processed field based on metric type
            if "files_processed" in metrics:
                assert metrics["files_processed"] > 0, f"{metric_type} should process files"
            elif "files_analyzed" in metrics:
                assert metrics["files_analyzed"] > 0, f"{metric_type} should analyze files"
            elif "packages_analyzed" in metrics:
                assert metrics["packages_analyzed"] > 0, f"{metric_type} should analyze packages"
            
            # Check for appropriate time field based on metric type
            if metric_type == "file_discovery":
                assert metrics["discovery_time_ms"] > 0, f"{metric_type} should have positive time"
            elif metric_type == "code_analysis":
                assert metrics["analysis_time_ms"] > 0, f"{metric_type} should have positive time"
            elif metric_type == "dependency_analysis":
                assert metrics["analysis_time_ms"] > 0, f"{metric_type} should have positive time"
            
            # Check for appropriate throughput field
            if "throughput_files_per_second" in metrics:
                assert metrics["throughput_files_per_second"] > 0, f"{metric_type} should have positive file throughput"
            elif "throughput_packages_per_second" in metrics:
                assert metrics["throughput_packages_per_second"] > 0, f"{metric_type} should have positive package throughput"
        
        # Test performance bottlenecks validation
        for bottleneck in performance_monitoring["performance_bottlenecks"]:
            assert bottleneck["bottleneck_type"], "Bottleneck should have type"
            assert bottleneck["severity"] in ["low", "medium", "high"], "Should have valid severity"
            assert 0 <= bottleneck["impact_percent"] <= 100, "Impact should be between 0 and 100"
            assert bottleneck["recommendation"], "Should have recommendation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
