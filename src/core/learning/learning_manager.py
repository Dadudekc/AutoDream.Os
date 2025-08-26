#!/usr/bin/env python3
"""
Learning Manager - Agent Cellphone V2
====================================

Specialized learning manager inheriting from BaseManager.
Follows V2 standards: 400 LOC, OOP design, SRP.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION IN PROGRESS
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig
from .learning_models import (
    LearningData, LearningGoal, LearningProgress, LearningMode,
    IntelligenceLevel, LearningStatus, LearningPattern, LearningStrategy,
    LearningMetrics, LearningSession, LearningConfiguration
)
from .unified_learning_engine import UnifiedLearningEngine, LearningEngineConfig


@dataclass
class LearningManagerConfig(ManagerConfig):
    """Extended configuration for Learning Manager"""
    max_concurrent_learners: int = 50
    learning_session_timeout: int = 3600  # 1 hour
    enable_adaptive_learning: bool = True
    enable_collaborative_learning: bool = True
    learning_rate: float = 0.1
    batch_size: int = 32
    max_iterations: int = 1000
    convergence_threshold: float = 0.001
    auto_cleanup_inactive_sessions: bool = True
    cleanup_interval_minutes: int = 30


class LearningManager(BaseManager):
    """
    Specialized Learning Manager inheriting from BaseManager
    
    This manager consolidates learning functionality previously scattered across:
    - src/core/learning_engine.py
    - src/core/decision/learning_engine.py
    - src/ai_ml/ai_agent_learner_core.py
    - gaming_systems/ai_agent_framework_core.py
    - And 5+ other learning implementations
    """
    
    def __init__(self, manager_id: str, name: str = "Learning Manager", description: str = ""):
        super().__init__(manager_id, name, description)
        
        # Extended configuration
        self.learning_config = LearningManagerConfig(
            manager_id=manager_id,
            name=name,
            description=description
        )
        
        # Core learning engine
        self.learning_engine: Optional[UnifiedLearningEngine] = None
        
        # Learning session management
        self.active_learners: Dict[str, Dict[str, Any]] = {}
        self.learning_sessions: Dict[str, LearningSession] = {}
        self.learning_goals: Dict[str, LearningGoal] = {}
        
        # Performance tracking
        self.total_learning_operations = 0
        self.successful_learning_operations = 0
        self.failed_learning_operations = 0
        self.learning_startup_time: Optional[datetime] = None
        
        # Cleanup scheduling
        self.last_cleanup_time: Optional[datetime] = None
        
        self.logger.info(f"LearningManager initialized: {manager_id}")
    
    def _on_start(self) -> bool:
        """Learning Manager specific startup logic"""
        try:
            self.logger.info("Starting Learning Manager...")
            
            # Initialize learning engine
            engine_config = LearningEngineConfig(
                max_concurrent_sessions=self.learning_config.max_concurrent_learners,
                session_timeout_minutes=self.learning_config.learning_session_timeout // 60,
                learning_rate=self.learning_config.learning_rate,
                batch_size=self.learning_config.batch_size,
                max_iterations=self.learning_config.max_iterations,
                convergence_threshold=self.learning_config.convergence_threshold,
                enable_adaptive_learning=self.learning_config.enable_adaptive_learning,
                enable_collaborative_learning=self.learning_config.enable_collaborative_learning
            )
            
            self.learning_engine = UnifiedLearningEngine(engine_config)
            self.learning_startup_time = datetime.now()
            
            # Start cleanup scheduler if enabled
            if self.learning_config.auto_cleanup_inactive_sessions:
                self._schedule_cleanup()
            
            self.logger.info("Learning Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Learning Manager: {e}")
            return False
    
    def _on_stop(self):
        """Learning Manager specific shutdown logic"""
        try:
            self.logger.info("Stopping Learning Manager...")
            
            # End all active learning sessions
            for session_id in list(self.active_learners.keys()):
                self.end_learning_session(session_id)
            
            # Clear learning engine
            self.learning_engine = None
            
            # Clear all learning data
            self.active_learners.clear()
            self.learning_sessions.clear()
            self.learning_goals.clear()
            
            self.logger.info("Learning Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error during Learning Manager shutdown: {e}")
    
    def _on_heartbeat(self):
        """Learning Manager specific heartbeat logic"""
        try:
            # Check for inactive sessions that need cleanup
            if (self.learning_config.auto_cleanup_inactive_sessions and 
                self._should_perform_cleanup()):
                self._cleanup_inactive_sessions()
            
            # Update learning metrics
            self._update_learning_metrics()
            
            # Check learning engine health
            if self.learning_engine:
                engine_status = self.learning_engine.get_engine_status()
                if engine_status.get("status") != "active":
                    self.logger.warning("Learning engine health check failed")
            
        except Exception as e:
            self.logger.error(f"Error during Learning Manager heartbeat: {e}")
    
    def _on_initialize_resources(self) -> bool:
        """Learning Manager specific resource initialization"""
        try:
            # Initialize learning storage
            self.active_learners = {}
            self.learning_sessions = {}
            self.learning_goals = {}
            
            # Initialize performance tracking
            self.total_learning_operations = 0
            self.successful_learning_operations = 0
            self.failed_learning_operations = 0
            
            self.logger.info("Learning Manager resources initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Learning Manager resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Learning Manager specific resource cleanup"""
        try:
            # Clear all learning data
            self.active_learners.clear()
            self.learning_sessions.clear()
            self.learning_goals.clear()
            
            # Clear learning engine
            self.learning_engine = None
            
            self.logger.info("Learning Manager resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error during Learning Manager resource cleanup: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Learning Manager specific recovery logic"""
        try:
            self.logger.info(f"Attempting Learning Manager recovery: {context}")
            
            # Attempt to restart learning engine
            if self.learning_engine is None:
                self._restart_learning_engine()
                return True
            
            # Attempt to recover learning sessions
            if self.active_learners:
                self._recover_learning_sessions()
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Learning Manager recovery failed: {e}")
            return False
    
    # SPECIALIZED LEARNING CAPABILITIES - ENHANCED FOR V2
    def create_learning_strategy(self, strategy_type: str, parameters: Dict[str, Any]) -> str:
        """Create a specialized learning strategy"""
        try:
            strategy_id = str(uuid.uuid4())
            
            if strategy_type == "adaptive":
                strategy = LearningStrategy(
                    strategy_id=strategy_id,
                    name="Adaptive Learning",
                    description="Dynamically adjusts learning parameters based on performance",
                    strategy_type="adaptive",
                    parameters=parameters,
                    created_at=datetime.now().isoformat()
                )
            elif strategy_type == "collaborative":
                strategy = LearningStrategy(
                    strategy_id=strategy_id,
                    name="Collaborative Learning",
                    description="Coordinates learning across multiple agents",
                    strategy_type="collaborative",
                    parameters=parameters,
                    created_at=datetime.now().isoformat()
                )
            elif strategy_type == "reinforcement":
                strategy = LearningStrategy(
                    strategy_id=strategy_id,
                    name="Reinforcement Learning",
                    description="Uses reward-based learning optimization",
                    strategy_type="reinforcement",
                    parameters=parameters,
                    created_at=datetime.now().isoformat()
                )
            else:
                raise ValueError(f"Unknown strategy type: {strategy_type}")
            
            self.learning_strategies[strategy_id] = strategy
            self.logger.info(f"Created learning strategy: {strategy_id}")
            return strategy_id
            
        except Exception as e:
            self.logger.error(f"Failed to create learning strategy: {e}")
            raise
    
    def apply_learning_strategy(self, session_id: str, strategy_id: str) -> bool:
        """Apply a learning strategy to a specific session"""
        try:
            if session_id not in self.learning_sessions:
                raise ValueError(f"Session not found: {session_id}")
            
            if strategy_id not in self.learning_strategies:
                raise ValueError(f"Strategy not found: {strategy_id}")
            
            strategy = self.learning_strategies[strategy_id]
            session = self.learning_sessions[session_id]
            
            # Apply strategy parameters to session
            session.applied_strategy = strategy_id
            session.learning_parameters.update(strategy.parameters)
            
            # Update learning engine with new parameters
            if self.learning_engine:
                self.learning_engine.update_session_parameters(session_id, strategy.parameters)
            
            self.logger.info(f"Applied strategy {strategy_id} to session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to apply learning strategy: {e}")
            return False
    
    def coordinate_collaborative_learning(self, agent_ids: List[str], shared_goal: str) -> str:
        """Coordinate collaborative learning across multiple agents"""
        try:
            collaboration_id = str(uuid.uuid4())
            
            # Create collaborative learning session
            collaboration_session = LearningSession(
                session_id=collaboration_id,
                goal_id=shared_goal,
                agent_ids=agent_ids,
                session_type="collaborative",
                start_time=datetime.now().isoformat(),
                status="active"
            )
            
            # Register agents for collaboration
            for agent_id in agent_ids:
                if agent_id in self.active_learners:
                    self.active_learners[agent_id]["collaboration_id"] = collaboration_id
                    self.active_learners[agent_id]["session_id"] = collaboration_id
            
            # Store collaboration session
            self.learning_sessions[collaboration_id] = collaboration_session
            
            # Initialize collaborative learning in engine
            if self.learning_engine:
                self.learning_engine.initialize_collaborative_learning(
                    collaboration_id, agent_ids, shared_goal
                )
            
            self.logger.info(f"Started collaborative learning: {collaboration_id}")
            return collaboration_id
            
        except Exception as e:
            self.logger.error(f"Failed to coordinate collaborative learning: {e}")
            raise
    
    def analyze_learning_patterns(self, agent_id: str, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze learning patterns for performance optimization"""
        try:
            if agent_id not in self.active_learners:
                raise ValueError(f"Agent not found: {agent_id}")
            
            # Get learning history for agent
            agent_sessions = [
                session for session in self.learning_sessions.values()
                if agent_id in session.agent_ids
            ]
            
            # Filter by time range
            cutoff_time = datetime.now() - timedelta(hours=time_range_hours)
            recent_sessions = [
                session for session in agent_sessions
                if datetime.fromisoformat(session.start_time) > cutoff_time
            ]
            
            # Analyze patterns
            pattern_analysis = {
                "total_sessions": len(recent_sessions),
                "success_rate": 0.0,
                "average_session_duration": 0.0,
                "preferred_strategies": [],
                "performance_trend": "stable",
                "optimization_opportunities": []
            }
            
            if recent_sessions:
                # Calculate success rate
                successful_sessions = [
                    s for s in recent_sessions
                    if s.status == "completed" and s.performance_score > 0.7
                ]
                pattern_analysis["success_rate"] = len(successful_sessions) / len(recent_sessions)
                
                # Calculate average duration
                durations = []
                for session in recent_sessions:
                    if session.end_time:
                        start = datetime.fromisoformat(session.start_time)
                        end = datetime.fromisoformat(session.end_time)
                        durations.append((end - start).total_seconds() / 60)  # minutes
                
                if durations:
                    pattern_analysis["average_session_duration"] = sum(durations) / len(durations)
                
                # Identify preferred strategies
                strategy_counts = {}
                for session in recent_sessions:
                    if session.applied_strategy:
                        strategy_counts[session.applied_strategy] = strategy_counts.get(session.applied_strategy, 0) + 1
                
                if strategy_counts:
                    pattern_analysis["preferred_strategies"] = [
                        strategy_id for strategy_id, count in 
                        sorted(strategy_counts.items(), key=lambda x: x[1], reverse=True)
                    ]
                
                # Performance trend analysis
                if len(recent_sessions) >= 3:
                    recent_performance = [
                        s.performance_score for s in recent_sessions[-3:]
                        if hasattr(s, 'performance_score') and s.performance_score is not None
                    ]
                    if len(recent_performance) >= 2:
                        if recent_performance[-1] > recent_performance[0]:
                            pattern_analysis["performance_trend"] = "improving"
                        elif recent_performance[-1] < recent_performance[0]:
                            pattern_analysis["performance_trend"] = "declining"
                
                # Identify optimization opportunities
                if pattern_analysis["success_rate"] < 0.6:
                    pattern_analysis["optimization_opportunities"].append("Low success rate - consider strategy adjustment")
                if pattern_analysis["average_session_duration"] > 120:  # 2 hours
                    pattern_analysis["optimization_opportunities"].append("Long sessions - consider breaking into smaller goals")
            
            self.logger.info(f"Pattern analysis completed for agent {agent_id}")
            return pattern_analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze learning patterns: {e}")
            return {}
    
    def optimize_learning_performance(self, agent_id: str) -> Dict[str, Any]:
        """Optimize learning performance based on pattern analysis"""
        try:
            # Get pattern analysis
            patterns = self.analyze_learning_patterns(agent_id)
            
            optimization_plan = {
                "agent_id": agent_id,
                "current_performance": patterns.get("success_rate", 0.0),
                "recommended_strategy": None,
                "parameter_adjustments": {},
                "session_optimizations": []
            }
            
            # Recommend strategy based on patterns
            if patterns.get("success_rate", 0.0) < 0.5:
                optimization_plan["recommended_strategy"] = "adaptive"
                optimization_plan["parameter_adjustments"] = {
                    "learning_rate": 0.05,  # Reduce learning rate
                    "batch_size": 16,        # Smaller batches
                    "max_iterations": 500    # Fewer iterations
                }
            elif patterns.get("average_session_duration", 0.0) > 120:
                optimization_plan["recommended_strategy"] = "reinforcement"
                optimization_plan["session_optimizations"] = [
                    "Break large goals into smaller sub-goals",
                    "Implement progress checkpoints",
                    "Add intermediate rewards"
                ]
            else:
                optimization_plan["recommended_strategy"] = "collaborative"
                optimization_plan["parameter_adjustments"] = {
                    "enable_collaborative_learning": True,
                    "collaboration_threshold": 0.8
                }
            
            # Apply optimizations if learning engine is available
            if self.learning_engine and optimization_plan["recommended_strategy"]:
                strategy_id = self.create_learning_strategy(
                    optimization_plan["recommended_strategy"],
                    optimization_plan["parameter_adjustments"]
                )
                
                # Apply to active sessions
                for session_id, session in self.learning_sessions.items():
                    if agent_id in session.agent_ids and session.status == "active":
                        self.apply_learning_strategy(session_id, strategy_id)
            
            self.logger.info(f"Performance optimization completed for agent {agent_id}")
            return optimization_plan
            
        except Exception as e:
            self.logger.error(f"Failed to optimize learning performance: {e}")
            return {}
    
    # ============================================================================
    # LEARNING SESSION MANAGEMENT - Core functionality
    # ============================================================================
    
    def start_learning_session(
        self,
        agent_id: str,
        learning_goals: List[str],
        strategies: List[str],
        session_name: Optional[str] = None
    ) -> str:
        """Start a new learning session for an agent"""
        try:
            if not self.learning_engine:
                raise RuntimeError("Learning engine not initialized")
            
            # Check if agent already has an active session
            if agent_id in self.active_learners:
                existing_session = self.active_learners[agent_id]
                self.logger.warning(f"Agent {agent_id} already has active session: {existing_session['session_id']}")
                return existing_session['session_id']
            
            # Create learning session
            session_id = self.learning_engine.create_learning_session(
                agent_id=agent_id,
                learning_goals=learning_goals,
                strategies=strategies,
                session_name=session_name
            )
            
            # Track active learner
            self.active_learners[agent_id] = {
                "session_id": session_id,
                "start_time": datetime.now(),
                "learning_goals": learning_goals,
                "strategies": strategies,
                "status": "active"
            }
            
            # Store session reference
            if session_id in self.learning_engine.learning_sessions:
                self.learning_sessions[session_id] = self.learning_engine.learning_sessions[session_id]
            
            self.logger.info(f"Started learning session {session_id} for agent {agent_id}")
            self.total_learning_operations += 1
            self.successful_learning_operations += 1
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to start learning session: {e}")
            self.total_learning_operations += 1
            self.failed_learning_operations += 1
            raise
    
    def end_learning_session(self, session_id: str) -> bool:
        """End a learning session"""
        try:
            if not self.learning_engine:
                return False
            
            # Find agent for this session
            agent_id = None
            for aid, learner_data in self.active_learners.items():
                if learner_data["session_id"] == session_id:
                    agent_id = aid
                    break
            
            if not agent_id:
                self.logger.warning(f"Session {session_id} not found in active learners")
                return False
            
            # End session in learning engine
            success = self.learning_engine.end_learning_session(session_id)
            
            if success:
                # Remove from active learners
                self.active_learners.pop(agent_id, None)
                
                # Remove session reference
                self.learning_sessions.pop(session_id, None)
                
                self.logger.info(f"Ended learning session {session_id} for agent {agent_id}")
                self.total_learning_operations += 1
                self.successful_learning_operations += 1
                
                return True
            else:
                self.logger.error(f"Failed to end session {session_id} in learning engine")
                self.total_learning_operations += 1
                self.failed_learning_operations += 1
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to end learning session: {e}")
            self.total_learning_operations += 1
            self.failed_learning_operations += 1
            return False
    
    def add_learning_data(
        self,
        session_id: str,
        context: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        performance_score: float,
        learning_mode: LearningMode = LearningMode.ADAPTIVE
    ) -> bool:
        """Add learning data to an active session"""
        try:
            if not self.learning_engine:
                return False
            
            success = self.learning_engine.add_learning_data(
                session_id=session_id,
                context=context,
                input_data=input_data,
                output_data=output_data,
                performance_score=performance_score,
                learning_mode=learning_mode
            )
            
            if success:
                self.total_learning_operations += 1
                self.successful_learning_operations += 1
            else:
                self.total_learning_operations += 1
                self.failed_learning_operations += 1
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to add learning data: {e}")
            self.total_learning_operations += 1
            self.failed_learning_operations += 1
            return False
    
    # ============================================================================
    # LEARNING GOAL MANAGEMENT - Core functionality
    # ============================================================================
    
    def create_learning_goal(
        self,
        title: str,
        description: str,
        target_metrics: Dict[str, float],
        priority: int = 1,
        deadline: Optional[datetime] = None
    ) -> str:
        """Create a new learning goal"""
        try:
            if not self.learning_engine:
                raise RuntimeError("Learning engine not initialized")
            
            goal_id = self.learning_engine.create_learning_goal(
                title=title,
                description=description,
                target_metrics=target_metrics,
                priority=priority,
                deadline=deadline
            )
            
            # Store goal reference
            if goal_id in self.learning_engine.learning_goals:
                self.learning_goals[goal_id] = self.learning_engine.learning_goals[goal_id]
            
            self.logger.info(f"Created learning goal: {goal_id} - {title}")
            return goal_id
            
        except Exception as e:
            self.logger.error(f"Failed to create learning goal: {e}")
            raise
    
    def update_learning_goal(self, goal_id: str, **kwargs) -> bool:
        """Update an existing learning goal"""
        try:
            if not self.learning_engine:
                return False
            
            success = self.learning_engine.update_learning_goal(goal_id, **kwargs)
            
            if success:
                # Update local reference
                if goal_id in self.learning_goals:
                    goal = self.learning_goals[goal_id]
                    for key, value in kwargs.items():
                        if hasattr(goal, key):
                            setattr(goal, key, value)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update learning goal: {e}")
            return False
    
    # ============================================================================
    # LEARNING PATTERN ANALYSIS - Advanced functionality
    # ============================================================================
    
    def analyze_learning_patterns(self, agent_id: str) -> List[LearningPattern]:
        """Analyze learning patterns for a specific agent"""
        try:
            if not self.learning_engine:
                return []
            
            # Find active session for agent
            if agent_id not in self.active_learners:
                self.logger.warning(f"No active learning session found for agent {agent_id}")
                return []
            
            session_id = self.active_learners[agent_id]["session_id"]
            patterns = self.learning_engine.identify_learning_patterns(agent_id, session_id)
            
            self.logger.info(f"Identified {len(patterns)} learning patterns for agent {agent_id}")
            return patterns
            
        except Exception as e:
            self.logger.error(f"Failed to analyze learning patterns: {e}")
            return []
    
    def get_learning_performance_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive learning performance summary for an agent"""
        try:
            if not self.learning_engine:
                return {"error": "Learning engine not initialized"}
            
            summary = self.learning_engine.get_learning_performance_summary(agent_id)
            
            # Add manager-specific metrics
            if agent_id in self.active_learners:
                learner_data = self.active_learners[agent_id]
                summary["manager_status"] = "active"
                summary["session_start_time"] = learner_data["start_time"].isoformat()
                summary["session_duration"] = (datetime.now() - learner_data["start_time"]).total_seconds()
            else:
                summary["manager_status"] = "inactive"
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get learning performance summary: {e}")
            return {"error": str(e)}
    
    # ============================================================================
    # CLEANUP AND MAINTENANCE - Resource management
    # ============================================================================
    
    def _schedule_cleanup(self):
        """Schedule automatic cleanup of inactive sessions"""
        self.last_cleanup_time = datetime.now()
        self.logger.info("Scheduled automatic cleanup of inactive sessions")
    
    def _should_perform_cleanup(self) -> bool:
        """Check if cleanup should be performed"""
        if not self.last_cleanup_time:
            return True
        
        time_since_cleanup = datetime.now() - self.last_cleanup_time
        return time_since_cleanup.total_seconds() >= (self.learning_config.cleanup_interval_minutes * 60)
    
    def _cleanup_inactive_sessions(self):
        """Clean up inactive learning sessions"""
        try:
            if not self.learning_engine:
                return
            
            current_time = datetime.now()
            sessions_to_cleanup = []
            
            # Find sessions that have exceeded timeout
            for agent_id, learner_data in self.active_learners.items():
                session_start = learner_data["start_time"]
                session_duration = (current_time - session_start).total_seconds()
                
                if session_duration > self.learning_config.learning_session_timeout:
                    sessions_to_cleanup.append(learner_data["session_id"])
            
            # Clean up expired sessions
            for session_id in sessions_to_cleanup:
                self.logger.info(f"Cleaning up expired session: {session_id}")
                self.end_learning_session(session_id)
            
            if sessions_to_cleanup:
                self.logger.info(f"Cleaned up {len(sessions_to_cleanup)} expired sessions")
            
            self.last_cleanup_time = current_time
            
        except Exception as e:
            self.logger.error(f"Error during session cleanup: {e}")
    
    def _restore_learning_session(self, agent_id: str, learner_data: Dict[str, Any]) -> bool:
        """Restore a learning session during recovery"""
        try:
            session_id = learner_data["session_id"]
            
            # Check if session still exists in learning engine
            if (self.learning_engine and 
                session_id in self.learning_engine.learning_sessions):
                
                # Restore session reference
                self.learning_sessions[session_id] = self.learning_engine.learning_sessions[session_id]
                
                # Update status
                learner_data["status"] = "restored"
                
                self.logger.info(f"Restored learning session {session_id} for agent {agent_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to restore learning session: {e}")
            return False
    
    def _update_learning_metrics(self):
        """Update learning performance metrics"""
        try:
            # Update manager metrics
            self.metrics.operations_processed = self.total_learning_operations
            self.metrics.errors_count = self.failed_learning_operations
            
            # Calculate success rate
            if self.total_learning_operations > 0:
                success_rate = (self.successful_learning_operations / self.total_learning_operations) * 100.0
                self.metrics.performance_score = success_rate
            
            # Update last operation time
            self.metrics.last_operation = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Failed to update learning metrics: {e}")
    
    # ============================================================================
    # STATUS AND MONITORING - Extended functionality
    # ============================================================================
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get comprehensive learning status"""
        base_status = super().get_status()
        
        learning_status = {
            **base_status,
            "learning_engine_status": "active" if self.learning_engine else "inactive",
            "active_learners": len(self.active_learners),
            "total_learning_sessions": len(self.learning_sessions),
            "total_learning_goals": len(self.learning_goals),
            "learning_operations": {
                "total": self.total_learning_operations,
                "successful": self.successful_learning_operations,
                "failed": self.failed_learning_operations,
                "success_rate": (self.successful_learning_operations / max(1, self.total_learning_operations)) * 100.0
            },
            "cleanup_status": {
                "auto_cleanup_enabled": self.learning_config.auto_cleanup_inactive_sessions,
                "last_cleanup": self.last_cleanup_time.isoformat() if self.last_cleanup_time else None,
                "cleanup_interval_minutes": self.learning_config.cleanup_interval_minutes
            }
        }
        
        # Add learning engine status if available
        if self.learning_engine:
            try:
                engine_status = self.learning_engine.get_engine_status()
                learning_status["engine_details"] = engine_status
            except Exception as e:
                learning_status["engine_details"] = {"error": str(e)}
        
        return learning_status
