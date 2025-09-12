"""
Agent Status Similarity Index
- Ingests agent status JSON blobs
- Supports nearest-neighbor queries to find similar states
- Surfaces top agents + similarity for coordination
"""
from __future__ import annotations
from typing import Dict, List, Tuple
import os
import json
from .embeddings import build_provider
from .vector_store import VectorStore
from .utils import json_to_text


class StatusIndex:
    def __init__(self, cfg: Dict):
        self.cfg = cfg
        self.provider = build_provider(cfg)
        sp = cfg.get("status_index", {})
        self.keep_fields = sp.get("fields_keep", [])
        self.store = VectorStore(
            sp.get("store_path", "runtime/semantic/vector_store/status"),
            backend=cfg.get("store", {}).get("backend", "auto"),
            normalize=cfg.get("store", {}).get("normalize", True),
        )

    def ingest_dir(self, dir_path: str) -> int:
        """Load all *.json files and add to the index (id=filename)."""
        if not os.path.isdir(dir_path):
            return 0
        ids, metas, texts = [], [], []
        for name in os.listdir(dir_path):
            if not name.endswith(".json"):
                continue
            fpath = os.path.join(dir_path, name)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                text = json_to_text(data, keep=self.keep_fields)
                ids.append(os.path.splitext(name)[0])
                metas.append({
                    "type": "status",
                    "agent_id": data.get("agent_id"),
                    "status": data.get("status"),
                    "source_file": fpath
                })
                texts.append(text)
            except Exception:
                continue
        if not ids:
            return 0
        vecs = self.provider.embed_texts(texts)
        self.store.add(ids, vecs, metas)
        return len(ids)

    def upsert_status(self, status_id: str, data: Dict):
        text = json_to_text(data, keep=self.keep_fields)
        vec = self.provider.embed_texts([text])
        self.store.add([status_id], vec, [{
            "type": "status",
            "agent_id": data.get("agent_id"),
            "status": data.get("status")
        }])

    def similar(self, status_like: Dict | str, top_k: int | None = None, min_conf: float | None = None
                ) -> List[Tuple[str, float, Dict]]:
        sp = self.cfg.get("status_index", {})
        k = int(top_k or sp.get("top_k", 3))
        th = float(min_conf or sp.get("min_confidence", 0.50))
        if isinstance(status_like, str):
            qtext = status_like.strip()
        else:
            qtext = json_to_text(status_like, keep=self.keep_fields)
        qvec = self.provider.embed_texts([qtext])
        hits = self.store.search(qvec, top_k=k)[0]
        return [(i, s, m) for (i, s, m) in hits if s >= th]
