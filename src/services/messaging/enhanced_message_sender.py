#!/usr/bin/env python3
"""
Enhanced Message Sender
=======================

Provides enhanced message sending with coordinate validation,
clipboard validation, and UI Ops facade integration.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
import time
from typing import Optional, Tuple

from src.libs.uiops import UI

logger = logging.getLogger(__name__)


class CoordinateValidator:
    """Validates coordinates before use."""
    
    @staticmethod
    def validate_coordinates(coords: Tuple[int, int]) -> Tuple[bool, str]:
        """Validate coordinates are valid and within bounds."""
        try:
            if not coords or len(coords) != 2:
                return False, "Invalid coordinates format"
            
            x, y = coords
            
            # Check for valid integers
            if not isinstance(x, int) or not isinstance(y, int):
                return False, "Coordinates must be integers"
            
            # Check bounds (adjust for your screen setup)
            if x < 0 or x > 4000 or y < 0 or y > 4000:
                return False, f"Coordinates out of bounds: ({x}, {y})"
            
            # Check for obviously invalid coordinates
            if x == 0 and y == 0:
                return False, "Coordinates (0, 0) are likely invalid"
            
            return True, "Coordinates valid"
            
        except Exception as e:
            return False, f"Coordinate validation error: {e}"


class ClipboardValidator:
    """Validates clipboard operations."""
    
    @staticmethod
    def validate_clipboard_content(text: str) -> Tuple[bool, str]:
        """Validate text is safe for clipboard."""
        try:
            if not text or not isinstance(text, str):
                return False, "Text must be non-empty string"
            
            if len(text) > 50000:  # Reasonable clipboard limit
                return False, "Text too long for clipboard"
            
            # Check for problematic characters
            problematic_chars = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05"]
            for char in problematic_chars:
                if char in text:
                    return False, f"Text contains problematic character: {repr(char)}"
            
            return True, "Text valid for clipboard"
            
        except Exception as e:
            return False, f"Clipboard validation error: {e}"


class EnhancedMessageSender:
    """Enhanced message sender with validation and UI Ops integration."""
    
    def __init__(self):
        """Initialize enhanced message sender."""
        self.ui = UI()
        self.coord_validator = CoordinateValidator()
        self.clipboard_validator = ClipboardValidator()
        self._last_clipboard_content = ""
        
    def send_to_coordinates(
        self, 
        coords: Tuple[int, int], 
        text: str,
        max_retries: int = 3,
        retry_delay: float = 0.5
    ) -> bool:
        """Send message to coordinates with full validation."""
        try:
            # Step 1: Validate coordinates
            coords_valid, coords_msg = self.coord_validator.validate_coordinates(coords)
            if not coords_valid:
                logger.error(f"❌ Coordinate validation failed: {coords_msg}")
                return False
            
            logger.info(f"✅ Coordinate validation passed: {coords_msg}")
            
            # Step 2: Validate text content
            text_valid, text_msg = self.clipboard_validator.validate_clipboard_content(text)
            if not text_valid:
                logger.error(f"❌ Text validation failed: {text_msg}")
                return False
            
            logger.info(f"✅ Text validation passed: {text_msg}")
            
            # Step 3: Save current clipboard
            original_clipboard = self._save_current_clipboard()
            
            # Step 4: Send message with retries
            for attempt in range(max_retries):
                try:
                    success = self._send_message_with_ui_ops(coords, text)
                    if success:
                        logger.info(f"✅ Message sent successfully on attempt {attempt + 1}")
                        return True
                    else:
                        logger.warning(f"⚠️ Message send failed on attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            
                except Exception as e:
                    logger.warning(f"⚠️ Message send exception on attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
            
            logger.error(f"❌ Message send failed after {max_retries} attempts")
            return False
            
        except Exception as e:
            logger.error(f"❌ Critical error in send_to_coordinates: {e}")
            return False
        
        finally:
            # Always attempt to restore clipboard
            self._restore_clipboard(original_clipboard)
    
    def _save_current_clipboard(self) -> str:
        """Save current clipboard content."""
        try:
            # Use UI Ops to get clipboard content
            self._last_clipboard_content = self.ui.get_clipboard()
            logger.debug(f"Saved clipboard content: {self._last_clipboard_content[:50]}...")
            return self._last_clipboard_content
        except Exception as e:
            logger.warning(f"Failed to save clipboard content: {e}")
            return ""
    
    def _restore_clipboard(self, original_content: str):
        """Restore clipboard content."""
        try:
            if original_content and len(original_content) < 1000:
                self.ui.set_clipboard(original_content)
                logger.debug("Clipboard content restored")
            else:
                self.ui.set_clipboard("")
                logger.debug("Clipboard cleared")
        except Exception as e:
            logger.warning(f"Failed to restore clipboard: {e}")
    
    def _send_message_with_ui_ops(self, coords: Tuple[int, int], text: str) -> bool:
        """Send message using UI Ops facade."""
        try:
            # Step 1: Set clipboard content
            self.ui.set_clipboard(text)
            
            # Step 2: Verify clipboard was set correctly
            clipboard_content = self.ui.get_clipboard()
            if clipboard_content != text:
                logger.error("❌ Clipboard content verification failed")
                return False
            
            logger.debug("✅ Clipboard content verified")
            
            # Step 3: Click at coordinates to focus
            self.ui.click(coords[0], coords[1])
            self.ui.sleep(0.3)
            
            # Step 4: Ensure focus with second click
            self.ui.click(coords[0], coords[1])
            self.ui.sleep(0.2)
            
            # Step 5: Paste content
            self.ui.hotkey("ctrl", "v")
            self.ui.sleep(0.2)
            
            # Step 6: Send message
            self.ui.press("enter")
            self.ui.sleep(0.1)
            
            logger.debug("✅ Message sent via UI Ops")
            return True
            
        except Exception as e:
            logger.error(f"❌ UI Ops message send failed: {e}")
            return False
    
    def get_clipboard_status(self) -> dict:
        """Get clipboard status information."""
        try:
            content = self.ui.get_clipboard()
            return {
                "has_content": bool(content),
                "content_length": len(content),
                "content_preview": content[:100] if content else "",
                "is_valid": self.clipboard_validator.validate_clipboard_content(content)[0]
            }
        except Exception as e:
            return {
                "error": str(e),
                "has_content": False,
                "is_valid": False
            }
    
    def get_coordinate_status(self, coords: Tuple[int, int]) -> dict:
        """Get coordinate validation status."""
        is_valid, message = self.coord_validator.validate_coordinates(coords)
        return {
            "coordinates": coords,
            "is_valid": is_valid,
            "message": message
        }


# Global enhanced sender instance
_global_sender: Optional[EnhancedMessageSender] = None


def get_enhanced_sender() -> EnhancedMessageSender:
    """Get global enhanced message sender instance."""
    global _global_sender
    if _global_sender is None:
        _global_sender = EnhancedMessageSender()
    return _global_sender

