#!/usr/bin/env python3
"""
Validation Framework Unit Tests
===============================

Unit tests for the V3 validation framework components.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.validation.validation_framework_core import V3ValidationFrameworkCore
from src.validation.validation_utils import (
    load_json_file,
    save_json_file,
    check_file_exists,
    validate_required_fields,
    get_team_alpha_agents,
    format_validation_summary
)
from src.validation.contract_system_validator import ContractSystemValidator
from src.validation.documentation_validator import DocumentationValidator
from src.validation.integration_validator import IntegrationValidator
from src.validation.performance_validator import PerformanceValidator
from src.validation.quality_gates_validator import QualityGatesValidator
from src.validation.security_validator import SecurityValidator
from src.validation.v3_directives_validator import V3DirectivesValidator


class TestV3ValidationFrameworkCore:
    """Test cases for V3ValidationFrameworkCore."""
    
    def test_initialization(self):
        """Test validation framework initialization."""
        framework = V3ValidationFrameworkCore()
        
        assert framework.agent_workspaces == Path("agent_workspaces")
        assert framework.validation_results == {}
    
    def test_run_validation_suite(self, temp_dir):
        """Test running the complete validation suite."""
        framework = V3ValidationFrameworkCore()
        
        # Mock the agent workspaces directory
        with patch.object(framework, 'agent_workspaces', temp_dir):
            # Create mock agent workspace
            agent_dir = temp_dir / "Agent-1"
            agent_dir.mkdir(parents=True, exist_ok=True)
            
            # Mock all validators to return success
            with patch('src.validation.validation_framework_core.V3DirectivesValidator') as mock_v3, \
                 patch('src.validation.validation_framework_core.QualityGatesValidator') as mock_quality, \
                 patch('src.validation.validation_framework_core.ContractSystemValidator') as mock_contract, \
                 patch('src.validation.validation_framework_core.IntegrationValidator') as mock_integration, \
                 patch('src.validation.validation_framework_core.PerformanceValidator') as mock_performance, \
                 patch('src.validation.validation_framework_core.SecurityValidator') as mock_security, \
                 patch('src.validation.validation_framework_core.DocumentationValidator') as mock_docs:
                
                # Configure mock validators
                mock_v3.return_value.validate.return_value = {"status": "passed", "score": 95}
                mock_quality.return_value.validate.return_value = {"status": "passed", "score": 90}
                mock_contract.return_value.validate.return_value = {"status": "passed", "score": 85}
                mock_integration.return_value.validate.return_value = {"status": "passed", "score": 88}
                mock_performance.return_value.validate.return_value = {"status": "passed", "score": 92}
                mock_security.return_value.validate.return_value = {"status": "passed", "score": 87}
                mock_docs.return_value.validate.return_value = {"status": "passed", "score": 89}
                
                results = framework.run_validation_suite()
                
                assert isinstance(results, dict)
                assert "v3_directives" in results
                assert "quality_gates" in results
                assert "contract_system" in results
                assert "integration" in results
                assert "performance" in results
                assert "security" in results
                assert "documentation" in results
    
    def test_get_validation_summary(self):
        """Test getting validation summary."""
        framework = V3ValidationFrameworkCore()
        framework.validation_results = {
            "v3_directives": {"status": "passed", "score": 95},
            "quality_gates": {"status": "passed", "score": 90},
            "contract_system": {"status": "failed", "score": 60}
        }
        
        summary = framework.get_validation_summary()
        
        assert isinstance(summary, dict)
        assert "total_validators" in summary
        assert "passed_validators" in summary
        assert "failed_validators" in summary
        assert "average_score" in summary
        assert summary["total_validators"] == 3
        assert summary["passed_validators"] == 2
        assert summary["failed_validators"] == 1


class TestValidationUtils:
    """Test cases for validation utility functions."""
    
    def test_load_json_file_success(self, temp_dir):
        """Test successful JSON file loading."""
        test_file = temp_dir / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))
        
        result = load_json_file(test_file)
        
        assert result == test_data
    
    def test_load_json_file_not_found(self, temp_dir):
        """Test loading non-existent JSON file."""
        test_file = temp_dir / "nonexistent.json"
        
        result = load_json_file(test_file)
        
        assert result is None
    
    def test_load_json_file_invalid(self, temp_dir):
        """Test loading invalid JSON file."""
        test_file = temp_dir / "invalid.json"
        test_file.write_text("invalid json content")
        
        result = load_json_file(test_file)
        
        assert result is None
    
    def test_save_json_file_success(self, temp_dir):
        """Test successful JSON file saving."""
        test_file = temp_dir / "test.json"
        test_data = {"key": "value", "number": 42}
        
        result = save_json_file(test_file, test_data)
        
        assert result is True
        assert test_file.exists()
        
        # Verify content
        loaded_data = json.loads(test_file.read_text())
        assert loaded_data == test_data
    
    def test_save_json_file_failure(self, temp_dir):
        """Test JSON file saving failure."""
        # Try to save to a directory (should fail)
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()
        
        result = save_json_file(test_dir, {"key": "value"})
        
        assert result is False
    
    def test_check_file_exists_true(self, temp_dir):
        """Test file existence check when file exists."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        result = check_file_exists(test_file)
        
        assert result is True
    
    def test_check_file_exists_false(self, temp_dir):
        """Test file existence check when file doesn't exist."""
        test_file = temp_dir / "nonexistent.txt"
        
        result = check_file_exists(test_file)
        
        assert result is False
    
    def test_validate_required_fields_all_present(self):
        """Test validation when all required fields are present."""
        data = {"field1": "value1", "field2": "value2", "field3": "value3"}
        required_fields = ["field1", "field2"]
        
        result = validate_required_fields(data, required_fields)
        
        assert result is True
    
    def test_validate_required_fields_missing(self):
        """Test validation when required fields are missing."""
        data = {"field1": "value1"}
        required_fields = ["field1", "field2", "field3"]
        
        result = validate_required_fields(data, required_fields)
        
        assert result is False
    
    def test_get_team_alpha_agents(self):
        """Test getting Team Alpha agents list."""
        agents = get_team_alpha_agents()
        
        assert isinstance(agents, list)
        assert len(agents) == 4
        assert "Agent-1" in agents
        assert "Agent-2" in agents
        assert "Agent-3" in agents
        assert "Agent-4" in agents
    
    def test_format_validation_summary(self):
        """Test validation summary formatting."""
        summary = format_validation_summary(3, 5)
        
        assert summary == "3/5 tests passed"


class TestContractSystemValidator:
    """Test cases for ContractSystemValidator."""
    
    def test_initialization(self):
        """Test contract system validator initialization."""
        validator = ContractSystemValidator()
        assert validator is not None
    
    def test_validate_contracts(self, temp_dir):
        """Test contract validation."""
        validator = ContractSystemValidator()
        
        # Create mock contract data
        contract_data = {
            "contracts": [
                {
                    "id": "TEST-001",
                    "title": "Test Contract",
                    "status": "active",
                    "priority": "high"
                }
            ]
        }
        
        result = validator.validate(contract_data)
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "score" in result


class TestDocumentationValidator:
    """Test cases for DocumentationValidator."""
    
    def test_initialization(self):
        """Test documentation validator initialization."""
        validator = DocumentationValidator()
        assert validator is not None
    
    def test_validate_documentation(self, temp_dir):
        """Test documentation validation."""
        validator = DocumentationValidator()
        
        # Create test documentation files
        readme_file = temp_dir / "README.md"
        readme_file.write_text("# Test Project\n\nThis is a test project.")
        
        result = validator.validate({"readme_path": str(readme_file)})
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "score" in result


class TestIntegrationValidator:
    """Test cases for IntegrationValidator."""
    
    def test_initialization(self):
        """Test integration validator initialization."""
        validator = IntegrationValidator()
        assert validator is not None
    
    def test_validate_integration(self):
        """Test integration validation."""
        validator = IntegrationValidator()
        
        result = validator.validate({})
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "score" in result


class TestPerformanceValidator:
    """Test cases for PerformanceValidator."""
    
    def test_initialization(self):
        """Test performance validator initialization."""
        validator = PerformanceValidator()
        assert validator is not None
    
    def test_validate_performance(self):
        """Test performance validation."""
        validator = PerformanceValidator()
        
        result = validator.validate({})
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "score" in result


class TestQualityGatesValidator:
    """Test cases for QualityGatesValidator."""
    
    def test_initialization(self):
        """Test quality gates validator initialization."""
        validator = QualityGatesValidator()
        assert validator is not None
    
    def test_validate_quality_gates(self):
        """Test quality gates validation."""
        validator = QualityGatesValidator()
        
        result = validator.validate({})
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "score" in result


class TestSecurityValidator:
    """Test cases for SecurityValidator."""
    
    def test_initialization(self):
        """Test security validator initialization."""
        validator = SecurityValidator()
        assert validator is not None
    
    def test_validate_security(self):
        """Test security validation."""
        validator = SecurityValidator()
        
        result = validator.validate({})
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "score" in result


class TestV3DirectivesValidator:
    """Test cases for V3DirectivesValidator."""
    
    def test_initialization(self):
        """Test V3 directives validator initialization."""
        validator = V3DirectivesValidator()
        assert validator is not None
    
    def test_validate_v3_directives(self):
        """Test V3 directives validation."""
        validator = V3DirectivesValidator()
        
        result = validator.validate({})
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "score" in result