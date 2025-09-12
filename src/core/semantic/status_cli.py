"""
CLI demo:
  python -m src.core.semantic.status_cli "survey completed, 50 files analyzed"
  python -m src.core.semantic.status_cli @data/semantic_seed/status/Agent-1.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

# Add project root to Python path when running as module
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from .status_index import StatusIndex


def load_cfg():
    p = Path("config/semantic_config.yaml")
    return yaml.safe_load(p.read_text()) if p.exists() else {}


def main():
    if len(sys.argv) < 2:
        print("usage: status_cli.py <query_text | @path.json>")
        sys.exit(1)
    raw = " ".join(sys.argv[1:])
    if raw.startswith("@"):
        with open(raw[1:], encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = raw

    cfg = load_cfg()
    idx = StatusIndex(cfg)

    # one-time seed ingest
    seed_dir = (cfg.get("status_index") or {}).get("seed_dir")
    if seed_dir:
        idx.ingest_dir(seed_dir)

    hits = idx.similar(data)
    out = {
        "query_kind": "json" if isinstance(data, dict) else "text",
        "results": [{"id": i, "score": s, "meta": m} for (i, s, m) in hits],
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
