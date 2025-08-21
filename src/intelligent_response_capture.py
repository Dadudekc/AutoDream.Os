#!/usr/bin/env python3
"""
Intelligent Response Capture System - Agent Cellphone V2
======================================================

This system captures agent responses, builds a database, and uses it for:
- Automated task generation
- Intelligent workflow orchestration  
- Progress analytics
- Quality assessment
- Collaborative task chaining
"""

import time
import json
import sqlite3
from pathlib import Path
import sys
from datetime import datetime
import hashlib
import re

# Add src to path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

class AgentResponseDatabase:
    """Database for storing and analyzing agent responses."""
    
    def __init__(self, db_path="agent_responses.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the response database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for comprehensive response tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                response_file TEXT NOT NULL,
                response_content TEXT,
                response_hash TEXT UNIQUE,
                task_id TEXT,
                response_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                processing_status TEXT DEFAULT 'new'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS response_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_id INTEGER,
                analysis_type TEXT,
                analysis_result TEXT,
                confidence_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (response_id) REFERENCES agent_responses (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_response_id INTEGER,
                task_title TEXT,
                task_description TEXT,
                assigned_agent TEXT,
                priority TEXT,
                dependencies TEXT,
                generated_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (source_response_id) REFERENCES agent_responses (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_chains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chain_name TEXT,
                trigger_response_type TEXT,
                next_task_template TEXT,
                conditions TEXT,
                created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")

class IntelligentResponseCapture:
    """Captures and analyzes agent responses intelligently."""
    
    def __init__(self):
        self.db = AgentResponseDatabase()
        self.response_patterns = {
            'code_file': r'\.py$|\.js$|\.ts$|\.java$|\.cpp$|\.h$',
            'documentation': r'\.md$|\.txt$|\.rst$|\.docx?$',
            'data_file': r'\.json$|\.xml$|\.csv$|\.yaml$|\.yml$',
            'image_file': r'\.png$|\.jpg$|\.jpeg$|\.gif$|\.svg$',
            'log_file': r'\.log$|\.out$|\.err$'
        }
        
        # Define intelligent workflow triggers
        self.workflow_triggers = {
            'code_completion': {
                'trigger': 'code_file',
                'action': 'generate_test_task',
                'conditions': ['file_size > 100', 'contains_function_definitions']
            },
            'analysis_report': {
                'trigger': 'documentation',
                'action': 'generate_implementation_task',
                'conditions': ['contains_issues', 'contains_recommendations']
            },
            'error_log': {
                'trigger': 'log_file',
                'action': 'generate_debug_task',
                'conditions': ['contains_error', 'contains_stack_trace']
            }
        }
    
    def capture_response(self, agent_id, response_file_path):
        """Capture and analyze a new agent response."""
        try:
            file_path = Path(response_file_path)
            if not file_path.exists():
                return False
            
            # Read response content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Generate content hash
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Determine response type
            response_type = self.classify_response(file_path, content)
            
            # Store in database
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO agent_responses 
                (agent_id, response_file, response_content, response_hash, response_type, file_size)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (agent_id, str(file_path), content, content_hash, response_type, file_path.stat().st_size))
            
            response_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            if response_id:
                print(f"✅ Captured response from {agent_id}: {file_path.name} ({response_type})")
                
                # Analyze response and generate new tasks
                self.analyze_and_generate_tasks(response_id, content, response_type, agent_id)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error capturing response: {e}")
            return False
    
    def classify_response(self, file_path, content):
        """Classify the type of response based on file and content."""
        filename = file_path.name.lower()
        
        # Check file extension patterns
        for response_type, pattern in self.response_patterns.items():
            if re.search(pattern, filename):
                return response_type
        
        # Check content patterns for better classification
        if 'def ' in content or 'class ' in content:
            return 'code_file'
        elif 'error' in content.lower() or 'exception' in content.lower():
            return 'error_report'
        elif 'analysis' in content.lower() or 'report' in content.lower():
            return 'analysis_report'
        elif 'task' in content.lower() or 'todo' in content.lower():
            return 'task_update'
        
        return 'unknown'
    
    def analyze_and_generate_tasks(self, response_id, content, response_type, agent_id):
        """Analyze response and automatically generate new tasks."""
        try:
            # Analyze content for actionable insights
            analysis_result = self.analyze_content(content, response_type)
            
            # Store analysis
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO response_analysis 
                (response_id, analysis_type, analysis_result, confidence_score)
                VALUES (?, ?, ?, ?)
            ''', (response_id, 'content_analysis', json.dumps(analysis_result), 0.8))
            
            # Generate new tasks based on analysis
            new_tasks = self.generate_tasks_from_analysis(analysis_result, agent_id, response_id)
            
            for task in new_tasks:
                cursor.execute('''
                    INSERT INTO generated_tasks 
                    (source_response_id, task_title, task_description, assigned_agent, priority, dependencies)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (response_id, task['title'], task['description'], task['agent'], task['priority'], json.dumps(task['dependencies'])))
                
                print(f"🚀 Generated new task: {task['title']} -> {task['agent']}")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error in analysis and task generation: {e}")
    
    def analyze_content(self, content, response_type):
        """Analyze content for actionable insights."""
        analysis = {
            'type': response_type,
            'length': len(content),
            'contains_code': 'def ' in content or 'class ' in content,
            'contains_errors': 'error' in content.lower() or 'exception' in content.lower(),
            'contains_todos': 'todo' in content.lower() or 'fixme' in content.lower(),
            'contains_issues': 'issue' in content.lower() or 'bug' in content.lower(),
            'contains_recommendations': 'recommend' in content.lower() or 'should' in content.lower(),
            'completion_status': self.assess_completion_status(content, response_type)
        }
        
        return analysis
    
    def assess_completion_status(self, content, response_type):
        """Assess if the response indicates task completion."""
        if response_type == 'code_file':
            # Check if code looks complete
            if 'def ' in content and 'return ' in content:
                return 'likely_complete'
            elif 'class ' in content and 'def ' in content:
                return 'likely_complete'
            else:
                return 'incomplete'
        elif response_type == 'analysis_report':
            if 'conclusion' in content.lower() or 'summary' in content.lower():
                return 'likely_complete'
            else:
                return 'incomplete'
        
        return 'unknown'
    
    def generate_tasks_from_analysis(self, analysis, source_agent, response_id):
        """Generate new tasks based on content analysis."""
        new_tasks = []
        
        if analysis['contains_errors']:
            # Generate debug task
            new_tasks.append({
                'title': f"Debug Issues from {source_agent}",
                'description': f"Investigate and fix errors identified by {source_agent}",
                'agent': self.select_agent_for_task('debug'),
                'priority': 'high',
                'dependencies': [f'response_{response_id}']
            })
        
        if analysis['contains_todos']:
            # Generate implementation task
            new_tasks.append({
                'title': f"Implement TODOs from {source_agent}",
                'description': f"Complete TODO items identified by {source_agent}",
                'agent': self.select_agent_for_task('implementation'),
                'priority': 'medium',
                'dependencies': [f'response_{response_id}']
            })
        
        if analysis['contains_recommendations']:
            # Generate optimization task
            new_tasks.append({
                'title': f"Apply Recommendations from {source_agent}",
                'description': f"Implement recommendations from {source_agent}",
                'agent': self.select_agent_for_task('optimization'),
                'priority': 'medium',
                'dependencies': [f'response_{response_id}']
            })
        
        if analysis['completion_status'] == 'likely_complete':
            # Generate testing task
            new_tasks.append({
                'title': f"Test Completed Work from {source_agent}",
                'description': f"Verify and test the completed work from {source_agent}",
                'agent': self.select_agent_for_task('testing'),
                'priority': 'normal',
                'dependencies': [f'response_{response_id}']
            })
        
        return new_tasks
    
    def select_agent_for_task(self, task_type):
        """Intelligently select the best agent for a task type."""
        # This could be enhanced with agent capability matching
        agent_assignments = {
            'debug': 'Agent-4',  # Error & Health Systems
            'implementation': 'Agent-1',  # Scanner Services
            'optimization': 'Agent-3',  # Performance & Health
            'testing': 'Agent-2',  # Core System Analysis
        }
        
        return agent_assignments.get(task_type, 'Agent-1')
    
    def get_agent_progress_summary(self):
        """Get comprehensive progress summary for all agents."""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Get response counts by agent
        cursor.execute('''
            SELECT agent_id, COUNT(*) as response_count, 
                   SUM(file_size) as total_size,
                   MAX(timestamp) as last_response
            FROM agent_responses 
            GROUP BY agent_id
        ''')
        
        agent_stats = cursor.fetchall()
        
        # Get task generation stats
        cursor.execute('''
            SELECT COUNT(*) as total_tasks, 
                   COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks
            FROM generated_tasks
        ''')
        
        task_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'agent_stats': agent_stats,
            'task_stats': task_stats,
            'total_responses': sum(stat[1] for stat in agent_stats),
            'total_generated_tasks': task_stats[0] if task_stats else 0
        }

def main():
    """Main function to demonstrate the intelligent response capture system."""
    print("🚀 Intelligent Response Capture System - Agent Cellphone V2")
    print("=" * 60)
    
    # Initialize the system
    capture_system = IntelligentResponseCapture()
    
    # Show current progress summary
    print("\n📊 Current System Status:")
    summary = capture_system.get_agent_progress_summary()
    
    for agent_stat in summary['agent_stats']:
        agent_id, response_count, total_size, last_response = agent_stat
        print(f"  {agent_id}: {response_count} responses, {total_size or 0} bytes")
    
    print(f"\n🎯 Generated Tasks: {summary['total_generated_tasks']}")
    print(f"📈 Total Responses: {summary['total_responses']}")
    
    print("\n🔍 This system will automatically:")
    print("  • Capture all agent responses")
    print("  • Analyze content for actionable insights")
    print("  • Generate new tasks automatically")
    print("  • Build intelligent workflow chains")
    print("  • Provide comprehensive progress analytics")
    
    print("\n💡 The system transforms passive monitoring into active workflow orchestration!")

if __name__ == "__main__":
    main()
