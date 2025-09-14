"""Coordinator that composes specialized service managers."""

from __future__ import annotations

from typing import Any

from .contracts import Manager, ManagerContext, ManagerResult
from .core_onboarding_manager import CoreOnboardingManager
from .core_recovery_manager import CoreRecoveryManager
from .core_results_manager import CoreResultsManager


class CoreServiceCoordinator(Manager):
    """Routes service operations to specialized managers."""

    def __init__(self) -> None:
        self.onboarding = CoreOnboardingManager()
        self.recovery = CoreRecoveryManager()
        self.results = CoreResultsManager()
        self.initialized = False

    def initialize(self, context: ManagerContext) -> bool:
        self.onboarding.initialize(context)
        self.recovery.initialize(context)
        self.results.initialize(context)
        self.initialized = True
        return True

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        onboarding_ops = {
            "onboard_agent",
            "start_onboarding",
            "complete_onboarding",
            "get_onboarding_status",
        }
        recovery_ops = {
            "register_recovery_strategy",
            "recover_from_error",
            "get_recovery_strategies",
        }
        results_ops = {"process_results", "get_results"}

        if operation in onboarding_ops:
            return self.onboarding.execute(context, operation, payload.get("agent_data", payload))
        if operation in recovery_ops:
            return self.recovery.execute(context, operation, payload.get("error_data", payload))
        if operation in results_ops:
            return self.results.execute(context, operation, payload.get("results_data", payload))
        return ManagerResult(False, {}, {}, f"Unknown operation: {operation}")

    def cleanup(self, context: ManagerContext) -> bool:
        self.onboarding.cleanup(context)
        self.recovery.cleanup(context)
        self.results.cleanup(context)
        return True

    def get_status(self) -> dict[str, Any]:
        status = {
            "onboarding_status": self.onboarding.get_status(),
            "recovery_status": self.recovery.get_status(),
            "results_status": self.results.get_status(),
            "total_onboarding_sessions": self.onboarding.get_status()["total_sessions"],
            "initialized": self.initialized,
        }
        return status
