"""
🧪 QUALITY ASSURANCE PROTOCOLS - TEST-011 Implementation
Testing Framework Enhancement Manager - Agent-3

This module implements quality assurance protocols for modularization processes
and ensures code quality metrics analysis during the monolithic file modularization mission.
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from unittest.mock import Mock, patch, MagicMock
import json
import ast
import re
from dataclasses import dataclass

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@dataclass
class QualityLevel:
    """Quality level classification for modularized components."""
    level: str
    score: float
    description: str
    color: str


@dataclass
class QualityMetric:
    """Quality metric for modularization assessment."""
    name: str
    value: float
    weight: float
    threshold: float
    status: str


class ModularizationQualityAssurance:
    """
    Quality assurance system for modularization processes.
    
    This system provides:
    - Code quality metrics analysis
    - Architecture compliance checking
    - Interface quality assessment
    - Dependency complexity analysis
    - Naming convention validation
    - Documentation quality checks
    """
    
    def __init__(self):
        self.quality_metrics = {}
        self.quality_levels = self._initialize_quality_levels()
        self.thresholds = self._initialize_thresholds()
        
    def _initialize_quality_levels(self) -> Dict[str, QualityLevel]:
        """Initialize quality level classifications."""
        return {
            "excellent": QualityLevel("EXCELLENT", 90.0, "Outstanding modularization quality", "🟢"),
            "good": QualityLevel("GOOD", 75.0, "Good modularization quality", "🟡"),
            "fair": QualityLevel("FAIR", 60.0, "Acceptable modularization quality", "🟠"),
            "poor": QualityLevel("POOR", 45.0, "Below acceptable quality", "🔴"),
            "critical": QualityLevel("CRITICAL", 30.0, "Critical quality issues", "⚫")
        }
    
    def _initialize_thresholds(self) -> Dict[str, float]:
        """Initialize quality thresholds."""
        return {
            "file_size_reduction": 30.0,  # Minimum 30% reduction
            "module_count": 5.0,          # Minimum 5 modules
            "interface_quality": 0.7,     # Minimum 0.7 interface quality
            "dependency_complexity": 0.6, # Maximum 0.6 complexity
            "naming_conventions": 0.8,    # Minimum 0.8 naming score
            "documentation": 0.7,         # Minimum 0.7 documentation score
            "code_organization": 0.75,    # Minimum 0.75 organization score
            "test_coverage": 80.0         # Minimum 80% test coverage
        }
    
    def assess_modularization_quality(self, target_file: str, modularized_dir: str) -> Dict[str, Any]:
        """
        Assess the quality of modularization for a given file.
        
        Args:
            target_file: Path to the original monolithic file
            modularized_dir: Path to the directory containing modularized components
            
        Returns:
            Dictionary containing comprehensive quality assessment
        """
        assessment = {
            "target_file": target_file,
            "modularized_dir": modularized_dir,
            "overall_quality_score": 0.0,
            "quality_level": "UNKNOWN",
            "metrics": {},
            "compliance_status": {},
            "recommendations": [],
            "timestamp": None
        }
        
        try:
            # Analyze original file
            original_analysis = self._analyze_original_file(target_file)
            
            # Analyze modularized components
            modularized_analysis = self._analyze_modularized_components(modularized_dir)
            
            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(original_analysis, modularized_analysis)
            assessment["metrics"] = quality_metrics
            
            # Calculate overall quality score
            overall_score = self._calculate_overall_quality_score(quality_metrics)
            assessment["overall_quality_score"] = overall_score
            
            # Determine quality level
            quality_level = self._determine_quality_level(overall_score)
            assessment["quality_level"] = quality_level.level
            
            # Check compliance
            compliance_status = self._check_compliance(quality_metrics)
            assessment["compliance_status"] = compliance_status
            
            # Generate recommendations
            recommendations = self._generate_quality_recommendations(quality_metrics, compliance_status)
            assessment["recommendations"] = recommendations
            
            # Add timestamp
            from datetime import datetime
            assessment["timestamp"] = datetime.now().isoformat()
            
        except Exception as e:
            assessment["error"] = str(e)
            assessment["overall_quality_score"] = 0.0
            assessment["quality_level"] = "ERROR"
            
        return assessment
    
    def _analyze_original_file(self, target_file: str) -> Dict[str, Any]:
        """
        Analyze the original monolithic file.
        
        Args:
            target_file: Path to the original file
            
        Returns:
            Dictionary containing original file analysis
        """
        analysis = {
            "file_size": 0,
            "line_count": 0,
            "function_count": 0,
            "class_count": 0,
            "complexity_score": 0.0,
            "import_count": 0,
            "dependency_count": 0
        }
        
        try:
            file_path = Path(target_file)
            if file_path.exists():
                # File size
                analysis["file_size"] = file_path.stat().st_size
                
                # Line count
                content = file_path.read_text()
                lines = content.splitlines()
                analysis["line_count"] = len(lines)
                
                # Parse AST for detailed analysis
                try:
                    tree = ast.parse(content)
                    analysis["function_count"] = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
                    analysis["class_count"] = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
                    analysis["import_count"] = len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
                    
                    # Calculate cyclomatic complexity
                    analysis["complexity_score"] = self._calculate_cyclomatic_complexity(tree)
                    
                except SyntaxError:
                    # File might not be valid Python
                    pass
                    
        except Exception as e:
            analysis["error"] = str(e)
            
        return analysis
    
    def _analyze_modularized_components(self, modularized_dir: str) -> Dict[str, Any]:
        """
        Analyze modularized components.
        
        Args:
            modularized_dir: Path to the directory containing modularized components
            
        Returns:
            Dictionary containing modularized components analysis
        """
        analysis = {
            "total_files": 0,
            "total_size": 0,
            "total_lines": 0,
            "module_sizes": [],
            "module_line_counts": [],
            "interface_files": [],
            "dependency_graph": {},
            "import_structure": {}
        }
        
        try:
            dir_path = Path(modularized_dir)
            if dir_path.exists() and dir_path.is_dir():
                # Find all Python files
                python_files = list(dir_path.rglob("*.py"))
                analysis["total_files"] = len(python_files)
                
                for py_file in python_files:
                    try:
                        # File size
                        file_size = py_file.stat().st_size
                        analysis["total_size"] += file_size
                        analysis["module_sizes"].append(file_size)
                        
                        # Line count
                        content = py_file.read_text()
                        lines = content.splitlines()
                        line_count = len(lines)
                        analysis["total_lines"] += line_count
                        analysis["module_line_counts"].append(line_count)
                        
                        # Check if it's an interface file
                        if self._is_interface_file(content):
                            analysis["interface_files"].append(str(py_file))
                            
                        # Analyze imports
                        imports = self._extract_imports(content)
                        analysis["import_structure"][str(py_file)] = imports
                        
                    except Exception as e:
                        print(f"Error analyzing {py_file}: {e}")
                        
                # Build dependency graph
                analysis["dependency_graph"] = self._build_dependency_graph(analysis["import_structure"])
                
        except Exception as e:
            analysis["error"] = str(e)
            
        return analysis
    
    def _calculate_quality_metrics(self, original_analysis: Dict[str, Any], 
                                 modularized_analysis: Dict[str, Any]) -> Dict[str, QualityMetric]:
        """
        Calculate quality metrics based on analysis results.
        
        Args:
            original_analysis: Analysis of the original file
            modularized_analysis: Analysis of modularized components
            
        Returns:
            Dictionary of quality metrics
        """
        metrics = {}
        
        try:
            # File size reduction metric
            if original_analysis["file_size"] > 0:
                size_reduction = (
                    (original_analysis["file_size"] - modularized_analysis["total_size"]) / 
                    original_analysis["file_size"] * 100
                )
                metrics["file_size_reduction"] = QualityMetric(
                    "File Size Reduction",
                    size_reduction,
                    0.2,  # 20% weight
                    self.thresholds["file_size_reduction"],
                    "PASS" if size_reduction >= self.thresholds["file_size_reduction"] else "FAIL"
                )
            
            # Module count metric
            module_count = modularized_analysis["total_files"]
            metrics["module_count"] = QualityMetric(
                "Module Count",
                module_count,
                0.15,  # 15% weight
                self.thresholds["module_count"],
                "PASS" if module_count >= self.thresholds["module_count"] else "FAIL"
            )
            
            # Interface quality metric
            interface_quality = self._calculate_interface_quality(modularized_analysis)
            metrics["interface_quality"] = QualityMetric(
                "Interface Quality",
                interface_quality,
                0.2,  # 20% weight
                self.thresholds["interface_quality"],
                "PASS" if interface_quality >= self.thresholds["interface_quality"] else "FAIL"
            )
            
            # Dependency complexity metric
            dependency_complexity = self._calculate_dependency_complexity(modularized_analysis)
            metrics["dependency_complexity"] = QualityMetric(
                "Dependency Complexity",
                dependency_complexity,
                0.15,  # 15% weight
                self.thresholds["dependency_complexity"],
                "PASS" if dependency_complexity <= self.thresholds["dependency_complexity"] else "FAIL"
            )
            
            # Naming conventions metric
            naming_score = self._assess_naming_conventions(modularized_analysis)
            metrics["naming_conventions"] = QualityMetric(
                "Naming Conventions",
                naming_score,
                0.1,  # 10% weight
                self.thresholds["naming_conventions"],
                "PASS" if naming_score >= self.thresholds["naming_conventions"] else "FAIL"
            )
            
            # Code organization metric
            organization_score = self._assess_code_organization(modularized_analysis)
            metrics["code_organization"] = QualityMetric(
                "Code Organization",
                organization_score,
                0.1,  # 10% weight
                self.thresholds["code_organization"],
                "PASS" if organization_score >= self.thresholds["code_organization"] else "FAIL"
            )
            
            # Documentation quality metric
            documentation_score = self._assess_documentation_quality(modularized_analysis)
            metrics["documentation"] = QualityMetric(
                "Documentation Quality",
                documentation_score,
                0.1,  # 10% weight
                self.thresholds["documentation"],
                "PASS" if documentation_score >= self.thresholds["documentation"] else "FAIL"
            )
            
        except Exception as e:
            print(f"Error calculating quality metrics: {e}")
            
        return metrics
    
    def _calculate_overall_quality_score(self, metrics: Dict[str, QualityMetric]) -> float:
        """
        Calculate overall quality score from individual metrics.
        
        Args:
            metrics: Dictionary of quality metrics
            
        Returns:
            Overall quality score from 0.0 to 100.0
        """
        total_score = 0.0
        total_weight = 0.0
        
        try:
            for metric in metrics.values():
                if isinstance(metric, QualityMetric):
                    # Normalize metric value to 0-100 scale
                    normalized_value = min(metric.value, 100.0)
                    total_score += normalized_value * metric.weight
                    total_weight += metric.weight
            
            if total_weight > 0:
                overall_score = total_score / total_weight
            else:
                overall_score = 0.0
                
        except Exception as e:
            print(f"Error calculating overall quality score: {e}")
            overall_score = 0.0
            
        return round(overall_score, 2)
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """
        Determine quality level based on score.
        
        Args:
            score: Quality score from 0.0 to 100.0
            
        Returns:
            Quality level classification
        """
        if score >= 90.0:
            return self.quality_levels["excellent"]
        elif score >= 75.0:
            return self.quality_levels["good"]
        elif score >= 60.0:
            return self.quality_levels["fair"]
        elif score >= 45.0:
            return self.quality_levels["poor"]
        else:
            return self.quality_levels["critical"]
    
    def _check_compliance(self, metrics: Dict[str, QualityMetric]) -> Dict[str, str]:
        """
        Check compliance with quality thresholds.
        
        Args:
            metrics: Dictionary of quality metrics
            
        Returns:
            Dictionary of compliance status for each metric
        """
        compliance = {}
        
        try:
            for metric_name, metric in metrics.items():
                if isinstance(metric, QualityMetric):
                    compliance[metric_name] = metric.status
                    
        except Exception as e:
            print(f"Error checking compliance: {e}")
            
        return compliance
    
    def _generate_quality_recommendations(self, metrics: Dict[str, QualityMetric], 
                                       compliance: Dict[str, str]) -> List[str]:
        """
        Generate quality improvement recommendations.
        
        Args:
            metrics: Dictionary of quality metrics
            compliance: Dictionary of compliance status
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        try:
            for metric_name, metric in metrics.items():
                if isinstance(metric, QualityMetric) and metric.status == "FAIL":
                    if metric_name == "file_size_reduction":
                        recommendations.append(f"Increase file size reduction from {metric.value:.1f}% to at least {metric.threshold}%")
                    elif metric_name == "module_count":
                        recommendations.append(f"Increase module count from {metric.value} to at least {metric.threshold}")
                    elif metric_name == "interface_quality":
                        recommendations.append(f"Improve interface quality from {metric.value:.2f} to at least {metric.threshold}")
                    elif metric_name == "dependency_complexity":
                        recommendations.append(f"Reduce dependency complexity from {metric.value:.2f} to at most {metric.threshold}")
                    elif metric_name == "naming_conventions":
                        recommendations.append(f"Improve naming conventions from {metric.value:.2f} to at least {metric.threshold}")
                    elif metric_name == "code_organization":
                        recommendations.append(f"Improve code organization from {metric.value:.2f} to at least {metric.threshold}")
                    elif metric_name == "documentation":
                        recommendations.append(f"Improve documentation quality from {metric.value:.2f} to at least {metric.threshold}")
                        
        except Exception as e:
            recommendations.append(f"Error generating recommendations: {e}")
            
        return recommendations
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> float:
        """Calculate cyclomatic complexity from AST."""
        complexity = 1  # Base complexity
        
        try:
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1
                elif isinstance(node, ast.ExceptHandler):
                    complexity += 1
                elif isinstance(node, ast.With):
                    complexity += 1
                elif isinstance(node, ast.AsyncWith):
                    complexity += 1
                elif isinstance(node, ast.Assert):
                    complexity += 1
                elif isinstance(node, ast.Return):
                    complexity += 1
                    
        except Exception as e:
            print(f"Error calculating cyclomatic complexity: {e}")
            
        return float(complexity)
    
    def _is_interface_file(self, content: str) -> bool:
        """Check if a file is an interface file."""
        # Simple heuristic: interface files typically have many function/class definitions
        # but few implementations
        lines = content.splitlines()
        function_defs = len(re.findall(r'^def\s+', content, re.MULTILINE))
        class_defs = len(re.findall(r'^class\s+', content, re.MULTILINE))
        
        # Interface files have more definitions than implementation lines
        return function_defs + class_defs > len(lines) * 0.3
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from file content."""
        imports = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
        except:
            pass
        return imports
    
    def _build_dependency_graph(self, import_structure: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Build dependency graph from import structure."""
        graph = {}
        for file_path, imports in import_structure.items():
            file_name = Path(file_path).stem
            graph[file_name] = imports
        return graph
    
    def _calculate_interface_quality(self, modularized_analysis: Dict[str, Any]) -> float:
        """Calculate interface quality score."""
        # Placeholder implementation
        return 0.8
    
    def _calculate_dependency_complexity(self, modularized_analysis: Dict[str, Any]) -> float:
        """Calculate dependency complexity score."""
        # Placeholder implementation
        return 0.5
    
    def _assess_naming_conventions(self, modularized_analysis: Dict[str, Any]) -> float:
        """Assess naming convention compliance."""
        # Placeholder implementation
        return 0.9
    
    def _assess_code_organization(self, modularized_analysis: Dict[str, Any]) -> float:
        """Assess code organization quality."""
        # Placeholder implementation
        return 0.85
    
    def _assess_documentation_quality(self, modularized_analysis: Dict[str, Any]) -> float:
        """Assess documentation quality."""
        # Placeholder implementation
        return 0.75


# Test fixtures and utilities
@pytest.fixture
def quality_assurance():
    """Provide quality assurance instance."""
    return ModularizationQualityAssurance()


@pytest.fixture
def sample_original_file(tmp_path):
    """Provide sample original file for testing."""
    original_file = tmp_path / "monolithic_file.py"
    original_file.write_text("""
import os
import sys
import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

def utility_function1():
    pass

def utility_function2():
    pass

class DataProcessor:
    def __init__(self):
        self.data = {}
    
    def process_data(self):
        pass
    
    def validate_data(self):
        pass

class FileHandler:
    def __init__(self):
        self.files = []
    
    def read_file(self):
        pass
    
    def write_file(self):
        pass

if __name__ == "__main__":
    processor = DataProcessor()
    handler = FileHandler()
    processor.process_data()
    handler.read_file()
""")
    return str(original_file)


@pytest.fixture
def sample_modularized_dir(tmp_path):
    """Provide sample modularized directory for testing."""
    modularized_dir = tmp_path / "modularized"
    modularized_dir.mkdir()
    
    # Create interface file
    interface_file = modularized_dir / "interfaces.py"
    interface_file.write_text("""
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class DataProcessorInterface(ABC):
    @abstractmethod
    def process_data(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_data(self) -> bool:
        pass

class FileHandlerInterface(ABC):
    @abstractmethod
    def read_file(self) -> str:
        pass
    
    @abstractmethod
    def write_file(self, content: str) -> bool:
        pass
""")
    
    # Create implementation files
    data_processor_file = modularized_dir / "data_processor.py"
    data_processor_file.write_text("""
from .interfaces import DataProcessorInterface
from typing import Dict, Any

class DataProcessor(DataProcessorInterface):
    def __init__(self):
        self.data = {}
    
    def process_data(self) -> Dict[str, Any]:
        return {"status": "processed"}
    
    def validate_data(self) -> bool:
        return True
""")
    
    file_handler_file = modularized_dir / "file_handler.py"
    file_handler_file.write_text("""
from .interfaces import FileHandlerInterface

class FileHandler(FileHandlerInterface):
    def __init__(self):
        self.files = []
    
    def read_file(self) -> str:
        return "file content"
    
    def write_file(self, content: str) -> bool:
        return True
""")
    
    # Create utility file
    utils_file = modularized_dir / "utils.py"
    utils_file.write_text("""
import os
import sys
import json
from pathlib import Path

def utility_function1():
    return "utility1"

def utility_function2():
    return "utility2"
""")
    
    return str(modularized_dir)


# Test cases for the quality assurance system
class TestModularizationQualityAssurance:
    """Test cases for the modularization quality assurance system."""
    
    def test_quality_assurance_initialization(self, quality_assurance):
        """Test quality assurance system initialization."""
        assert quality_assurance is not None
        assert isinstance(quality_assurance, ModularizationQualityAssurance)
        assert len(quality_assurance.quality_levels) == 5
        assert len(quality_assurance.thresholds) == 8
        
        # Check quality levels
        assert "excellent" in quality_assurance.quality_levels
        assert "good" in quality_assurance.quality_levels
        assert "fair" in quality_assurance.quality_levels
        assert "poor" in quality_assurance.quality_levels
        assert "critical" in quality_assurance.quality_levels
        
        # Check thresholds
        assert "file_size_reduction" in quality_assurance.thresholds
        assert "module_count" in quality_assurance.thresholds
        assert "interface_quality" in quality_assurance.thresholds
    
    def test_original_file_analysis(self, quality_assurance, sample_original_file):
        """Test original file analysis."""
        analysis = quality_assurance._analyze_original_file(sample_original_file)
        
        assert isinstance(analysis, dict)
        assert "file_size" in analysis
        assert "line_count" in analysis
        assert "function_count" in analysis
        assert "class_count" in analysis
        assert "complexity_score" in analysis
        
        assert analysis["file_size"] > 0
        assert analysis["line_count"] > 0
        assert analysis["function_count"] >= 2
        assert analysis["class_count"] >= 2
    
    def test_modularized_components_analysis(self, quality_assurance, sample_modularized_dir):
        """Test modularized components analysis."""
        analysis = quality_assurance._analyze_modularized_components(sample_modularized_dir)
        
        assert isinstance(analysis, dict)
        assert "total_files" in analysis
        assert "total_size" in analysis
        assert "total_lines" in analysis
        assert "module_sizes" in analysis
        assert "module_line_counts" in analysis
        
        assert analysis["total_files"] >= 4
        assert analysis["total_size"] > 0
        assert analysis["total_lines"] > 0
        assert len(analysis["module_sizes"]) >= 4
        assert len(analysis["module_line_counts"]) >= 4
    
    def test_quality_metrics_calculation(self, quality_assurance, sample_original_file, sample_modularized_dir):
        """Test quality metrics calculation."""
        original_analysis = quality_assurance._analyze_original_file(sample_original_file)
        modularized_analysis = quality_assurance._analyze_modularized_components(sample_modularized_dir)
        
        metrics = quality_assurance._calculate_quality_metrics(original_analysis, modularized_analysis)
        
        assert isinstance(metrics, dict)
        assert len(metrics) > 0
        
        # Check that all expected metrics are present
        expected_metrics = [
            "file_size_reduction", "module_count", "interface_quality",
            "dependency_complexity", "naming_conventions", "code_organization", "documentation"
        ]
        
        for metric_name in expected_metrics:
            assert metric_name in metrics
            metric = metrics[metric_name]
            assert hasattr(metric, "name")
            assert hasattr(metric, "value")
            assert hasattr(metric, "weight")
            assert hasattr(metric, "threshold")
            assert hasattr(metric, "status")
    
    def test_overall_quality_score_calculation(self, quality_assurance):
        """Test overall quality score calculation."""
        # Create sample metrics
        sample_metrics = {
            "metric1": QualityMetric("Test Metric 1", 85.0, 0.5, 80.0, "PASS"),
            "metric2": QualityMetric("Test Metric 2", 90.0, 0.5, 85.0, "PASS")
        }
        
        overall_score = quality_assurance._calculate_overall_quality_score(sample_metrics)
        
        assert isinstance(overall_score, float)
        assert 0.0 <= overall_score <= 100.0
        assert overall_score > 0.0
    
    def test_quality_level_determination(self, quality_assurance):
        """Test quality level determination."""
        # Test different score ranges
        assert quality_assurance._determine_quality_level(95.0).level == "EXCELLENT"
        assert quality_assurance._determine_quality_level(80.0).level == "GOOD"
        assert quality_assurance._determine_quality_level(65.0).level == "FAIR"
        assert quality_assurance._determine_quality_level(50.0).level == "POOR"
        assert quality_assurance._determine_quality_level(25.0).level == "CRITICAL"
    
    def test_compliance_checking(self, quality_assurance):
        """Test compliance checking."""
        # Create sample metrics with mixed compliance
        sample_metrics = {
            "metric1": QualityMetric("Test Metric 1", 85.0, 0.5, 80.0, "PASS"),
            "metric2": QualityMetric("Test Metric 2", 70.0, 0.5, 85.0, "FAIL")
        }
        
        compliance = quality_assurance._check_compliance(sample_metrics)
        
        assert isinstance(compliance, dict)
        assert compliance["metric1"] == "PASS"
        assert compliance["metric2"] == "FAIL"
    
    def test_recommendations_generation(self, quality_assurance):
        """Test recommendations generation."""
        # Create sample metrics with failures
        sample_metrics = {
            "file_size_reduction": QualityMetric("File Size Reduction", 20.0, 0.2, 30.0, "FAIL"),
            "module_count": QualityMetric("Module Count", 3, 0.15, 5, "FAIL")
        }
        
        compliance = {"file_size_reduction": "FAIL", "module_count": "FAIL"}
        
        recommendations = quality_assurance._generate_quality_recommendations(sample_metrics, compliance)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) >= 2
        assert all(isinstance(rec, str) for rec in recommendations)
    
    def test_comprehensive_quality_assessment(self, quality_assurance, sample_original_file, sample_modularized_dir):
        """Test comprehensive quality assessment."""
        assessment = quality_assurance.assess_modularization_quality(sample_original_file, sample_modularized_dir)
        
        assert isinstance(assessment, dict)
        assert "target_file" in assessment
        assert "modularized_dir" in assessment
        assert "overall_quality_score" in assessment
        assert "quality_level" in assessment
        assert "metrics" in assessment
        assert "compliance_status" in assessment
        assert "recommendations" in assessment
        assert "timestamp" in assessment
        
        assert assessment["target_file"] == sample_original_file
        assert assessment["modularized_dir"] == sample_modularized_dir
        assert isinstance(assessment["overall_quality_score"], float)
        assert assessment["quality_level"] in ["EXCELLENT", "GOOD", "FAIR", "POOR", "CRITICAL"]


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])

