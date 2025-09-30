#!/usr/bin/env python3
"""
Enhanced Message Validator - Pre-Paste Validation
================================================

Enhanced message validation system that validates messages before pasting
to prevent paste failures in the consolidated messaging system.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
import re
import time

logger = logging.getLogger(__name__)

# Lazy import to prevent hard dep at import time
try:
    import pyperclip

    PYPERCLIP_AVAILABLE = True
except Exception as e:
    pyperclip = None
    PYPERCLIP_AVAILABLE = False
    logger.warning(f"Pyperclip import failed: {e}")


class EnhancedMessageValidator:
    """Enhanced message validator with pre-paste validation."""

    def __init__(self) -> None:
        """Initialize enhanced message validator."""
        self.pyperclip_available = PYPERCLIP_AVAILABLE
        self.max_message_length = 10000
        self.max_clipboard_size = 50000  # Reasonable clipboard limit

        # Problematic characters that can cause paste failures
        self.problematic_chars = [
            "\x00",  # Null bytes
            "\x01",  # Start of heading
            "\x02",  # Start of text
            "\x03",  # End of text
            "\x04",  # End of transmission
            "\x05",  # Enquiry
            "\x06",  # Acknowledge
            "\x07",  # Bell
            "\x08",  # Backspace
            "\x0b",  # Vertical tab
            "\x0c",  # Form feed
            "\x0e",  # Shift out
            "\x0f",  # Shift in
            "\x10",  # Data link escape
            "\x11",  # Device control 1
            "\x12",  # Device control 2
            "\x13",  # Device control 3
            "\x14",  # Device control 4
            "\x15",  # Negative acknowledge
            "\x16",  # Synchronous idle
            "\x17",  # End of transmission block
            "\x18",  # Cancel
            "\x19",  # End of medium
            "\x1a",  # Substitute
            "\x1b",  # Escape
            "\x1c",  # File separator
            "\x1d",  # Group separator
            "\x1e",  # Record separator
            "\x1f",  # Unit separator
        ]

    def validate_message_for_paste(self, message: str) -> dict[str, any]:
        """Validate message content before pasting."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "sanitized_message": message,
            "paste_safe": True,
        }

        if not message:
            validation_result["valid"] = False
            validation_result["errors"].append("Message content cannot be empty")
            return validation_result

        # Check message length
        if len(message) > self.max_message_length:
            validation_result["valid"] = False
            validation_result["errors"].append(
                f"Message too long (max {self.max_message_length} characters)"
            )
            return validation_result

        # Check clipboard availability
        if not self.pyperclip_available:
            validation_result["warnings"].append("Pyperclip not available - paste may fail")
            validation_result["paste_safe"] = False

        # Check for problematic characters
        problematic_found = []
        for char in self.problematic_chars:
            if char in message:
                problematic_found.append(f"Control character {repr(char)}")
                validation_result["paste_safe"] = False

        if problematic_found:
            validation_result["warnings"].extend(problematic_found)
            # Sanitize the message
            sanitized = message
            for char in self.problematic_chars:
                sanitized = sanitized.replace(char, "")
            validation_result["sanitized_message"] = sanitized

        # Check for extremely long lines (can cause paste issues)
        lines = message.split("\n")
        long_lines = [i for i, line in enumerate(lines) if len(line) > 1000]
        if long_lines:
            validation_result["warnings"].append(f"Long lines detected at positions: {long_lines}")
            validation_result["paste_safe"] = False

        # Check for excessive special characters
        special_char_count = len(re.findall(r"[^\w\s\n\r\t]", message))
        if special_char_count > len(message) * 0.3:  # More than 30% special chars
            validation_result["warnings"].append(
                "High ratio of special characters may cause paste issues"
            )
            validation_result["paste_safe"] = False

        # Check for clipboard size
        if len(message.encode("utf-8")) > self.max_clipboard_size:
            validation_result["warnings"].append("Message size may exceed clipboard limits")
            validation_result["paste_safe"] = False

        return validation_result

    def test_clipboard_functionality(self) -> dict[str, any]:
        """Test clipboard functionality before pasting."""
        test_result = {"clipboard_working": False, "error": None, "test_message": None}

        if not self.pyperclip_available:
            test_result["error"] = "Pyperclip not available"
            return test_result

        try:
            # Test with a simple message
            test_message = "CLIPBOARD_TEST_" + str(int(time.time()))
            pyperclip.copy(test_message)
            time.sleep(0.1)  # Brief wait
            clipboard_content = pyperclip.paste()

            if clipboard_content == test_message:
                test_result["clipboard_working"] = True
                test_result["test_message"] = test_message
            else:
                test_result[
                    "error"
                ] = f"Clipboard test failed: expected '{test_message}', got '{clipboard_content}'"

        except Exception as e:
            test_result["error"] = f"Clipboard test error: {e}"

        return test_result

    def validate_and_prepare_for_paste(self, message: str) -> dict[str, any]:
        """Comprehensive validation and preparation for paste operation."""
        result = {
            "ready_for_paste": False,
            "validation": None,
            "clipboard_test": None,
            "recommendations": [],
            "final_message": message,
        }

        # Validate message content
        validation = self.validate_message_for_paste(message)
        result["validation"] = validation

        # Test clipboard functionality
        clipboard_test = self.test_clipboard_functionality()
        result["clipboard_test"] = clipboard_test

        # Determine if ready for paste
        if validation["valid"] and validation["paste_safe"] and clipboard_test["clipboard_working"]:
            result["ready_for_paste"] = True
            result["final_message"] = validation["sanitized_message"]
        else:
            # Generate recommendations
            if not validation["valid"]:
                result["recommendations"].extend(validation["errors"])
            if not validation["paste_safe"]:
                result["recommendations"].extend(validation["warnings"])
            if not clipboard_test["clipboard_working"]:
                result["recommendations"].append(f"Clipboard issue: {clipboard_test['error']}")
                result["recommendations"].append("Consider using typing instead of paste")

        return result

    def get_paste_alternative_strategy(self, message: str) -> dict[str, any]:
        """Get alternative strategy if paste fails."""
        return {
            "use_typing": True,
            "typing_interval": 0.01,
            "chunk_size": 100,  # Type in chunks to avoid issues
            "delay_between_chunks": 0.1,
            "message_chunks": [message[i : i + 100] for i in range(0, len(message), 100)],
        }

    def validate_coordinates(self, coordinates: list[int]) -> dict[str, any]:
        """Validate agent coordinates before focusing."""
        result = {"valid": True, "errors": [], "warnings": []}

        if not coordinates or len(coordinates) != 2:
            result["valid"] = False
            result["errors"].append("Coordinates must be a list of 2 integers [x, y]")
            return result

        x, y = coordinates

        # Check for reasonable screen coordinates
        if x < 0 or y < 0:
            result["warnings"].append("Negative coordinates detected")

        if x > 10000 or y > 10000:
            result["warnings"].append(
                "Very large coordinates detected - may be outside screen bounds"
            )

        if not isinstance(x, int) or not isinstance(y, int):
            result["valid"] = False
            result["errors"].append("Coordinates must be integers")

        return result

    def get_validation_summary(self, validation_result: dict[str, any]) -> str:
        """Get human-readable validation summary."""
        if validation_result["ready_for_paste"]:
            return "✅ Message ready for paste"
        else:
            recommendations = validation_result.get("recommendations", [])
            if recommendations:
                return f"⚠️ Paste issues detected: {'; '.join(recommendations)}"
            else:
                return "❌ Message not ready for paste"


# Integration with existing PyAutoGUI handler
def enhance_pyautogui_handler_with_validation():
    """Enhance PyAutoGUI handler with pre-paste validation."""

    class EnhancedPyAutoGUIHandler:
        """Enhanced PyAutoGUI handler with pre-paste validation."""

        def __init__(self, original_handler):
            self.original_handler = original_handler
            self.validator = EnhancedMessageValidator()

        def send_message_content_with_validation(
            self, message: str, use_paste: bool = True
        ) -> bool:
            """Send message content with pre-paste validation."""

            # Validate message before pasting
            validation_result = self.validator.validate_and_prepare_for_paste(message)

            if not validation_result["ready_for_paste"]:
                logger.warning(
                    f"Paste validation failed: {self.validator.get_validation_summary(validation_result)}"
                )

                # Try alternative strategy
                if use_paste:
                    logger.info("Falling back to typing method")
                    return self.original_handler.send_message_content(
                        validation_result["final_message"], use_paste=False
                    )
                else:
                    logger.error("Both paste and typing methods failed validation")
                    return False

            # Use validated message
            return self.original_handler.send_message_content(
                validation_result["final_message"], use_paste=use_paste
            )

    return EnhancedPyAutoGUIHandler


if __name__ == "__main__":
    # Test the enhanced validator
    validator = EnhancedMessageValidator()

    # Test with various message types
    test_messages = [
        "Simple message",
        "Message with special chars: !@#$%^&*()",
        "Message with control chars: \x00\x01\x02",
        "Very long message: " + "x" * 5000,
        "Message with newlines:\nLine 1\nLine 2\nLine 3",
    ]

    for msg in test_messages:
        print(f"\nTesting message: {repr(msg[:50])}...")
        result = validator.validate_and_prepare_for_paste(msg)
        print(f"Ready for paste: {result['ready_for_paste']}")
        print(f"Summary: {validator.get_validation_summary(result)}")
        if result["recommendations"]:
            print(f"Recommendations: {result['recommendations']}")
