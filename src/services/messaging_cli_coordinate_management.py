#!/usr/bin/env python3
"""
Messaging CLI Coordinate Management - Agent Cellphone V2
======================================================

Coordinate management functionality for messaging CLI operations.
V2 Compliance: Clean, tested, class-based, reusable, scalable code.

Author: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from .messaging_cli_utils import MessagingCLIUtils

logger = logging.getLogger(__name__)


class MessagingCLICoordinateManagement:
    """Coordinate management functionality for messaging CLI operations."""

    def __init__(self):
        """Initialize coordinate management with dependencies."""
        self.utils = MessagingCLIUtils()

    def set_onboarding_coordinates(self, coord_string: str) -> Dict[str, Any]:
        """Set onboarding coordinates for an agent.

        Args:
            coord_string: Format "Agent-1,x,y"

        Returns:
            Result dictionary with success/error information
        """
        try:
            # Parse input: "Agent-1,x,y"
            parts = coord_string.split(',')
            if len(parts) != 3:
                return {"error": "Invalid format. Use: agent_id,x,y"}

            agent_id, x_str, y_str = parts

            try:
                x, y = int(x_str), int(y_str)
            except ValueError:
                return {"error": "Coordinates must be integers"}

            # Load current coordinates
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            # Update onboarding coordinates
            if agent_id in coords_data.get('agents', {}):
                coords_data['agents'][agent_id]['onboarding_input_coords'] = [x, y]
                coords_data['last_updated'] = datetime.now().isoformat()

                # Save updated coordinates
                if self.utils.write_json(coords_file, coords_data):
                    return {
                        "success": True,
                        "agent_id": agent_id,
                        "onboarding_coords": [x, y],
                        "message": f"Updated onboarding coordinates for {agent_id}"
                    }
                else:
                    return {"error": "Failed to save coordinates"}
            else:
                return {"error": f"Agent {agent_id} not found"}

        except Exception as e:
            logger.error(f"Error setting onboarding coordinates: {e}")
            return {"error": str(e)}

    def set_chat_coordinates(self, coord_string: str) -> Dict[str, Any]:
        """Set chat coordinates for an agent.

        Args:
            coord_string: Format "Agent-1,x,y"

        Returns:
            Result dictionary with success/error information
        """
        try:
            # Parse input: "Agent-1,x,y"
            parts = coord_string.split(',')
            if len(parts) != 3:
                return {"error": "Invalid format. Use: agent_id,x,y"}

            agent_id, x_str, y_str = parts

            try:
                x, y = int(x_str), int(y_str)
            except ValueError:
                return {"error": "Coordinates must be integers"}

            # Load current coordinates
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            # Update chat coordinates
            if agent_id in coords_data.get('agents', {}):
                coords_data['agents'][agent_id]['chat_input_coordinates'] = [x, y]
                coords_data['last_updated'] = datetime.now().isoformat()

                # Save updated coordinates
                if self.utils.write_json(coords_file, coords_data):
                    return {
                        "success": True,
                        "agent_id": agent_id,
                        "chat_coords": [x, y],
                        "message": f"Updated chat coordinates for {agent_id}"
                    }
                else:
                    return {"error": "Failed to save coordinates"}
            else:
                return {"error": f"Agent {agent_id} not found"}

        except Exception as e:
            logger.error(f"Error setting chat coordinates: {e}")
            return {"error": str(e)}

    def update_coordinates_from_file(self, file_path: str) -> Dict[str, Any]:
        """Update coordinates from a file.

        Args:
            file_path: Path to the coordinates file

        Returns:
            Result dictionary with success/error information
        """
        try:
            import os
            if not os.path.exists(file_path):
                return {"error": f"File {file_path} not found"}

            # Load new coordinates
            new_coords = self.utils.read_json(file_path)
            if not new_coords:
                return {"error": "Could not load coordinates from file"}

            # Validate structure
            if 'agents' not in new_coords:
                return {"error": "Invalid coordinates file format - missing 'agents' key"}

            # Update timestamp
            new_coords['last_updated'] = datetime.now().isoformat()

            # Save to main coordinates file
            coords_file = "cursor_agent_coords.json"
            if self.utils.write_json(coords_file, new_coords):
                return {
                    "success": True,
                    "message": f"Updated coordinates from {file_path}",
                    "agents_updated": len(new_coords.get('agents', {}))
                }
            else:
                return {"error": "Failed to save coordinates"}

        except Exception as e:
            logger.error(f"Error updating coordinates from file: {e}")
            return {"error": str(e)}

    def interactive_coordinate_capture(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Interactive coordinate capture mode.

        Args:
            agent_id: Optional specific agent to update, if None updates all agents

        Returns:
            Result dictionary with success/error information
        """
        try:
            from pynput import mouse

            print("Hover over ONBOARDING location and press ENTER...")

            captured_coords = []
            current_coords = [0, 0]

            def on_mouse_move(x, y):
                nonlocal current_coords
                current_coords = [x, y]

            def on_mouse_click(x, y, button, pressed):
                if pressed and button == mouse.Button.left:
                    nonlocal captured_coords
                    captured_coords.append([x, y])
                    if len(captured_coords) == 1:
                        print("Hover over CHAT location and press ENTER...")
                    elif len(captured_coords) == 2:
                        print("Done!")
                        return False

            listener = mouse.Listener(on_move=on_mouse_move, on_click=on_mouse_click)
            listener.start()

            while len(captured_coords) < 2:
                try:
                    input()
                    if len(captured_coords) == 0:
                        captured_coords.append(current_coords.copy())
                        print(f"Onboarding: {current_coords}")
                    elif len(captured_coords) == 1:
                        captured_coords.append(current_coords.copy())
                        print(f"Chat: {current_coords}")
                        break
                except KeyboardInterrupt:
                    break

            listener.stop()

            if len(captured_coords) == 2:
                onboarding_coords = captured_coords[0]
                chat_coords = captured_coords[1]

                if agent_id:
                    result = self.update_agent_coordinates(agent_id, onboarding_coords, chat_coords)
                else:
                    result = self.update_all_agents_coordinates(onboarding_coords, chat_coords)
                return result
            else:
                return {"error": "Capture cancelled"}

        except ImportError:
            return {"error": "Install pynput: pip install pynput"}
        except Exception as e:
            return {"error": str(e)}

    def update_agent_coordinates(self, agent_id: str, onboarding_coords: List[int], chat_coords: List[int]) -> Dict[str, Any]:
        """Update coordinates for a specific agent.

        Args:
            agent_id: The agent identifier
            onboarding_coords: [x, y] coordinates for onboarding input
            chat_coords: [x, y] coordinates for chat input

        Returns:
            Result dictionary with success/error information
        """
        try:
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            if agent_id not in coords_data.get('agents', {}):
                return {"error": f"Agent {agent_id} not found"}

            # Update coordinates
            coords_data['agents'][agent_id]['onboarding_input_coords'] = onboarding_coords
            coords_data['agents'][agent_id]['chat_input_coordinates'] = chat_coords
            coords_data['last_updated'] = datetime.now().isoformat()

            if self.utils.write_json(coords_file, coords_data):
                return {
                    "success": True,
                    "agent_id": agent_id,
                    "onboarding_coords": onboarding_coords,
                    "chat_coords": chat_coords,
                    "message": f"Updated coordinates for {agent_id}"
                }
            else:
                return {"error": "Failed to save coordinates"}

        except Exception as e:
            logger.error(f"Error updating agent coordinates: {e}")
            return {"error": str(e)}

    def update_all_agents_coordinates(self, onboarding_coords: List[int], chat_coords: List[int]) -> Dict[str, Any]:
        """Update coordinates for all agents.

        Args:
            onboarding_coords: [x, y] coordinates for onboarding input
            chat_coords: [x, y] coordinates for chat input

        Returns:
            Result dictionary with success/error information
        """
        try:
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            agents = coords_data.get('agents', {})
            updated_count = 0

            # Update coordinates for all agents
            for agent_id in agents:
                agents[agent_id]['onboarding_input_coords'] = onboarding_coords
                agents[agent_id]['chat_input_coordinates'] = chat_coords
                updated_count += 1

            coords_data['last_updated'] = datetime.now().isoformat()

            if self.utils.write_json(coords_file, coords_data):
                return {
                    "success": True,
                    "agents_updated": updated_count,
                    "onboarding_coords": onboarding_coords,
                    "chat_coords": chat_coords,
                    "message": f"Updated coordinates for all {updated_count} agents"
                }
            else:
                return {"error": "Failed to save coordinates"}

        except Exception as e:
            logger.error(f"Error updating all agents coordinates: {e}")
            return {"error": str(e)}

    def capture_onboarding_only(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Capture only onboarding coordinates.

        Args:
            agent_id: Optional specific agent to update

        Returns:
            Result dictionary with success/error information
        """
        try:
            from pynput import mouse

            print("Hover over ONBOARDING location and press ENTER...")

            current_coords = [0, 0]

            def on_mouse_move(x, y):
                nonlocal current_coords
                current_coords = [x, y]

            listener = mouse.Listener(on_move=on_mouse_move)
            listener.start()

            try:
                input()
                onboarding_coords = current_coords.copy()
                print(f"Onboarding: {onboarding_coords}")

                if agent_id:
                    result = self.update_onboarding_coordinates(agent_id, onboarding_coords)
                else:
                    result = self.update_all_onboarding_coordinates(onboarding_coords)
                return result

            except KeyboardInterrupt:
                return {"error": "Capture cancelled"}
            finally:
                listener.stop()

        except ImportError:
            return {"error": "Install pynput: pip install pynput"}
        except Exception as e:
            return {"error": str(e)}

    def capture_chat_only(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Capture only chat coordinates.

        Args:
            agent_id: Optional specific agent to update

        Returns:
            Result dictionary with success/error information
        """
        try:
            from pynput import mouse

            print("Hover over CHAT location and press ENTER...")

            current_coords = [0, 0]

            def on_mouse_move(x, y):
                nonlocal current_coords
                current_coords = [x, y]

            listener = mouse.Listener(on_move=on_mouse_move)
            listener.start()

            try:
                input()
                chat_coords = current_coords.copy()
                print(f"Chat: {chat_coords}")

                if agent_id:
                    result = self.update_chat_coordinates(agent_id, chat_coords)
                else:
                    result = self.update_all_chat_coordinates(chat_coords)
                return result

            except KeyboardInterrupt:
                return {"error": "Capture cancelled"}
            finally:
                listener.stop()

        except ImportError:
            return {"error": "Install pynput: pip install pynput"}
        except Exception as e:
            return {"error": str(e)}

    def update_onboarding_coordinates(self, agent_id: str, onboarding_coords: List[int]) -> Dict[str, Any]:
        """Update only onboarding coordinates for a specific agent.

        Args:
            agent_id: The agent identifier
            onboarding_coords: [x, y] coordinates for onboarding input

        Returns:
            Result dictionary with success/error information
        """
        try:
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            if agent_id not in coords_data.get('agents', {}):
                return {"error": f"Agent {agent_id} not found"}

            # Update onboarding coordinates
            coords_data['agents'][agent_id]['onboarding_input_coords'] = onboarding_coords
            coords_data['last_updated'] = datetime.now().isoformat()

            if self.utils.write_json(coords_file, coords_data):
                return {
                    "success": True,
                    "agent_id": agent_id,
                    "onboarding_coords": onboarding_coords,
                    "message": f"Updated onboarding coordinates for {agent_id}"
                }
            else:
                return {"error": "Failed to save coordinates"}

        except Exception as e:
            logger.error(f"Error updating onboarding coordinates: {e}")
            return {"error": str(e)}

    def update_chat_coordinates(self, agent_id: str, chat_coords: List[int]) -> Dict[str, Any]:
        """Update only chat coordinates for a specific agent.

        Args:
            agent_id: The agent identifier
            chat_coords: [x, y] coordinates for chat input

        Returns:
            Result dictionary with success/error information
        """
        try:
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            if agent_id not in coords_data.get('agents', {}):
                return {"error": f"Agent {agent_id} not found"}

            # Update chat coordinates
            coords_data['agents'][agent_id]['chat_input_coordinates'] = chat_coords
            coords_data['last_updated'] = datetime.now().isoformat()

            if self.utils.write_json(coords_file, coords_data):
                return {
                    "success": True,
                    "agent_id": agent_id,
                    "chat_coords": chat_coords,
                    "message": f"Updated chat coordinates for {agent_id}"
                }
            else:
                return {"error": "Failed to save coordinates"}

        except Exception as e:
            logger.error(f"Error updating chat coordinates: {e}")
            return {"error": str(e)}

    def update_all_onboarding_coordinates(self, onboarding_coords: List[int]) -> Dict[str, Any]:
        """Update onboarding coordinates for all agents.

        Args:
            onboarding_coords: [x, y] coordinates for onboarding input

        Returns:
            Result dictionary with success/error information
        """
        try:
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            agents = coords_data.get('agents', {})
            updated_count = 0

            # Update onboarding coordinates for all agents
            for agent_id in agents:
                agents[agent_id]['onboarding_input_coords'] = onboarding_coords
                updated_count += 1

            coords_data['last_updated'] = datetime.now().isoformat()

            if self.utils.write_json(coords_file, coords_data):
                return {
                    "success": True,
                    "agents_updated": updated_count,
                    "onboarding_coords": onboarding_coords,
                    "message": f"Updated onboarding coordinates for all {updated_count} agents"
                }
            else:
                return {"error": "Failed to save coordinates"}

        except Exception as e:
            logger.error(f"Error updating all onboarding coordinates: {e}")
            return {"error": str(e)}

    def update_all_chat_coordinates(self, chat_coords: List[int]) -> Dict[str, Any]:
        """Update chat coordinates for all agents.

        Args:
            chat_coords: [x, y] coordinates for chat input

        Returns:
            Result dictionary with success/error information
        """
        try:
            coords_file = "cursor_agent_coords.json"
            coords_data = self.utils.read_json(coords_file)

            if not coords_data:
                return {"error": "Could not load coordinates file"}

            agents = coords_data.get('agents', {})
            updated_count = 0

            # Update chat coordinates for all agents
            for agent_id in agents:
                agents[agent_id]['chat_input_coordinates'] = chat_coords
                updated_count += 1

            coords_data['last_updated'] = datetime.now().isoformat()

            if self.utils.write_json(coords_file, coords_data):
                return {
                    "success": True,
                    "agents_updated": updated_count,
                    "chat_coords": chat_coords,
                    "message": f"Updated chat coordinates for all {updated_count} agents"
                }
            else:
                return {"error": "Failed to save coordinates"}

        except Exception as e:
            logger.error(f"Error updating all chat coordinates: {e}")
            return {"error": str(e)}

    def get_chat_input_xy(self, agent_id: str) -> Tuple[int, int]:
        """Get chat input coordinates for an agent.

        Args:
            agent_id: The agent identifier

        Returns:
            Tuple of (x, y) coordinates
        """
        coords_file = "cursor_agent_coords.json"
        coords_data = self.utils.read_json(coords_file)

        if coords_data and agent_id in coords_data.get('agents', {}):
            coords = coords_data['agents'][agent_id].get('chat_input_coordinates', [0, 0])
            return tuple(coords)

        return (0, 0)

    def get_onboarding_input_xy(self, agent_id: str) -> Tuple[int, int]:
        """Get onboarding input coordinates for an agent.

        Args:
            agent_id: The agent identifier

        Returns:
            Tuple of (x, y) coordinates
        """
        coords_file = "cursor_agent_coords.json"
        coords_data = self.utils.read_json(coords_file)

        if coords_data and agent_id in coords_data.get('agents', {}):
            coords = coords_data['agents'][agent_id].get('onboarding_input_coords', [0, 0])
            return tuple(coords)

        return (0, 0)
