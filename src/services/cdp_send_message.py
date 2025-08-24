#!/usr/bin/env python3
"""
Headless CDP Messenger for Cursor Agent Chats
============================================

Send messages into Cursor agent chats WITHOUT moving the mouse by injecting text
and "press Enter" via the Chrome DevTools Protocol (CDP). Works in the background;
no pointer motion, no PyAutoGUI.

Usage:
    python cdp_send_message.py "Your message here" [--all]
    python cdp_send_message.py "Agent-3: begin integration tests" [--target Agent-3]
"""

import sys
import os
import json
import time
import urllib.request

from src.utils.stability_improvements import stability_manager, safe_import
from urllib.error import URLError
import argparse
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    import websocket

    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print(
        "⚠️  websocket-client not available. Install with: pip install websocket-client"
    )

# Configuration
CDP_PORT = int(os.environ.get("CURSOR_CDP_PORT", "9222"))
LIST_URL = f"http://127.0.0.1:{CDP_PORT}/json"

# JavaScript template for injecting messages
JS_TEMPLATE = r"""
(() => {
  const msg = %s;
  const targetAgent = %s;

  // Enhanced selectors for Cursor/Electron chat input
  const candidates = [
    'textarea[placeholder*="Ask"]',
    'textarea[placeholder*="Message"]',
    'textarea[placeholder*="Type"]',
    'textarea[placeholder*="Chat"]',
    'textarea',
    '[contenteditable="true"]',
    '[role="textbox"]',
    '.chat-input',
    '.message-input',
    '.input-area'
  ];

  function findInput() {
    // First try: direct selectors
    for (const sel of candidates) {
      const el = document.querySelector(sel);
      if (el) return el;
    }

    // Second try: shadow DOM traversal
    const walker = document.createTreeWalker(
      document,
      NodeFilter.SHOW_ELEMENT,
      null
    );

    let node;
    while (node = walker.nextNode()) {
      if (node.shadowRoot) {
        for (const sel of candidates) {
          const el = node.shadowRoot.querySelector(sel);
          if (el) return el;
        }
      }
    }

    // Third try: look for any textarea or contenteditable
    const anyInput = document.querySelector('textarea, [contenteditable="true"]');
    if (anyInput) return anyInput;

    return null;
  }

  function findAgentChat(targetAgent) {
    // Look for agent-specific chat areas
    const agentSelectors = [
      `[data-agent="${targetAgent}"]`,
      `[data-agent-id="${targetAgent}"]`,
      `[data-agent-name="${targetAgent}"]`,
      `[title*="${targetAgent}"]`,
      `[aria-label*="${targetAgent}"]`
    ];

    for (const sel of agentSelectors) {
      const el = document.querySelector(sel);
      if (el) return el;
    }

    // Look for text containing agent name
    const walker = document.createTreeWalker(
      document,
      NodeFilter.SHOW_TEXT,
      null
    );

    let textNode;
    while (textNode = walker.nextNode()) {
      if (textNode.textContent.includes(targetAgent)) {
        // Find the closest input element
        let parent = textNode.parentElement;
        while (parent && parent !== document.body) {
          const input = parent.querySelector('textarea, [contenteditable="true"]');
          if (input) return input;
          parent = parent.parentElement;
        }
      }
    }

    return null;
  }

  // Try to find agent-specific chat first
  let el = findAgentChat(targetAgent);
  if (!el) {
    // Fallback to general input
    el = findInput();
  }

  if (!el) {
    return {
      ok: false,
      reason: "input_not_found",
      message: `Could not find input for ${targetAgent}`,
      candidates: candidates
    };
  }

  // Clear existing content
  if ('value' in el) {
    el.value = "";
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.value = msg;
    el.dispatchEvent(new Event('input', {bubbles: true}));
  } else if (el.isContentEditable) {
    el.textContent = "";
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.textContent = msg;
    el.dispatchEvent(new Event('input', {bubbles: true}));
  } else {
    return { ok: false, reason: "unsupported_input_type" };
  }

  // Try clicking a 'send' button first
  const sendButtons = [
    ...document.querySelectorAll('button'),
    ...document.querySelectorAll('[role="button"]'),
    ...document.querySelectorAll('.btn'),
    ...document.querySelectorAll('.send-button')
  ];

  const sendBtn = sendButtons.find(b => {
    const text = (b.textContent || '').toLowerCase();
    const ariaLabel = (b.getAttribute('aria-label') || '').toLowerCase();
    const className = (b.className || '').toLowerCase();

    return /send|submit|enter|go/i.test(text) ||
           /send|submit|enter|go/i.test(ariaLabel) ||
           /send|submit/i.test(className);
  });

  if (sendBtn) {
    sendBtn.click();
    return {
      ok: true,
      method: "button_click",
      target: targetAgent,
      message: msg.substring(0, 50) + "..."
    };
  }

  // Fallback: synthetic Enter key
  const evDown = new KeyboardEvent('keydown', {
    key: 'Enter',
    code: 'Enter',
    keyCode: 13,
    which: 13,
    bubbles: true,
    cancelable: true
  });

  const evUp = new KeyboardEvent('keyup', {
    key: 'Enter',
    code: 'Enter',
    keyCode: 13,
    which: 13,
    bubbles: true,
    cancelable: true
  });

  el.dispatchEvent(evDown);
  el.dispatchEvent(evUp);

  return {
    ok: true,
    method: "enter_key",
    target: targetAgent,
    message: msg.substring(0, 50) + "..."
  };
})()
"""


def http_json(url, timeout=5.0):
    """Make HTTP request and return JSON response"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        raise URLError(f"HTTP request failed: {e}")


def choose_targets(port=None, kind="page"):
    """Choose CDP targets, filtering for Cursor/Electron pages"""
    if port is None:
        port = CDP_PORT

    list_url = f"http://127.0.0.1:{port}/json"

    try:
        lst = http_json(list_url)
    except URLError as e:
        print(f"❌ CDP connection failed: {e}")
        print(f"💡 Make sure Cursor is running with: --remote-debugging-port={port}")
        return []

    # Filter out devtools and pick Cursor/Electron pages
    out = []
    for t in lst:
        if t.get("type") != kind:
            continue

        url = (t.get("url") or "").lower()
        title = (t.get("title") or "").lower()

        if url.startswith("devtools"):
            continue

        # Heuristics: likely chat panes or Cursor webviews
        if any(
            keyword in title or keyword in url
            for keyword in ["cursor", "chat", "agent", "ai"]
        ):
            out.append(t)

    # Fallback: if none matched, try all pages
    if not out:
        out = [
            t
            for t in lst
            if t.get("type") == kind and not (t.get("url") or "").startswith("devtools")
        ]

    return out


def send_to_target(ws_url, message, target_agent="General"):
    """Send message to a specific CDP target via WebSocket"""
    if not WEBSOCKET_AVAILABLE:
        return {"ok": False, "reason": "websocket_not_available"}

    try:
        ws = websocket.create_connection(ws_url, timeout=10)
        seq = 0

        def send(method, params=None):
            nonlocal seq
            seq += 1
            ws.send(json.dumps({"id": seq, "method": method, "params": params or {}}))

            while True:
                resp = json.loads(ws.recv())
                if resp.get("id") == seq:
                    return resp

        # Enable runtime and evaluate the script
        send("Runtime.enable")

        # Prepare JavaScript with message and target agent
        js = JS_TEMPLATE % (json.dumps(message), json.dumps(target_agent))

        res = send(
            "Runtime.evaluate",
            {"expression": js, "awaitPromise": False, "returnByValue": True},
        )

        ws.close()

        out = res.get("result", {}).get("result", {}).get("value")
        return out or {"ok": False, "reason": "no_result"}

    except Exception as e:
        return {"ok": False, "reason": f"websocket_error: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(
        description="Send messages to Cursor agent chats via CDP (no mouse movement)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cdp_send_message.py "Agent-3: begin integration tests for services_v2/auth. Report in 60m."
  python cdp_send_message.py "Agent-3: begin integration tests" --target "Agent-3"
  python cdp_send_message.py "ALL AGENTS: no acknowledgments—only diffs, commits, and checkmarks." --all
  python cdp_send_message.py "URGENT: System alert!" --target "Agent-5" --priority high
        """,
    )

    parser.add_argument("message", help="Message to send")
    parser.add_argument(
        "--target", default="General", help="Target agent (default: General)"
    )
    parser.add_argument("--all", action="store_true", help="Broadcast to all targets")
    parser.add_argument(
        "--priority",
        choices=["low", "normal", "high", "urgent", "critical"],
        default="normal",
        help="Message priority",
    )
    parser.add_argument(
        "--port", type=int, default=CDP_PORT, help=f"CDP port (default: {CDP_PORT})"
    )

    args = parser.parse_args()

    # Use local variables for port and list URL
    cdp_port = args.port
    list_url = f"http://127.0.0.1:{cdp_port}/json"

    print(f"🚀 CDP Messenger - Port {cdp_port}")
    print(f"📨 Message: {args.message}")
    print(f"🎯 Target: {args.target}")
    print(f"⚡ Priority: {args.priority.upper()}")
    print("=" * 60)

    # Check if websocket is available
    if not WEBSOCKET_AVAILABLE:
        print("❌ websocket-client not available")
        print("💡 Install with: pip install websocket-client")
        sys.exit(1)

    # Get targets
    try:
        targets = choose_targets(cdp_port)
        if not targets:
            print("❌ No suitable CDP targets found")
            print(
                f"💡 Make sure Cursor is running with: --remote-debugging-port={cdp_port}"
            )
            sys.exit(2)

        print(f"✅ Found {len(targets)} CDP target(s)")

    except Exception as e:
        print(f"❌ Error getting targets: {e}")
        sys.exit(2)

    # Send messages
    sent = 0
    for i, t in enumerate(targets):
        try:
            print(
                f"\n📤 Sending to target {i+1}/{len(targets)}: {t.get('title', 'Unknown')}"
            )

            result = send_to_target(
                t["webSocketDebuggerUrl"], args.message, args.target
            )

            if result.get("ok"):
                print(
                    f"✅ Success: {result.get('method', 'unknown')} - {result.get('message', '')}"
                )
                sent += 1
            else:
                print(f"❌ Failed: {result.get('reason', 'unknown error')}")
                if result.get("message"):
                    print(f"   Details: {result['message']}")

            # If not broadcasting, stop after first target
            if not args.all:
                break

        except Exception as e:
            print(f"❌ Error with target {i+1}: {e}")
            continue

    # Summary
    print("\n" + "=" * 60)
    if sent > 0:
        print(f"🎉 Successfully sent message to {sent} target(s)")
        print(f"💡 Message: {args.message}")
        if args.target != "General":
            print(f"🎯 Target Agent: {args.target}")
    else:
        print("❌ Failed to send message to any target")
        sys.exit(3)


if __name__ == "__main__":
    main()
