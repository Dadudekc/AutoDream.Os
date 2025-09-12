"""
Ingest_Statuses Module

This module provides script functionality for the swarm system.

Component Type: Script
Priority: Medium
Dependencies: src.core.semantic


EXAMPLE USAGE:
==============

# Run the script directly
python ingest_statuses.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.semantic.ingest_statuses import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.semantic.ingest_statuses import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.semantic.status_index import StatusIndex


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=False, help="Directory containing status JSON files")
    args = ap.parse_args()

    cfg_p = Path("config/semantic_config.yaml")
    cfg = yaml.safe_load(cfg_p.read_text()) if cfg_p.exists() else {}
    idx = StatusIndex(cfg)
    seed_dir = args.dir or (cfg.get("status_index") or {}).get("seed_dir")
    if not seed_dir:
        print("No directory provided and no status_index.seed_dir in config.")
        return
    n = idx.ingest_dir(seed_dir)
    print(f"Ingested {n} status files into StatusIndex.")


if __name__ == "__main__":
    main()
