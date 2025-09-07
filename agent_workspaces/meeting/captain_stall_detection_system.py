#!/usr/bin/env python3
"""
Captain Stall Detection System
Agent-2 Implementation - PHASE TRANSITION OPTIMIZATION MANAGER

Mission: Integrate stall detection into Captain's workflow loop
Deliverables:
1. Captain monitoring loop implementation
2. 7-minute stall detection algorithm
3. Status monitoring integration points
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

class CaptainStallDetectionSystem:
    """
    Captain Workflow Loop with Integrated Stall Detection
    
    Monitors agent progress and detects stalls in the workflow
    Implements 7-minute stall detection algorithm
    Provides status monitoring integration points
    """
    
    def __init__(self, meeting_file_path: str = "agent_workspaces/meeting/meeting.json"):
        self.meeting_file_path = Path(meeting_file_path)
        self.stall_threshold_minutes = 7
        self.monitoring_interval_seconds = 60  # Check every minute
        self.last_status_check = None
        self.stall_detection_history = []
        self.agent_progress_tracking = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("CaptainStallDetection")
        
        # Initialize system
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize the stall detection system"""
        self.logger.info("Initializing Captain Stall Detection System...")
        
        # Load current meeting status
        self.current_status = self.load_meeting_status()
        
        # Initialize agent progress tracking
        self.initialize_agent_tracking()
        
        # Start monitoring loop
        self.start_monitoring_loop()
    
    def load_meeting_status(self) -> Dict:
        """Load current meeting status from JSON file"""
        try:
            if self.meeting_file_path.exists():
                with open(self.meeting_file_path, 'r') as f:
                    return json.load(f)
            else:
                self.logger.warning(f"Meeting file not found: {self.meeting_file_path}")
                return {}
        except Exception as e:
            self.logger.error(f"Error loading meeting status: {e}")
            return {}
    
    def initialize_agent_tracking(self):
        """Initialize tracking for all agents"""
        if not self.current_status or 'agent_status' not in self.current_status:
            return
        
        current_time = datetime.now()
        
        for agent_id, agent_data in self.current_status['agent_status'].items():
            self.agent_progress_tracking[agent_id] = {
                'last_activity': current_time,
                'last_status': agent_data.get('status', 'UNKNOWN'),
                'current_task': agent_data.get('current_task', 'UNKNOWN'),
                'progress_history': [],
                'stall_detected': False,
                'stall_start_time': None,
                'stall_duration_minutes': 0
            }
        
        self.logger.info(f"Initialized tracking for {len(self.agent_progress_tracking)} agents")
    
    def start_monitoring_loop(self):
        """Start the main monitoring loop"""
        self.logger.info("Starting Captain monitoring loop...")
        
        while True:
            try:
                # Perform stall detection check
                self.perform_stall_detection()
                
                # Update meeting status
                self.update_meeting_status()
                
                # Log current status
                self.log_current_status()
                
                # Wait for next check
                time.sleep(self.monitoring_interval_seconds)
                
            except KeyboardInterrupt:
                self.logger.info("Monitoring loop stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval_seconds)
    
    def perform_stall_detection(self):
        """Perform stall detection for all agents"""
        current_time = datetime.now()
        
        for agent_id, tracking_data in self.agent_progress_tracking.items():
            # Check if agent status has changed
            current_agent_status = self.get_current_agent_status(agent_id)
            
            if current_agent_status != tracking_data['last_status']:
                # Agent status changed - reset stall tracking
                self.reset_stall_tracking(agent_id, current_time, current_agent_status)
            else:
                # Check for stall condition
                self.check_stall_condition(agent_id, current_time)
    
    def get_current_agent_status(self, agent_id: str) -> str:
        """Get current status for a specific agent"""
        try:
            # Reload meeting status to get latest data
            current_status = self.load_meeting_status()
            if 'agent_status' in current_status and agent_id in current_status['agent_status']:
                return current_status['agent_status'][agent_id].get('status', 'UNKNOWN')
        except Exception as e:
            self.logger.error(f"Error getting agent status for {agent_id}: {e}")
        
        return 'UNKNOWN'
    
    def reset_stall_tracking(self, agent_id: str, current_time: datetime, new_status: str):
        """Reset stall tracking for an agent"""
        if agent_id in self.agent_progress_tracking:
            tracking_data = self.agent_progress_tracking[agent_id]
            
            # Record progress history
            if tracking_data['last_status'] != 'UNKNOWN':
                progress_entry = {
                    'timestamp': tracking_data['last_activity'],
                    'status': tracking_data['last_status'],
                    'duration_minutes': (current_time - tracking_data['last_activity']).total_seconds() / 60
                }
                tracking_data['progress_history'].append(progress_entry)
            
            # Reset tracking data
            tracking_data['last_activity'] = current_time
            tracking_data['last_status'] = new_status
            tracking_data['stall_detected'] = False
            tracking_data['stall_start_time'] = None
            tracking_data['stall_duration_minutes'] = 0
            
            self.logger.info(f"Reset stall tracking for {agent_id}: {new_status}")
    
    def check_stall_condition(self, agent_id: str, current_time: datetime):
        """Check if an agent is in a stall condition"""
        tracking_data = self.agent_progress_tracking[agent_id]
        
        # Calculate time since last activity
        time_since_last_activity = (current_time - tracking_data['last_activity']).total_seconds() / 60
        
        # Check if stall threshold exceeded
        if time_since_last_activity >= self.stall_threshold_minutes:
            if not tracking_data['stall_detected']:
                # Stall just detected
                tracking_data['stall_detected'] = True
                tracking_data['stall_start_time'] = tracking_data['last_activity']
                tracking_data['stall_duration_minutes'] = time_since_last_activity
                
                self.logger.warning(f"STALL DETECTED for {agent_id}: {time_since_last_activity:.1f} minutes")
                self.record_stall_detection(agent_id, time_since_last_activity)
            else:
                # Stall continuing - update duration
                tracking_data['stall_duration_minutes'] = time_since_last_activity
        else:
            # No stall condition
            if tracking_data['stall_detected']:
                # Stall resolved
                self.logger.info(f"Stall resolved for {agent_id} after {tracking_data['stall_duration_minutes']:.1f} minutes")
                tracking_data['stall_detected'] = False
                tracking_data['stall_start_time'] = None
                tracking_data['stall_duration_minutes'] = 0
    
    def record_stall_detection(self, agent_id: str, stall_duration_minutes: float):
        """Record a stall detection event"""
        stall_event = {
            'timestamp': datetime.now(),
            'agent_id': agent_id,
            'stall_duration_minutes': stall_duration_minutes,
            'current_task': self.agent_progress_tracking[agent_id].get('current_task', 'UNKNOWN'),
            'last_status': self.agent_progress_tracking[agent_id].get('last_status', 'UNKNOWN')
        }
        
        self.stall_detection_history.append(stall_event)
        
        # Log stall event
        self.logger.warning(f"STALL EVENT RECORDED: {agent_id} - {stall_duration_minutes:.1f} minutes")
        
        # Trigger stall response actions
        self.trigger_stall_response(agent_id, stall_duration_minutes)
    
    def trigger_stall_response(self, agent_id: str, stall_duration_minutes: float):
        """Trigger appropriate response actions for detected stalls"""
        if stall_duration_minutes >= self.stall_threshold_minutes:
            # Immediate response required
            self.logger.critical(f"CRITICAL STALL: {agent_id} stalled for {stall_duration_minutes:.1f} minutes")
            
            # Send urgent directive to stalled agent
            self.send_urgent_directive(agent_id)
            
            # Notify Captain
            self.notify_captain_of_stall(agent_id, stall_duration_minutes)
            
            # Update meeting status
            self.update_stall_status_in_meeting(agent_id, True, stall_duration_minutes)
    
    def send_urgent_directive(self, agent_id: str):
        """Send urgent directive to stalled agent"""
        directive = {
            'type': 'URGENT_STALL_RESOLUTION_DIRECTIVE',
            'timestamp': datetime.now().isoformat(),
            'agent_id': agent_id,
            'message': f'URGENT: Agent {agent_id} detected in stall condition. Immediate action required.',
            'action_required': 'Report progress or request assistance within 5 minutes',
            'priority': 'CRITICAL'
        }
        
        self.logger.info(f"Urgent directive sent to {agent_id}: {directive['message']}")
        
        # Store directive for tracking
        self.store_directive(agent_id, directive)
    
    def notify_captain_of_stall(self, agent_id: str, stall_duration_minutes: float):
        """Notify Captain of detected stall"""
        notification = {
            'type': 'STALL_DETECTION_NOTIFICATION',
            'timestamp': datetime.now().isoformat(),
            'agent_id': agent_id,
            'stall_duration_minutes': stall_duration_minutes,
            'severity': 'HIGH' if stall_duration_minutes >= 10 else 'MEDIUM',
            'recommended_action': 'Immediate intervention required'
        }
        
        self.logger.warning(f"Captain notified of stall: {agent_id} - {stall_duration_minutes:.1f} minutes")
        
        # Store notification
        self.store_captain_notification(notification)
    
    def update_stall_status_in_meeting(self, agent_id: str, stall_detected: bool, stall_duration: float):
        """Update stall status in meeting.json file"""
        try:
            # Load current meeting status
            meeting_status = self.load_meeting_status()
            
            if 'agent_status' in meeting_status and agent_id in meeting_status['agent_status']:
                # Add stall detection information
                if 'stall_detection' not in meeting_status['agent_status'][agent_id]:
                    meeting_status['agent_status'][agent_id]['stall_detection'] = {}
                
                meeting_status['agent_status'][agent_id]['stall_detection'].update({
                    'stall_detected': stall_detected,
                    'stall_duration_minutes': stall_duration,
                    'last_stall_check': datetime.now().isoformat(),
                    'stall_threshold_minutes': self.stall_threshold_minutes
                })
                
                # Add system-wide stall detection status
                if 'stall_detection_system' not in meeting_status:
                    meeting_status['stall_detection_system'] = {}
                
                meeting_status['stall_detection_system'].update({
                    'status': 'ACTIVE_MONITORING',
                    'last_updated': datetime.now().isoformat(),
                    'total_stalls_detected': len(self.stall_detection_history),
                    'active_stalls': len([a for a in self.agent_progress_tracking.values() if a['stall_detected']]),
                    'stall_threshold_minutes': self.stall_threshold_minutes
                })
                
                # Save updated meeting status
                self.save_meeting_status(meeting_status)
                
        except Exception as e:
            self.logger.error(f"Error updating stall status in meeting: {e}")
    
    def store_directive(self, agent_id: str, directive: Dict):
        """Store directive for tracking purposes"""
        directive_file = Path(f"agent_workspaces/{agent_id}/stall_resolution_directives.json")
        directive_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            directives = []
            if directive_file.exists():
                with open(directive_file, 'r') as f:
                    directives = json.load(f)
            
            directives.append(directive)
            
            with open(directive_file, 'w') as f:
                json.dump(directives, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error storing directive for {agent_id}: {e}")
    
    def store_captain_notification(self, notification: Dict):
        """Store Captain notification"""
        notification_file = Path("agent_workspaces/meeting/captain_stall_notifications.json")
        notification_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            notifications = []
            if notification_file.exists():
                with open(notification_file, 'r') as f:
                    notifications = json.load(f)
            
            notifications.append(notification)
            
            with open(notification_file, 'w') as f:
                json.dump(notifications, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error storing Captain notification: {e}")
    
    def save_meeting_status(self, meeting_status: Dict):
        """Save updated meeting status to file"""
        try:
            with open(self.meeting_file_path, 'w') as f:
                json.dump(meeting_status, f, indent=2, default=str)
            
            self.logger.info("Meeting status updated with stall detection information")
            
        except Exception as e:
            self.logger.error(f"Error saving meeting status: {e}")
    
    def log_current_status(self):
        """Log current system status"""
        active_stalls = len([a for a in self.agent_progress_tracking.values() if a['stall_detected']])
        total_agents = len(self.agent_progress_tracking)
        
        self.logger.info(f"Status: {active_stalls}/{total_agents} agents in stall condition")
        
        if active_stalls > 0:
            for agent_id, tracking_data in self.agent_progress_tracking.items():
                if tracking_data['stall_detected']:
                    self.logger.warning(f"  {agent_id}: {tracking_data['stall_duration_minutes']:.1f} minutes stalled")
    
    def get_stall_summary(self) -> Dict:
        """Get summary of current stall detection status"""
        active_stalls = [a for a in self.agent_progress_tracking.values() if a['stall_detected']]
        
        return {
            'total_agents': len(self.agent_progress_tracking),
            'active_stalls': len(active_stalls),
            'stall_threshold_minutes': self.stall_threshold_minutes,
            'last_check': datetime.now().isoformat(),
            'stall_history_count': len(self.stall_detection_history),
            'active_stall_details': [
                {
                    'agent_id': agent_id,
                    'stall_duration_minutes': tracking_data['stall_duration_minutes'],
                    'current_task': tracking_data['current_task'],
                    'last_status': tracking_data['last_status']
                }
                for agent_id, tracking_data in self.agent_progress_tracking.items()
                if tracking_data['stall_detected']
            ]
        }
    
    def emergency_stall_resolution(self, agent_id: str):
        """Emergency stall resolution for critical situations"""
        self.logger.critical(f"EMERGENCY STALL RESOLUTION TRIGGERED for {agent_id}")
        
        # Send emergency directive
        emergency_directive = {
            'type': 'EMERGENCY_STALL_RESOLUTION',
            'timestamp': datetime.now().isoformat(),
            'agent_id': agent_id,
            'message': f'EMERGENCY: Agent {agent_id} requires immediate intervention',
            'action_required': 'Captain intervention required within 2 minutes',
            'priority': 'CRITICAL_EMERGENCY'
        }
        
        self.store_directive(agent_id, emergency_directive)
        self.notify_captain_of_stall(agent_id, 999)  # High severity
        
        return emergency_directive

def main():
    """Main function to start the stall detection system"""
    print("🚀 Starting Captain Stall Detection System...")
    print("Agent-2: PHASE TRANSITION OPTIMIZATION MANAGER")
    print("Mission: Integrate stall detection into Captain's workflow loop")
    print("Deliverables: Monitoring loop, 7-min stall detection, Status integration")
    print("=" * 60)
    
    # Initialize and start the system
    stall_detection_system = CaptainStallDetectionSystem()
    
    try:
        # Keep the system running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stall detection system stopped by user")
        print("Final stall summary:")
        summary = stall_detection_system.get_stall_summary()
        print(json.dumps(summary, indent=2, default=str))

if __name__ == "__main__":
    main()
