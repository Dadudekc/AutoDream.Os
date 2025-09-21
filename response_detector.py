#!/usr/bin/env python3

"""
Robust response detection for ChatGPT UI (Thea)
- Quorum-based signals (streaming/stop, regenerate, stability window)
- Optional auto-continue for truncated generations
- Safe JS probes (no :has selectors)
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ResponseWaitResult(Enum):
    COMPLETE = "complete"
    CONTINUE_REQUIRED = "continue_required"
    TIMEOUT = "timeout"
    NO_TURN = "no_turn"


@dataclass
class TurnInfo:
    turn_id: str | None
    text_length: int
    has_code: bool
    streaming: bool
    regenerate: bool
    continue_btn: bool


class ResponseDetector:
    def __init__(self, driver):
        self.driver = driver
        self._last_turn_id: str | None = None

    # ---------------------------
    # Public API
    # ---------------------------
    def wait_until_complete(
        self,
        timeout: int = 120,
        stable_secs: float = 3.0,
        poll: float = 0.5,
        auto_continue: bool = True,
        max_continue_clicks: int = 1,
    ) -> ResponseWaitResult:
        """
        Wait until last assistant response is complete.
        Heuristics (need 2-of-3 to finish):
          1) Not streaming (no Stop button)
          2) Regenerate button visible
          3) Text length stable for `stable_secs`
        If 'Continue generating' appears, optionally click it once and keep waiting.
        """
        start = time.time()
        stable_start = None
        prev_len = None
        continue_clicks = 0

        # Wait until an assistant turn appears or text starts flowing
# SECURITY: Token placeholder - replace with environment variable

        while time.time() - start < timeout:
            info = self._probe()

            if info is None:
                time.sleep(poll)
                continue

            # Text stability tracking
            if prev_len is None or info.text_length != prev_len:
                prev_len = info.text_length
                stable_start = time.time()
            is_stable = (time.time() - (stable_start or time.time())) >= stable_secs

            # CONTINUE handling (truncate guard)
            if info.continue_btn and not info.streaming:
                if auto_continue and continue_clicks < max_continue_clicks:
                    if self._click_continue():
                        continue_clicks += 1
                        # reset stability window after continuing
                        prev_len = None
                        stable_start = None
                        time.sleep(1.0)
                        continue
                else:
                    return ResponseWaitResult.CONTINUE_REQUIRED

            # Quorum: require 2 of 3
            signals_met = sum(
                [
                    (not info.streaming),
                    info.regenerate,
                    is_stable and info.text_length > 0,
                ]
            )

            if signals_met >= 2:
                return ResponseWaitResult.COMPLETE

            time.sleep(poll)

        return ResponseWaitResult.TIMEOUT

    def extract_response_text(self, min_len: int = 20) -> str:
        """
        Return the visible innerText of the last assistant block.
        """
        js = """
        const toLower = s => (s || '').toLowerCase();
        const visible = el => {
          if (!el) return false;
          const r = el.getBoundingClientRect();
          const st = window.getComputedStyle(el);
          return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none';
        };

        const blocks = Array.from(
          document.querySelectorAll('article, div.markdown, div.prose, div[data-message-author-role]')
        ).filter(visible);

        const last = blocks.length ? blocks[blocks.length - 1] : null;
        let text = '';
        if (last) {
          // Prefer innerText (respects CSS), fallback to textContent
          text = last.innerText && last.innerText.trim()
                 ? last.innerText.trim() : (last.textContent || '').trim();
        }
        return text;
        """
        try:
            text = self.driver.execute_script(js) or ""
        except Exception:
            text = ""
        if text and len(text) >= min_len:
            return text
        return ""

    # ---------------------------
    # Internals
    # ---------------------------
# SECURITY: Token placeholder - replace with environment variable
        start = time.time()
        while time.time() - start < timeout:
            info = self._probe()
            if info and (info.text_length > 0 or info.streaming):
                return
            time.sleep(poll)

    def _probe(self) -> TurnInfo | None:
        """
        Lightweight JS probe of page state.
        Avoids brittle selectors; looks for general UI affordances.
        """
        js = """
        const toLower = s => (s || '').toLowerCase();
        const visible = el => {
          if (!el) return false;
          const r = el.getBoundingClientRect();
          const st = window.getComputedStyle(el);
          return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none';
        };

        // Buttons: scan once
        const buttons = Array.from(document.querySelectorAll('button')).filter(visible);
        const hasBtn = (fragList) => buttons.some(b => {
          const t = toLower(b.innerText || '');
          const a = toLower(b.getAttribute('aria-label') || '');
          return fragList.some(f => t.includes(f) || a.includes(f));
        });

        // Heuristics
        const streaming   = hasBtn(['stop generating','stop']);          // strong when generating
        const regenerate  = hasBtn(['regenerate','retry']);              // strong when finished
        const continueBtn = hasBtn(['continue','continue generating']);  // indicates truncation

        // Find last visible assistant-ish content block
        const blocks = Array.from(
          document.querySelectorAll('article, div.markdown, div.prose, div[data-message-author-role]')
        ).filter(visible);

        const last = blocks.length ? blocks[blocks.length - 1] : null;
        let textLen = 0;
        let hasCode = false;
        let turnId = null;

        if (last) {
          const txt = (last.innerText && last.innerText.trim()) || (last.textContent || '').trim();
          textLen = (txt || '').length;
          hasCode = !!last.querySelector('pre, code');
          const turn = last.closest('[data-testid^="conversation-turn-"]');
          if (turn) {
            turnId = turn.getAttribute('data-testid') || null;
          }
        }

        return { streaming, regenerate, continueBtn, textLen, hasCode, turnId };
        """

        try:
            res: dict[str, Any] = self.driver.execute_script(js) or {}
        except Exception:
            return None

        if not res:
            return None

        info = TurnInfo(
            turn_id=res.get("turnId"),
            text_length=int(res.get("textLen", 0) or 0),
            has_code=bool(res.get("hasCode", False)),
            streaming=bool(res.get("streaming", False)),
            regenerate=bool(res.get("regenerate", False)),
            continue_btn=bool(res.get("continueBtn", False)),
        )

        # Track last turn id in case callers want to use it later
        if info.turn_id:
            self._last_turn_id = info.turn_id

        return info

    def _click_continue(self) -> bool:
        js_click = """
        const toLower = s => (s || '').toLowerCase();
        const visible = el => {
          if (!el) return false;
          const r = el.getBoundingClientRect();
          const st = window.getComputedStyle(el);
          return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none';
        };
        const btns = Array.from(document.querySelectorAll('button')).filter(visible);
        const target = btns.find(b => {
          const t = toLower(b.innerText || '');
          const a = toLower(b.getAttribute('aria-label') || '');
          return t.includes('continue') || a.includes('continue');
        });
        if (target) { target.click(); return true; }
        return false;
        """
        try:
            return bool(self.driver.execute_script(js_click))
        except Exception:
            return False
