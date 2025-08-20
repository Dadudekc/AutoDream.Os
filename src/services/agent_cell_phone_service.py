#!/usr/bin/env python3
"""
Agent Cell Phone Service - Agent Cellphone V2
=============================================

Agent coordination service with strict OOP design and CLI testing interface.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AgentCellPhoneService:
    """
    Agent Cell Phone Service - Single responsibility: Agent coordination and communication.
    
    This service manages agent coordination including:
    - Agent initialization
    - Message routing
    - Coordinate management
    - Agent status tracking
    """
    
    def __init__(self, config_path: str = "config"):
        """Initialize Agent Cell Phone Service with configuration path."""
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()
        self.agents = {}
        self.coordinates = self._load_coordinates()
        self.modes = self._load_modes()
        self.status = "initialized"
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("AgentCellPhoneService")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_coordinates(self) -> Dict:
        """Load agent coordinates from configuration."""
        coords_file = self.config_path / "cursor_agent_coords.json"
        
        try:
            if coords_file.exists():
                with open(coords_file, 'r') as f:
                    coords = json.load(f)
                    self.logger.info("Agent coordinates loaded successfully")
                    return coords
            else:
                self.logger.warning("Coordinates file not found")
                return {}
        except Exception as e:
            self.logger.error(f"Failed to load coordinates: {e}")
            return {}
    
    def _load_modes(self) -> Dict:
        """Load runtime modes from configuration."""
        modes_file = self.config_path / "modes_runtime.json"
        
        try:
            if modes_file.exists():
                with open(modes_file, 'r') as f:
                    modes = json.load(f)
                    self.logger.info("Runtime modes loaded successfully")
                    return modes
            else:
                self.logger.warning("Modes file not found")
                return {}
        except Exception as e:
            self.logger.error(f"Failed to load modes: {e}")
            return {}
    
    def initialize_agent(self, agent_id: str, layout_mode: str = "5-agent") -> bool:
        """Initialize an agent with specified layout mode."""
        try:
            if layout_mode not in self.coordinates:
                self.logger.error(f"Layout mode '{layout_mode}' not found")
                return False
            
            if agent_id not in self.coordinates[layout_mode]:
                self.logger.error(f"Agent '{agent_id}' not found in layout '{layout_mode}'")
                return False
            
            # Initialize agent
            self.agents[agent_id] = {
                "id": agent_id,
                "layout_mode": layout_mode,
                "coordinates": self.coordinates[layout_mode][agent_id],
                "status": "active",
                "messages": []
            }
            
            self.logger.info(f"Agent '{agent_id}' initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Agent initialization failed: {e}")
            return False
    
    def send_message(self, from_agent: str, to_agent: str, message: str, tag: str = "TASK") -> bool:
        """Send a message from one agent to another."""
        try:
            if from_agent not in self.agents:
                self.logger.error(f"From agent '{from_agent}' not initialized")
                return False
            
            if to_agent not in self.agents and to_agent != "all":
                self.logger.error(f"To agent '{to_agent}' not initialized")
                return False
            
            # Create message
            msg = {
                "from": from_agent,
                "to": to_agent,
                "message": message,
                "tag": tag,
                "timestamp": self._get_timestamp()
            }
            
            # Add to sender's message list
            self.agents[from_agent]["messages"].append(msg)
            
            # Add to receiver's message list if not "all"
            if to_agent != "all":
                self.agents[to_agent]["messages"].append(msg)
            
            self.logger.info(f"Message sent from '{from_agent}' to '{to_agent}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Message sending failed: {e}")
            return False
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get status of a specific agent."""
        return self.agents.get(agent_id)
    
    def get_all_agents_status(self) -> Dict:
        """Get status of all agents."""
        return {
            agent_id: {
                "id": agent["id"],
                "layout_mode": agent["layout_mode"],
                "status": agent["status"],
                "message_count": len(agent["messages"])
            }
            for agent_id, agent in self.agents.items()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def shutdown_service(self) -> bool:
        """Shutdown the service."""
        try:
            self.logger.info("Shutting down Agent Cell Phone Service...")
            self.status = "shutdown"
            self.agents.clear()
            self.logger.info("Service shutdown complete")
            return True
        except Exception as e:
            self.logger.error(f"Service shutdown failed: {e}")
            return False


def main():
    """CLI interface for Agent Cell Phone Service testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Cell Phone Service Testing Interface")
    parser.add_argument("--init", action="store_true", help="Initialize service")
    parser.add_argument("--agent", type=str, help="Initialize specific agent")
    parser.add_argument("--layout", type=str, default="5-agent", help="Layout mode for agent")
    parser.add_argument("--send", nargs=3, metavar=("FROM", "TO", "MESSAGE"), help="Send message between agents")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument("--test", action="store_true", help="Run service tests")
    
    args = parser.parse_args()
    
    # Create service instance
    service = AgentCellPhoneService()
    
    if args.init or not any([args.init, args.agent, args.send, args.status, args.test]):
        print("📱 Agent Cell Phone Service - Agent Cellphone V2")
        print("Service initialized successfully")
    
    if args.agent:
        success = service.initialize_agent(args.agent, args.layout)
        print(f"Agent '{args.agent}' initialization: {'✅ Success' if success else '❌ Failed'}")
    
    if args.send:
        from_agent, to_agent, message = args.send
        success = service.send_message(from_agent, to_agent, message)
        print(f"Message sending: {'✅ Success' if success else '❌ Failed'}")
    
    if args.status:
        print("📊 Service Status:")
        print(f"  Status: {service.status}")
        print(f"  Agents: {len(service.agents)}")
        print(f"  Coordinates loaded: {bool(service.coordinates)}")
        print(f"  Modes loaded: {bool(service.modes)}")
        
        if service.agents:
            print("\nAgent Status:")
            for agent_id, agent in service.agents.items():
                print(f"  {agent_id}: {agent['status']} ({len(agent['messages'])} messages)")
    
    if args.test:
        print("🧪 Running service tests...")
        try:
            # Test agent initialization
            success = service.initialize_agent("Agent-1", "5-agent")
            print(f"Agent initialization test: {'✅ Success' if success else '❌ Failed'}")
            
            # Test message sending
            if success:
                success = service.send_message("Agent-1", "Agent-2", "Test message", "TEST")
                print(f"Message sending test: {'✅ Success' if success else '❌ Failed'}")
            
        except Exception as e:
            print(f"❌ Service test failed: {e}")


if __name__ == "__main__":
    main()
