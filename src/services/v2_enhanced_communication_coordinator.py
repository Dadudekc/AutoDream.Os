#!/usr/bin/env python3
"""
V2 Enhanced Communication Coordinator
Incorporates superior V1 communication patterns with FSM-based coordination
"""

import logging
import json
import time
import asyncio
import threading
from typing import Dict, Any, Optional, List, Callable, Union
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import queue

# Import multimedia services
try:
    from .multimedia.media_processor_service import MediaProcessorService
    from .multimedia.content_management_service import ContentManagementService
    from .multimedia.streaming_service import StreamingService
    from .v2_message_delivery_service import V2MessageDeliveryService
except ImportError:
    # Fallback for standalone usage
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    from multimedia.media_processor_service import MediaProcessorService
    from multimedia.content_management_service import ContentManagementService
    from multimedia.streaming_service import StreamingService
    from v2_message_delivery_service import V2MessageDeliveryService

logger = logging.getLogger(__name__)

class CommunicationMode(Enum):
    """Enhanced communication modes from V1"""
    HIERARCHICAL = "hierarchical"      # Top-down coordination
    COLLABORATIVE = "collaborative"    # Peer-to-peer collaboration
    DEMOCRATIC = "democratic"          # Voting-based decisions
    EMERGENCY = "emergency"            # Crisis response mode
    INNOVATION = "innovation"          # Creative problem solving
    PRESIDENTIAL = "presidential"      # Presidential captaincy mode

class TaskPriority(Enum):
    """Task priority levels from V1"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    PRESIDENTIAL = "presidential"

class TaskStatus(Enum):
    """Task status states from V1"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"
    FAILED = "failed"

class CaptaincyTerm(Enum):
    """Presidential captaincy terms from V1"""
    CAMPAIGN_TERM = "campaign_term"      # Task-list based term
    ELECTION_PHASE = "election_phase"    # Election and voting phase
    TRANSITION_PHASE = "transition_phase" # Handoff between captains

@dataclass
class CoordinationTask:
    """Task structure from V1"""
    task_id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    assigned_agents: List[str]
    dependencies: List[str]
    created_at: datetime
    due_date: Optional[datetime]
    estimated_hours: float
    actual_hours: float
    progress_percentage: float
    tags: List[str]
    metadata: Dict[str, Any]

@dataclass
class CollaborationSession:
    """Collaboration session from V1"""
    session_id: str
    title: str
    objective: str
    participating_agents: List[str]
    session_type: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    achievements: List[str]
    challenges: List[str]
    next_steps: List[str]
    session_notes: str

@dataclass
class PresidentialDecision:
    """Presidential decision structure from V1"""
    decision_id: str
    president_agent: str
    term: CaptaincyTerm
    decision_type: str
    title: str
    description: str
    impact_scope: str
    implementation_plan: List[str]
    success_metrics: List[str]
    created_at: datetime
    status: str = "proposed"
    approval_votes: Dict[str, bool] = None

class V2EnhancedCommunicationCoordinator:
    """
    V2 Enhanced Communication Coordinator
    Incorporates superior V1 communication patterns with multimedia integration
    """
    
    def __init__(self):
        self.multimedia_services = {}
        self.agent_connections = {}
        self.communication_status = {}
        self.coordination_events = {}
        
        # V1-style coordination components
        self.tasks: Dict[str, CoordinationTask] = {}
        self.blocked_tasks: List[str] = []
        self.completed_tasks: List[CoordinationTask] = []
        self.agent_workloads: Dict[str, Dict[str, Any]] = {}
        
        # V1-style collaboration components
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.session_history: List[CollaborationSession] = []
        
        # V1-style presidential components
        self.presidential_decisions: Dict[str, PresidentialDecision] = {}
        self.current_captain: Optional[str] = None
        self.captaincy_term: Optional[CaptaincyTerm] = None
        self.captaincy_start: Optional[datetime] = None
        
        # Communication queues and channels
        self.message_queues: Dict[str, queue.Queue] = {}
        self.broadcast_channels: Dict[str, List[str]] = {}
        self.private_channels: Dict[str, List[str]] = {}
        
        # V2 Message Delivery Service for actual message delivery
        self.message_delivery_service = None
        
        # Initialize all components
        self._initialize_multimedia_services()
        self._initialize_agent_coordination()
        self._initialize_v1_communication_patterns()
        self._setup_communication_monitoring()
        self._initialize_message_delivery_service()
    
    def _initialize_multimedia_services(self):
        """Initialize multimedia services"""
        try:
            logger.info("🎬 Initializing multimedia services for V2 communication...")
            
            self.multimedia_services['media_processor'] = MediaProcessorService()
            self.multimedia_services['content_manager'] = ContentManagementService()
            self.multimedia_services['streaming'] = StreamingService()
            
            logger.info("✅ All multimedia services initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing multimedia services: {e}")
            raise
    
    def _initialize_message_delivery_service(self):
        """Initialize V2 message delivery service"""
        try:
            logger.info("📤 Initializing V2 message delivery service...")
            
            self.message_delivery_service = V2MessageDeliveryService()
            logger.info("✅ V2 message delivery service initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing message delivery service: {e}")
            # Don't raise - system can still work without delivery service
            self.message_delivery_service = None
    
    def _initialize_agent_coordination(self):
        """Initialize agent coordination with V1-style roles"""
        try:
            logger.info("🤝 Initializing V1-style agent coordination...")
            
            self.agent_connections = {
                'agent_1': {
                    'role': 'Repository Development Specialist',
                    'multimedia_needs': ['content_generation', 'documentation_videos'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.COLLABORATIVE,
                    'task_capacity': 3,
                    'current_workload': 0
                },
                'agent_2': {
                    'role': 'Enhanced Collaborative System Specialist',
                    'multimedia_needs': ['collaboration_streams', 'team_meetings'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.COLLABORATIVE,
                    'task_capacity': 3,
                    'current_workload': 0
                },
                'agent_3': {
                    'role': 'Multimedia & Content Specialist (SELF)',
                    'multimedia_needs': ['core_multimedia_services'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.COLLABORATIVE,
                    'task_capacity': 3,
                    'current_workload': 0
                },
                'agent_4': {
                    'role': 'Quality Assurance & Testing Specialist',
                    'multimedia_needs': ['test_videos', 'quality_demos'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.HIERARCHICAL,
                    'task_capacity': 2,
                    'current_workload': 0
                },
                'agent_5': {
                    'role': 'Captain & Coordination Specialist',
                    'multimedia_needs': ['coordination_streams', 'status_reports'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.PRESIDENTIAL,
                    'task_capacity': 5,
                    'current_workload': 0
                },
                'agent_6': {
                    'role': 'Performance & Optimization Specialist',
                    'multimedia_needs': ['performance_metrics', 'optimization_demos'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.INNOVATION,
                    'task_capacity': 2,
                    'current_workload': 0
                },
                'agent_7': {
                    'role': 'Integration & API Specialist',
                    'multimedia_needs': ['api_demos', 'integration_tutorials'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.COLLABORATIVE,
                    'task_capacity': 3,
                    'current_workload': 0
                },
                'agent_8': {
                    'role': 'Workflow & Automation Specialist',
                    'multimedia_needs': ['workflow_demos', 'automation_videos'],
                    'status': 'active',
                    'last_communication': time.time(),
                    'communication_mode': CommunicationMode.INNOVATION,
                    'task_capacity': 2,
                    'current_workload': 0
                }
            }
            
            # Initialize message queues for each agent
            for agent_id in self.agent_connections:
                self.message_queues[agent_id] = queue.Queue()
            
            # Initialize broadcast channels
            self.broadcast_channels = {
                'general': list(self.agent_connections.keys()),
                'coordination': ['agent_5', 'agent_3'],
                'multimedia': ['agent_3', 'agent_4', 'agent_6'],
                'development': ['agent_1', 'agent_2', 'agent_7', 'agent_8']
            }
            
            logger.info(f"✅ V1-style agent coordination initialized for {len(self.agent_connections)} agents")
            
        except Exception as e:
            logger.error(f"❌ Error initializing agent coordination: {e}")
            raise
    
    def _initialize_v1_communication_patterns(self):
        """Initialize V1-style communication patterns"""
        try:
            logger.info("🔄 Initializing V1-style communication patterns...")
            
            # Set initial captain (Agent-5 as default)
            self.current_captain = 'agent_5'
            self.captaincy_term = CaptaincyTerm.CAMPAIGN_TERM
            self.captaincy_start = datetime.now()
            
            # Initialize communication status
            self.communication_status = {
                'overall_status': 'active',
                'communication_mode': CommunicationMode.PRESIDENTIAL.value,
                'current_captain': self.current_captain,
                'captaincy_term': self.captaincy_term.value,
                'captaincy_start': self.captaincy_start.isoformat(),
                'total_coordination_events': 0,
                'active_tasks': 0,
                'active_sessions': 0,
                'pending_decisions': 0
            }
            
            logger.info("✅ V1-style communication patterns initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing V1 communication patterns: {e}")
            raise
    
    def _setup_communication_monitoring(self):
        """Setup monitoring for communication system"""
        try:
            logger.info("📊 Setting up V2 communication monitoring...")
            
            # Start communication monitoring thread
            self.communication_thread = threading.Thread(
                target=self._communication_monitoring_loop,
                daemon=True
            )
            self.communication_thread.start()
            
            logger.info("✅ Communication monitoring setup complete")
            
        except Exception as e:
            logger.error(f"❌ Error setting up communication monitoring: {e}")
            raise
    
    def _communication_monitoring_loop(self):
        """Continuous monitoring loop for communication system"""
        while True:
            try:
                # Check agent communication status
                self._check_agent_communication_status()
                
                # Monitor multimedia service health
                self._monitor_multimedia_services()
                
                # Update communication metrics
                self._update_communication_metrics()
                
                # Process message queues
                self._process_message_queues()
                
                # Sleep for monitoring interval
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Error in communication monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_agent_communication_status(self):
        """Check communication status with all agents"""
        try:
            current_time = time.time()
            
            for agent_id, agent_info in self.agent_connections.items():
                # Check if agent is responsive
                time_since_last_comm = current_time - agent_info['last_communication']
                
                if time_since_last_comm > 300:  # 5 minutes
                    agent_info['status'] = 'inactive'
                    logger.warning(f"⚠️ Agent {agent_id} ({agent_info['role']}) appears inactive")
                else:
                    agent_info['status'] = 'active'
            
            # Update overall status
            active_agents = sum(1 for agent in self.agent_connections.values() if agent['status'] == 'active')
            total_agents = len(self.agent_connections)
            
            if active_agents == total_agents:
                self.communication_status['overall_status'] = 'active'
            else:
                self.communication_status['overall_status'] = 'degraded'
                logger.warning(f"⚠️ {total_agents - active_agents} agents are inactive")
                
        except Exception as e:
            logger.error(f"❌ Error checking agent communication status: {e}")
    
    def _monitor_multimedia_services(self):
        """Monitor health of multimedia services"""
        try:
            services_healthy = True
            
            for service_name, service in self.multimedia_services.items():
                try:
                    if hasattr(service, 'get_system_status'):
                        status = service.get_system_status()
                        if status.get('status') == 'error':
                            services_healthy = False
                            logger.error(f"❌ Service {service_name} reports error status")
                    else:
                        if not service:
                            services_healthy = False
                            logger.error(f"❌ Service {service_name} is None")
                            
                except Exception as e:
                    services_healthy = False
                    logger.error(f"❌ Error checking service {service_name}: {e}")
            
            if not services_healthy:
                logger.warning("⚠️ Some multimedia services are unhealthy")
                
        except Exception as e:
            logger.error(f"❌ Error monitoring multimedia services: {e}")
    
    def _update_communication_metrics(self):
        """Update communication metrics"""
        try:
            current_time = time.time()
            
            # Update communication status
            self.communication_status.update({
                'active_tasks': len(self.tasks),
                'active_sessions': len(self.active_sessions),
                'pending_decisions': len([d for d in self.presidential_decisions.values() if d.status == 'proposed'])
            })
            
        except Exception as e:
            logger.error(f"❌ Error updating communication metrics: {e}")
    
    def _process_message_queues(self):
        """Process message queues for all agents"""
        try:
            for agent_id, message_queue in self.message_queues.items():
                try:
                    # Process up to 10 messages per cycle
                    for _ in range(10):
                        if message_queue.empty():
                            break
                        
                        message = message_queue.get_nowait()
                        self._process_agent_message(agent_id, message)
                        
                except Exception as e:
                    logger.error(f"❌ Error processing messages for {agent_id}: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Error processing message queues: {e}")
    
    def _process_agent_message(self, agent_id: str, message: Dict[str, Any]):
        """Process individual agent message"""
        try:
            message_type = message.get('type', 'unknown')
            
            if message_type == 'task_update':
                self._handle_task_update_message(agent_id, message)
            elif message_type == 'collaboration_request':
                self._handle_collaboration_request_message(agent_id, message)
            elif message_type == 'presidential_decision':
                self._handle_presidential_decision_message(agent_id, message)
            elif message_type == 'multimedia_request':
                self._handle_multimedia_request_message(agent_id, message)
            else:
                logger.warning(f"⚠️ Unknown message type from {agent_id}: {message_type}")
                
        except Exception as e:
            logger.error(f"❌ Error processing message from {agent_id}: {e}")
    
    def _handle_task_update_message(self, agent_id: str, message: Dict[str, Any]):
        """Handle task update message from agent"""
        try:
            task_id = message.get('task_id')
            if task_id in self.tasks:
                task = self.tasks[task_id]
                
                # Update task progress
                if 'progress' in message:
                    old_progress = task.progress_percentage
                    task.progress_percentage = message['progress']
                    
                    # Update status based on progress
                    if task.progress_percentage == 100.0:
                        task.status = TaskStatus.COMPLETED
                        self._complete_task(task_id)
                    elif task.progress_percentage > 0 and task.status == TaskStatus.ASSIGNED:
                        task.status = TaskStatus.IN_PROGRESS
                    
                    logger.info(f"📈 Task {task.title} progress: {old_progress}% → {task.progress_percentage}%")
                    
                    # Notify stakeholders
                    self._notify_task_progress_update(task, old_progress, task.progress_percentage)
                    
        except Exception as e:
            logger.error(f"❌ Error handling task update message: {e}")
    
    def _handle_collaboration_request_message(self, agent_id: str, message: Dict[str, Any]):
        """Handle collaboration request message from agent"""
        try:
            session_type = message.get('session_type', 'general')
            objective = message.get('objective', 'Collaboration session')
            participants = message.get('participants', [agent_id])
            
            # Create collaboration session
            session = CollaborationSession(
                session_id=str(uuid.uuid4()),
                title=f"{session_type.title()} Session",
                objective=objective,
                participating_agents=participants,
                session_type=session_type,
                start_time=datetime.now(),
                end_time=None,
                status='active',
                achievements=[],
                challenges=[],
                next_steps=[],
                session_notes=''
            )
            
            self.active_sessions[session.session_id] = session
            
            # Notify participants
            for participant in participants:
                if participant in self.agent_connections:
                    self._send_private_message(participant, {
                        'type': 'collaboration_session_started',
                        'session_id': session.session_id,
                        'title': session.title,
                        'objective': session.objective
                    })
            
            logger.info(f"🤝 Collaboration session started: {session.title}")
            
        except Exception as e:
            logger.error(f"❌ Error handling collaboration request message: {e}")
    
    def _handle_presidential_decision_message(self, agent_id: str, message: Dict[str, Any]):
        """Handle presidential decision message from agent"""
        try:
            if agent_id == self.current_captain:
                decision = PresidentialDecision(
                    decision_id=str(uuid.uuid4()),
                    president_agent=agent_id,
                    term=self.captaincy_term,
                    decision_type=message.get('decision_type', 'general'),
                    title=message.get('title', 'Presidential Decision'),
                    description=message.get('description', ''),
                    impact_scope=message.get('impact_scope', 'system_wide'),
                    implementation_plan=message.get('implementation_plan', []),
                    success_metrics=message.get('success_metrics', []),
                    created_at=datetime.now(),
                    status='proposed',
                    approval_votes={}
                )
                
                self.presidential_decisions[decision.decision_id] = decision
                
                # Broadcast decision to all agents
                self._broadcast_message('general', {
                    'type': 'presidential_decision_proposed',
                    'decision_id': decision.decision_id,
                    'title': decision.title,
                    'description': decision.description,
                    'president': agent_id
                })
                
                logger.info(f"🏛️ Presidential decision proposed: {decision.title}")
            else:
                logger.warning(f"⚠️ Non-captain agent {agent_id} attempted to make presidential decision")
                
        except Exception as e:
            logger.error(f"❌ Error handling presidential decision message: {e}")
    
    def _handle_multimedia_request_message(self, agent_id: str, message: Dict[str, Any]):
        """Handle multimedia request message from agent"""
        try:
            request_type = message.get('request_type', 'unknown')
            
            if request_type == 'content_generation':
                self._handle_content_generation_request(agent_id, message)
            elif request_type == 'streaming_setup':
                self._handle_streaming_setup_request(agent_id, message)
            elif request_type == 'media_processing':
                self._handle_media_processing_request(agent_id, message)
            else:
                logger.warning(f"⚠️ Unknown multimedia request type: {request_type}")
                
        except Exception as e:
            logger.error(f"❌ Error handling multimedia request message: {e}")
    
    def _handle_content_generation_request(self, agent_id: str, message: Dict[str, Any]):
        """Handle content generation request"""
        try:
            content_manager = self.multimedia_services['content_manager']
            
            pipeline_name = message.get('pipeline_name', f'{agent_id}_pipeline')
            content_type = message.get('content_type', 'blog')
            source_data = message.get('source_data', {})
            
            pipeline_config = {
                'name': pipeline_name,
                'type': content_type,
                'source': agent_id,
                'output_format': message.get('output_format', 'markdown')
            }
            
            if content_manager.create_content_pipeline(pipeline_name, pipeline_config):
                if content_manager.start_content_generation(pipeline_name, source_data):
                    # Send success response
                    self._send_private_message(agent_id, {
                        'type': 'content_generation_started',
                        'pipeline_name': pipeline_name,
                        'status': 'success'
                    })
                else:
                    self._send_private_message(agent_id, {
                        'type': 'content_generation_error',
                        'error': 'Failed to start content generation'
                    })
            else:
                self._send_private_message(agent_id, {
                    'type': 'content_generation_error',
                    'error': 'Failed to create content pipeline'
                })
                
        except Exception as e:
            logger.error(f"❌ Error handling content generation request: {e}")
            self._send_private_message(agent_id, {
                'type': 'content_generation_error',
                'error': str(e)
            })
    
    def _handle_streaming_setup_request(self, agent_id: str, message: Dict[str, Any]):
        """Handle streaming setup request"""
        try:
            streaming_service = self.multimedia_services['streaming']
            
            stream_name = message.get('stream_name', f'{agent_id}_stream')
            stream_config = {
                'name': stream_name,
                'source': message.get('source', 'webcam'),
                'platforms': message.get('platforms', ['youtube']),
                'quality': message.get('quality', '720p'),
                'fps': message.get('fps', 30)
            }
            
            if streaming_service.start_live_stream(stream_name, stream_config):
                self._send_private_message(agent_id, {
                    'type': 'streaming_started',
                    'stream_name': stream_name,
                    'status': 'success'
                })
            else:
                self._send_private_message(agent_id, {
                    'type': 'streaming_error',
                    'error': 'Failed to start streaming'
                })
                
        except Exception as e:
            logger.error(f"❌ Error handling streaming setup request: {e}")
            self._send_private_message(agent_id, {
                'type': 'streaming_error',
                'error': str(e)
            })
    
    def _handle_media_processing_request(self, agent_id: str, message: Dict[str, Any]):
        """Handle media processing request"""
        try:
            media_processor = self.multimedia_services['media_processor']
            
            pipeline_name = message.get('pipeline_name', f'{agent_id}_media_pipeline')
            pipeline_config = {
                'name': pipeline_name,
                'type': 'multimedia',
                'enable_video': message.get('enable_video', True),
                'enable_audio': message.get('enable_audio', True),
                'video': message.get('video', {}),
                'audio': message.get('audio', {}),
                'video_effects': message.get('video_effects', []),
                'audio_effects': message.get('audio_effects', [])
            }
            
            if media_processor.start_multimedia_pipeline(pipeline_name, pipeline_config):
                self._send_private_message(agent_id, {
                    'type': 'media_processing_started',
                    'pipeline_name': pipeline_name,
                    'status': 'success'
                })
            else:
                self._send_private_message(agent_id, {
                    'type': 'media_processing_error',
                    'error': 'Failed to start media processing pipeline'
                })
                
        except Exception as e:
            logger.error(f"❌ Error handling media processing request: {e}")
            self._send_private_message(agent_id, {
                'type': 'media_processing_error',
                'error': str(e)
            })
    
    def _send_private_message(self, agent_id: str, message: Dict[str, Any]):
        """Send private message to specific agent"""
        try:
            if agent_id in self.message_queues:
                message['timestamp'] = time.time()
                message['sender'] = 'system'
                self.message_queues[agent_id].put(message)
                
                # Update last communication time
                if agent_id in self.agent_connections:
                    self.agent_connections[agent_id]['last_communication'] = time.time()
                
                # Actually deliver the message via V2 delivery service
                if self.message_delivery_service:
                    message_type = message.get('type', 'unknown')
                    content = message.get('message', '')
                    
                    # Extract relevant content based on message type
                    if message_type == 'task_assigned':
                        content = f"Task: {message.get('title', 'Unknown')} - {message.get('description', 'No description')}"
                    elif message_type == 'task_progress_update':
                        content = f"Progress: {message.get('old_progress', 0)}% → {message.get('new_progress', 0)}%"
                    elif message_type == 'collaboration_session_started':
                        content = f"Session: {message.get('title', 'Unknown')} - {message.get('objective', 'No objective')}"
                    elif message_type == 'presidential_decision_proposed':
                        content = f"Decision: {message.get('title', 'Unknown')} - {message.get('description', 'No description')}"
                    elif message_type == 'significant_progress':
                        content = f"Progress: {message.get('task_title', 'Unknown')} - {message.get('progress', 0)}%"
                    elif message_type == 'task_completed':
                        content = f"Completed: {message.get('task_title', 'Unknown')}"
                    elif message_type == 'multimedia_update':
                        content = message.get('message', 'Multimedia update')
                    
                    # Send via delivery service
                    self.message_delivery_service.send_message(
                        agent_id, 
                        message_type, 
                        content,
                        **message
                    )
                    
                    logger.info(f"📤 Message delivered to {agent_id} via V2 delivery service")
                else:
                    logger.warning(f"⚠️ Message delivery service not available - message only queued for {agent_id}")
                    
        except Exception as e:
            logger.error(f"❌ Error sending private message to {agent_id}: {e}")
    
    def _broadcast_message(self, channel: str, message: Dict[str, Any]):
        """Broadcast message to channel"""
        try:
            if channel in self.broadcast_channels:
                message['timestamp'] = time.time()
                message['sender'] = 'system'
                message['channel'] = channel
                
                for agent_id in self.broadcast_channels[channel]:
                    if agent_id in self.message_queues:
                        self.message_queues[agent_id].put(message.copy())
                        
                        # Update last communication time
                        if agent_id in self.agent_connections:
                            self.agent_connections[agent_id]['last_communication'] = time.time()
                
                # Actually broadcast via V2 delivery service
                if self.message_delivery_service:
                    message_type = message.get('type', 'broadcast')
                    content = message.get('message', 'Broadcast message')
                    
                    # Extract relevant content based on message type
                    if message_type == 'presidential_decision_proposed':
                        content = f"Presidential Decision: {message.get('title', 'Unknown')} - {message.get('description', 'No description')}"
                    elif message_type == 'significant_progress':
                        content = f"Significant Progress: {message.get('task_title', 'Unknown')} - {message.get('progress', 0)}%"
                    elif message_type == 'task_completed':
                        content = f"Task Completed: {message.get('task_title', 'Unknown')}"
                    elif message_type == 'multimedia_update':
                        content = message.get('message', 'Multimedia update')
                    
                    # Broadcast via delivery service
                    target_agents = self.broadcast_channels[channel]
                    results = self.message_delivery_service.broadcast_message(
                        message_type,
                        content,
                        target_agents,
                        **message
                    )
                    
                    logger.info(f"📢 Broadcast delivered to {len(target_agents)} agents via V2 delivery service")
                    logger.info(f"📊 Broadcast results: {results}")
                else:
                    logger.warning(f"⚠️ Message delivery service not available - broadcast only queued")
                
                logger.info(f"📢 Message broadcast to {channel} channel")
                
        except Exception as e:
            logger.error(f"❌ Error broadcasting message to {channel}: {e}")
    
    def _notify_task_progress_update(self, task: CoordinationTask, old_progress: float, new_progress: float):
        """Notify stakeholders of task progress update"""
        try:
            message = {
                'type': 'task_progress_update',
                'task_id': task.task_id,
                'title': task.title,
                'old_progress': old_progress,
                'new_progress': new_progress,
                'status': task.status.value
            }
            
            # Notify assigned agents
            for agent_id in task.assigned_agents:
                self._send_private_message(agent_id, message)
            
            # Notify coordinators if significant progress
            if new_progress - old_progress >= 25:
                self._broadcast_message('coordination', {
                    'type': 'significant_progress',
                    'task_title': task.title,
                    'progress': new_progress
                })
                
        except Exception as e:
            logger.error(f"❌ Error notifying task progress update: {e}")
    
    def _complete_task(self, task_id: str):
        """Mark task as completed"""
        try:
            task = self.tasks[task_id]
            
            # Move to completed tasks
            self.completed_tasks.append(task)
            del self.tasks[task_id]
            
            # Update agent workloads
            for agent_id in task.assigned_agents:
                if agent_id in self.agent_workloads:
                    if task_id in self.agent_workloads[agent_id]['active_tasks']:
                        self.agent_workloads[agent_id]['active_tasks'].remove(task_id)
                    if task_id not in self.agent_workloads[agent_id]['completed_tasks']:
                        self.agent_workloads[agent_id]['completed_tasks'].append(task_id)
            
            # Check blocked tasks for dependency resolution
            self._check_blocked_tasks()
            
            # Notify completion
            self._broadcast_message('general', {
                'type': 'task_completed',
                'task_title': task.title,
                'assigned_agents': task.assigned_agents
            })
            
            logger.info(f"🎉 Task completed: {task.title}")
            
        except Exception as e:
            logger.error(f"❌ Error completing task: {e}")
    
    def _check_blocked_tasks(self):
        """Check if any blocked tasks can now proceed"""
        try:
            for task_id in self.blocked_tasks[:]:  # Copy list to avoid modification during iteration
                if task_id in self.tasks:
                    task = self.tasks[task_id]
                    
                    # Check if all dependencies are completed
                    dependencies_satisfied = True
                    for dep_id in task.dependencies:
                        if not any(dep_id == completed_task.task_id for completed_task in self.completed_tasks):
                            dependencies_satisfied = False
                            break
                    
                    if dependencies_satisfied:
                        # Dependencies satisfied, task can proceed
                        task.status = TaskStatus.PENDING
                        self.blocked_tasks.remove(task_id)
                        logger.info(f"✅ Task {task.title} dependencies satisfied")
                        
        except Exception as e:
            logger.error(f"❌ Error checking blocked tasks: {e}")
    
    def get_communication_status(self) -> Dict[str, Any]:
        """Get overall communication status"""
        try:
            return {
                'communication_status': self.communication_status,
                'agent_connections': self.agent_connections,
                'multimedia_services': {
                    name: 'healthy' if service else 'unhealthy' 
                    for name, service in self.multimedia_services.items()
                },
                'active_tasks': len(self.tasks),
                'active_sessions': len(self.active_sessions),
                'presidential_decisions': len(self.presidential_decisions),
                'message_queues': {
                    agent_id: queue.qsize() 
                    for agent_id, queue in self.message_queues.items()
                },
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting communication status: {e}")
            return {'error': str(e)}
    
    def create_task(self, title: str, description: str, priority: TaskPriority, 
                    assigned_agents: List[str], dependencies: List[str] = None) -> str:
        """Create a new coordination task"""
        try:
            task_id = str(uuid.uuid4())
            
            task = CoordinationTask(
                task_id=task_id,
                title=title,
                description=description,
                priority=priority,
                status=TaskStatus.PENDING,
                assigned_agents=assigned_agents,
                dependencies=dependencies or [],
                created_at=datetime.now(),
                due_date=None,
                estimated_hours=0.0,
                actual_hours=0.0,
                progress_percentage=0.0,
                tags=[],
                metadata={}
            )
            
            self.tasks[task_id] = task
            
            # Check dependencies
            if dependencies:
                self._check_task_dependencies(task_id)
            
            # Notify assigned agents
            for agent_id in assigned_agents:
                self._send_private_message(agent_id, {
                    'type': 'task_assigned',
                    'task_id': task_id,
                    'title': title,
                    'description': description,
                    'priority': priority.value
                })
            
            logger.info(f"📋 Task created: {title}")
            return task_id
            
        except Exception as e:
            logger.error(f"❌ Error creating task: {e}")
            return None
    
    def _check_task_dependencies(self, task_id: str):
        """Check if task dependencies are satisfied"""
        try:
            task = self.tasks[task_id]
            
            if not task.dependencies:
                return  # No dependencies
            
            # Check if all dependencies are completed
            for dep_id in task.dependencies:
                if not any(dep_id == completed_task.task_id for completed_task in self.completed_tasks):
                    # Dependency not satisfied, block task
                    task.status = TaskStatus.BLOCKED
                    if task_id not in self.blocked_tasks:
                        self.blocked_tasks.append(task_id)
                    logger.info(f"⚠️ Task {task.title} is blocked by dependencies")
                    return
            
            # All dependencies satisfied
            task.status = TaskStatus.PENDING
            if task_id in self.blocked_tasks:
                self.blocked_tasks.remove(task_id)
            logger.info(f"✅ Task {task.title} dependencies satisfied")
            
        except Exception as e:
            logger.error(f"❌ Error checking task dependencies: {e}")

# CLI interface for V2 enhanced communication
def main():
    """CLI interface for V2 Enhanced Communication Coordinator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='V2 Enhanced Communication Coordinator')
    parser.add_argument('--status', action='store_true', help='Show communication status')
    parser.add_argument('--create-task', nargs=4, metavar=('TITLE', 'DESCRIPTION', 'PRIORITY', 'AGENTS'), 
                       help='Create a new task (title description priority agents)')
    parser.add_argument('--broadcast', nargs=2, metavar=('CHANNEL', 'MESSAGE'), 
                       help='Broadcast message to channel')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring mode')
    
    args = parser.parse_args()
    
    try:
        coordinator = V2EnhancedCommunicationCoordinator()
        
        if args.status:
            status = coordinator.get_communication_status()
            print(json.dumps(status, indent=2, default=str))
            
        elif args.create_task:
            title, description, priority_str, agents_str = args.create_task
            priority = TaskPriority(priority_str.lower())
            agents = agents_str.split(',')
            
            task_id = coordinator.create_task(title, description, priority, agents)
            if task_id:
                print(f"✅ Task created with ID: {task_id}")
            else:
                print("❌ Failed to create task")
                
        elif args.broadcast:
            channel, message = args.broadcast
            coordinator._broadcast_message(channel, {'message': message})
            print(f"📢 Message broadcast to {channel} channel")
            
        elif args.monitor:
            print("🔍 Starting V2 communication monitoring...")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    status = coordinator.get_communication_status()
                    print(f"\n📊 Status Update: {status['communication_status']['overall_status']}")
                    print(f"Active Tasks: {status['active_tasks']}")
                    print(f"Active Sessions: {status['active_sessions']}")
                    print(f"Presidential Decisions: {status['presidential_decisions']}")
                    time.sleep(30)
            except KeyboardInterrupt:
                print("\n👋 Monitoring stopped")
                
        else:
            print("🚀 V2 Enhanced Communication Coordinator ready")
            print("Use --help for available commands")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
