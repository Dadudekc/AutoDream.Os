from pathlib import Path
import sys

# Expose cleanup validator modules from Agent-7 workspace
agent_path = Path(__file__).resolve().parents[3] / "agent_workspaces" / "Agent-7"
if str(agent_path) not in sys.path:
    sys.path.append(str(agent_path))

from contract_cleanup_validator import (
    CleanupStatus,
    StandardCompliance,
    CleanupRequirement,
    StandardRequirement,
    CleanupValidation,
    ContractCleanupValidator,
    CleanupCLI,
    main,
)

__all__ = [
    "CleanupStatus",
    "StandardCompliance",
    "CleanupRequirement",
    "StandardRequirement",
    "CleanupValidation",
    "ContractCleanupValidator",
    "CleanupCLI",
    "main",
]
