from __future__ import annotations
from typing import List
import logging
logger = logging.getLogger(__name__)

def hard_onboarding(agents: List[str], mode: str, assign_roles: str, dry_run: bool, use_ui: bool, ui_retries: int, ui_tolerance: int) -> int:
    """Delegates to OnboardingHandler (kept separate under services/handlers)."""
    try:
        from src.services.handlers.onboarding_handler import OnboardingHandler
        h = OnboardingHandler()
        return h._handle_hard_onboarding(
            confirm_yes=True,
            dry_run=dry_run,
            agents=agents,
            timeout=30,
            use_ui=use_ui,
            ui_retries=ui_retries,
            ui_tolerance=ui_tolerance,
            mode=mode,
            role_map_str=assign_roles or "",
            emit_proof=False,
            audit_cleanup=False,
        )
    except Exception as e:
        logger.error(f"[onboarding] failed: {e}")
        return 1
