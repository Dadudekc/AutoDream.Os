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
