#!/usr/bin/env python3
"""
Messaging Gateway - Discord ↔ PyAutoGUI Bridge (V2)
===================================================

Unified, testable bridge that routes Discord-originated messages into
PyAutoGUI-driven agent UIs via the UnifiedMessagingSystem (if present),
with safe fallbacks, config-driven coordinates, and summary helpers.

Author: Agent-4 (Captain - Discord Integration Coordinator)
License: MIT
"""

from __future__ import annotations

import asyncio
import importlib
import json
import logging
import os
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


# -------- Utilities ----------------------------------------------------------


def _import_symbol(spec: str, default_attr: str = "UnifiedMessagingSystem") -> Any:
    """
    Import "pkg.mod:Class" or "pkg.mod.Class" or bare module "pkg.mod" (then default_attr).
    Returns the attribute (class/callable). Raises ImportError on failure.
    """
    mod_name: str
    attr_name: str | None = None

    if ":" in spec:
        mod_name, attr_name = spec.split(":", 1)
    else:
        parts = spec.split(".")
        if len(parts) > 1 and parts[-1][:1].isupper():
            mod_name = ".".join(parts[:-1])
            attr_name = parts[-1]
        else:
            mod_name = spec
            attr_name = None

    module = importlib.import_module(mod_name)
    if attr_name:
        return getattr(module, attr_name)
    return getattr(module, default_attr)


def _first_ok(candidates: tuple[str, ...]) -> Any:
    last_err: Exception | None = None
    for spec in candidates:
        try:
            return _import_symbol(spec)
        except Exception as e:
            last_err = e
            continue
    raise ImportError(f"UnifiedMessagingSystem not found. Last error: {last_err}")


# -------- Data Models --------------------------------------------------------


@dataclass(frozen=True)
class DispatchResult:
    request_id: str
    agent: str
    backend: str
    status: str
    ts: float
    extra: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# -------- Gateway ------------------------------------------------------------


class MessagingGateway:
    """
    Routes messages to agents' UI via UnifiedMessagingSystem (PyAutoGUI channel).
    - Config-driven coordinates with normalization
    - Safe fallback core if UMS unavailable
    - Deterministic, structured DispatchResult responses
    """

    _CORE_SPECS: tuple[str, ...] = (
        # Most explicit (module + class)
        "src.core.unified_messaging:UnifiedMessagingSystem",
        "core.unified_messaging:UnifiedMessagingSystem",
        # Dotted class path variants
        "src.core.unified_messaging.UnifiedMessagingSystem",
        "core.unified_messaging.UnifiedMessagingSystem",
        # Bare module → default attr lookup
        "src.core.unified_messaging",
        "core.unified_messaging",
    )

    def __init__(
        self, coordinates_path: str = "config/coordinates.json", dry_run: bool | None = None
    ):
        # Resolve core
        try:
            UMS = _first_ok(self._CORE_SPECS)
            self.core = UMS()  # type: ignore[call-arg]
            self.backend_name = "unified_messaging"
            log.info("UnifiedMessagingSystem loaded for PyAutoGUI dispatch.")
        except Exception as e:
            log.warning("Falling back to BasicMessagingCore: %s", e)
            self.core = self._basic_core()
            self.backend_name = "basic_core"

        # Config
        self.coordinates_path = coordinates_path
        self.agent_coordinates = self._load_agent_coordinates()

        # Summary template
        self.summary_template = os.getenv(
            "SUMMARY_PROMPT_TEMPLATE",
            (
                "Captain request — send a concise status summary now:\n"
                "1) Current task & objective\n"
                "2) Actions completed since last report\n"
                "3) Blockers/risk\n"
                "4) Next 2 steps\n"
                "5) ETA to next milestone\n"
                "Reply in 5 bullet points, ≤80 chars each."
            ),
        )

        # Dry-run switch (never touch UI; for tests)
        if dry_run is None:
            dry_run_env = os.getenv("GATEWAY_DRY_RUN", "").lower()
            self.dry_run = dry_run_env in {"1", "true", "yes", "on"}
        else:
            self.dry_run = dry_run

    # ----- Core Fallback -----------------------------------------------------

    @staticmethod
    def _basic_core():
        class BasicMessagingCore:
            def send_message(
                self, message: str, target: dict[str, Any], **kwargs
            ) -> dict[str, Any]:
                print(f"📤 [BASIC] {target.get('window_title', '?')}: {message[:60]}...")
                return {"ok": True, "channel": kwargs.get("channel", "pyautogui")}

            def receive_message(self, source: dict[str, Any]):
                print(f"📥 [BASIC] receive from {source.get('window_title', '?')}")
                return {"ok": True, "messages": []}

            def broadcast_message(self, message: str, **kwargs) -> dict[str, Any]:
                print(f"📢 [BASIC] broadcast: {message[:60]}...")
                return {"ok": True}

        return BasicMessagingCore()

    # ----- Config & Normalization -------------------------------------------

    def _load_agent_coordinates(self) -> dict[str, dict[str, Any]]:
        try:
            p = Path(self.coordinates_path)
            data = json.loads(p.read_text(encoding="utf-8"))
            agents = data.get("agents") or data  # allow raw object {Agent-1: {...}}
            assert isinstance(agents, dict)
            return agents
        except Exception as e:
            log.warning("Coordinates load failed (%s). Using sane defaults.", e)
            return {
                f"Agent-{i}": {
                    "mention": f"@Agent-{i}",
                    "inbox_path": f"agent_workspaces/Agent-{i}/inbox",
                    "pyautogui_target": {
                        "window_title": f"Cursor - Agent {i}",
                        "focus_xy": [200 + (i in {2, 4}) * 760, 120 + (i in {3, 4}) * 440],
                        "input_xy": [420 + (i in {2, 4}) * 760, 980],
                    },
                }
                for i in range(1, 5)
            }

    def _normalize_target(self, agent_key: str) -> dict[str, Any]:
        info = self.agent_coordinates.get(agent_key, {})
        if not info:
            raise KeyError(f"Unknown agent '{agent_key}' in coordinates.")
        # New format: direct chat_input_coordinates / onboarding_input_coords
        if "chat_input_coordinates" in info:
            return {
                "window_title": info.get("window_title", f"Cursor - {agent_key}"),
                "focus_xy": info.get("onboarding_input_coords", [0, 0]),
                "input_xy": info.get("chat_input_coordinates", [0, 0]),
            }
        # Legacy format: nested pyautogui_target
        tgt = info.get("pyautogui_target") or {}
        if {"window_title", "focus_xy", "input_xy"} - set(tgt):
            raise KeyError(f"Agent '{agent_key}' target incomplete in coordinates.")
        return tgt

    # ----- Public API --------------------------------------------------------

    def list_available_agents(self):
        return list(self.agent_coordinates.keys())

    async def send(self, agent_key: str, message: str, meta: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Async wrapper for send_pyautogui. Returns dict format for Discord integration.
        """
        result = self.send_pyautogui(agent_key, message, meta)
        # Convert DispatchResult to dict format expected by Discord code
        return {
            "status": result.status,
            "agent": result.agent,
            "backend": result.backend,
            "request_id": result.request_id,
            "timestamp": result.ts,
            "extra": result.extra
        }

    def get_agent_status(self, agent_key: str) -> dict[str, Any]:
        tgt = self._normalize_target(agent_key)
        try:
            return self.core.receive_message(tgt)
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def request_agent_summary(
        self, agent_key: str, requested_by: str, context: str | None = None
    ) -> DispatchResult:
        prompt = self.summary_template
        if context:
            prompt += f"\nContext: {context}"
        return self.send_pyautogui(
            agent_key, prompt, meta={"requested_by": requested_by, "type": "summary_request"}
        )

    def send_pyautogui(
        self, agent_key: str, text: str, meta: dict[str, Any] | None = None
    ) -> DispatchResult:
        """
        Synchronous send. Returns structured DispatchResult.
        Resilient to core signature variations.
        """
        req_id = str(uuid.uuid4())
        ts = time.time()
        tgt = self._normalize_target(agent_key)
        payload_meta = {"channel": "pyautogui", "agent": agent_key, **(meta or {})}

        if self.dry_run:
            log.info("[DRY-RUN] %s -> %s", agent_key, tgt.get("window_title"))
            return DispatchResult(
                request_id=req_id,
                agent=agent_key,
                backend=f"{self.backend_name}:dry",
                status="skipped",
                ts=ts,
                extra={"meta": payload_meta},
            )

        # Attempt rich signature, fallback to simple
        try:
            result = self.core.send_message(
                message=text,
                target=tgt,
                channel="pyautogui",
                sender="DiscordOps",
                sender_type="DISCORD",
                metadata=payload_meta,
            )
            ok = bool(result.get("ok", True)) if isinstance(result, dict) else bool(result)
        except TypeError:
            result = self.core.send_message(text, tgt)  # type: ignore[misc]
            ok = bool(result)
        except Exception as e:
            return DispatchResult(
                req_id, agent_key, self.backend_name, "error", ts, {"error": str(e)}
            )

        status = "sent" if ok else "failed"
        return DispatchResult(
            req_id, agent_key, self.backend_name, status, ts, {"meta": payload_meta}
        )
