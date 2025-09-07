"""
Prompt Loader for Messaging System
Loads onboarding prompts from external files instead of hardcoded strings
"""

import json
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PromptLoader:
    """Loads prompts from external files for the messaging system"""
    
    def __init__(self, prompts_base_path: str = "prompts"):
        self.prompts_base_path = Path(prompts_base_path)
        self.role_mapping_path = self.prompts_base_path / "agents" / "role_mapping.json"
        self.captain_prompt_path = self.prompts_base_path / "captain" / "onboarding.md"
        self.agent_prompt_path = self.prompts_base_path / "agents" / "onboarding.md"
        
        # Load role mappings
        self.role_mappings = self._load_role_mappings()
    
    def _load_role_mappings(self) -> Dict[str, str]:
        """Load agent role mappings from JSON file"""
        try:
            if self.role_mapping_path.exists():
                with open(self.role_mapping_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("agent_roles", {})
            else:
                logger.warning(f"Role mapping file not found: {self.role_mapping_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading role mappings: {e}")
            return {}
    
    def get_agent_role(self, agent_number: int) -> str:
        """Get role for a specific agent number"""
        return self.role_mappings.get(str(agent_number), "SYSTEM AGENT")
    
    def load_captain_onboarding(self, agent_id: str, custom_message: str = None) -> str:
        """Load captain onboarding prompt from file"""
        try:
            if self.captain_prompt_path.exists():
                with open(self.captain_prompt_path, 'r', encoding='utf-8') as f:
                    prompt_template = f.read()
                
                # Replace placeholders
                prompt = prompt_template.format(agent_id=agent_id)
                
                if custom_message:
                    prompt = prompt.replace("{custom_message}", custom_message)
                else:
                    prompt = prompt.replace("## 📝 **ADDITIONAL INSTRUCTIONS:** {custom_message}", "")
                
                return prompt
            else:
                logger.warning(f"Captain prompt file not found: {self.captain_prompt_path}")
                return self._get_fallback_captain_prompt(agent_id, custom_message)
                
        except Exception as e:
            logger.error(f"Error loading captain prompt: {e}")
            return self._get_fallback_captain_prompt(agent_id, custom_message)
    
    def load_agent_onboarding(self, agent_id: str, agent_number: int, contract_info: str = "", custom_message: str = None) -> str:
        """Load agent onboarding prompt from file"""
        try:
            if self.agent_prompt_path.exists():
                with open(self.agent_prompt_path, 'r', encoding='utf-8') as f:
                    prompt_template = f.read()
                
                # Get role for this agent
                role = self.get_agent_role(agent_number)
                
                # Replace placeholders
                prompt = prompt_template.format(
                    agent_id=agent_id,
                    role=role,
                    contract_info=contract_info
                )
                
                if custom_message:
                    prompt = prompt.replace("{custom_message}", custom_message)
                else:
                    prompt = prompt.replace("## 📝 **ADDITIONAL INSTRUCTIONS:** {custom_message}", "")
                
                return prompt
            else:
                logger.warning(f"Agent prompt file not found: {self.agent_prompt_path}")
                return self._get_fallback_agent_prompt(agent_id, agent_number, contract_info, custom_message)
                
        except Exception as e:
            logger.error(f"Error loading agent prompt: {e}")
            return self._get_fallback_agent_prompt(agent_id, agent_number, contract_info, custom_message)
    
    def _get_fallback_captain_prompt(self, agent_id: str, custom_message: str = None) -> str:
        """Fallback captain prompt if file loading fails"""
        base_message = f"""🚨 **CAPTAIN IDENTITY CONFIRMATION: You are {agent_id} - THE CAPTAIN!** 🚨

🎯 **YOUR ROLE:** Strategic Oversight & Emergency Intervention Manager
📋 **PRIMARY RESPONSIBILITIES:**
1. **Create and assign tasks** to all agents
2. **Monitor agent status.json files** for stall detection
3. **Respond to messages in your inbox** at: agent_workspaces/{agent_id}/inbox/
4. **Coordinate system-wide operations** and maintain momentum
5. **Implement stall prevention** when agents exceed 1 agent cycle response time
6. **Maintain 8x agent efficiency** through prompt frequency
7. **Ensure cycle continuity** with no gaps between prompts

📁 **YOUR WORKSPACE:** agent_workspaces/{agent_id}/
📊 **STATUS TRACKING:** Update your status.json with timestamp every time you act
⏰ **STALL DETECTION:** Monitor all agents for 1+ agent cycle inactivity

🚨 **IMMEDIATE ACTIONS REQUIRED:**
1. **Check your inbox** for any pending messages
2. **Update your status.json** with current timestamp
3. **Create next round of tasks** for agents
4. **Begin system oversight** and momentum maintenance

🎯 **SUCCESS CRITERIA:** All agents actively working, system momentum maintained, stall prevention active

Captain {agent_id} - You are the strategic leader of this operation!"""
        
        if custom_message:
            base_message += f"\n\n📝 **ADDITIONAL INSTRUCTIONS:** {custom_message}"
        
        return base_message
    
    def _get_fallback_agent_prompt(self, agent_id: str, agent_number: int, contract_info: str = "", custom_message: str = None) -> str:
        """Fallback agent prompt if file loading fails"""
        role = self.get_agent_role(agent_number)
        
        base_message = f"""🚨 **AGENT IDENTITY CONFIRMATION: You are {agent_id} - {role}** 🚨

🎯 **YOUR ROLE:** {role}
📋 **PRIMARY RESPONSIBILITIES:**
1. **Accept assigned tasks** using --get-next-task flag
2. **Update your status.json** with timestamp every time you act
3. **Check your inbox** for messages at: agent_workspaces/{agent_id}/inbox/
4. **Respond to all inbox messages** from other agents
5. **Maintain continuous workflow** - never stop working
6. **Report progress** using --captain flag regularly

📁 **YOUR WORKSPACE:** agent_workspaces/{agent_id}/
📊 **STATUS UPDATES:** Must update status.json with timestamp every Captain prompt cycle
⏰ **CHECK-IN FREQUENCY:** Every time you are prompted or complete a task

🚨 **IMMEDIATE ACTIONS REQUIRED:**
1. **Check your inbox** for any pending messages
2. **Update your status.json** with current timestamp
3. **Accept your assigned task** using --get-next-task flag
4. **Begin working immediately** on your assigned responsibilities

🎯 **SUCCESS CRITERIA:** Active task completion, regular status updates, inbox responsiveness, continuous workflow

{agent_id} - You are a critical component of this system! Maintain momentum!"""
        
        if contract_info:
            base_message += f"\n\n📋 **ASSIGNED CONTRACT:** {contract_info}"
        
        if custom_message:
            base_message += f"\n\n📝 **ADDITIONAL INSTRUCTIONS:** {custom_message}"
        
        return base_message
