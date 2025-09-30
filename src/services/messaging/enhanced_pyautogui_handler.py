#!/usr/bin/env python3
"""
Enhanced PyAutoGUI Handler - Pre-Paste Validation Integration
============================================================

Enhanced PyAutoGUI handler that integrates pre-paste validation
to prevent paste failures in the consolidated messaging system.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
import time

logger = logging.getLogger(__name__)

# Lazy import to prevent hard dep at import time
try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    pyautogui = None
    pyperclip = None
    PYAUTOGUI_AVAILABLE = False
    logger.warning(f"PyAutoGUI import failed: {e}")


class EnhancedPyAutoGUIHandler:
    """Enhanced PyAutoGUI handler with pre-paste validation."""

    def __init__(self) -> None:
        """Initialize enhanced PyAutoGUI handler."""
        self.pyautogui_available = PYAUTOGUI_AVAILABLE
        # Import the enhanced validator
        from .enhanced_message_validator import EnhancedMessageValidator
        self.validator = EnhancedMessageValidator()

        if self.pyautogui_available:
            # Configure PyAutoGUI settings
            pyautogui.PAUSE = 0.1
            pyautogui.FAILSAFE = True

    def is_available(self) -> bool:
        """Check if PyAutoGUI is available."""
        return self.pyautogui_available

    def validate_coordinates(self, coordinates: list[int]) -> dict[str, any]:
        """Validate agent coordinates before focusing."""
        return self.validator.validate_coordinates(coordinates)

    def focus_agent_window(self, coordinates: list[int]) -> bool:
        """Focus on agent window using coordinates with validation."""
        if not self.pyautogui_available:
            logger.error("PyAutoGUI not available")
            return False

        # Validate coordinates first
        coord_validation = self.validate_coordinates(coordinates)
        if not coord_validation["valid"]:
            logger.error(f"Invalid coordinates: {coord_validation['errors']}")
            return False

        if coord_validation["warnings"]:
            logger.warning(f"Coordinate warnings: {coord_validation['warnings']}")

        try:
            x, y = coordinates
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)  # Wait for focus
            return True
        except Exception as e:
            logger.error(f"Error focusing agent window: {e}")
            return False

    def clear_input_area(self) -> bool:
        """Clear the input area."""
        if not self.pyautogui_available:
            return False

        try:
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.1)
            return True
        except Exception as e:
            logger.error(f"Error clearing input area: {e}")
            return False

    def create_new_tab(self, method: str = "ctrl_t") -> bool:
        """Create new tab or window."""
        if not self.pyautogui_available:
            return False

        try:
            if method == "ctrl_t":
                pyautogui.hotkey("ctrl", "t")
            elif method == "ctrl_n":
                pyautogui.hotkey("ctrl", "n")
            time.sleep(1.0)  # Wait for tab/window creation
            return True
        except Exception as e:
            logger.error(f"Error creating new tab: {e}")
            return False

    def send_message_content_with_validation(self, message: str, use_paste: bool = True) -> bool:
        """Send message content with pre-paste validation."""
        if not self.pyautogui_available:
            logger.error("PyAutoGUI not available")
            return False

        # Validate message before pasting
        validation_result = self.validator.validate_and_prepare_for_paste(message)

        if not validation_result["ready_for_paste"]:
            logger.warning(
                f"Paste validation failed: {self.validator.get_validation_summary(validation_result)}"
            )

            # Try alternative strategy
            if use_paste:
                logger.info("Falling back to typing method")
                return self._send_message_by_typing(validation_result["final_message"])
            else:
                logger.error("Both paste and typing methods failed validation")
                return False

        # Use validated message for paste
        try:
            if use_paste and pyperclip:
                pyperclip.copy(validation_result["final_message"])
                time.sleep(1.0)  # Wait for clipboard
                pyautogui.hotkey("ctrl", "v")
            else:
                return self._send_message_by_typing(validation_result["final_message"])

            time.sleep(0.5)
            pyautogui.press("enter")
            logger.info("Message sent successfully via validated paste")
            return True
        except Exception as e:
            logger.error(f"Error sending validated message content: {e}")
            # Fallback to typing
            return self._send_message_by_typing(validation_result["final_message"])

    def _send_message_by_typing(self, message: str) -> bool:
        """Send message by typing with chunking for large messages."""
        if not self.pyautogui_available:
            return False

        try:
            # For very long messages, type in chunks
            if len(message) > 1000:
                chunk_size = 100
                chunks = [message[i : i + chunk_size] for i in range(0, len(message), chunk_size)]

                for i, chunk in enumerate(chunks):
                    pyautogui.typewrite(chunk, interval=0.01)
                    if i < len(chunks) - 1:  # Not the last chunk
                        time.sleep(0.1)  # Brief pause between chunks
            else:
                pyautogui.typewrite(message, interval=0.01)

            time.sleep(0.5)
            pyautogui.press("enter")
            logger.info("Message sent successfully via typing")
            return True
        except Exception as e:
            logger.error(f"Error sending message by typing: {e}")
            return False

    def send_message_to_agent_with_validation(
        self,
        coordinates: list[int],
        message: str,
        use_paste: bool = True,
        new_tab_method: str = "ctrl_t",
    ) -> bool:
        """Send complete message to agent via PyAutoGUI with validation."""
        if not self.pyautogui_available:
            logger.error("PyAutoGUI not available for message delivery")
            return False

        try:
            # Focus on agent window
            if not self.focus_agent_window(coordinates):
                return False

            # Clear input area
            if not self.clear_input_area():
                return False

            # Create new tab
            if not self.create_new_tab(new_tab_method):
                return False

            # Send message content with validation
            if not self.send_message_content_with_validation(message, use_paste):
                return False

            logger.info("Message sent successfully via enhanced PyAutoGUI")
            return True

        except Exception as e:
            logger.error(f"Error in enhanced PyAutoGUI message delivery: {e}")
            return False

    def send_bulk_messages_with_validation(
        self,
        agent_list: list[tuple],
        message: str,
        use_paste: bool = True,
        new_tab_method: str = "ctrl_t",
    ) -> dict:
        """Send message to multiple agents with validation."""
        results = {"success": [], "failed": []}

        # Pre-validate message for all agents
        validation_result = self.validator.validate_and_prepare_for_paste(message)
        if not validation_result["ready_for_paste"]:
            logger.warning(
                f"Bulk message validation failed: {self.validator.get_validation_summary(validation_result)}"
            )
            # Use sanitized message for all agents
            message = validation_result["final_message"]

        for agent_id, coordinates in agent_list:
            try:
                success = self.send_message_to_agent_with_validation(
                    coordinates, message, use_paste, new_tab_method
                )
                if success:
                    results["success"].append(agent_id)
                    time.sleep(1.0)  # Inter-agent delay
                else:
                    results["failed"].append(agent_id)
            except Exception as e:
                logger.error(f"Error sending to {agent_id}: {e}")
                results["failed"].append(agent_id)

        return results

    def get_screen_info(self) -> dict:
        """Get PyAutoGUI screen information."""
        if not self.pyautogui_available:
            return {"available": False, "error": "PyAutoGUI not available"}

        try:
            screen_size = pyautogui.size()
            return {
                "available": True,
                "screen_size": screen_size,
                "width": screen_size.width,
                "height": screen_size.height,
            }
        except Exception as e:
            return {"available": False, "error": str(e)}

    def test_messaging_functionality(self) -> dict[str, any]:
        """Test messaging functionality with validation."""
        test_result = {
            "pyautogui_available": self.pyautogui_available,
            "validator_available": True,
            "clipboard_test": None,
            "screen_info": None,
            "overall_status": "unknown",
        }

        if not self.pyautogui_available:
            test_result["overall_status"] = "failed"
            test_result["error"] = "PyAutoGUI not available"
            return test_result

        # Test clipboard functionality
        test_result["clipboard_test"] = self.validator.test_clipboard_functionality()

        # Test screen info
        test_result["screen_info"] = self.get_screen_info()

        # Determine overall status
        if (
            test_result["clipboard_test"]["clipboard_working"]
            and test_result["screen_info"]["available"]
        ):
            test_result["overall_status"] = "success"
        else:
            test_result["overall_status"] = "partial"
            test_result["issues"] = []
            if not test_result["clipboard_test"]["clipboard_working"]:
                test_result["issues"].append("Clipboard not working")
            if not test_result["screen_info"]["available"]:
                test_result["issues"].append("Screen info not available")

        return test_result


if __name__ == "__main__":
    # Test the enhanced handler
    handler = EnhancedPyAutoGUIHandler()

    print("Enhanced PyAutoGUI Handler Test")
    print("=" * 40)

    # Test availability
    print(f"PyAutoGUI Available: {handler.is_available()}")

    # Test messaging functionality
    test_result = handler.test_messaging_functionality()
    print(f"Overall Status: {test_result['overall_status']}")

    if test_result.get("issues"):
        print(f"Issues: {test_result['issues']}")

    # Test message validation
    test_message = "Test message for validation"
    validation_result = handler.validator.validate_and_prepare_for_paste(test_message)
    print(f"Message Validation: {handler.validator.get_validation_summary(validation_result)}")
