#!/usr/bin/env python3
"""
Onboarding Orchestrator - Agent Cellphone V2
============================================

Orchestrates the onboarding process for multiple agents.
Follows Single Responsibility Principle with 200 LOC limit.
"""

from typing import Dict, List, Optional
from pathlib import Path
import json
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from .agent_info import AgentInfoManager
from .message_builder import OnboardingMessageBuilder
from .cli_utils import CLIExecutor


class OnboardingOrchestrator:
    """Orchestrates the onboarding process for multiple agents"""
    
    def __init__(self):
        self.agent_info = AgentInfoManager()
        self.message_builder = OnboardingMessageBuilder()
        self.cli_executor = CLIExecutor()
    
    def onboard_agent(self, agent_name: str, style: str = "full", 
                     use_emojis: bool = True) -> bool:
        """
        Onboard a single agent
        
        Args:
            agent_name: Name of the agent to onboard
            style: Message style for onboarding
            use_emojis: Whether to use emoji formatting
            
        Returns:
            True if onboarding was successful, False otherwise
        """
        try:
            # Get agent information
            info = self.agent_info.get_agent_info(agent_name)
            
            # Create onboarding message
            message = self.message_builder.create_comprehensive_message(agent_name, style)
            
            # Send onboarding message via CLI
            cmd_args = [
                "python", "src/agent_cell_phone.py",
                "-a", agent_name,
                "-m", message,
                "-t", "onboarding"
            ]
            
            success = self.cli_executor.run_simple_command(
                cmd_args, 
                f"Onboarding {agent_name} with {style} style"
            )
            
            if success:
                if use_emojis:
                    print(f"✅ Successfully onboarded {agent_name}")
                else:
                    print(f"Successfully onboarded {agent_name}")
                return True
            else:
                if use_emojis:
                    print(f"❌ Failed to onboard {agent_name}")
                else:
                    print(f"Failed to onboard {agent_name}")
                return False
                
        except Exception as e:
            if use_emojis:
                print(f"❌ Exception during {agent_name} onboarding: {e}")
            else:
                print(f"Exception during {agent_name} onboarding: {e}")
            return False
    
    def onboard_all_agents(self, style: str = "full", use_emojis: bool = True) -> Dict[str, bool]:
        """
        Onboard all available agents
        
        Args:
            style: Message style for onboarding
            use_emojis: Whether to use emoji formatting
            
        Returns:
            Dictionary mapping agent names to onboarding success status
        """
        results = {}
        all_agents = self.agent_info.get_all_agents()
        
        if use_emojis:
            print(f"🚀 Starting onboarding for {len(all_agents)} agents...")
        else:
            print(f"Starting onboarding for {len(all_agents)} agents...")
        
        for agent_name in all_agents:
            results[agent_name] = self.onboard_agent(agent_name, style, use_emojis)
        
        return results
    
    def onboard_agent_list(self, agent_names: List[str], style: str = "full",
                          use_emojis: bool = True) -> Dict[str, bool]:
        """
        Onboard a specific list of agents
        
        Args:
            agent_names: List of agent names to onboard
            style: Message style for onboarding
            use_emojis: Whether to use emoji formatting
            
        Returns:
            Dictionary mapping agent names to onboarding success status
        """
        results = {}
        
        if use_emojis:
            print(f"🚀 Starting onboarding for {len(agent_names)} specified agents...")
        else:
            print(f"Starting onboarding for {len(agent_names)} specified agents...")
        
        for agent_name in agent_names:
            if agent_name in self.agent_info.get_all_agents():
                results[agent_name] = self.onboard_agent(agent_name, style, use_emojis)
            else:
                if use_emojis:
                    print(f"⚠️ Agent {agent_name} not found, skipping...")
                else:
                    print(f"Agent {agent_name} not found, skipping...")
                results[agent_name] = False
        
        return results
    
    def print_onboarding_summary(self, results: Dict[str, bool], use_emojis: bool = True):
        """Print a summary of onboarding results"""
        total_agents = len(results)
        successful = sum(1 for success in results.values() if success)
        failed = total_agents - successful
        
        if use_emojis:
            print(f"\n📊 Onboarding Summary:")
            print(f"  Total Agents: {total_agents}")
            print(f"  Successful: {successful}")
            print(f"  Failed: {failed}")
            
            if successful == total_agents:
                print("🎉 All agents onboarded successfully!")
            else:
                print("⚠️ Some agents failed to onboard")
                
                # Show failed agents
                failed_agents = [name for name, success in results.items() if not success]
                if failed_agents:
                    print(f"  Failed agents: {', '.join(failed_agents)}")
        else:
            print(f"\nOnboarding Summary:")
            print(f"  Total Agents: {total_agents}")
            print(f"  Successful: {successful}")
            print(f"  Failed: {failed}")
            
            if successful == total_agents:
                print("All agents onboarded successfully!")
            else:
                print("Some agents failed to onboard")
                
                # Show failed agents
                failed_agents = [name for name, success in results.items() if not success]
                if failed_agents:
                    print(f"  Failed agents: {', '.join(failed_agents)}")
    
    def get_onboarding_status(self) -> Dict[str, Dict]:
        """Get current onboarding status for all agents"""
        status = {}
        all_agents = self.agent_info.get_all_agents()
        
        for agent_name in all_agents:
            # Check if agent has workspace and status
            workspace_path = Path(f"agent_workspaces/{agent_name}")
            status_file = workspace_path / "status.json"
            
            agent_status = {
                "name": agent_name,
                "role": all_agents[agent_name]["role"],
                "workspace_exists": workspace_path.exists(),
                "status_file_exists": status_file.exists(),
                "has_inbox": (workspace_path / "inbox").exists(),
                "has_tasks": (workspace_path / "tasks").exists()
            }
            
            # Try to load status if it exists
            if status_file.exists():
                try:
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    agent_status["current_status"] = status_data.get("status", "unknown")
                    agent_status["last_updated"] = status_data.get("last_updated", "unknown")
                except Exception:
                    agent_status["current_status"] = "error_loading"
                    agent_status["last_updated"] = "unknown"
            else:
                agent_status["current_status"] = "not_onboarded"
                agent_status["last_updated"] = "never"
            
            status[agent_name] = agent_status
        
        return status


def main():
    """CLI interface for testing the Onboarding Orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Onboarding Orchestrator CLI")
    parser.add_argument("--agent", "-a", help="Specific agent to onboard")
    parser.add_argument("--all", action="store_true", help="Onboard all agents")
    parser.add_argument("--list", "-l", nargs="+", help="List of agents to onboard")
    parser.add_argument("--style", "-s", choices=["full", "ascii", "simple"], 
                       default="full", help="Message style")
    parser.add_argument("--no-emojis", action="store_true", help="Disable emoji formatting")
    parser.add_argument("--status", action="store_true", help="Show onboarding status")
    
    args = parser.parse_args()
    
    orchestrator = OnboardingOrchestrator()
    use_emojis = not args.no_emojis
    
    if args.status:
        status = orchestrator.get_onboarding_status()
        print("📊 Onboarding Status:")
        for agent_name, agent_status in status.items():
            emoji = "✅" if agent_status["status_file_exists"] else "❌"
            print(f"  {emoji} {agent_name}: {agent_status['current_status']}")
    
    elif args.agent:
        success = orchestrator.onboard_agent(args.agent, args.style, use_emojis)
        print(f"Onboarding result: {'✅ Success' if success else '❌ Failed'}")
    
    elif args.all:
        results = orchestrator.onboard_all_agents(args.style, use_emojis)
        orchestrator.print_onboarding_summary(results, use_emojis)
    
    elif args.list:
        results = orchestrator.onboard_agent_list(args.list, args.style, use_emojis)
        orchestrator.print_onboarding_summary(results, use_emojis)
    
    else:
        print("Onboarding Orchestrator - Use --help for options")


if __name__ == "__main__":
    main()
