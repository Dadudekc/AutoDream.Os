"""
Test Specialized Managers - Phase-2 V2 Compliance Refactoring
============================================================

Tests for the new specialized service managers extracted from CoreServiceManager.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import pytest
from datetime import datetime
from src.core.managers import (
    CoreOnboardingManager,
    CoreRecoveryManager,
    CoreResultsManager,
    CoreServiceCoordinator,
)
from src.core.managers.contracts import ManagerContext, ManagerResult


def mock_logger(msg):
    """Mock logger function for testing."""
    pass


class TestCoreOnboardingManager:
    """Test CoreOnboardingManager functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.manager = CoreOnboardingManager()
        self.context = ManagerContext(
            config={"test": True},
            logger=mock_logger,
            metrics={"timestamp": 1234567890},
            timestamp=datetime.now(),
        )

    def test_initialize(self):
        """Test manager initialization."""
        assert self.manager.initialize(self.context) is True
        assert len(self.manager.get_status()["templates"]) > 0

    def test_onboard_agent(self):
        """Test agent onboarding."""
        self.manager.initialize(self.context)

        result = self.manager.execute(
            self.context,
            "onboard_agent",
            {
                "agent_id": "test_agent",
                "agent_name": "Test Agent",
                "role": "developer",
                "template": "default",
            },
        )
        assert result.success is True
        assert "session_id" in result.data
        assert result.data["agent_id"] == "test_agent"

    def test_onboarding_workflow(self):
        """Test complete onboarding workflow."""
        self.manager.initialize(self.context)

        # Start onboarding
        onboard_result = self.manager.execute(
            self.context,
            "onboard_agent",
            {
                "agent_id": "test_agent",
                "agent_name": "Test Agent",
                "role": "developer",
            },
        )
        assert onboard_result.success is True
        session_id = onboard_result.data["session_id"]

        # Start onboarding process
        start_result = self.manager.execute(
            self.context,
            "start_onboarding",
            {"session_id": session_id},
        )
        assert start_result.success is True

        # Complete onboarding
        complete_result = self.manager.execute(
            self.context,
            "complete_onboarding",
            {
                "session_id": session_id,
                "success": True,
                "notes": "Test completion",
            },
        )
        assert complete_result.success is True

    def test_cleanup(self):
        """Test manager cleanup."""
        self.manager.initialize(self.context)
        assert self.manager.cleanup(self.context) is True


class TestCoreRecoveryManager:
    """Test CoreRecoveryManager functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.manager = CoreRecoveryManager()
        self.context = ManagerContext(
            config={"test": True},
            logger=mock_logger,
            metrics={"timestamp": 1234567890},
            timestamp=datetime.now(),
        )

    def test_initialize(self):
        """Test manager initialization."""
        assert self.manager.initialize(self.context) is True
        assert len(self.manager.get_status()["strategies"]) > 0

    def test_recover_from_error(self):
        """Test error recovery."""
        self.manager.initialize(self.context)

        result = self.manager.execute(
            self.context,
            "recover_from_error",
            {
                "error_type": "network",
                "error_message": "Connection timeout",
                "context": {"severity": "low"},
            },
        )
        assert result.success is True
        assert "recovery_id" in result.data

    def test_register_recovery_strategy(self):
        """Test recovery strategy registration."""
        self.manager.initialize(self.context)

        result = self.manager.execute(
            self.context,
            "register_recovery_strategy",
            {
                "strategy_name": "test_strategy",
                "strategy_type": "retry",
                "conditions": {"error_types": ["test"]},
                "actions": ["retry", "wait"],
            },
        )
        assert result.success is True
        assert result.data["registered"] is True

    def test_cleanup(self):
        """Test manager cleanup."""
        self.manager.initialize(self.context)
        assert self.manager.cleanup(self.context) is True


class TestCoreResultsManager:
    """Test CoreResultsManager functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.manager = CoreResultsManager()
        self.context = ManagerContext(
            config={"test": True},
            logger=mock_logger,
            metrics={"timestamp": 1234567890},
            timestamp=datetime.now(),
        )

    def test_initialize(self):
        """Test manager initialization."""
        assert self.manager.initialize(self.context) is True
        status = self.manager.get_status()
        assert status["active_results"] == 0
        assert status["v2_compliant"] is True

    def test_process_results(self):
        """Test results processing."""
        self.manager.initialize(self.context)

        result = self.manager.execute(
            self.context,
            "process_results",
            {
                "result_data": {"rules": [], "data": {}},
                "result_type": "validation",
                "validation_rules": [],
            },
        )
        assert result.success is True
        assert "result_id" in result.data
        assert result.data["result_id"] is not None

    def test_get_results(self):
        """Test results retrieval."""
        self.manager.initialize(self.context)

        # Process a result first
        process_result = self.manager.execute(
            self.context,
            "process_results",
            {
                "result_data": {"rules": [], "data": {}},
                "result_type": "validation",
                "validation_rules": [],
            },
        )
        assert process_result.success is True
        result_id = process_result.data["result_id"]

        # Get results
        result = self.manager.execute(
            self.context,
            "get_results",
            {"result_id": result_id},
        )
        assert result.success is True
        assert len(result.data["results"]) == 1

    def test_cleanup(self):
        """Test manager cleanup."""
        self.manager.initialize(self.context)
        assert self.manager.cleanup(self.context) is True


class TestCoreServiceCoordinator:
    """Test CoreServiceCoordinator functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.manager = CoreServiceCoordinator()
        self.context = ManagerContext(
            config={"test": True},
            logger=mock_logger,
            metrics={"timestamp": 1234567890},
            timestamp=datetime.now(),
        )

    def test_initialize(self):
        """Test coordinator initialization."""
        assert self.manager.initialize(self.context) is True
        status = self.manager.get_status()
        assert status["initialized"] is True
        assert "onboarding_status" in status
        assert "recovery_status" in status
        assert "results_status" in status

    def test_onboard_agent(self):
        """Test agent onboarding through coordinator."""
        self.manager.initialize(self.context)

        result = self.manager.execute(
            self.context,
            "onboard_agent",
            {
                "agent_id": "test_agent",
                "agent_name": "Test Agent",
                "role": "developer",
            },
        )
        assert result.success is True
        assert "session_id" in result.data

    def test_recover_from_error(self):
        """Test error recovery through coordinator."""
        self.manager.initialize(self.context)

        result = self.manager.execute(
            self.context,
            "recover_from_error",
            {
                "error_type": "network",
                "error_message": "Connection timeout",
                "context": {"severity": "low"},
            },
        )
        assert result.success is True
        assert "recovery_id" in result.data

    def test_process_results(self):
        """Test results processing through coordinator."""
        self.manager.initialize(self.context)

        result = self.manager.execute(
            self.context,
            "process_results",
            {
                "result_data": {"rules": [], "data": {}},
                "result_type": "validation",
                "validation_rules": [],
            },
        )
        assert result.success is True
        assert "result_id" in result.data
        assert result.data["result_id"] is not None

    def test_cleanup(self):
        """Test coordinator cleanup."""
        self.manager.initialize(self.context)
        assert self.manager.cleanup(self.context) is True


class TestV2ComplianceRefactoring:
    """Test V2 compliance refactoring goals."""

    def test_file_size_compliance(self):
        """Test that specialized managers meet V2 compliance."""
        import os

        manager_files = [
            "src/core/managers/core_onboarding_manager.py",
            "src/core/managers/core_recovery_manager.py",
            "src/core/managers/core_results_manager.py",
            "src/core/managers/core_service_coordinator.py",
        ]

        for file_path in manager_files:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = len(f.readlines())
                # V2 compliance: ≤400 lines guideline
                assert lines <= 400, f"{file_path} exceeds V2 compliance (400 lines): {lines}"

    def test_specialized_managers_functionality(self):
        """Test that specialized managers provide focused functionality."""
        # Test onboarding manager focuses on onboarding
        onboarding_manager = CoreOnboardingManager()
        context = ManagerContext(
            config={"test": True},
            logger=mock_logger,
            metrics={"timestamp": 1234567890},
            timestamp=datetime.now(),
        )
        onboarding_manager.initialize(context)

        # Should handle onboarding operations
        assert hasattr(onboarding_manager, "onboard_agent")
        assert hasattr(onboarding_manager, "start_onboarding")
        assert hasattr(onboarding_manager, "complete_onboarding")

        # Test recovery manager focuses on recovery
        recovery_manager = CoreRecoveryManager()
        recovery_manager.initialize(context)

        # Should handle recovery operations
        assert hasattr(recovery_manager, "recover_from_error")
        assert hasattr(recovery_manager, "register_recovery_strategy")

        # Test results manager focuses on results
        results_manager = CoreResultsManager()
        results_manager.initialize(context)

        # Should handle results operations
        assert hasattr(results_manager, "process_results")
        assert hasattr(results_manager, "get_results")

    def test_coordinator_integration(self):
        """Test that coordinator properly integrates specialized managers."""
        coordinator = CoreServiceCoordinator()
        context = ManagerContext(
            config={"test": True},
            logger=mock_logger,
            metrics={"timestamp": 1234567890},
            timestamp=datetime.now(),
        )

        assert coordinator.initialize(context) is True

        # Test that coordinator routes operations correctly
        result = coordinator.execute(
            context,
            "onboard_agent",
            {
                "agent_id": "test_agent",
                "agent_name": "Test Agent",
            },
        )
        assert result.success is True

        # Register a recovery strategy first
        recovery_result = coordinator.execute(
            context,
            "register_recovery_strategy",
            {
                "strategy_name": "test_retry",
                "strategy_type": "retry",
                "conditions": {"error_type": "test"},
                "actions": ["retry", "log"],
                "enabled": True,
            },
        )
        assert recovery_result.success is True

        result = coordinator.execute(
            context,
            "recover_from_error",
            {
                "error_type": "test",
                "error_message": "Test error",
            },
        )
        assert result.success is True

        result = coordinator.execute(
            context,
            "process_results",
            {
                "result_id": "test_result",
                "result_type": "general",
                "data": {},
            },
        )
        assert result.success is True
