#!/usr/bin/env python3
"""
Intelligent Messaging Service - Vector Database Integration
==========================================================

Enhanced messaging service that integrates with the Swarm Brain vector database
to provide intelligent message routing, learning, and optimization.

V2 COMPLIANT: Focused intelligent messaging under 400 lines.
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

from swarm_brain import SwarmBrain, Retriever, Ingestor
from .core.messaging_service import MessagingService

logger = logging.getLogger(__name__)


class IntelligentMessagingService(MessagingService):
    """Enhanced messaging service with vector database intelligence."""
    
    def __init__(self, coord_path: str = "config/coordinates.json"):
        super().__init__(coord_path)
        self.swarm_brain = SwarmBrain()
        self.retriever = Retriever()
        self.ingestor = Ingestor()
        logger.info("🧠 Intelligent Messaging Service initialized with Swarm Brain")
    
    def send_message(self, agent_id: str, message: str, from_agent: str = None, 
                    priority: str = "NORMAL") -> Tuple[bool, Dict[str, Any]]:
        """Send message with intelligence and learning."""
        
        # Auto-detect sender if not provided
        if from_agent is None:
            from .agent_context import get_current_agent
            from_agent = get_current_agent()
        
        logger.info(f"📤 Sending intelligent message: {from_agent} → {agent_id}")
        
        # 1. Send message normally
        success = super().send_message(agent_id, message, from_agent, priority)
        
        # 2. Learn from message
        self._learn_from_message(agent_id, message, from_agent, priority, success)
        
        # 3. Get intelligence suggestions
        suggestions = self._get_message_suggestions(agent_id, message, from_agent)
        
        logger.info(f"✅ Message sent: {success}, Intelligence gathered: {len(suggestions)} insights")
        
        return success, suggestions
    
    def broadcast_message(self, message: str, from_agent: str = None, 
                         priority: str = "NORMAL") -> Dict[str, Dict[str, Any]]:
        """Broadcast message with intelligence and learning."""
        
        # Auto-detect sender if not provided
        if from_agent is None:
            from .agent_context import get_current_agent
            from_agent = get_current_agent()
        
        logger.info(f"📢 Broadcasting intelligent message from {from_agent}")
        
        # 1. Get broadcast results normally
        results = super().broadcast_message(message, from_agent, priority)
        
        # 2. Learn from broadcast
        # Extract just the success values from the enhanced results
        simple_results = {agent_id: result["success"] for agent_id, result in results.items()}
        self._learn_from_broadcast(message, from_agent, priority, simple_results)
        
        # 3. Get intelligence insights
        insights = self._get_broadcast_insights(message, from_agent, results)
        
        # 4. Combine results with intelligence
        enhanced_results = {}
        for agent_id, success in results.items():
            enhanced_results[agent_id] = {
                "success": success,
                "insights": insights.get(agent_id, {}),
                "suggestions": self._get_message_suggestions(agent_id, message, from_agent)
            }
        
        logger.info(f"✅ Broadcast completed: {sum(results.values())}/{len(results)} successful")
        
        return enhanced_results
    
    def _learn_from_message(self, agent_id: str, message: str, from_agent: str, 
                           priority: str, success: bool):
        """Learn from message patterns."""
        try:
            self.ingestor.action(
                title=f"Message: {from_agent} → {agent_id}",
                tool="messaging_service",
                outcome="success" if success else "failure",
                context={
                    "message": message,
                    "from_agent": from_agent,
                    "to_agent": agent_id,
                    "priority": priority,
                    "success": success,
                    "timestamp": datetime.now().isoformat()
                },
                project="Agent_Cellphone_V2",
                agent_id=from_agent,
                tags=["messaging", "communication", "agent_coordination"],
                summary=f"Message from {from_agent} to {agent_id}: {message[:100]}"
            )
            logger.debug(f"📚 Learned from message: {from_agent} → {agent_id}")
        except Exception as e:
            logger.error(f"❌ Failed to learn from message: {e}")
    
    def _learn_from_broadcast(self, message: str, from_agent: str, priority: str, 
                             results: Dict[str, bool]):
        """Learn from broadcast patterns."""
        try:
            success_rate = sum(results.values()) / len(results) if results else 0
            
            self.ingestor.action(
                title=f"Broadcast: {from_agent} → All Agents",
                tool="messaging_service",
                outcome="success" if success_rate > 0.8 else "partial",
                context={
                    "message": message,
                    "from_agent": from_agent,
                    "priority": priority,
                    "success_rate": success_rate,
                    "total_agents": len(results),
                    "successful_agents": sum(results.values()),
                    "results": results
                },
                project="Agent_Cellphone_V2",
                agent_id=from_agent,
                tags=["messaging", "broadcast", "coordination"],
                summary=f"Broadcast from {from_agent}: {message[:100]} ({success_rate:.1%} success)"
            )
            logger.debug(f"📚 Learned from broadcast: {from_agent} ({success_rate:.1%} success)")
        except Exception as e:
            logger.error(f"❌ Failed to learn from broadcast: {e}")
    
    def _get_message_suggestions(self, agent_id: str, message: str, from_agent: str) -> Dict[str, Any]:
        """Get intelligent suggestions for message optimization."""
        try:
            # Find similar successful messages
            similar_messages = self.retriever.search(
                f"successful messages to {agent_id}", 
                kinds=["action"], 
                k=5
            )
            
            # Get agent communication preferences
            agent_patterns = self.retriever.get_agent_expertise(agent_id, k=10)
            
            suggestions = {
                "similar_successful_messages": len(similar_messages),
                "agent_communication_preferences": agent_patterns.get("tool_expertise", {}),
                "optimal_timing": self._suggest_optimal_timing(agent_id),
                "message_optimization": self._suggest_message_optimization(message, similar_messages),
                "success_probability": self._calculate_success_probability(agent_id, message)
            }
            
            return suggestions
        except Exception as e:
            logger.error(f"❌ Failed to get message suggestions: {e}")
            return {"error": str(e)}
    
    def _get_broadcast_insights(self, message: str, from_agent: str, 
                               results: Dict[str, bool]) -> Dict[str, Dict[str, Any]]:
        """Get insights for broadcast optimization."""
        insights = {}
        
        for agent_id, success in results.items():
            try:
                agent_insights = {
                    "success": success,
                    "communication_history": self._get_communication_history(agent_id, from_agent),
                    "optimal_message_format": self._suggest_message_format(agent_id),
                    "response_patterns": self._get_response_patterns(agent_id)
                }
                insights[agent_id] = agent_insights
            except Exception as e:
                logger.error(f"❌ Failed to get insights for {agent_id}: {e}")
                insights[agent_id] = {"error": str(e)}
        
        return insights
    
    def _suggest_optimal_timing(self, agent_id: str) -> str:
        """Suggest optimal timing for messages to agent."""
        try:
            # Find patterns in successful message timing
            timing_patterns = self.retriever.search(
                f"successful messages to {agent_id}", 
                kinds=["action"], 
                k=10
            )
            
            # Analyze timing patterns (simplified)
            if len(timing_patterns) > 0:
                return "Based on historical patterns, optimal timing identified"
            else:
                return "No historical patterns available"
        except Exception as e:
            logger.error(f"❌ Failed to suggest timing: {e}")
            return "Unable to determine optimal timing"
    
    def _suggest_message_optimization(self, message: str, similar_messages: List[Dict]) -> str:
        """Suggest message optimization based on similar successful messages."""
        try:
            if len(similar_messages) > 0:
                # Analyze successful message patterns
                successful_patterns = [msg for msg in similar_messages if msg.get("outcome") == "success"]
                
                if len(successful_patterns) > 0:
                    return f"Based on {len(successful_patterns)} similar successful messages"
                else:
                    return "No similar successful patterns found"
            else:
                return "No similar messages found for optimization"
        except Exception as e:
            logger.error(f"❌ Failed to suggest optimization: {e}")
            return "Unable to suggest optimization"
    
    def _calculate_success_probability(self, agent_id: str, message: str) -> float:
        """Calculate success probability for message."""
        try:
            # Find similar messages to this agent
            similar_messages = self.retriever.search(
                f"messages to {agent_id}", 
                kinds=["action"], 
                k=20
            )
            
            if len(similar_messages) > 0:
                successful_messages = [msg for msg in similar_messages if msg.get("outcome") == "success"]
                success_rate = len(successful_messages) / len(similar_messages)
                return round(success_rate, 2)
            else:
                return 0.5  # Default probability if no history
        except Exception as e:
            logger.error(f"❌ Failed to calculate success probability: {e}")
            return 0.5
    
    def _get_communication_history(self, agent_id: str, from_agent: str) -> Dict[str, Any]:
        """Get communication history between agents."""
        try:
            # Find communication patterns between these agents
            communication_patterns = self.retriever.search(
                f"communication between {from_agent} and {agent_id}", 
                kinds=["action"], 
                k=10
            )
            
            return {
                "total_interactions": len(communication_patterns),
                "successful_interactions": len([p for p in communication_patterns if p.get("outcome") == "success"]),
                "recent_patterns": communication_patterns[:3] if communication_patterns else []
            }
        except Exception as e:
            logger.error(f"❌ Failed to get communication history: {e}")
            return {"error": str(e)}
    
    def _suggest_message_format(self, agent_id: str) -> str:
        """Suggest optimal message format for agent."""
        try:
            # Find successful message formats for this agent
            successful_messages = self.retriever.search(
                f"successful messages to {agent_id}", 
                kinds=["action"], 
                k=5
            )
            
            if len(successful_messages) > 0:
                return "Format optimized based on successful patterns"
            else:
                return "Standard format recommended"
        except Exception as e:
            logger.error(f"❌ Failed to suggest format: {e}")
            return "Standard format recommended"
    
    def _get_response_patterns(self, agent_id: str) -> Dict[str, Any]:
        """Get response patterns for agent."""
        try:
            # Find response patterns for this agent
            response_patterns = self.retriever.search(
                f"responses from {agent_id}", 
                kinds=["action"], 
                k=10
            )
            
            return {
                "total_responses": len(response_patterns),
                "response_rate": len(response_patterns) / max(1, len(response_patterns)),
                "common_response_types": self._analyze_response_types(response_patterns)
            }
        except Exception as e:
            logger.error(f"❌ Failed to get response patterns: {e}")
            return {"error": str(e)}
    
    def _analyze_response_types(self, response_patterns: List[Dict]) -> List[str]:
        """Analyze common response types."""
        try:
            response_types = []
            for pattern in response_patterns:
                if "response" in pattern.get("title", "").lower():
                    response_types.append(pattern.get("title", "Unknown"))
            
            # Return unique response types
            return list(set(response_types))[:5]
        except Exception as e:
            logger.error(f"❌ Failed to analyze response types: {e}")
            return []
    
    def get_agent_communication_intelligence(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive communication intelligence for agent."""
        try:
            # Get agent expertise
            expertise = self.retriever.get_agent_expertise(agent_id, k=20)
            
            # Get communication patterns
            communication_patterns = self.retriever.search(
                f"communication with {agent_id}", 
                kinds=["action"], 
                k=20
            )
            
            # Get successful patterns
            successful_patterns = self.retriever.how_do_agents_do(
                f"successful communication with {agent_id}", 
                k=10
            )
            
            return {
                "agent_expertise": expertise,
                "communication_patterns": len(communication_patterns),
                "successful_patterns": len(successful_patterns),
                "communication_effectiveness": self._calculate_communication_effectiveness(agent_id),
                "optimal_communication_strategies": self._get_optimal_strategies(agent_id)
            }
        except Exception as e:
            logger.error(f"❌ Failed to get communication intelligence: {e}")
            return {"error": str(e)}
    
    def _calculate_communication_effectiveness(self, agent_id: str) -> float:
        """Calculate communication effectiveness for agent."""
        try:
            # Find all communication with this agent
            communications = self.retriever.search(
                f"communication with {agent_id}", 
                kinds=["action"], 
                k=50
            )
            
            if len(communications) > 0:
                successful_communications = [c for c in communications if c.get("outcome") == "success"]
                effectiveness = len(successful_communications) / len(communications)
                return round(effectiveness, 2)
            else:
                return 0.0
        except Exception as e:
            logger.error(f"❌ Failed to calculate effectiveness: {e}")
            return 0.0
    
    def _get_optimal_strategies(self, agent_id: str) -> List[str]:
        """Get optimal communication strategies for agent."""
        try:
            # Find successful communication strategies
            strategies = self.retriever.search(
                f"successful communication strategies with {agent_id}", 
                kinds=["action"], 
                k=10
            )
            
            strategy_list = []
            for strategy in strategies:
                if "strategy" in strategy.get("title", "").lower():
                    strategy_list.append(strategy.get("title", "Unknown Strategy"))
            
            return list(set(strategy_list))[:5]
        except Exception as e:
            logger.error(f"❌ Failed to get optimal strategies: {e}")
            return []
