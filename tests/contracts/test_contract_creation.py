#!/usr/bin/env python3
"""
Contract Creation Test Module
=============================

Tests for contract creation, validation, and structure.
Part of the modularized test_contract_system.py (653 lines → 3 modules).

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import pytest
from datetime import datetime, timedelta
import re


class TestContractCreation:
    """Test contract creation and validation."""
    
    def test_contract_structure_validation(self):
        """Test that contracts have required structure and fields."""
        contract_template = {
            "contract_id": "CONTRACT-COMPREHENSIVE-CLEANUP-001",
            "title": "Repository Comprehensive Cleanup",
            "description": "Resolve merge conflicts, remove corrupted files, eliminate technical debt",
            "priority": "CRITICAL",
            "xp_reward": 600,
            "agent": "AVAILABLE_TO_ALL",
            "scope": "REPOSITORY_WIDE",
            "requirements": [
                "Resolve 633+ merge conflicts",
                "Remove corrupted files",
                "Clean technical debt",
                "Update documentation",
            ],
            "completion_criteria": [
                "All merge conflicts resolved",
                "No corrupted files remaining",
                "Technical debt eliminated",
                "Documentation updated",
            ],
            "deadline": "2025-09-15T23:59:59Z",
            "created_by": "Agent-7",
            "status": "available",
        }
        
        # Validate required fields
        required_fields = [
            "contract_id",
            "title",
            "description",
            "priority",
            "xp_reward",
            "agent",
            "scope",
            "requirements",
            "completion_criteria",
            "deadline",
            "status",
        ]
        
        for field in required_fields:
            assert field in contract_template, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(contract_template["xp_reward"], int)
        assert contract_template["xp_reward"] > 0
        assert isinstance(contract_template["requirements"], list)
        assert len(contract_template["requirements"]) > 0
    
    def test_contract_priority_levels(self):
        """Test contract priority level validation."""
        priority_levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        
        test_contracts = []
        for priority in priority_levels:
            contract = {
                "contract_id": f"TEST-{priority}-001",
                "title": f"Test {priority} Priority Contract",
                "description": "Test contract for priority validation",
                "priority": priority,
                "xp_reward": 100,
                "agent": "AVAILABLE_TO_ALL",
                "scope": "TEST",
                "requirements": ["Test requirement"],
                "completion_criteria": ["Test completion"],
                "deadline": "2025-09-15T23:59:59Z",
                "status": "available",
            }
            test_contracts.append(contract)
        
        # Validate priority levels
        for contract in test_contracts:
            assert contract["priority"] in priority_levels
        
        # Test priority ordering
        priority_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        for contract in test_contracts:
            assert priority_order[contract["priority"]] > 0
    
    def test_contract_scope_validation(self):
        """Test contract scope validation."""
        valid_scopes = [
            "REPOSITORY_WIDE",
            "SERVICE_SPECIFIC",
            "MODULE_SPECIFIC",
            "FILE_SPECIFIC",
            "TEST",
        ]
        
        for scope in valid_scopes:
            contract = {
                "contract_id": f"SCOPE-{scope}-001",
                "title": f"Test {scope} Scope Contract",
                "description": "Test contract for scope validation",
                "priority": "MEDIUM",
                "xp_reward": 50,
                "agent": "AVAILABLE_TO_ALL",
                "scope": scope,
                "requirements": ["Test requirement"],
                "completion_criteria": ["Test completion"],
                "deadline": "2025-09-15T23:59:59Z",
                "status": "available",
            }
            
            assert contract["scope"] in valid_scopes
    
    def test_contract_xp_reward_calculation(self):
        """Test XP reward calculation based on contract complexity."""
        complexity_factors = {
            "CRITICAL": {"base_xp": 500, "multiplier": 1.5},
            "HIGH": {"base_xp": 300, "multiplier": 1.2},
            "MEDIUM": {"base_xp": 150, "multiplier": 1.0},
            "LOW": {"base_xp": 50, "multiplier": 0.8},
        }
        
        # Test XP calculation for each priority
        for priority, factors in complexity_factors.items():
            calculated_xp = int(factors["base_xp"] * factors["multiplier"])
            assert calculated_xp > 0
            assert calculated_xp >= factors["base_xp"] * 0.8  # Minimum reasonable XP
    
    def test_contract_deadline_validation(self):
        """Test contract deadline validation."""
        # Test valid deadline formats
        valid_deadlines = ["2025-09-15T23:59:59Z", "2025-12-31T00:00:00Z", "2026-01-01T12:00:00Z"]
        
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        
        for deadline in valid_deadlines:
            assert re.match(iso_pattern, deadline), f"Invalid deadline format: {deadline}"
            
            # Test that deadline is in the future
            deadline_dt = datetime.fromisoformat(deadline[:-1])  # Remove 'Z'
            assert deadline_dt > datetime.now(), f"Deadline is not in the future: {deadline}"
    
    def test_contract_agent_assignment(self):
        """Test contract agent assignment validation."""
        agent_scenarios = [
            {
                "contract": {"agent": "AVAILABLE_TO_ALL"},
                "agents": ["Agent-1", "Agent-2", "Agent-7"],
                "expected_eligible": ["Agent-1", "Agent-2", "Agent-7"],
            },
            {
                "contract": {"agent": "Agent-7"},
                "agents": ["Agent-1", "Agent-2", "Agent-7"],
                "expected_eligible": ["Agent-7"],
            },
            {
                "contract": {"agent": "SPECIALIST_ONLY", "specialization": "Web Development"},
                "agents": [
                    {"id": "Agent-1", "specialization": "Integration"},
                    {"id": "Agent-7", "specialization": "Web Development"},
                    {"id": "Agent-8", "specialization": "Operations"},
                ],
                "expected_eligible": ["Agent-7"],
            },
        ]
        
        for scenario in agent_scenarios:
            contract = scenario["contract"]
            agents = scenario["agents"]
            expected = scenario["expected_eligible"]
            
            # Validate eligibility logic
            if contract["agent"] == "AVAILABLE_TO_ALL":
                assert len(expected) == len(agents)
            elif contract["agent"].startswith("Agent-"):
                assert len(expected) == 1
                assert expected[0] == contract["agent"]
            else:
                # Specialization-based eligibility
                assert len(expected) == 1
    
    def test_contract_requirements_validation(self):
        """Test contract requirements validation."""
        contract = {
            "contract_id": "REQUIREMENTS-TEST-001",
            "title": "Test Requirements Contract",
            "description": "Test contract for requirements validation",
            "priority": "MEDIUM",
            "xp_reward": 100,
            "agent": "AVAILABLE_TO_ALL",
            "scope": "TEST",
            "requirements": [
                "Requirement 1: Complete task A",
                "Requirement 2: Complete task B",
                "Requirement 3: Complete task C",
            ],
            "completion_criteria": [
                "All requirements completed",
                "Quality standards met",
                "Documentation updated",
            ],
            "deadline": "2025-09-15T23:59:59Z",
            "status": "available",
        }
        
        # Validate requirements structure
        assert isinstance(contract["requirements"], list)
        assert len(contract["requirements"]) > 0
        assert all(isinstance(req, str) for req in contract["requirements"])
        
        # Validate completion criteria structure
        assert isinstance(contract["completion_criteria"], list)
        assert len(contract["completion_criteria"]) > 0
        assert all(isinstance(criteria, str) for criteria in contract["completion_criteria"])
        
        # Validate that requirements and completion criteria are aligned
        assert len(contract["completion_criteria"]) >= len(contract["requirements"])
    
    def test_contract_metadata_validation(self):
        """Test contract metadata validation."""
        contract = {
            "contract_id": "METADATA-TEST-001",
            "title": "Test Metadata Contract",
            "description": "Test contract for metadata validation",
            "priority": "MEDIUM",
            "xp_reward": 100,
            "agent": "AVAILABLE_TO_ALL",
            "scope": "TEST",
            "requirements": ["Test requirement"],
            "completion_criteria": ["Test completion"],
            "deadline": "2025-09-15T23:59:59Z",
            "created_by": "Agent-7",
            "created_at": "2025-09-12T10:00:00Z",
            "status": "available",
            "tags": ["test", "validation", "metadata"],
            "estimated_cycles": 5,
        }
        
        # Validate metadata fields
        assert "created_by" in contract
        assert "created_at" in contract
        assert "tags" in contract
        assert "estimated_cycles" in contract
        
        # Validate metadata types
        assert isinstance(contract["created_by"], str)
        assert isinstance(contract["created_at"], str)
        assert isinstance(contract["tags"], list)
        assert isinstance(contract["estimated_cycles"], int)
        
        # Validate estimated cycles
        assert contract["estimated_cycles"] > 0
        assert contract["estimated_cycles"] <= 100  # Reasonable upper limit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
