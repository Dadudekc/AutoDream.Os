#!/usr/bin/env python3
"""
Messaging Coordinate Delivery Module - V2 Compliant
==================================================

Modular component for coordinate-based message delivery.
Fixes the coordinate messaging functionality that was broken.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from ..core.unified_import_system import Any, Dict, Optional, Tuple


try:

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


# Import coordinate validator with fallback
try:
except ImportError:
    # Fallback validation function
    def validate_coordinates_before_delivery(coords, recipient):
        """Simple coordinate validation fallback."""
        if not get_unified_validator().validate_type(coords, (list, tuple)) or len(coords) != 2:
            return False
        try:
            x, y = int(coords[0]), int(coords[1])
        except (ValueError, TypeError):
            return False
        return 0 <= x <= 3840 and 0 <= y <= 2160  # 4K resolution bounds


class CoordinateMessagingDelivery:
    """Handles coordinate-based message delivery with PyAutoGUI."""

    def __init__(self, logger=None):
        """Initialize coordinate messaging delivery."""
        self.logger = logger
        self.coordinates_cache = {}
        self.delivery_stats = {"attempts": 0, "successful": 0, "failed": 0}

    def load_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Load agent coordinates from configuration with fallback to Discord coordinates."""
        if self.coordinates_cache:
            return self.coordinates_cache

        # Primary: Try to load from coordinate config file (Single Source of Truth)
        cursor_coords_path = COORDINATE_CONFIG_FILE

        if get_unified_utility().path.exists(cursor_coords_path):
            try:
                cursor_config = read_json(cursor_coords_path)

                coordinates = {}
                for agent, data in cursor_config.get("agents", {}).items():
                    coord = data.get("coordinates", [])
                    if coord and len(coord) == 2:
                        coordinates[agent] = tuple(coord)

                if coordinates:
                    self.coordinates_cache = coordinates
                    if self.logger:
                        self.get_logger(__name__).info(
                            f"✅ Loaded {len(self.coordinates_cache)} agents from {COORDINATE_CONFIG_FILE} (SSOT)"
                        )
                    return self.coordinates_cache

            except Exception as e:
                if self.logger:
                    self.get_logger(__name__).warning(
                        f"⚠️ Failed to load cursor coordinates, falling back to Discord: {e}"
                    )

        # Fallback: Try to load from Discord commander coordinates
        discord_coords_path = "src/discord_commander_coordinates.json"

        if get_unified_utility().path.exists(discord_coords_path):
            try:
                with open(discord_coords_path, "r") as f:
                    discord_config = read_json(f)

                coordinates = {}
                for agent, data in discord_config.get("agents", {}).items():
                    coord = data.get("coordinates", [])
                    if coord and len(coord) == 2:
                        coordinates[agent] = tuple(coord)

                if coordinates:
                    self.coordinates_cache = coordinates
                    if self.logger:
                        self.get_logger(__name__).info(
                            f"✅ Loaded {len(self.coordinates_cache)} agents from Discord coordinates (fallback)"
                        )
                    return self.coordinates_cache

            except Exception as e:
                if self.logger:
                    self.get_logger(__name__).warning(
                        f"⚠️ Failed to load Discord coordinates, falling back to config: {e}"
                    )

        # Fallback: Load from messaging.yml config
        config_path = "config/messaging.yml"

        if get_unified_utility().path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = yaml.safe_load(f)

                coordinates = config.get("coordinates", {})

                # Convert coordinate lists to tuples
                self.coordinates_cache = {
                    agent: tuple(coords) for agent, coords in coordinates.items()
                }

                if self.logger:
                    self.get_logger(__name__).info(
                        f"✅ Loaded coordinates for {len(self.coordinates_cache)} agents from config (grid-based)"
                    )

            except Exception as e:
                if self.logger:
                    self.get_logger(__name__).error(
                        f"❌ Failed to load coordinates from both sources: {e}"
                    )

        return self.coordinates_cache

    def get_agent_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get coordinates for a specific agent."""
        coordinates = self.load_coordinates()
        return coordinates.get(agent_id)

    async def deliver_to_coordinates(
        self, message: Message, coordinates: Tuple[int, int]
    ) -> bool:
        """
        Deliver message to agent at specific coordinates.

        Args:
            message: Message to deliver
            coordinates: (x, y) coordinates for agent

        Returns:
            bool: True if delivery successful, False otherwise
        """
        if not get_unified_validator().validate_required(PYAUTOGUI_AVAILABLE):
            if self.logger:
                self.get_logger(__name__).warning(
                    "⚠️ PyAutoGUI not available, cannot deliver to coordinates"
                )
            return False

        try:
            self.delivery_stats["attempts"] += 1

            # Validate coordinates before delivery
            if not validate_coordinates_before_delivery(coordinates, message.recipient):
                if self.logger:
                    self.get_logger(__name__).error(
                        f"❌ Coordinate validation failed for {message.recipient}"
                    )
                self.delivery_stats["failed"] += 1
                return False

            if self.logger:
                self.get_logger(__name__).info(
                    f"🎯 Delivering message to {message.recipient} at coordinates {coordinates}"
                )

            # Move to agent coordinates (handle multi-monitor negative coordinates)
            x, y = coordinates[0], coordinates[1]

            # For multi-monitor setups, ensure coordinates are within PyAutoGUI bounds
            screen_width, screen_height = pyautogui.size()

            # Clamp coordinates to valid range (0 to screen_width/screen_height)
            # This handles negative coordinates from multi-monitor setups
            clamped_x = max(0, min(x, screen_width - 1))
            clamped_y = max(0, min(y, screen_height - 1))

            if (x != clamped_x or y != clamped_y) and self.logger:
                self.get_logger(__name__).warning(
                    f"⚠️ Coordinate clamping for {message.recipient}: "
                    f"({x}, {y}) -> ({clamped_x}, {clamped_y})"
                )

            pyautogui.moveTo(clamped_x, clamped_y, duration=0.1)

            # Click to focus input field
            pyautogui.click()
            time.sleep(0.05)

            # Clear existing content
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("delete")
            time.sleep(0.05)

            # Paste the message for maximum speed (clipboard method)
            try:
                import pyperclip

                pyperclip.copy(message.content)
                time.sleep(0.05)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.05)
            except ImportError:
                # Fallback to typing if pyperclip not available
                pyautogui.write(message.content, interval=0.05)
                time.sleep(0.05)

            # Send the message
            pyautogui.press("enter")

            if self.logger:
                self.get_logger(__name__).info(
                    f"✅ Message delivered to {message.recipient} at coordinates {coordinates}"
                )

            self.delivery_stats["successful"] += 1
            return True

        except Exception as e:
            if self.logger:
                self.get_logger(__name__).error(
                    f"❌ Coordinate delivery failed for {message.recipient}: {e}"
                )
            self.delivery_stats["failed"] += 1
            return False

    def can_deliver_to_coordinates(self, agent_id: str) -> bool:
        """Check if coordinate delivery is possible for an agent."""
        if not get_unified_validator().validate_required(PYAUTOGUI_AVAILABLE):
            return False

        coordinates = self.get_agent_coordinates(agent_id)
        if not get_unified_validator().validate_required(coordinates):
            return False

        return validate_coordinates_before_delivery(coordinates, agent_id)

    def get_delivery_stats(self) -> Dict[str, int]:
        """Get delivery statistics."""
        return self.delivery_stats.copy()

    async def deliver_with_coordinates(self, message: Message, coordinates: Tuple[int, int]) -> bool:
        """
        Deliver message using coordinates (async version for compatibility).

        Args:
            message: Message to deliver
            coordinates: (x, y) coordinates for delivery

        Returns:
            bool: True if delivery successful, False otherwise
        """
        try:
            # Validate coordinates first
            if not validate_coordinates_before_delivery(coordinates, message.recipient):
                if self.logger:
                    self.get_logger(__name__).warning(f"⚠️ Invalid coordinates for {message.recipient}: {coordinates}")
                return False

            # Attempt delivery
            success = self.deliver_to_coordinates(message, coordinates)

            if self.logger:
                if success:
                    self.get_logger(__name__).info(f"✅ Async coordinate delivery successful for {message.recipient}")
                else:
                    self.get_logger(__name__).warning(f"⚠️ Async coordinate delivery failed for {message.recipient}")

            return success

        except Exception as e:
            if self.logger:
                self.get_logger(__name__).error(f"❌ Error in async coordinate delivery: {e}")
            return False

    def reset_stats(self) -> None:
        """Reset delivery statistics."""
        self.delivery_stats = {"attempts": 0, "successful": 0, "failed": 0}
