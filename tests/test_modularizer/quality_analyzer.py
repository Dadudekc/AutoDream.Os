"""
🧪 QUALITY ASSURANCE ANALYZER - MODULARIZED COMPONENT
Testing Framework Enhancement Manager - Agent-3

This module contains quality analysis functionality.
Extracted from quality_assurance_protocols.py for better modularity.
"""

from pathlib import Path
from typing import Dict, Any, List
from .quality_utilities import analyze_file_structure, is_interface_file, extract_imports, build_dependency_graph


class QualityAnalyzer:
    """Analyzer for quality assessment components."""
    
    def analyze_original_file(self, target_file: str) -> Dict[str, Any]:
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
                # Use utility function for file analysis
                file_analysis = analyze_file_structure(file_path)
                analysis.update(file_analysis)
                
        except Exception as e:
            analysis["error"] = str(e)
            
        return analysis
    
    def analyze_modularized_components(self, modularized_dir: str) -> Dict[str, Any]:
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
                        if is_interface_file(content):
                            analysis["interface_files"].append(str(py_file))
                            
                        # Analyze imports
                        imports = extract_imports(content)
                        analysis["import_structure"][str(py_file)] = imports
                        
                    except Exception as e:
                        print(f"Error analyzing {py_file}: {e}")
                        
                # Build dependency graph
                analysis["dependency_graph"] = build_dependency_graph(analysis["import_structure"])
                
        except Exception as e:
            analysis["error"] = str(e)
            
        return analysis
    
    def calculate_all_metrics(self, original_analysis: Dict[str, Any], 
                            modularized_analysis: Dict[str, Any],
                            metrics_calculator,
                            quality_assessor) -> Dict[str, Any]:
        """
        Calculate all quality metrics based on analysis results.
        
        Args:
            original_analysis: Analysis of the original file
            modularized_analysis: Analysis of modularized components
            metrics_calculator: Instance of QualityMetricsCalculator
            quality_assessor: Instance of QualityAssessor
            
        Returns:
            Dictionary of quality metrics
        """
        metrics = {}
        
        try:
            # File size reduction metric
            if original_analysis["file_size"] > 0:
                metrics["file_size_reduction"] = metrics_calculator.calculate_file_size_reduction(
                    original_analysis["file_size"], 
                    modularized_analysis["total_size"]
                )
            
            # Module count metric
            module_count = modularized_analysis["total_files"]
            metrics["module_count"] = metrics_calculator.calculate_module_count_metric(module_count)
            
            # Interface quality metric
            interface_quality = quality_assessor.assess_interface_quality(modularized_analysis)
            metrics["interface_quality"] = metrics_calculator.calculate_interface_quality_metric(interface_quality)
            
            # Dependency complexity metric
            dependency_complexity = quality_assessor.assess_dependency_complexity(modularized_analysis)
            metrics["dependency_complexity"] = metrics_calculator.calculate_dependency_complexity_metric(dependency_complexity)
            
            # Naming conventions metric
            naming_score = quality_assessor.assess_naming_conventions(modularized_analysis)
            metrics["naming_conventions"] = metrics_calculator.calculate_naming_conventions_metric(naming_score)
            
            # Code organization metric
            organization_score = quality_assessor.assess_code_organization(modularized_analysis)
            metrics["code_organization"] = metrics_calculator.calculate_code_organization_metric(organization_score)
            
            # Documentation quality metric
            documentation_score = quality_assessor.assess_documentation_quality(modularized_analysis)
            metrics["documentation"] = metrics_calculator.calculate_documentation_metric(documentation_score)
            
        except Exception as e:
            print(f"Error calculating quality metrics: {e}")
            
        return metrics
