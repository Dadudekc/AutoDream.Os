"""
Test Categories Configuration

Centralized configuration for all test categories in the testing framework.
"""

from typing import Dict, Any


class TestCategories:
    """Test categories configuration and management."""
    
    @staticmethod
    def get_categories() -> Dict[str, Dict[str, Any]]:
        """Get all test categories configuration."""
        return {
            "smoke": {
                "description": "Smoke tests for basic functionality validation",
                "marker": "smoke",
                "timeout": 60,
                "critical": True,
                "command": ["-m", "smoke"],
            },
            "unit": {
                "description": "Unit tests for individual components",
                "marker": "unit",
                "timeout": 120,
                "critical": True,
                "command": ["-m", "unit"],
            },
            "integration": {
                "description": "Integration tests for component interaction",
                "marker": "integration",
                "timeout": 300,
                "critical": False,
                "command": ["-m", "integration"],
            },
            "performance": {
                "description": "Performance and load testing",
                "marker": "performance",
                "timeout": 600,
                "critical": False,
                "command": ["-m", "performance"],
            },
            "security": {
                "description": "Security and vulnerability testing",
                "marker": "security",
                "timeout": 180,
                "critical": True,
                "command": ["-m", "security"],
            },
            "api": {
                "description": "API endpoint testing",
                "marker": "api",
                "timeout": 240,
                "critical": False,
                "command": ["-m", "api"],
            },
        }
    
    @staticmethod
    def get_category(category: str) -> Dict[str, Any]:
        """Get configuration for a specific test category."""
        categories = TestCategories.get_categories()
        return categories.get(category, {})
    
    @staticmethod
    def list_categories() -> list:
        """List all available test categories."""
        return list(TestCategories.get_categories().keys())
    
    @staticmethod
    def is_critical(category: str) -> bool:
        """Check if a test category is critical."""
        config = TestCategories.get_category(category)
        return config.get('critical', False)
    
    @staticmethod
    def get_timeout(category: str) -> int:
        """Get timeout for a test category."""
        config = TestCategories.get_category(category)
        return config.get('timeout', 300)

