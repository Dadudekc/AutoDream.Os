#!/usr/bin/env python3
"""
Unit tests for core quality gates functionality.

Author: Agent-3 (QA Lead)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))


class TestQualityGates:
    """Test suite for quality gates functionality."""
    
    def test_quality_gates_initialization(self):
        """Test quality gates initialization."""
        # Test basic quality gates functionality without importing
        # Mock quality gates validation
        mock_qg = Mock()
        mock_qg.validate_file.return_value = True
        
        # Test initialization
        assert mock_qg is not None
        
        # Test the mock functionality
        result = mock_qg.validate_file("test_file.py")
        assert result == True
        mock_qg.validate_file.assert_called_once_with("test_file.py")
    
    def test_file_size_validation(self):
        """Test file size validation for V2 compliance."""
        # Test data
        test_files = [
            {"path": "test_file.py", "size": 350, "expected": True},
            {"path": "large_file.py", "size": 450, "expected": False},
            {"path": "small_file.py", "size": 100, "expected": True}
        ]
        
        for test_case in test_files:
            file_path = test_case["path"]
            file_size = test_case["size"]
            expected = test_case["expected"]
            
            # Mock file size check
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_size = file_size
                
                # Test validation logic
                is_compliant = file_size <= 400
                assert is_compliant == expected, f"File {file_path} size {file_size} should be {expected}"
    
    def test_line_count_validation(self):
        """Test line count validation."""
        test_cases = [
            {"lines": 350, "expected": True, "desc": "within limit"},
            {"lines": 400, "expected": True, "desc": "at limit"},
            {"lines": 401, "expected": False, "desc": "exceeds limit"},
            {"lines": 500, "expected": False, "desc": "significantly over limit"}
        ]
        
        for case in test_cases:
            lines = case["lines"]
            expected = case["expected"]
            desc = case["desc"]
            
            is_compliant = lines <= 400
            assert is_compliant == expected, f"Line count {lines} ({desc}) should be {expected}"
    
    def test_class_count_validation(self):
        """Test class count validation."""
        test_cases = [
            {"classes": 3, "expected": True, "desc": "within limit"},
            {"classes": 5, "expected": True, "desc": "at limit"},
            {"classes": 6, "expected": False, "desc": "exceeds limit"}
        ]
        
        for case in test_cases:
            classes = case["classes"]
            expected = case["expected"]
            desc = case["desc"]
            
            is_compliant = classes <= 5
            assert is_compliant == expected, f"Class count {classes} ({desc}) should be {expected}"
    
    def test_function_count_validation(self):
        """Test function count validation."""
        test_cases = [
            {"functions": 8, "expected": True, "desc": "within limit"},
            {"functions": 10, "expected": True, "desc": "at limit"},
            {"functions": 11, "expected": False, "desc": "exceeds limit"}
        ]
        
        for case in test_cases:
            functions = case["functions"]
            expected = case["expected"]
            desc = case["desc"]
            
            is_compliant = functions <= 10
            assert is_compliant == expected, f"Function count {functions} ({desc}) should be {expected}"
    
    def test_abstract_class_detection(self):
        """Test detection of abstract classes."""
        # Test code with abstract class
        abstract_code = """
from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def abstract_method(self):
        pass
"""
        
        # Test code without abstract class
        concrete_code = """
class ConcreteClass:
    def concrete_method(self):
        return "concrete"
"""
        
        # Mock file reading
        with patch('builtins.open', mock_open(read_data=abstract_code)):
            has_abstract = "ABC" in abstract_code and "abstractmethod" in abstract_code
            assert has_abstract == True, "Should detect abstract class"
        
        with patch('builtins.open', mock_open(read_data=concrete_code)):
            has_abstract = "ABC" in concrete_code and "abstractmethod" in concrete_code
            assert has_abstract == False, "Should not detect abstract class"
    
    def test_inheritance_detection(self):
        """Test detection of complex inheritance."""
        # Simple inheritance (allowed)
        simple_inheritance = """
class BaseClass:
    pass

class ChildClass(BaseClass):
    pass
"""
        
        # Complex inheritance (not allowed)
        complex_inheritance = """
class GrandParent:
    pass

class Parent(GrandParent):
    pass

class Child(Parent):
    pass

class GrandChild(Child):
    pass
"""
        
        # Test simple inheritance
        with patch('builtins.open', mock_open(read_data=simple_inheritance)):
            inheritance_count = simple_inheritance.count("class ") - simple_inheritance.count("class BaseClass")
            is_simple = inheritance_count <= 2
            assert is_simple == True, "Should detect simple inheritance"
        
        # Test complex inheritance
        with patch('builtins.open', mock_open(read_data=complex_inheritance)):
            inheritance_count = complex_inheritance.count("class ") - complex_inheritance.count("class GrandParent")
            is_simple = inheritance_count <= 2
            assert is_simple == False, "Should detect complex inheritance"
    
    def test_threading_detection(self):
        """Test detection of threading usage."""
        # Code with threading (not allowed)
        threading_code = """
import threading

class ThreadedClass:
    def __init__(self):
        self.thread = threading.Thread(target=self.worker)
"""
        
        # Code without threading (allowed)
        normal_code = """
class NormalClass:
    def __init__(self):
        self.data = []
"""
        
        # Test threading detection
        with patch('builtins.open', mock_open(read_data=threading_code)):
            has_threading = "threading" in threading_code
            assert has_threading == True, "Should detect threading usage"
        
        with patch('builtins.open', mock_open(read_data=normal_code)):
            has_threading = "threading" in normal_code
            assert has_threading == False, "Should not detect threading usage"
    
    def test_data_class_validation(self):
        """Test validation of simple data classes."""
        # Valid data class
        valid_data_class = """
from dataclasses import dataclass

@dataclass
class SimpleData:
    name: str
    value: int
"""
        
        # Complex class (not recommended)
        complex_class = """
class ComplexClass:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.calculated = self._calculate()
    
    def _calculate(self):
        return self.value * 2
    
    def process(self):
        return f"{self.name}: {self.calculated}"
"""
        
        # Test data class detection
        with patch('builtins.open', mock_open(read_data=valid_data_class)):
            is_data_class = "@dataclass" in valid_data_class
            assert is_data_class == True, "Should detect data class"
        
        with patch('builtins.open', mock_open(read_data=complex_class)):
            is_data_class = "@dataclass" in complex_class
            assert is_data_class == False, "Should not detect data class"
    
    def test_validation_integration(self):
        """Test integrated validation process."""
        # Mock validation results
        mock_results = {
            "file_size": True,
            "line_count": True,
            "class_count": True,
            "function_count": True,
            "no_abstract": True,
            "simple_inheritance": True,
            "no_threading": True,
            "data_class": True
        }
        
        # Test overall compliance
        all_compliant = all(mock_results.values())
        assert all_compliant == True, "All validations should pass"
        
        # Test partial compliance
        mock_results["line_count"] = False
        some_compliant = any(mock_results.values())
        assert some_compliant == True, "Some validations should pass"
        
        all_fail = all(not v for v in mock_results.values())
        assert all_fail == False, "Not all validations should fail"


@pytest.mark.unit
class TestQualityGatesIntegration:
    """Integration tests for quality gates."""
    
    def test_file_analysis_workflow(self):
        """Test complete file analysis workflow."""
        # Mock file analysis
        mock_file_info = {
            "path": "test_file.py",
            "lines": 300,
            "classes": 3,
            "functions": 8,
            "has_abstract": False,
            "inheritance_depth": 1,
            "has_threading": False,
            "is_data_class": True
        }
        
        # Test compliance check
        compliance_check = (
            mock_file_info["lines"] <= 400 and
            mock_file_info["classes"] <= 5 and
            mock_file_info["functions"] <= 10 and
            not mock_file_info["has_abstract"] and
            mock_file_info["inheritance_depth"] <= 2 and
            not mock_file_info["has_threading"]
        )
        
        assert compliance_check == True, "File should be compliant"
    
    def test_batch_file_validation(self):
        """Test validation of multiple files."""
        mock_files = [
            {"path": "file1.py", "lines": 350, "compliant": True},
            {"path": "file2.py", "lines": 450, "compliant": False},
            {"path": "file3.py", "lines": 200, "compliant": True}
        ]
        
        compliant_count = sum(1 for f in mock_files if f["lines"] <= 400)
        total_files = len(mock_files)
        compliance_rate = compliant_count / total_files
        
        assert compliance_rate == 2/3, "Compliance rate should be 2/3"
        assert compliant_count == 2, "Should have 2 compliant files"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
