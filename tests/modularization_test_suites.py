"""
File-Type Specific Test Suites for Monolithic File Modularization

This module provides specialized testing capabilities for different types of
monolithic files, including test files, core modules, agent workspaces, and
utility files.
"""

import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class TestFileMetrics:
    """Specific metrics for test files."""
    test_functions: int
    test_classes: int
    test_methods: int
    assertions_per_test: float
    test_data_sets: int
    mock_objects: int
    integration_tests: int
    unit_tests: int


@dataclass
class CoreModuleMetrics:
    """Specific metrics for core system modules."""
    public_functions: int
    public_classes: int
    private_functions: int
    private_classes: int
    interface_methods: int
    abstract_classes: int
    singleton_patterns: int
    factory_patterns: int


@dataclass
class AgentWorkspaceMetrics:
    """Specific metrics for agent workspace files."""
    agent_specific_functions: int
    communication_methods: int
    task_management_functions: int
    state_management_functions: int
    external_api_calls: int
    database_operations: int
    file_operations: int


@dataclass
class UtilityFileMetrics:
    """Specific metrics for utility files."""
    utility_functions: int
    helper_classes: int
    constants: int
    configuration_options: int
    data_structures: int
    algorithms: int


class TestFileAnalyzer:
    """Specialized analyzer for test files."""
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.ast_tree = None
        
    def analyze_test_file(self) -> TestFileMetrics:
        """Analyze a test file and return test-specific metrics."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.ast_tree = ast.parse(content)
            
            metrics = TestFileMetrics(
                test_functions=self._count_test_functions(),
                test_classes=self._count_test_classes(),
                test_methods=self._count_test_methods(),
                assertions_per_test=self._calculate_assertions_per_test(),
                test_data_sets=self._count_test_data_sets(),
                mock_objects=self._count_mock_objects(),
                integration_tests=self._count_integration_tests(),
                unit_tests=self._count_unit_tests()
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing test file {self.file_path}: {e}")
            raise
    
    def _count_test_functions(self) -> int:
        """Count functions that start with 'test_'."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('test_'):
                    count += 1
        return count
    
    def _count_test_classes(self) -> int:
        """Count test classes."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                if node.name.startswith('Test') or 'test' in node.name.lower():
                    count += 1
        return count
    
    def _count_test_methods(self) -> int:
        """Count test methods within test classes."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                # Check if this is a method within a test class
                if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
                    if node.name.startswith('test_'):
                        count += 1
        return count
    
    def _calculate_assertions_per_test(self) -> float:
        """Calculate average assertions per test."""
        test_count = self._count_test_functions() + self._count_test_methods()
        if test_count == 0:
            return 0.0
            
        assertion_count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr.startswith('assert'):
                    assertion_count += 1
                elif hasattr(node.func, 'id') and str(node.func.id).startswith('assert'):
                    assertion_count += 1
                    
        return assertion_count / test_count if test_count > 0 else 0.0
    
    def _count_test_data_sets(self) -> int:
        """Count test data sets and fixtures."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and 'data' in target.id.lower():
                        count += 1
                    elif isinstance(target, ast.Name) and 'fixture' in target.id.lower():
                        count += 1
        return count
    
    def _count_mock_objects(self) -> int:
        """Count mock objects and patches."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and 'mock' in str(node.func.id).lower():
                    count += 1
                elif hasattr(node.func, 'attr') and 'mock' in str(node.func.attr).lower():
                    count += 1
        return count
    
    def _count_integration_tests(self) -> int:
        """Count integration tests based on file content patterns."""
        if not self.ast_tree:
            return 0
            
        # Look for integration test indicators
        integration_indicators = ['database', 'api', 'network', 'external', 'integration']
        count = 0
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('test_'):
                    # Check function name and docstring for integration indicators
                    if any(indicator in node.name.lower() for indicator in integration_indicators):
                        count += 1
        return count
    
    def _count_unit_tests(self) -> int:
        """Count unit tests."""
        total_tests = self._count_test_functions() + self._count_test_methods()
        integration_tests = self._count_integration_tests()
        return total_tests - integration_tests


class CoreModuleAnalyzer:
    """Specialized analyzer for core system modules."""
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.ast_tree = None
        
    def analyze_core_module(self) -> CoreModuleMetrics:
        """Analyze a core module and return core-specific metrics."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.ast_tree = ast.parse(content)
            
            metrics = CoreModuleMetrics(
                public_functions=self._count_public_functions(),
                public_classes=self._count_public_classes(),
                private_functions=self._count_private_functions(),
                private_classes=self._count_private_classes(),
                interface_methods=self._count_interface_methods(),
                abstract_classes=self._count_abstract_classes(),
                singleton_patterns=self._count_singleton_patterns(),
                factory_patterns=self._count_factory_patterns()
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing core module {self.file_path}: {e}")
            raise
    
    def _count_public_functions(self) -> int:
        """Count public functions (not starting with underscore)."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):
                    count += 1
        return count
    
    def _count_public_classes(self) -> int:
        """Count public classes (not starting with underscore)."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                if not node.name.startswith('_'):
                    count += 1
        return count
    
    def _count_private_functions(self) -> int:
        """Count private functions (starting with underscore)."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('_'):
                    count += 1
        return count
    
    def _count_private_classes(self) -> int:
        """Count private classes (starting with underscore)."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                if node.name.startswith('_'):
                    count += 1
        return count
    
    def _count_interface_methods(self) -> int:
        """Count interface methods (methods with only pass or raise)."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                # Check if method body is minimal (interface-like)
                if len(node.body) == 1:
                    if isinstance(node.body[0], ast.Pass):
                        count += 1
                    elif isinstance(node.body[0], ast.Raise):
                        count += 1
        return count
    
    def _count_abstract_classes(self) -> int:
        """Count abstract classes."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                # Check for ABC inheritance or abstractmethod decorators
                for base in node.bases:
                    if hasattr(base, 'id') and 'ABC' in str(base.id):
                        count += 1
                        break
        return count
    
    def _count_singleton_patterns(self) -> int:
        """Count singleton pattern implementations."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                # Look for singleton indicators
                if 'singleton' in node.name.lower() or 'instance' in node.name.lower():
                    count += 1
        return count
    
    def _count_factory_patterns(self) -> int:
        """Count factory pattern implementations."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                # Look for factory indicators
                if 'factory' in node.name.lower() or 'creator' in node.name.lower():
                    count += 1
        return count


class AgentWorkspaceAnalyzer:
    """Specialized analyzer for agent workspace files."""
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.ast_tree = None
        
    def analyze_agent_workspace(self) -> AgentWorkspaceMetrics:
        """Analyze an agent workspace file and return agent-specific metrics."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.ast_tree = ast.parse(content)
            
            metrics = AgentWorkspaceMetrics(
                agent_specific_functions=self._count_agent_functions(),
                communication_methods=self._count_communication_methods(),
                task_management_functions=self._count_task_management_functions(),
                state_management_functions=self._count_state_management_functions(),
                external_api_calls=self._count_external_api_calls(),
                database_operations=self._count_database_operations(),
                file_operations=self._count_file_operations()
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing agent workspace {self.file_path}: {e}")
            raise
    
    def _count_agent_functions(self) -> int:
        """Count agent-specific functions."""
        if not self.ast_tree:
            return 0
            
        count = 0
        agent_keywords = ['agent', 'task', 'mission', 'contract', 'workflow']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if any(keyword in node.name.lower() for keyword in agent_keywords):
                    count += 1
        return count
    
    def _count_communication_methods(self) -> int:
        """Count communication-related methods."""
        if not self.ast_tree:
            return 0
            
        count = 0
        comm_keywords = ['send', 'receive', 'message', 'communication', 'notify']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if any(keyword in node.name.lower() for keyword in comm_keywords):
                    count += 1
        return count
    
    def _count_task_management_functions(self) -> int:
        """Count task management functions."""
        if not self.ast_tree:
            return 0
            
        count = 0
        task_keywords = ['task', 'mission', 'contract', 'assignment', 'execute']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if any(keyword in node.name.lower() for keyword in task_keywords):
                    count += 1
        return count
    
    def _count_state_management_functions(self) -> int:
        """Count state management functions."""
        if not self.ast_tree:
            return 0
            
        count = 0
        state_keywords = ['state', 'status', 'update', 'change', 'transition']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if any(keyword in node.name.lower() for keyword in state_keywords):
                    count += 1
        return count
    
    def _count_external_api_calls(self) -> int:
        """Count external API calls."""
        if not self.ast_tree:
            return 0
            
        count = 0
        api_keywords = ['http', 'request', 'api', 'rest', 'client']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and any(keyword in str(node.func.id).lower() for keyword in api_keywords):
                    count += 1
        return count
    
    def _count_database_operations(self) -> int:
        """Count database operations."""
        if not self.ast_tree:
            return 0
            
        count = 0
        db_keywords = ['query', 'insert', 'update', 'delete', 'database', 'db']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and any(keyword in str(node.func.id).lower() for keyword in db_keywords):
                    count += 1
        return count
    
    def _count_file_operations(self) -> int:
        """Count file operations."""
        if not self.ast_tree:
            return 0
            
        count = 0
        file_keywords = ['read', 'write', 'open', 'save', 'load', 'file']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and any(keyword in str(node.func.id).lower() for keyword in file_keywords):
                    count += 1
        return count


class UtilityFileAnalyzer:
    """Specialized analyzer for utility files."""
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.ast_tree = None
        
    def analyze_utility_file(self) -> UtilityFileMetrics:
        """Analyze a utility file and return utility-specific metrics."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.ast_tree = ast.parse(content)
            
            metrics = UtilityFileMetrics(
                utility_functions=self._count_utility_functions(),
                helper_classes=self._count_helper_classes(),
                constants=self._count_constants(),
                configuration_options=self._count_configuration_options(),
                data_structures=self._count_data_structures(),
                algorithms=self._count_algorithms()
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing utility file {self.file_path}: {e}")
            raise
    
    def _count_utility_functions(self) -> int:
        """Count utility functions."""
        if not self.ast_tree:
            return 0
            
        count = 0
        utility_keywords = ['util', 'helper', 'format', 'parse', 'convert', 'validate']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if any(keyword in node.name.lower() for keyword in utility_keywords):
                    count += 1
        return count
    
    def _count_helper_classes(self) -> int:
        """Count helper classes."""
        if not self.ast_tree:
            return 0
            
        count = 0
        helper_keywords = ['helper', 'util', 'support', 'assist']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                if any(keyword in node.name.lower() for keyword in helper_keywords):
                    count += 1
        return count
    
    def _count_constants(self) -> int:
        """Count constant definitions."""
        if not self.ast_tree:
            return 0
            
        count = 0
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        count += 1
        return count
    
    def _count_configuration_options(self) -> int:
        """Count configuration options."""
        if not self.ast_tree:
            return 0
            
        count = 0
        config_keywords = ['config', 'setting', 'option', 'parameter']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and any(keyword in target.id.lower() for keyword in config_keywords):
                        count += 1
        return count
    
    def _count_data_structures(self) -> int:
        """Count data structure definitions."""
        if not self.ast_tree:
            return 0
            
        count = 0
        ds_keywords = ['list', 'dict', 'set', 'tuple', 'queue', 'stack', 'tree', 'graph']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                if any(keyword in node.name.lower() for keyword in ds_keywords):
                    count += 1
        return count
    
    def _count_algorithms(self) -> int:
        """Count algorithm implementations."""
        if not self.ast_tree:
            return 0
            
        count = 0
        algo_keywords = ['sort', 'search', 'filter', 'map', 'reduce', 'algorithm']
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                if any(keyword in node.name.lower() for keyword in algo_keywords):
                    count += 1
        return count


class FileTypeTestSuiteFactory:
    """Factory for creating file-type specific test suites."""
    
    @staticmethod
    def create_analyzer(file_path: Path, file_type: str):
        """Create the appropriate analyzer based on file type."""
        if 'test' in str(file_path).lower():
            return TestFileAnalyzer(file_path)
        elif 'core' in str(file_path).lower() or 'src/core' in str(file_path):
            return CoreModuleAnalyzer(file_path)
        elif 'agent_workspace' in str(file_path) or 'agent_workspaces' in str(file_path):
            return AgentWorkspaceAnalyzer(file_path)
        else:
            return UtilityFileAnalyzer(file_path)
    
    @staticmethod
    def analyze_file_by_type(file_path: Path, file_type: str) -> Dict[str, Any]:
        """Analyze a file using the appropriate analyzer and return results."""
        analyzer = FileTypeTestSuiteFactory.create_analyzer(file_path, file_type)
        
        if isinstance(analyzer, TestFileAnalyzer):
            metrics = analyzer.analyze_test_file()
            return {
                "file_type": "test_file",
                "metrics": asdict(metrics),
                "recommendations": FileTypeTestSuiteFactory._get_test_file_recommendations(metrics)
            }
        elif isinstance(analyzer, CoreModuleAnalyzer):
            metrics = analyzer.analyze_core_module()
            return {
                "file_type": "core_module",
                "metrics": asdict(metrics),
                "recommendations": FileTypeTestSuiteFactory._get_core_module_recommendations(metrics)
            }
        elif isinstance(analyzer, AgentWorkspaceAnalyzer):
            metrics = analyzer.analyze_agent_workspace()
            return {
                "file_type": "agent_workspace",
                "metrics": asdict(metrics),
                "recommendations": FileTypeTestSuiteFactory._get_agent_workspace_recommendations(metrics)
            }
        else:
            metrics = analyzer.analyze_utility_file()
            return {
                "file_type": "utility_file",
                "metrics": asdict(metrics),
                "recommendations": FileTypeTestSuiteFactory._get_utility_file_recommendations(metrics)
            }
    
    @staticmethod
    def _get_test_file_recommendations(metrics: TestFileMetrics) -> List[str]:
        """Get recommendations for test files."""
        recommendations = []
        
        if metrics.test_functions < 5:
            recommendations.append("Add more test functions to improve coverage")
        if metrics.assertions_per_test < 2:
            recommendations.append("Increase assertions per test for better validation")
        if metrics.test_data_sets < 3:
            recommendations.append("Add more test data sets for comprehensive testing")
        if metrics.mock_objects < 2:
            recommendations.append("Use more mock objects to isolate units under test")
            
        return recommendations
    
    @staticmethod
    def _get_core_module_recommendations(metrics: CoreModuleMetrics) -> List[str]:
        """Get recommendations for core modules."""
        recommendations = []
        
        if metrics.public_functions > 20:
            recommendations.append("Consider splitting into multiple modules")
        if metrics.private_functions > 15:
            recommendations.append("Extract private functions to utility modules")
        if metrics.interface_methods < 3:
            recommendations.append("Define more interface methods for better abstraction")
        if metrics.abstract_classes < 2:
            recommendations.append("Use abstract classes for common interfaces")
            
        return recommendations
    
    @staticmethod
    def _get_agent_workspace_recommendations(metrics: AgentWorkspaceMetrics) -> List[str]:
        """Get recommendations for agent workspace files."""
        recommendations = []
        
        if metrics.agent_specific_functions > 25:
            recommendations.append("Split agent functionality into specialized modules")
        if metrics.communication_methods > 10:
            recommendations.append("Extract communication logic to separate module")
        if metrics.task_management_functions > 15:
            recommendations.append("Create dedicated task management module")
        if metrics.external_api_calls > 8:
            recommendations.append("Abstract external API calls into service layer")
            
        return recommendations
    
    @staticmethod
    def _get_utility_file_recommendations(metrics: UtilityFileMetrics) -> List[str]:
        """Get recommendations for utility files."""
        recommendations = []
        
        if metrics.utility_functions > 30:
            recommendations.append("Group related utilities into specialized modules")
        if metrics.helper_classes > 10:
            recommendations.append("Organize helper classes by functionality")
        if metrics.constants > 20:
            recommendations.append("Move constants to configuration files")
        if metrics.configuration_options > 15:
            recommendations.append("Use configuration management system")
            
        return recommendations


def run_file_type_specific_tests(file_paths: List[Path]) -> Dict[str, Any]:
    """Run file-type specific tests for a list of files."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "files_analyzed": len(file_paths),
        "file_type_results": {}
    }
    
    for file_path in file_paths:
        try:
            # Determine file type based on path and content
            file_type = _determine_file_type(file_path)
            
            # Analyze using appropriate analyzer
            analysis_result = FileTypeTestSuiteFactory.analyze_file_by_type(file_path, file_type)
            
            # Store results by file type
            file_type = analysis_result["file_type"]
            if file_type not in results["file_type_results"]:
                results["file_type_results"][file_type] = []
                
            results["file_type_results"][file_type].append({
                "file_path": str(file_path),
                "analysis": analysis_result
            })
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            if "errors" not in results:
                results["errors"] = []
            results["errors"].append({
                "file_path": str(file_path),
                "error": str(e)
            })
    
    return results


def _determine_file_type(file_path: Path) -> str:
    """Determine the type of file based on path and content."""
    path_str = str(file_path).lower()
    
    if 'test' in path_str:
        return 'test_file'
    elif 'core' in path_str or 'src/core' in path_str:
        return 'core_module'
    elif 'agent_workspace' in path_str or 'agent_workspaces' in path_str:
        return 'agent_workspace'
    else:
        return 'utility_file'
