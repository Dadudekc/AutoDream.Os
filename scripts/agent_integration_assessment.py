#!/usr/bin/env python3
"""
Agent Integration Assessment Script
Agent_Cellphone_V2_Repository - Multi-Agent Web Integration

Purpose: Automatically assess each agent's current web integration status
Output: Detailed integration requirements and priority matrix
"""

import os
import sys
import json
import time
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess
import importlib.util

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class AgentIntegrationAssessment:
    """
    Comprehensive assessment of all agent systems for web integration
    """
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.assessment_results = {}
        self.agent_configs = {}
        self.integration_priorities = {}
        self.web_requirements = {}
        
        # Setup logging
        self._setup_logging()
        
        # Load agent configurations
        self._load_agent_configs()
        
        # Initialize assessment results
        self._initialize_assessment_results()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('agent_integration_assessment.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_agent_configs(self):
        """Load agent configurations and roles"""
        try:
            # Load agent roles
            roles_file = self.repo_root / "config" / "agents" / "agent_roles.json"
            if roles_file.exists():
                with open(roles_file, 'r') as f:
                    self.agent_configs['roles'] = json.load(f)
                self.logger.info("✅ Agent roles loaded successfully")
            else:
                self.logger.warning("⚠️ Agent roles file not found")
                self.agent_configs['roles'] = {}
            
            # Load agent locations
            locations_file = self.repo_root / "agent_complete_locations.json"
            if locations_file.exists():
                with open(locations_file, 'r') as f:
                    self.agent_configs['locations'] = json.load(f)
                self.logger.info("✅ Agent locations loaded successfully")
            else:
                self.logger.warning("⚠️ Agent locations file not found")
                self.agent_configs['locations'] = {}
                
        except Exception as e:
            self.logger.error(f"❌ Error loading agent configs: {e}")
            self.agent_configs = {}
    
    def _initialize_assessment_results(self):
        """Initialize assessment results structure"""
        self.assessment_results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'pending',
            'agents': {},
            'integration_priorities': [],
            'web_requirements': {},
            'recommendations': []
        }
    
    async def assess_all_agents(self) -> Dict[str, Any]:
        """
        Assess all agent systems for web integration readiness
        """
        self.logger.info("🚀 Starting comprehensive agent integration assessment...")
        
        # Define agent assessment order (priority-based)
        agent_assessment_order = [
            'Agent-1',  # Foundation & Testing - High priority
            'Agent-5',  # Business Intelligence - High priority
            'Agent-4',  # Security & Infrastructure - High priority
            'Agent-2',  # AI & ML Integration - Medium priority
            'Agent-3',  # Multimedia & Content - Medium priority
            'Agent-6',  # Gaming & Entertainment - Medium priority
            'Agent-8',  # Integration & Performance - Medium priority
            'Agent-7'   # Web Development - Already complete
        ]
        
        for agent_id in agent_assessment_order:
            self.logger.info(f"🔍 Assessing {agent_id}...")
            agent_result = await self._assess_single_agent(agent_id)
            self.assessment_results['agents'][agent_id] = agent_result
            
            # Brief pause between assessments
            await asyncio.sleep(0.5)
        
        # Generate integration priorities and recommendations
        self._generate_integration_priorities()
        self._generate_web_requirements()
        self._generate_recommendations()
        
        # Update overall status
        self._update_overall_status()
        
        self.logger.info("✅ Agent integration assessment completed successfully")
        return self.assessment_results
    
    async def _assess_single_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Assess a single agent system
        """
        try:
            agent_info = self._get_agent_info(agent_id)
            
            # Perform system assessment
            system_status = await self._assess_agent_system(agent_id)
            
            # Assess web integration readiness
            web_readiness = await self._assess_web_readiness(agent_id)
            
            # Assess integration complexity
            integration_complexity = self._assess_integration_complexity(agent_id)
            
            # Compile assessment result
            result = {
                'agent_id': agent_id,
                'agent_info': agent_info,
                'system_status': system_status,
                'web_readiness': web_readiness,
                'integration_complexity': integration_complexity,
                'integration_priority': self._calculate_integration_priority(agent_id, web_readiness, integration_complexity),
                'estimated_effort': self._estimate_integration_effort(integration_complexity),
                'dependencies': self._identify_dependencies(agent_id),
                'recommendations': self._generate_agent_recommendations(agent_id, web_readiness, integration_complexity)
            }
            
            self.logger.info(f"✅ {agent_id} assessment completed - Priority: {result['integration_priority']}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error assessing {agent_id}: {e}")
            return {
                'agent_id': agent_id,
                'error': str(e),
                'status': 'failed'
            }
    
    def _get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        """Get basic agent information"""
        info = {
            'id': agent_id,
            'name': 'Unknown',
            'role': 'Unknown',
            'location': None,
            'status': 'unknown'
        }
        
        # Get role information
        if 'roles' in self.agent_configs and agent_id in self.agent_configs['roles']['roles']:
            role_data = self.agent_configs['roles']['roles'][agent_id]
            info['role'] = role_data.get('primary', 'Unknown')
            info['capabilities'] = role_data.get('capabilities', [])
        
        # Get location information
        if 'locations' in self.agent_configs and agent_id in self.agent_configs['locations']:
            location_data = self.agent_configs['locations'][agent_id]
            info['name'] = location_data.get('name', 'Unknown')
            info['location'] = location_data.get('input_location', None)
        
        return info
    
    async def _assess_agent_system(self, agent_id: str) -> Dict[str, Any]:
        """
        Assess the current system status of an agent
        """
        system_status = {
            'operational': False,
            'web_interface': False,
            'api_endpoints': False,
            'data_sources': False,
            'integration_points': False,
            'health_status': 'unknown'
        }
        
        try:
            # Check if agent has existing web components
            web_components = self._check_web_components(agent_id)
            system_status.update(web_components)
            
            # Check agent-specific directories and files
            agent_files = self._check_agent_files(agent_id)
            system_status.update(agent_files)
            
            # Check for existing APIs or services
            api_status = await self._check_api_status(agent_id)
            system_status.update(api_status)
            
            # Determine overall operational status
            system_status['operational'] = any([
                system_status['web_interface'],
                system_status['api_endpoints'],
                system_status['data_sources']
            ])
            
            # Set health status
            if system_status['operational']:
                system_status['health_status'] = 'healthy'
            elif system_status['web_interface'] or system_status['api_endpoints']:
                system_status['health_status'] = 'partial'
            else:
                system_status['health_status'] = 'inactive'
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error assessing system status for {agent_id}: {e}")
            system_status['health_status'] = 'error'
        
        return system_status
    
    def _check_web_components(self, agent_id: str) -> Dict[str, Any]:
        """Check for existing web components"""
        web_status = {
            'web_interface': False,
            'web_templates': False,
            'web_static_files': False,
            'web_scripts': False
        }
        
        try:
            # Check for web-related directories
            web_dirs = [
                f"src/web/{agent_id.lower()}",
                f"templates/{agent_id.lower()}",
                f"static/{agent_id.lower()}",
                f"scripts/{agent_id.lower()}_web"
            ]
            
            for web_dir in web_dirs:
                dir_path = self.repo_root / web_dir
                if dir_path.exists():
                    if 'web' in web_dir:
                        web_status['web_interface'] = True
                    elif 'templates' in web_dir:
                        web_status['web_templates'] = True
                    elif 'static' in web_dir:
                        web_status['web_static_files'] = True
                    elif 'scripts' in web_dir:
                        web_status['web_scripts'] = True
            
            # Check for web-related files
            web_files = [
                f"{agent_id.lower()}_web.py",
                f"{agent_id.lower()}_portal.py",
                f"{agent_id.lower()}_dashboard.py"
            ]
            
            for web_file in web_files:
                file_path = self.repo_root / "src" / "web" / web_file
                if file_path.exists():
                    web_status['web_interface'] = True
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Error checking web components for {agent_id}: {e}")
        
        return web_status
    
    def _check_agent_files(self, agent_id: str) -> Dict[str, Any]:
        """Check for agent-specific files and directories"""
        file_status = {
            'data_sources': False,
            'config_files': False,
            'log_files': False,
            'test_files': False
        }
        
        try:
            # Check for agent-specific directories
            agent_dirs = [
                f"data/{agent_id.lower()}",
                f"config/{agent_id.lower()}",
                f"logs/{agent_id.lower()}",
                f"tests/{agent_id.lower()}"
            ]
            
            for agent_dir in agent_dirs:
                dir_path = self.repo_root / agent_dir
                if dir_path.exists():
                    if 'data' in agent_dir:
                        file_status['data_sources'] = True
                    elif 'config' in agent_dir:
                        file_status['config_files'] = True
                    elif 'logs' in agent_dir:
                        file_status['log_files'] = True
                    elif 'tests' in agent_dir:
                        file_status['test_files'] = True
            
            # Check for agent-specific files
            agent_files = [
                f"{agent_id.lower()}_config.json",
                f"{agent_id.lower()}_data.json",
                f"{agent_id.lower()}_status.json"
            ]
            
            for agent_file in agent_files:
                file_path = self.repo_root / "config" / agent_file
                if file_path.exists():
                    file_status['config_files'] = True
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Error checking agent files for {agent_id}: {e}")
        
        return file_status
    
    async def _check_api_status(self, agent_id: str) -> Dict[str, Any]:
        """Check for existing API endpoints or services"""
        api_status = {
            'api_endpoints': False,
            'rest_api': False,
            'websocket_api': False,
            'grpc_api': False
        }
        
        try:
            # Check for API-related files
            api_files = [
                f"{agent_id.lower()}_api.py",
                f"{agent_id.lower()}_service.py",
                f"{agent_id.lower()}_endpoints.py"
            ]
            
            for api_file in api_files:
                file_path = self.repo_root / "src" / "web" / api_file
                if file_path.exists():
                    api_status['api_endpoints'] = True
                    api_status['rest_api'] = True
            
            # Check for service definitions
            service_files = [
                f"services/{agent_id.lower()}_service.py",
                f"api/{agent_id.lower()}_endpoints.py"
            ]
            
            for service_file in service_files:
                file_path = self.repo_root / "src" / service_file
                if file_path.exists():
                    api_status['api_endpoints'] = True
                    
        except Exception as e:
            self.logger.warning(f"⚠️ Error checking API status for {agent_id}: {e}")
        
        return api_status
    
    async def _assess_web_readiness(self, agent_id: str) -> Dict[str, Any]:
        """
        Assess how ready an agent is for web integration
        """
        readiness = {
            'score': 0,  # 0-100
            'level': 'not_ready',
            'web_experience': 'none',
            'integration_complexity': 'high',
            'estimated_timeline': 'unknown'
        }
        
        try:
            # Calculate readiness score based on existing components
            score = 0
            
            # Check for existing web components (30 points)
            if self._has_web_components(agent_id):
                score += 30
                readiness['web_experience'] = 'basic'
            
            # Check for API endpoints (25 points)
            if self._has_api_endpoints(agent_id):
                score += 25
                readiness['web_experience'] = 'intermediate'
            
            # Check for data sources (20 points)
            if self._has_data_sources(agent_id):
                score += 20
            
            # Check for configuration files (15 points)
            if self._has_config_files(agent_id):
                score += 15
            
            # Check for test files (10 points)
            if self._has_test_files(agent_id):
                score += 10
            
            readiness['score'] = score
            
            # Determine readiness level
            if score >= 80:
                readiness['level'] = 'ready'
                readiness['estimated_timeline'] = '1-2 days'
            elif score >= 60:
                readiness['level'] = 'mostly_ready'
                readiness['estimated_timeline'] = '2-3 days'
            elif score >= 40:
                readiness['level'] = 'partially_ready'
                readiness['estimated_timeline'] = '3-5 days'
            elif score >= 20:
                readiness['level'] = 'minimally_ready'
                readiness['estimated_timeline'] = '5-7 days'
            else:
                readiness['level'] = 'not_ready'
                readiness['estimated_timeline'] = '7-10 days'
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error assessing web readiness for {agent_id}: {e}")
            readiness['level'] = 'error'
        
        return readiness
    
    def _has_web_components(self, agent_id: str) -> bool:
        """Check if agent has web components"""
        try:
            web_dirs = [
                f"src/web/{agent_id.lower()}",
                f"templates/{agent_id.lower()}",
                f"static/{agent_id.lower()}"
            ]
            
            for web_dir in web_dirs:
                dir_path = self.repo_root / web_dir
                if dir_path.exists():
                    return True
            
            # Check for web files
            web_files = [
                f"{agent_id.lower()}_web.py",
                f"{agent_id.lower()}_portal.py"
            ]
            
            for web_file in web_files:
                file_path = self.repo_root / "src" / "web" / web_file
                if file_path.exists():
                    return True
            
            return False
        except:
            return False
    
    def _has_api_endpoints(self, agent_id: str) -> bool:
        """Check if agent has API endpoints"""
        try:
            api_files = [
                f"{agent_id.lower()}_api.py",
                f"{agent_id.lower()}_service.py"
            ]
            
            for api_file in api_files:
                file_path = self.repo_root / "src" / "web" / api_file
                if file_path.exists():
                    return True
            
            return False
        except:
            return False
    
    def _has_data_sources(self, agent_id: str) -> bool:
        """Check if agent has data sources"""
        try:
            data_dir = self.repo_root / "data" / agent_id.lower()
            return data_dir.exists()
        except:
            return False
    
    def _has_config_files(self, agent_id: str) -> bool:
        """Check if agent has configuration files"""
        try:
            config_file = self.repo_root / "config" / f"{agent_id.lower()}_config.json"
            return config_file.exists()
        except:
            return False
    
    def _has_test_files(self, agent_id: str) -> bool:
        """Check if agent has test files"""
        try:
            test_dir = self.repo_root / "tests" / agent_id.lower()
            return test_dir.exists()
        except:
            return False
    
    def _assess_integration_complexity(self, agent_id: str) -> Dict[str, Any]:
        """
        Assess the complexity of integrating an agent with web systems
        """
        complexity = {
            'level': 'medium',
            'factors': [],
            'risk_level': 'medium',
            'estimated_effort': 'medium'
        }
        
        try:
            factors = []
            risk_score = 0
            
            # Check agent role complexity
            if agent_id in ['Agent-1', 'Agent-5']:  # High priority agents
                factors.append('high_priority_integration')
                risk_score += 2
            
            # Check for existing web components
            if self._has_web_components(agent_id):
                factors.append('existing_web_components')
                risk_score -= 1
            
            # Check for API endpoints
            if self._has_api_endpoints(agent_id):
                factors.append('existing_api_endpoints')
                risk_score -= 1
            
            # Check for data sources
            if self._has_data_sources(agent_id):
                factors.append('data_sources_available')
                risk_score -= 1
            
            # Check for configuration files
            if self._has_config_files(agent_id):
                factors.append('configuration_available')
                risk_score -= 1
            
            complexity['factors'] = factors
            
            # Determine complexity level based on risk score
            if risk_score <= -2:
                complexity['level'] = 'low'
                complexity['risk_level'] = 'low'
                complexity['estimated_effort'] = 'low'
            elif risk_score <= 0:
                complexity['level'] = 'medium'
                complexity['risk_level'] = 'medium'
                complexity['estimated_effort'] = 'medium'
            else:
                complexity['level'] = 'high'
                complexity['risk_level'] = 'high'
                complexity['estimated_effort'] = 'high'
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error assessing integration complexity for {agent_id}: {e}")
            complexity['level'] = 'unknown'
            complexity['risk_level'] = 'high'
        
        return complexity
    
    def _calculate_integration_priority(self, agent_id: str, web_readiness: Dict[str, Any], integration_complexity: Dict[str, Any]) -> str:
        """Calculate integration priority for an agent"""
        try:
            # High priority agents
            if agent_id in ['Agent-1', 'Agent-5']:
                return 'high'
            
            # Medium priority agents
            if agent_id in ['Agent-2', 'Agent-4']:
                return 'medium'
            
            # Lower priority agents
            if agent_id in ['Agent-3', 'Agent-6', 'Agent-8']:
                return 'low'
            
            # Agent-7 is already complete
            if agent_id == 'Agent-7':
                return 'complete'
            
            return 'medium'
            
        except Exception as e:
            self.logger.warning(f"⚠️ Error calculating priority for {agent_id}: {e}")
            return 'medium'
    
    def _estimate_integration_effort(self, integration_complexity: Dict[str, Any]) -> str:
        """Estimate integration effort based on complexity"""
        complexity_level = integration_complexity.get('level', 'medium')
        
        effort_mapping = {
            'low': '1-2 days',
            'medium': '3-5 days',
            'high': '5-10 days',
            'unknown': '5-10 days'
        }
        
        return effort_mapping.get(complexity_level, '3-5 days')
    
    def _identify_dependencies(self, agent_id: str) -> List[str]:
        """Identify dependencies for agent integration"""
        dependencies = []
        
        try:
            # Common dependencies
            dependencies.extend([
                'web_development_environment',
                'unified_api_gateway',
                'authentication_system',
                'ui_component_library'
            ])
            
            # Agent-specific dependencies
            if agent_id == 'Agent-1':  # Foundation & Testing
                dependencies.extend([
                    'task_management_system',
                    'testing_framework_integration',
                    'coordination_hub'
                ])
            elif agent_id == 'Agent-2':  # AI & ML Integration
                dependencies.extend([
                    'ml_model_management',
                    'data_processing_pipeline',
                    'ai_workflow_visualization'
                ])
            elif agent_id == 'Agent-3':  # Multimedia & Content
                dependencies.extend([
                    'content_management_system',
                    'media_processing_interface',
                    'creative_workflow_dashboard'
                ])
            elif agent_id == 'Agent-4':  # Security & Infrastructure
                dependencies.extend([
                    'security_monitoring_dashboard',
                    'infrastructure_health_portal',
                    'threat_detection_interface'
                ])
            elif agent_id == 'Agent-5':  # Business Intelligence
                dependencies.extend([
                    'bi_dashboard',
                    'quality_metrics_interface',
                    'business_process_monitoring'
                ])
            elif agent_id == 'Agent-6':  # Gaming & Entertainment
                dependencies.extend([
                    'gaming_platform_interface',
                    'entertainment_content_portal',
                    'user_engagement_dashboard'
                ])
            elif agent_id == 'Agent-8':  # Integration & Performance
                dependencies.extend([
                    'performance_monitoring_dashboard',
                    'integration_status_portal',
                    'system_optimization_interface'
                ])
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error identifying dependencies for {agent_id}: {e}")
            dependencies = ['error_occurred']
        
        return dependencies
    
    def _generate_agent_recommendations(self, agent_id: str, web_readiness: Dict[str, Any], integration_complexity: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for agent integration"""
        recommendations = []
        
        try:
            readiness_level = web_readiness.get('level', 'not_ready')
            complexity_level = integration_complexity.get('level', 'medium')
            
            # General recommendations based on readiness
            if readiness_level == 'not_ready':
                recommendations.extend([
                    'Create basic web infrastructure',
                    'Establish data sources and configuration',
                    'Implement core API endpoints'
                ])
            elif readiness_level == 'minimally_ready':
                recommendations.extend([
                    'Enhance existing web components',
                    'Standardize API structure',
                    'Implement authentication and authorization'
                ])
            elif readiness_level == 'partially_ready':
                recommendations.extend([
                    'Complete web interface development',
                    'Integrate with unified API gateway',
                    'Implement real-time communication'
                ])
            elif readiness_level == 'mostly_ready':
                recommendations.extend([
                    'Finalize integration testing',
                    'Optimize performance and security',
                    'Deploy to production environment'
                ])
            elif readiness_level == 'ready':
                recommendations.extend([
                    'Conduct final validation',
                    'Document integration procedures',
                    'Prepare for production deployment'
                ])
            
            # Complexity-based recommendations
            if complexity_level == 'high':
                recommendations.extend([
                    'Implement phased integration approach',
                    'Establish comprehensive testing strategy',
                    'Create fallback mechanisms'
                ])
            elif complexity_level == 'medium':
                recommendations.extend([
                    'Follow standard integration patterns',
                    'Implement incremental testing',
                    'Monitor integration progress'
                ])
            elif complexity_level == 'low':
                recommendations.extend([
                    'Proceed with standard integration',
                    'Implement basic testing',
                    'Deploy when ready'
                ])
            
            # Agent-specific recommendations
            if agent_id == 'Agent-1':
                recommendations.extend([
                    'Prioritize coordination hub development',
                    'Implement task management interface',
                    'Establish testing dashboard'
                ])
            elif agent_id == 'Agent-5':
                recommendations.extend([
                    'Focus on BI dashboard development',
                    'Implement quality metrics display',
                    'Create business process monitoring'
                ])
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error generating recommendations for {agent_id}: {e}")
            recommendations = ['Error occurred during recommendation generation']
        
        return recommendations
    
    def _generate_integration_priorities(self):
        """Generate integration priority matrix"""
        try:
            priorities = []
            
            for agent_id, agent_data in self.assessment_results['agents'].items():
                if isinstance(agent_data, dict) and 'integration_priority' in agent_data:
                    priority = agent_data['integration_priority']
                    estimated_effort = agent_data.get('estimated_effort', 'unknown')
                    
                    priorities.append({
                        'agent_id': agent_id,
                        'priority': priority,
                        'estimated_effort': estimated_effort,
                        'readiness_score': agent_data.get('web_readiness', {}).get('score', 0),
                        'complexity_level': agent_data.get('integration_complexity', {}).get('level', 'unknown')
                    })
            
            # Sort by priority and readiness
            priorities.sort(key=lambda x: (
                {'high': 3, 'medium': 2, 'low': 1, 'complete': 0}.get(x['priority'], 1),
                -x['readiness_score']
            ), reverse=True)
            
            self.assessment_results['integration_priorities'] = priorities
            
        except Exception as e:
            self.logger.error(f"❌ Error generating integration priorities: {e}")
    
    def _generate_web_requirements(self):
        """Generate comprehensive web requirements"""
        try:
            requirements = {
                'infrastructure': [
                    'Unified Web API Gateway',
                    'Cross-Agent Communication Layer',
                    'Shared Authentication System',
                    'Common UI Component Library'
                ],
                'agent_portals': [],
                'integration_apis': [],
                'monitoring_tools': [
                    'System Health Dashboard',
                    'Integration Status Monitor',
                    'Performance Metrics Display'
                ]
            }
            
            # Generate agent-specific requirements
            for agent_id, agent_data in self.assessment_results['agents'].items():
                if isinstance(agent_data, dict):
                    agent_name = agent_data.get('agent_info', {}).get('name', agent_id)
                    requirements['agent_portals'].append(f"{agent_name} Web Portal")
                    requirements['integration_apis'].append(f"{agent_name} Integration API")
            
            self.assessment_results['web_requirements'] = requirements
            
        except Exception as e:
            self.logger.error(f"❌ Error generating web requirements: {e}")
    
    def _generate_recommendations(self):
        """Generate overall recommendations"""
        try:
            recommendations = [
                'Establish unified web integration framework',
                'Implement cross-agent communication protocols',
                'Create consistent UI/UX design system',
                'Establish comprehensive testing strategy',
                'Implement monitoring and alerting systems',
                'Create integration documentation and guides',
                'Establish deployment and rollback procedures'
            ]
            
            # Add agent-specific recommendations
            for agent_id, agent_data in self.assessment_results['agents'].items():
                if isinstance(agent_data, dict) and 'recommendations' in agent_data:
                    agent_recs = agent_data['recommendations']
                    if isinstance(agent_recs, list) and len(agent_recs) > 0:
                        recommendations.extend([f"{agent_id}: {rec}" for rec in agent_recs[:2]])
            
            self.assessment_results['recommendations'] = recommendations
            
        except Exception as e:
            self.logger.error(f"❌ Error generating recommendations: {e}")
    
    def _update_overall_status(self):
        """Update overall assessment status"""
        try:
            total_agents = len(self.assessment_results['agents'])
            completed_agents = 0
            ready_agents = 0
            in_progress_agents = 0
            
            for agent_id, agent_data in self.assessment_results['agents'].items():
                if isinstance(agent_data, dict):
                    if agent_data.get('integration_priority') == 'complete':
                        completed_agents += 1
                    elif agent_data.get('web_readiness', {}).get('level') in ['ready', 'mostly_ready']:
                        ready_agents += 1
                    elif agent_data.get('web_readiness', {}).get('level') in ['partially_ready', 'minimally_ready']:
                        in_progress_agents += 1
            
            # Calculate completion percentage
            completion_percentage = (completed_agents / total_agents) * 100 if total_agents > 0 else 0
            
            # Determine overall status
            if completion_percentage >= 100:
                status = 'complete'
            elif completion_percentage >= 75:
                status = 'nearly_complete'
            elif completion_percentage >= 50:
                status = 'in_progress'
            elif completion_percentage >= 25:
                status = 'started'
            else:
                status = 'not_started'
            
            self.assessment_results['overall_status'] = status
            self.assessment_results['completion_percentage'] = completion_percentage
            self.assessment_results['agent_counts'] = {
                'total': total_agents,
                'completed': completed_agents,
                'ready': ready_agents,
                'in_progress': in_progress_agents
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error updating overall status: {e}")
            self.assessment_results['overall_status'] = 'error'
    
    def save_assessment_results(self, output_file: str = None) -> str:
        """Save assessment results to file"""
        try:
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"agent_integration_assessment_{timestamp}.json"
            
            output_path = self.repo_root / "reports" / output_file
            
            # Ensure reports directory exists
            output_path.parent.mkdir(exist_ok=True)
            
            # Save results
            with open(output_path, 'w') as f:
                json.dump(self.assessment_results, f, indent=2, default=str)
            
            self.logger.info(f"✅ Assessment results saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"❌ Error saving assessment results: {e}")
            return ""
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report"""
        try:
            summary = []
            summary.append("# 🌐 Agent Integration Assessment Summary")
            summary.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            summary.append(f"**Overall Status**: {self.assessment_results.get('overall_status', 'unknown')}")
            summary.append(f"**Completion**: {self.assessment_results.get('completion_percentage', 0):.1f}%")
            summary.append("")
            
            # Agent counts
            counts = self.assessment_results.get('agent_counts', {})
            summary.append("## 📊 Agent Status Summary")
            summary.append(f"- **Total Agents**: {counts.get('total', 0)}")
            summary.append(f"- **Completed**: {counts.get('completed', 0)}")
            summary.append(f"- **Ready**: {counts.get('ready', 0)}")
            summary.append(f"- **In Progress**: {counts.get('in_progress', 0)}")
            summary.append("")
            
            # Integration priorities
            summary.append("## 🎯 Integration Priorities")
            priorities = self.assessment_results.get('integration_priorities', [])
            for i, priority in enumerate(priorities[:5], 1):
                summary.append(f"{i}. **{priority['agent_id']}** - {priority['priority'].title()} Priority")
                summary.append(f"   - Effort: {priority['estimated_effort']}")
                summary.append(f"   - Readiness: {priority['readiness_score']}/100")
                summary.append(f"   - Complexity: {priority['complexity_level'].title()}")
                summary.append("")
            
            # Key recommendations
            summary.append("## 💡 Key Recommendations")
            recommendations = self.assessment_results.get('recommendations', [])
            for i, rec in enumerate(recommendations[:5], 1):
                summary.append(f"{i}. {rec}")
            summary.append("")
            
            # Next steps
            summary.append("## 🚀 Next Steps")
            summary.append("1. **Immediate**: Begin high-priority agent integrations")
            summary.append("2. **Short-term**: Establish unified web infrastructure")
            summary.append("3. **Medium-term**: Complete all agent portal integrations")
            summary.append("4. **Long-term**: Optimize and scale the integrated system")
            
            return "\n".join(summary)
            
        except Exception as e:
            self.logger.error(f"❌ Error generating summary report: {e}")
            return f"Error generating summary report: {e}"

async def main():
    """Main execution function"""
    try:
        print("🚀 Starting Agent Integration Assessment...")
        print("=" * 60)
        
        # Create assessment instance
        assessment = AgentIntegrationAssessment()
        
        # Run comprehensive assessment
        results = await assessment.assess_all_agents()
        
        # Save results
        output_file = assessment.save_assessment_results()
        
        # Generate and display summary
        summary = assessment.generate_summary_report()
        print("\n" + "=" * 60)
        print("📋 ASSESSMENT SUMMARY")
        print("=" * 60)
        print(summary)
        print("\n" + "=" * 60)
        print(f"📁 Detailed results saved to: {output_file}")
        print("🎯 Ready for next phase: Cross-Agent Communication Protocol Design")
        print("=" * 60)
        
        return results
        
    except Exception as e:
        print(f"❌ Error during assessment: {e}")
        logging.error(f"Assessment failed: {e}")
        return None

if __name__ == "__main__":
    # Run the assessment
    asyncio.run(main())
