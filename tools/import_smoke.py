#!/usr/bin/env python3
"""
Quick import smoke to ensure new module names are importable.
Exit non-zero if any canonical import fails.
"""
import importlib, sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

MODULES = [
  "src.core.coordinate_loader_models",
  "src.core.coordinate_loader_core",
  "src.core.coordinate_loader_unified",
  "src.services.system_efficiency.status_tracking_system",
  "src.core.ml_pipeline_models",
  "src.core.ml_pipeline",
  "src.core.ml_pipeline_config",
  "src.core.ml_pipeline_core",
  "tools.database_search",
  "src.architecture.architecture_core",
  "src.core.config.config_manager",
  "src.services.messaging_service_utils",
  "src.services.messaging_cli",
  "src.services.messaging_service_main",
  "src.services.messaging_service",
  "src.services.messaging_service_core",
  "src.services.messaging_core",
  "src.core.coordination_workflow_core",
  "src.core.coordination_workflow_operations",
  "src.core.coordination_workflow_cli"
]

def main() -> int:
    failed = []
    for m in MODULES:
        try:
            importlib.import_module(m)
        except Exception as e:
            failed.append((m, str(e)))
    if failed:
        print("❌ import failures:")
        for m, e in failed:
            print(f" - {m}: {e}")
        return 2
    print("✅ import smoke passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
