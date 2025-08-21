#!/usr/bin/env python3
"""
CDP Message Delivery System
===========================

Chrome DevTools Protocol integration for headless message delivery.
Enables sending messages to Cursor chat without mouse movement.
"""

import asyncio
import json
import time
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class CDPTarget:
    """CDP target information."""
    id: str
    title: str
    url: str
    type: str
    web_socket_debugger_url: str


class CDPMessageDelivery:
    """Chrome DevTools Protocol message delivery system."""
    
    def __init__(self, cdp_port: int = 9222):
        self.cdp_port = cdp_port
        self.list_url = f"http://127.0.0.1:{cdp_port}/json"
        self.active_connections: Dict[str, Any] = {}
        
        # JavaScript template for message injection
        self.js_template = self._get_js_template()
    
    def _get_js_template(self) -> str:
        """Get JavaScript template for message injection."""
        return r"""
(() => {
  const msg = %s;
  
  // Candidate selectors for Cursor/Electron chat input
  const candidates = [
    'textarea[placeholder*="Ask"]',
    'textarea[placeholder*="Message"]',
    'textarea[placeholder*="Type"]',
    'textarea',
    '[contenteditable="true"]',
    'input[type="text"]'
  ];
  
  function findInput() {
    // Try direct selectors first
    for (const sel of candidates) {
      const el = document.querySelector(sel);
      if (el) return el;
    }
    
    // Try shadow DOMs
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
    
    // Try by placeholder text
    const inputs = document.querySelectorAll('input, textarea, [contenteditable]');
    for (const input of inputs) {
      const placeholder = input.getAttribute('placeholder') || '';
      if (placeholder.toLowerCase().includes('ask') || 
          placeholder.toLowerCase().includes('message') ||
          placeholder.toLowerCase().includes('type')) {
        return input;
      }
    }
    
    return null;
  }
  
  const el = findInput();
  if (!el) {
    return { 
      ok: false, 
      reason: "input_not_found",
      candidates: candidates,
      available_inputs: Array.from(document.querySelectorAll('input, textarea, [contenteditable]'))
        .map(i => ({ tag: i.tagName, placeholder: i.getAttribute('placeholder'), id: i.id, class: i.className }))
    };
  }
  
  // Set value/text
  if ('value' in el) {
    el.value = msg;
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
  } else if (el.isContentEditable) {
    el.textContent = msg;
    el.dispatchEvent(new Event('input', {bubbles: true}));
  } else {
    return { ok: false, reason: "unsupported_input_type", element: el.tagName };
  }
  
  // Try clicking a 'send' button
  const sendButtonSelectors = [
    'button[aria-label*="send"]',
    'button[aria-label*="submit"]',
    'button[title*="send"]',
    'button[title*="submit"]',
    'button:contains("Send")',
    'button:contains("Submit")'
  ];
  
  let btn = null;
  for (const selector of sendButtonSelectors) {
    try {
      btn = document.querySelector(selector);
      if (btn) break;
    } catch (e) {
      // Invalid selector, continue
    }
  }
  
  // Fallback: look for buttons with send-like text
  if (!btn) {
    const buttons = document.querySelectorAll('button');
    btn = Array.from(buttons).find(b => {
      const text = (b.textContent || '').toLowerCase();
      const ariaLabel = (b.getAttribute('aria-label') || '').toLowerCase();
      return text.includes('send') || text.includes('submit') || 
             ariaLabel.includes('send') || ariaLabel.includes('submit');
    });
  }
  
  if (btn) {
    btn.click();
    return { ok: true, method: "button_click", button: btn.textContent };
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
  
  return { ok: true, method: "enter_key" };
})()
"""
    
    def get_targets(self, target_type: str = "page") -> List[CDPTarget]:
        """Get available CDP targets."""
        try:
            with urllib.request.urlopen(self.list_url, timeout=2.5) as response:
                targets_data = json.loads(response.read().decode("utf-8"))
            
            targets = []
            for target_data in targets_data:
                if target_data.get("type") == target_type:
                    # Filter out devtools and other non-relevant targets
                    url = (target_data.get("url") or "").lower()
                    title = (target_data.get("title") or "").lower()
                    
                    if url.startswith("devtools://"):
                        continue
                    
                    # Heuristics for Cursor/chat targets
                    is_cursor_target = (
                        "cursor" in title or 
                        "cursor" in url or 
                        "chat" in url or
                        "agent" in title.lower() or
                        "message" in title.lower()
                    )
                    
                    if is_cursor_target:
                        target = CDPTarget(
                            id=target_data["id"],
                            title=target_data["title"],
                            url=target_data["url"],
                            type=target_data["type"],
                            web_socket_debugger_url=target_data["webSocketDebuggerUrl"]
                        )
                        targets.append(target)
            
            # If no specific targets found, return all pages
            if not targets:
                for target_data in targets_data:
                    if target_data.get("type") == target_type and not target_data.get("url", "").startswith("devtools://"):
                        target = CDPTarget(
                            id=target_data["id"],
                            title=target_data["title"],
                            url=target_data["url"],
                            type=target_data["type"],
                            web_socket_debugger_url=target_data["webSocketDebuggerUrl"]
                        )
                        targets.append(target)
            
            return targets
            
        except urllib.error.URLError as e:
            logger.error(f"CDP not reachable on port {self.cdp_port}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting CDP targets: {e}")
            return []
    
    async def send_message_async(self, target: CDPTarget, message: str) -> Dict[str, Any]:
        """Send message to a CDP target asynchronously."""
        try:
            import websockets
            
            # Connect to WebSocket
            async with websockets.connect(target.web_socket_debugger_url) as websocket:
                # Enable Runtime domain
                await self._send_cdp_command(websocket, "Runtime.enable")
                
                # Evaluate JavaScript
                js_code = self.js_template % json.dumps(message)
                result = await self._send_cdp_command(
                    websocket, 
                    "Runtime.evaluate", 
                    {"expression": js_code, "awaitPromise": False, "returnByValue": True}
                )
                
                return result.get("result", {}).get("result", {}).get("value", {})
                
        except ImportError:
            logger.error("websockets library not available. Install with: pip install websockets")
            return {"ok": False, "reason": "websockets_not_available"}
        except Exception as e:
            logger.error(f"Error sending message via CDP: {e}")
            return {"ok": False, "reason": str(e)}
    
    def send_message_sync(self, target: CDPTarget, message: str) -> Dict[str, Any]:
        """Send message to a CDP target synchronously."""
        try:
            import websocket
            
            # Create WebSocket connection
            ws = websocket.create_connection(target.web_socket_debugger_url, timeout=10)
            
            # Enable Runtime domain
            self._send_cdp_command_sync(ws, "Runtime.enable")
            
            # Evaluate JavaScript
            js_code = self.js_template % json.dumps(message)
            result = self._send_cdp_command_sync(
                ws, 
                "Runtime.evaluate", 
                {"expression": js_code, "awaitPromise": False, "returnByValue": True}
            )
            
            ws.close()
            return result.get("result", {}).get("result", {}).get("value", {})
            
        except ImportError:
            logger.error("websocket-client library not available. Install with: pip install websocket-client")
            return {"ok": False, "reason": "websocket_client_not_available"}
        except Exception as e:
            logger.error(f"Error sending message via CDP: {e}")
            return {"ok": False, "reason": str(e)}
    
    async def _send_cdp_command(self, websocket, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Send a CDP command and wait for response."""
        import websockets
        
        message_id = int(time.time() * 1000)
        command = {
            "id": message_id,
            "method": method,
            "params": params or {}
        }
        
        await websocket.send(json.dumps(command))
        
        # Wait for response
        while True:
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get("id") == message_id:
                return response_data
    
    def _send_cdp_command_sync(self, websocket, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Send a CDP command synchronously and wait for response."""
        import websocket
        
        message_id = int(time.time() * 1000)
        command = {
            "id": message_id,
            "method": method,
            "params": params or {}
        }
        
        websocket.send(json.dumps(command))
        
        # Wait for response
        while True:
            response = websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get("id") == message_id:
                return response_data
    
    def find_cursor_targets(self) -> List[CDPTarget]:
        """Find Cursor-specific targets."""
        all_targets = self.get_targets()
        cursor_targets = []
        
        for target in all_targets:
            # Look for Cursor-specific indicators
            if any(indicator in target.title.lower() for indicator in [
                "cursor", "agent", "chat", "message", "conversation"
            ]):
                cursor_targets.append(target)
        
        return cursor_targets
    
    def test_connection(self) -> bool:
        """Test CDP connection."""
        try:
            targets = self.get_targets()
            return len(targets) > 0
        except Exception:
            return False


class CDPMessageQueue:
    """CDP-based message queue for headless delivery."""
    
    def __init__(self, cdp_port: int = 9222):
        self.cdp_delivery = CDPMessageDelivery(cdp_port)
        self.message_queue: List[Dict[str, Any]] = []
        self.is_running = False
    
    def add_message(self, target_id: str, message: str, priority: int = 0) -> str:
        """Add message to queue."""
        message_id = f"cdp_msg_{int(time.time() * 1000)}"
        
        queue_item = {
            "id": message_id,
            "target_id": target_id,
            "message": message,
            "priority": priority,
            "timestamp": time.time(),
            "status": "pending"
        }
        
        self.message_queue.append(queue_item)
        # Sort by priority (higher priority first)
        self.message_queue.sort(key=lambda x: x["priority"], reverse=True)
        
        return message_id
    
    async def process_queue_async(self):
        """Process message queue asynchronously."""
        self.is_running = True
        
        while self.is_running and self.message_queue:
            if self.message_queue:
                queue_item = self.message_queue.pop(0)
                
                # Find target
                targets = self.cdp_delivery.get_targets()
                target = next((t for t in targets if t.id == queue_item["target_id"]), None)
                
                if target:
                    try:
                        result = await self.cdp_delivery.send_message_async(target, queue_item["message"])
                        queue_item["status"] = "completed"
                        queue_item["result"] = result
                        logger.info(f"CDP message {queue_item['id']} delivered: {result}")
                    except Exception as e:
                        queue_item["status"] = "failed"
                        queue_item["error"] = str(e)
                        logger.error(f"CDP message {queue_item['id']} failed: {e}")
                else:
                    queue_item["status"] = "failed"
                    queue_item["error"] = "target_not_found"
                    logger.error(f"CDP target {queue_item['target_id']} not found")
            
            await asyncio.sleep(0.1)  # Small delay
    
    def stop(self):
        """Stop the message queue."""
        self.is_running = False


# Utility functions for easy usage
def send_message_to_cursor(message: str, cdp_port: int = 9222, target_title: Optional[str] = None) -> Dict[str, Any]:
    """Send a message to Cursor via CDP."""
    cdp_delivery = CDPMessageDelivery(cdp_port)
    
    # Find targets
    targets = cdp_delivery.get_targets()
    
    if not targets:
        return {"ok": False, "reason": "no_cdp_targets_found"}
    
    # Find specific target if title provided
    if target_title:
        target = next((t for t in targets if target_title.lower() in t.title.lower()), None)
        if not target:
            return {"ok": False, "reason": f"target_with_title_{target_title}_not_found"}
        targets = [target]
    
    # Send to first available target
    target = targets[0]
    result = cdp_delivery.send_message_sync(target, message)
    
    return {
        "ok": result.get("ok", False),
        "target": target.title,
        "result": result
    }


def broadcast_message_to_cursor(message: str, cdp_port: int = 9222) -> List[Dict[str, Any]]:
    """Broadcast message to all Cursor targets."""
    cdp_delivery = CDPMessageDelivery(cdp_port)
    targets = cdp_delivery.get_targets()
    
    results = []
    for target in targets:
        try:
            result = cdp_delivery.send_message_sync(target, message)
            results.append({
                "target": target.title,
                "ok": result.get("ok", False),
                "result": result
            })
        except Exception as e:
            results.append({
                "target": target.title,
                "ok": False,
                "error": str(e)
            })
    
    return results


# Example usage
if __name__ == "__main__":
    # Test CDP connection
    cdp_delivery = CDPMessageDelivery()
    
    if cdp_delivery.test_connection():
        print("CDP connection successful!")
        
        # Get targets
        targets = cdp_delivery.get_targets()
        print(f"Found {len(targets)} targets:")
        for target in targets:
            print(f"  - {target.title} ({target.url})")
        
        # Send test message
        if targets:
            test_message = "Agent-1: Testing CDP message delivery system. Report status."
            result = cdp_delivery.send_message_sync(targets[0], test_message)
            print(f"Test message result: {result}")
    else:
        print("CDP connection failed. Make sure Cursor is running with --remote-debugging-port=9222")
