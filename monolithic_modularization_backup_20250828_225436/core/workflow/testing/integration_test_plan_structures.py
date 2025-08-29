#!/usr/bin/env python3
"""
Integration Test Plan Structures
===============================

Dataclasses defining result structures for the workflow integration test plan.
Follows V2 standards: <=200 LOC, single responsibility.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ContractIntegrationResult:
    """Results for contract workflow integration tests."""
    contracts_processed: int = 0
    workflows_created: int = 0
    integration_success: int = 0
    integration_failures: int = 0
    workflows: Dict[str, str] = field(default_factory=dict)
    details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LearningIntegrationResult:
    """Results for learning workflow integration tests."""
    learning_workflows_created: int = 0
    decision_workflows_created: int = 0
    integration_success: int = 0
    integration_failures: int = 0
    details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BusinessProcessIntegrationResult:
    """Results for business process workflow integration tests."""
    business_processes_created: int = 0
    approval_workflows: int = 0
    compliance_tracking: int = 0
    integration_success: int = 0
    integration_failures: int = 0
    details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PerformanceTestResult:
    """Results for performance and scalability tests."""
    workflow_creation_time: float = 0.0
    execution_time: float = 0.0
    memory_usage: float = 0.0
    concurrent_workflows: int = 0
    performance_score: float = 0.0
    details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DataModelCompatibilityResult:
    """Results for data model compatibility tests."""
    models_tested: int = 0
    compatibility_success: int = 0
    compatibility_failures: int = 0
    validation_errors: List[str] = field(default_factory=list)
    details: List[Dict[str, Any]] = field(default_factory=list)
