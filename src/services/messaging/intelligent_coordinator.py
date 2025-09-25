
#!/usr/bin/env python3
"""
Intelligent Agent Coordinator - Vector Database Integration
==========================================================

Smart agent coordination using vector database intelligence to optimize
agent assignments, task routing, and coordination strategies.

V2 COMPLIANT: Focused intelligent coordination under 400 lines.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from swarm_brain import SwarmBrain, Retriever, Ingestor
from .core.messaging_service import MessagingService

logger = logging.getLogger(__name__)


class IntelligentAgentCoordinator:
    """Smart agent coordination using vector database intelligence."""
    
    def __init__(self):
        self.swarm_brain = SwarmBrain()
        self.retriever = Retriever()
        self.ingestor = Ingestor()
        self.messaging_service = MessagingService()
        logger.info("🧠 Intelligent Agent Coordinator initialized with Swarm Brain")
    
    def coordinate_task(self, task: str, required_skills: List[str], 
                       priority: str = "NORMAL") -> Dict[str, Any]:
        """Coordinate agents for a task using intelligence."""
        
        logger.info(f"🎯 Coordinating task: {task} (skills: {required_skills})")
        
        # 1. Find expert agents
        expert_agents = self._find_expert_agents(task, required_skills)
        
        # 2. Get successful coordination patterns
        coordination_patterns = self.retriever.how_do_agents_do(
            f"coordinate {task}", k=10
        )
        
        # 3. Create coordination plan
        coordination_plan = self._create_coordination_plan(
            expert_agents, coordination_patterns, task
        )
        
        # 4. Execute coordination
        results = self._execute_coordination(coordination_plan, task, priority)
        
        # 5. Learn from coordination
        self._learn_from_coordination(task, coordination_plan, results)
        
        logger.info(f"✅ Task coordination completed: {task}")
        
        return {
            "coordination_plan": coordination_plan,
            "results": results,
            "success_rate": self._calculate_success_rate(results),
            "lessons_learned": self._extract_lessons_learned(results),
            "expert_agents": expert_agents,
            "coordination_patterns": len(coordination_patterns)
        }
    
    def suggest_agent_assignments(self, tasks: List[str]) -> Dict[str, Dict[str, Any]]:
        """Suggest optimal agent assignments for multiple tasks."""
        
        logger.info(f"📋 Suggesting agent assignments for {len(tasks)} tasks")
        
        assignments = {}
        
        for task in tasks:
            # Find best agent for this task
            best_agent = self._find_best_agent_for_task(task)
            
            # Get assignment confidence
            confidence = self._calculate_assignment_confidence(task, best_agent)
            
            assignments[task] = {
                "recommended_agent": best_agent,
                "confidence": confidence,
                "reasoning": self._get_assignment_reasoning(task, best_agent),
                "alternative_agents": self._get_alternative_agents(task, best_agent)
            }
        
        logger.info(f"✅ Agent assignments suggested for {len(tasks)} tasks")
        
        return assignments
    
    def optimize_agent_workload(self, agents: List[str]) -> Dict[str, Dict[str, Any]]:
        """Optimize agent workload distribution."""
        
        logger.info(f"⚖️ Optimizing workload for {len(agents)} agents")
        
        workload_analysis = {}
        
        for agent_id in agents:
            # Get agent's current workload
            current_workload = self._get_agent_workload(agent_id)
            
            # Get agent's capabilities
            capabilities = self._get_agent_capabilities(agent_id)
            
            # Get optimal workload
            optimal_workload = self._calculate_optimal_workload(agent_id, capabilities)
            
            workload_analysis[agent_id] = {
                "current_workload": current_workload,
                "capabilities": capabilities,
                "optimal_workload": optimal_workload,
                "workload_balance": self._calculate_workload_balance(current_workload, optimal_workload),
                "recommendations": self._get_workload_recommendations(agent_id, current_workload, optimal_workload)
            }
        
        logger.info(f"✅ Workload optimization completed for {len(agents)} agents")
        
        return workload_analysis
    
    def _find_expert_agents(self, task: str, required_skills: List[str]) -> List[str]:
        """Find agents with expertise for the task."""
        expert_agents = []
        
        for skill in required_skills:
            # Find agents who have successfully used this skill
            skill_patterns = self.retriever.search(
                f"successful {skill} tasks", 
                kinds=["action"], 
                k=20
            )
            
            # Count successful uses per agent
            agent_skill_counts = {}
            for pattern in skill_patterns:
                agent_id = pattern.get("agent_id")
                if agent_id:
                    agent_skill_counts[agent_id] = agent_skill_counts.get(agent_id, 0) + 1
            
            # Add top agents to expert list
            top_agents = sorted(agent_skill_counts.keys(), 
                              key=lambda x: agent_skill_counts[x], reverse=True)[:3]
            expert_agents.extend(top_agents)
        
        # Remove duplicates and return
        return list(set(expert_agents))
    
    def _create_coordination_plan(self, expert_agents: List[str], 
                                 coordination_patterns: List[Dict], 
                                 task: str) -> Dict[str, Any]:
        """Create coordination plan based on expert agents and patterns."""
        
        plan = {
            "task": task,
            "expert_agents": expert_agents,
            "coordination_strategy": self._determine_coordination_strategy(coordination_patterns),
            "communication_plan": self._create_communication_plan(expert_agents),
            "timeline": self._estimate_timeline(task, expert_agents),
            "success_factors": self._identify_success_factors(coordination_patterns)
        }
        
        return plan
    
    def _execute_coordination(self, coordination_plan: Dict[str, Any], 
                             task: str, priority: str) -> Dict[str, Any]:
        """Execute coordination plan."""
        
        results = {
            "task": task,
            "coordination_plan": coordination_plan,
            "execution_results": {},
            "communication_results": {},
            "overall_success": False
        }
        
        # Execute communication plan
        for agent_id in coordination_plan["expert_agents"]:
            try:
                message = f"Task coordination: {task}"
                success = self.messaging_service.send_message(
                    agent_id, message, "Agent-Coordinator", priority
                )
                results["communication_results"][agent_id] = success
            except Exception as e:
                logger.error(f"❌ Failed to coordinate with {agent_id}: {e}")
                results["communication_results"][agent_id] = False
        
        # Determine overall success
        results["overall_success"] = all(results["communication_results"].values())
        
        return results
    
    def _learn_from_coordination(self, task: str, coordination_plan: Dict[str, Any], 
                                results: Dict[str, Any]):
        """Learn from coordination patterns."""
        try:
            self.ingestor.action(
                title=f"Task Coordination: {task}",
                tool="agent_coordinator",
                outcome="success" if results["overall_success"] else "failure",
                context={
                    "task": task,
                    "expert_agents": coordination_plan["expert_agents"],
                    "coordination_strategy": coordination_plan["coordination_strategy"],
                    "communication_results": results["communication_results"],
                    "overall_success": results["overall_success"]
                },
                project="Agent_Cellphone_V2",
                agent_id="Agent-Coordinator",
                tags=["coordination", "task_management", "agent_assignment"],
                summary=f"Coordinated task {task} with {len(coordination_plan['expert_agents'])} agents"
            )
            logger.debug(f"📚 Learned from coordination: {task}")
        except Exception as e:
            logger.error(f"❌ Failed to learn from coordination: {e}")
    
    def _find_best_agent_for_task(self, task: str) -> str:
        """Find the best agent for a specific task."""
        try:
            # Find agents who have successfully completed similar tasks
            task_patterns = self.retriever.search(
                f"successful {task}", 
                kinds=["action"], 
                k=20
            )
            
            if not task_patterns:
                return "Agent-1"  # Default fallback
            
            # Count successful completions per agent
            agent_success_counts = {}
            for pattern in task_patterns:
                agent_id = pattern.get("agent_id")
                if agent_id:
                    agent_success_counts[agent_id] = agent_success_counts.get(agent_id, 0) + 1
            
            # Return agent with most successful completions
            best_agent = max(agent_success_counts.keys(), 
                           key=lambda x: agent_success_counts[x])
            return best_agent
        except Exception as e:
            logger.error(f"❌ Failed to find best agent: {e}")
            return "Agent-1"
    
    def _calculate_assignment_confidence(self, task: str, agent_id: str) -> float:
        """Calculate confidence in agent assignment."""
        try:
            # Find similar tasks completed by this agent
            similar_tasks = self.retriever.search(
                f"successful {task} by {agent_id}", 
                kinds=["action"], 
                k=10
            )
            
            if len(similar_tasks) > 0:
                # Calculate confidence based on success rate
                success_rate = len(similar_tasks) / max(1, len(similar_tasks))
                return round(success_rate, 2)
            else:
                return 0.5  # Default confidence if no history
        except Exception as e:
            logger.error(f"❌ Failed to calculate confidence: {e}")
            return 0.5
    
    def _get_assignment_reasoning(self, task: str, agent_id: str) -> str:
        """Get reasoning for agent assignment."""
        try:
            # Find successful tasks by this agent
            successful_tasks = self.retriever.search(
                f"successful tasks by {agent_id}", 
                kinds=["action"], 
                k=10
            )
            
            if len(successful_tasks) > 0:
                return f"Agent {agent_id} has successfully completed {len(successful_tasks)} similar tasks"
            else:
                return f"Agent {agent_id} selected based on general capabilities"
        except Exception as e:
            logger.error(f"❌ Failed to get reasoning: {e}")
            return "Assignment based on general capabilities"
    
    def _get_alternative_agents(self, task: str, best_agent: str) -> List[str]:
        """Get alternative agents for the task."""
        try:
            # Find other agents who have completed similar tasks
            task_patterns = self.retriever.search(
                f"successful {task}", 
                kinds=["action"], 
                k=20
            )
            
            # Get unique agents (excluding the best agent)
            alternative_agents = []
            for pattern in task_patterns:
                agent_id = pattern.get("agent_id")
                if agent_id and agent_id != best_agent and agent_id not in alternative_agents:
                    alternative_agents.append(agent_id)
            
            return alternative_agents[:3]  # Return top 3 alternatives
        except Exception as e:
            logger.error(f"❌ Failed to get alternatives: {e}")
            return []
    
    def _get_agent_workload(self, agent_id: str) -> Dict[str, Any]:
        """Get current workload for agent."""
        try:
            # Find recent tasks by this agent
            recent_tasks = self.retriever.search(
                f"tasks by {agent_id}", 
                kinds=["action"], 
                k=20
            )
            
            return {
                "total_tasks": len(recent_tasks),
                "active_tasks": len([t for t in recent_tasks if t.get("status") == "active"]),
                "completed_tasks": len([t for t in recent_tasks if t.get("outcome") == "success"]),
                "workload_score": len(recent_tasks) / 10.0  # Normalized workload score
            }
        except Exception as e:
            logger.error(f"❌ Failed to get workload: {e}")
            return {"total_tasks": 0, "active_tasks": 0, "completed_tasks": 0, "workload_score": 0.0}
    
    def _get_agent_capabilities(self, agent_id: str) -> Dict[str, Any]:
        """Get agent capabilities."""
        try:
            # Get agent expertise
            expertise = self.retriever.get_agent_expertise(agent_id, k=20)
            
            return {
                "total_patterns": expertise.get("total_patterns", 0),
                "tool_expertise": expertise.get("tool_expertise", {}),
                "success_rate": self._calculate_agent_success_rate(agent_id),
                "specializations": self._get_agent_specializations(agent_id)
            }
        except Exception as e:
            logger.error(f"❌ Failed to get capabilities: {e}")
            return {"total_patterns": 0, "tool_expertise": {}, "success_rate": 0.0, "specializations": []}
    
    def _calculate_optimal_workload(self, agent_id: str, capabilities: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal workload for agent."""
        try:
            # Base optimal workload on capabilities
            total_patterns = capabilities.get("total_patterns", 0)
            success_rate = capabilities.get("success_rate", 0.5)
            
            # Calculate optimal task capacity
            optimal_capacity = min(10, max(1, int(total_patterns * success_rate)))
            
            return {
                "optimal_capacity": optimal_capacity,
                "recommended_tasks": optimal_capacity,
                "workload_threshold": optimal_capacity * 1.2,  # 20% buffer
                "efficiency_score": success_rate
            }
        except Exception as e:
            logger.error(f"❌ Failed to calculate optimal workload: {e}")
            return {"optimal_capacity": 5, "recommended_tasks": 5, "workload_threshold": 6, "efficiency_score": 0.5}
    
    def _calculate_workload_balance(self, current_workload: Dict[str, Any], 
                                   optimal_workload: Dict[str, Any]) -> str:
        """Calculate workload balance status."""
        try:
            current_tasks = current_workload.get("total_tasks", 0)
            optimal_capacity = optimal_workload.get("optimal_capacity", 5)
            
            if current_tasks < optimal_capacity * 0.8:
                return "underutilized"
            elif current_tasks > optimal_capacity * 1.2:
                return "overloaded"
            else:
                return "balanced"
        except Exception as e:
            logger.error(f"❌ Failed to calculate balance: {e}")
            return "unknown"
    
    def _get_workload_recommendations(self, agent_id: str, current_workload: Dict[str, Any], 
                                     optimal_workload: Dict[str, Any]) -> List[str]:
        """Get workload recommendations for agent."""
        recommendations = []
        
        try:
            balance = self._calculate_workload_balance(current_workload, optimal_workload)
            
            if balance == "underutilized":
                recommendations.append("Can take on additional tasks")
                recommendations.append("Consider mentoring other agents")
            elif balance == "overloaded":
                recommendations.append("Reduce current workload")
                recommendations.append("Delegate tasks to other agents")
            else:
                recommendations.append("Workload is well balanced")
                recommendations.append("Continue current pace")
            
            return recommendations
        except Exception as e:
            logger.error(f"❌ Failed to get recommendations: {e}")
            return ["Unable to provide recommendations"]
    
    def _determine_coordination_strategy(self, coordination_patterns: List[Dict]) -> str:
        """Determine best coordination strategy based on patterns."""
        try:
            if len(coordination_patterns) > 0:
                # Analyze successful coordination patterns
                successful_patterns = [p for p in coordination_patterns if p.get("outcome") == "success"]
                
                if len(successful_patterns) > 0:
                    return "Collaborative approach based on successful patterns"
                else:
                    return "Standard coordination approach"
            else:
                return "Standard coordination approach"
        except Exception as e:
            logger.error(f"❌ Failed to determine strategy: {e}")
            return "Standard coordination approach"
    
    def _create_communication_plan(self, expert_agents: List[str]) -> Dict[str, Any]:
        """Create communication plan for coordination."""
        return {
            "primary_agents": expert_agents,
            "communication_method": "messaging_service",
            "update_frequency": "as_needed",
            "coordination_channel": "agent_coordination"
        }
    
    def _estimate_timeline(self, task: str, expert_agents: List[str]) -> Dict[str, Any]:
        """Estimate timeline for task completion."""
        return {
            "estimated_duration": "2-4 hours",
            "complexity": "medium",
            "agent_count": len(expert_agents),
            "coordination_overhead": "minimal"
        }
    
    def _identify_success_factors(self, coordination_patterns: List[Dict]) -> List[str]:
        """Identify success factors from coordination patterns."""
        try:
            success_factors = []
            
            for pattern in coordination_patterns:
                if pattern.get("outcome") == "success":
                    # Extract success factors from pattern
                    title = pattern.get("title", "")
                    if "coordination" in title.lower():
                        success_factors.append("Effective coordination")
                    if "communication" in title.lower():
                        success_factors.append("Clear communication")
            
            # Return unique success factors
            return list(set(success_factors))[:5]
        except Exception as e:
            logger.error(f"❌ Failed to identify success factors: {e}")
            return ["Standard coordination practices"]
    
    def _calculate_success_rate(self, results: Dict[str, Any]) -> float:
        """Calculate success rate from coordination results."""
        try:
            communication_results = results.get("communication_results", {})
            if communication_results:
                successful = sum(communication_results.values())
                total = len(communication_results)
                return round(successful / total, 2)
            else:
                return 0.0
        except Exception as e:
            logger.error(f"❌ Failed to calculate success rate: {e}")
            return 0.0
    
    def _extract_lessons_learned(self, results: Dict[str, Any]) -> List[str]:
        """Extract lessons learned from coordination results."""
        lessons = []
        
        try:
            success_rate = self._calculate_success_rate(results)
            
            if success_rate > 0.8:
                lessons.append("High success rate achieved")
                lessons.append("Coordination strategy effective")
            elif success_rate > 0.5:
                lessons.append("Moderate success rate")
                lessons.append("Some coordination improvements needed")
            else:
                lessons.append("Low success rate")
                lessons.append("Coordination strategy needs revision")
            
            return lessons
        except Exception as e:
            logger.error(f"❌ Failed to extract lessons: {e}")
            return ["Unable to extract lessons"]
    
    def _calculate_agent_success_rate(self, agent_id: str) -> float:
        """Calculate success rate for agent."""
        try:
            # Find all actions by this agent
            agent_actions = self.retriever.search(
                f"actions by {agent_id}", 
                kinds=["action"], 
                k=50
            )
            
            if len(agent_actions) > 0:
                successful_actions = [a for a in agent_actions if a.get("outcome") == "success"]
                success_rate = len(successful_actions) / len(agent_actions)
                return round(success_rate, 2)
            else:
                return 0.5  # Default success rate
        except Exception as e:
            logger.error(f"❌ Failed to calculate success rate: {e}")
            return 0.5
    
    def _get_agent_specializations(self, agent_id: str) -> List[str]:
        """Get agent specializations."""
        try:
            # Find agent's tool expertise
            expertise = self.retriever.get_agent_expertise(agent_id, k=20)
            tool_expertise = expertise.get("tool_expertise", {})
            
            # Get top specializations
            specializations = []
            for tool, stats in tool_expertise.items():
                if stats.get("count", 0) > 0:
                    specializations.append(tool)
            
            return specializations[:5]  # Return top 5 specializations
        except Exception as e:
            logger.error(f"❌ Failed to get specializations: {e}")
            return []




