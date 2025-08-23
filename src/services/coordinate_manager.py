#!/usr/bin/env python3
"""
Coordinate Manager for V2 Message Delivery Service
Handles agent coordinate loading, validation, and management
"""

import logging
import json
import os
import time
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class CoordinateManager:
    """Manages agent input coordinates for message delivery"""

    def __init__(self):
        self.agent_coordinates = {}
        self._initialize_agent_coordinates()

    def _initialize_agent_coordinates(self):
        """Initialize agent input coordinates from available sources"""
        try:
            logger.info("📍 Initializing agent input coordinates...")

            # Try to load from the actual coordinate files
            repo_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )

            # Preferred sources (in order)
            cursor_repo_path = os.path.join(
                repo_root,
                "Agent_Cellphone_V2_Repository",
                "config",
                "cursor_agent_coords.json",
            )
            cursor_runtime_path = os.path.join(
                repo_root, "runtime", "agent_comms", "cursor_agent_coords.json"
            )
            v2_locations_path = os.path.join(repo_root, "agent_complete_locations.json")

            loaded = (
                self._load_cursor_coords(cursor_repo_path)
                or self._load_cursor_coords(cursor_runtime_path)
                or self._load_v2_locations(v2_locations_path)
            )

            if not loaded:
                logger.warning(
                    "⚠️ No coordinate sources found, using placeholder coordinates"
                )
                self._initialize_placeholder_coordinates()

            logger.info(
                f"✅ Agent coordinates initialized for {len(self.agent_coordinates)} agents"
            )

        except Exception as e:
            logger.error(f"❌ Error initializing agent coordinates: {e}")
            self._initialize_placeholder_coordinates()

    def _load_cursor_coords(self, path: str) -> bool:
        """Load coordinates from cursor coordinate files"""
        if not os.path.exists(path):
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            layout = data.get("8-agent") or data.get("5-agent") or {}
            if not layout:
                return False

            self.agent_coordinates = {}
            for i in range(1, 9):
                key = f"Agent-{i}"
                info = layout.get(key)
                if not info:
                    continue
                
                box = info.get("input_box") or {}
                input_x = box.get("x")
                input_y = box.get("y")
                
                if input_x is None or input_y is None:
                    continue
                
                normalized_id = f"agent_{i}"
                self.agent_coordinates[normalized_id] = {
                    "input_x": int(input_x),
                    "input_y": int(input_y),
                    "status": "active",
                    "last_delivery": time.time(),
                    "name": key,
                    "color": "",
                }

            if self.agent_coordinates:
                logger.info(f"✅ Loaded agent coordinates from cursor coords: {path}")
                return True
            return False

        except Exception as e:
            logger.warning(f"⚠️ Error loading cursor coordinates from {path}: {e}")
            return False

    def _load_v2_locations(self, path: str) -> bool:
        """Load coordinates from V2 locations file"""
        if not os.path.exists(path):
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                agent_locations = json.load(f)
            
            self.agent_coordinates = {}
            for agent_id, agent_info in agent_locations.items():
                normalized_id = agent_id.lower().replace("-", "_")
                input_x, input_y = agent_info["input_location"]
                
                self.agent_coordinates[normalized_id] = {
                    "input_x": int(input_x),
                    "input_y": int(input_y),
                    "status": "active",
                    "last_delivery": time.time(),
                    "name": agent_info.get("name", agent_id),
                    "color": agent_info.get("color", ""),
                }

            if self.agent_coordinates:
                logger.info(f"✅ Loaded agent coordinates from V2 locations: {path}")
                return True
            return False

        except Exception as e:
            logger.warning(f"⚠️ Error loading V2 locations from {path}: {e}")
            return False

    def _initialize_placeholder_coordinates(self):
        """Initialize placeholder coordinates as fallback"""
        self.agent_coordinates = {
            "agent_1": {
                "input_x": 500,
                "input_y": 300,
                "status": "active",
                "last_delivery": time.time(),
                "name": "Foundation & Testing",
                "color": "🟢",
            },
            "agent_2": {
                "input_x": 600,
                "input_y": 300,
                "status": "active",
                "last_delivery": time.time(),
                "name": "AI & ML Integration",
                "color": "🔵",
            },
            "agent_3": {
                "input_x": 700,
                "input_y": 300,
                "status": "active",
                "last_delivery": time.time(),
                "name": "Multimedia & Content",
                "color": "🟡",
            },
            "agent_4": {
                "input_x": 800,
                "input_y": 300,
                "status": "active",
                "last_delivery": time.time(),
                "name": "Security & Infrastructure",
                "color": "🔴",
            },
            "agent_5": {
                "input_x": 500,
                "input_y": 400,
                "status": "active",
                "last_delivery": time.time(),
                "name": "Business Intelligence",
                "color": "🟣",
            },
            "agent_6": {
                "input_x": 600,
                "input_y": 400,
                "status": "active",
                "last_delivery": time.time(),
                "name": "Gaming & Entertainment",
                "color": "⚪",
            },
            "agent_7": {
                "input_x": 700,
                "input_y": 400,
                "status": "active",
                "last_delivery": time.time(),
                "name": "Web Development",
                "color": "⚫",
            },
            "agent_8": {
                "input_x": 800,
                "input_y": 400,
                "status": "active",
                "last_delivery": time.time(),
                "name": "Integration & Performance",
                "color": "⚪",
            },
        }

    def get_agent_coordinates(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get coordinates for a specific agent"""
        return self.agent_coordinates.get(agent_id)

    def get_all_coordinates(self) -> Dict[str, Any]:
        """Get all agent coordinates"""
        return self.agent_coordinates.copy()

    def update_agent_coordinates(
        self, agent_id: str, input_x: int, input_y: int
    ) -> bool:
        """Update agent input coordinates"""
        try:
            if agent_id in self.agent_coordinates:
                self.agent_coordinates[agent_id]["input_x"] = input_x
                self.agent_coordinates[agent_id]["input_y"] = input_y
                logger.info(
                    f"📍 Updated coordinates for {agent_id}: ({input_x}, {input_y})"
                )
                return True
            else:
                logger.warning(f"⚠️ Agent {agent_id} not found in coordinates")
                return False

        except Exception as e:
            logger.error(f"❌ Error updating coordinates: {e}")
            return False

    def update_delivery_timestamp(self, agent_id: str):
        """Update last delivery timestamp for an agent"""
        if agent_id in self.agent_coordinates:
            self.agent_coordinates[agent_id]["last_delivery"] = time.time()

    def get_agent_count(self) -> int:
        """Get total number of agents"""
        return len(self.agent_coordinates)

    def is_agent_active(self, agent_id: str) -> bool:
        """Check if an agent is active"""
        agent_info = self.agent_coordinates.get(agent_id)
        return agent_info is not None and agent_info.get("status") == "active"

