
# MIGRATED: This file has been migrated to the centralized configuration system
"""
Configuration for automated integration test suites.
"""

from .models import TestSuiteCategory, TestExecutionMode


# Default test suite configurations
DEFAULT_TEST_SUITES = {
    "core_system_basic": {
        "suite_id": "core_system_basic",
        "name": "Core System Basic Tests",
        "description": "Basic functionality tests for core system components",
        "category": TestSuiteCategory.CORE_SYSTEM,
        "priority": "HIGH",
        "execution_mode": TestExecutionMode.SEQUENTIAL,
        "timeout": 300,
        "max_retries": 2,
        "dependencies": [],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": False,
        "max_parallel_tests": 1
    },
    
    "workflow_basic": {
        "suite_id": "workflow_basic",
        "name": "Workflow System Basic Tests",
        "description": "Basic workflow functionality and state management tests",
        "category": TestSuiteCategory.WORKFLOW_SYSTEM,
        "priority": "HIGH",
        "execution_mode": TestExecutionMode.SEQUENTIAL,
        "timeout": 400,
        "max_retries": 2,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": False,
        "max_parallel_tests": 1
    },
    
    "agent_management_basic": {
        "suite_id": "agent_management_basic",
        "name": "Agent Management Basic Tests",
        "description": "Basic agent lifecycle and management tests",
        "category": TestSuiteCategory.AGENT_MANAGEMENT,
        "priority": "MEDIUM",
        "execution_mode": TestExecutionMode.PARALLEL,
        "timeout": 300,
        "max_retries": 2,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": True,
        "max_parallel_tests": 2
    },
    
    "communication_basic": {
        "suite_id": "communication_basic",
        "name": "Communication System Basic Tests",
        "description": "Basic communication and messaging tests",
        "category": TestSuiteCategory.COMMUNICATION_SYSTEM,
        "priority": "MEDIUM",
        "execution_mode": TestExecutionMode.PARALLEL,
        "timeout": 300,
        "max_retries": 2,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": True,
        "max_parallel_tests": 2
    },
    
    "api_integration_basic": {
        "suite_id": "api_integration_basic",
        "name": "API Integration Basic Tests",
        "description": "Basic API integration and endpoint tests",
        "category": TestSuiteCategory.API_INTEGRATION,
        "priority": "MEDIUM",
        "execution_mode": TestExecutionMode.PARALLEL,
        "timeout": 400,
        "max_retries": 2,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": True,
        "max_parallel_tests": 3
    },
    
    "database_integration_basic": {
        "suite_id": "database_integration_basic",
        "name": "Database Integration Basic Tests",
        "description": "Basic database connectivity and CRUD tests",
        "category": TestSuiteCategory.DATABASE_INTEGRATION,
        "priority": "MEDIUM",
        "execution_mode": TestExecutionMode.SEQUENTIAL,
        "timeout": 500,
        "max_retries": 3,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": False,
        "max_parallel_tests": 1
    },
    
    "end_to_end_basic": {
        "suite_id": "end_to_end_basic",
        "name": "End-to-End Basic Tests",
        "description": "Basic end-to-end workflow tests",
        "category": TestSuiteCategory.END_TO_END,
        "priority": "LOW",
        "execution_mode": TestExecutionMode.SEQUENTIAL,
        "timeout": 600,
        "max_retries": 2,
        "dependencies": [
            "core_system_basic",
            "workflow_basic",
            "agent_management_basic",
            "communication_basic"
        ],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": False,
        "max_parallel_tests": 1
    },
    
    "performance_basic": {
        "suite_id": "performance_basic",
        "name": "Performance Basic Tests",
        "description": "Basic performance and load testing",
        "category": TestSuiteCategory.PERFORMANCE,
        "priority": "LOW",
        "execution_mode": TestExecutionMode.PARALLEL,
        "timeout": 800,
        "max_retries": 1,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": True,
        "max_parallel_tests": 2
    },
    
    "security_basic": {
        "suite_id": "security_basic",
        "name": "Security Basic Tests",
        "description": "Basic security and authentication tests",
        "category": TestSuiteCategory.SECURITY,
        "priority": "HIGH",
        "execution_mode": TestExecutionMode.SEQUENTIAL,
        "timeout": 400,
        "max_retries": 2,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": False,
        "max_parallel_tests": 1
    },
    
    "compliance_basic": {
        "suite_id": "compliance_basic",
        "name": "Compliance Basic Tests",
        "description": "Basic compliance and standards tests",
        "category": TestSuiteCategory.COMPLIANCE,
        "priority": "MEDIUM",
        "execution_mode": TestExecutionMode.PARALLEL,
        "timeout": 300,
        "max_retries": 2,
        "dependencies": ["core_system_basic"],
        "prerequisites": [],
        "cleanup_required": True,
        "parallel_execution": True,
        "max_parallel_tests": 2
    }
}
