#!/usr/bin/env python3
"""
Monitor Reporting - Agent Cellphone V2
======================================

Reporting and analytics for monitoring data.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timedelta

from .monitor_types import AgentInfo, AgentStatus


class MonitorReporter:
    """
    Generates reports and analytics from monitoring data.
    
    Responsibilities:
    - Generate status reports
    - Create performance analytics
    - Export monitoring data
    - Provide trend analysis
    """
    
    def __init__(self, output_dir: Path = None):
        self.logger = logging.getLogger(f"{__name__}.MonitorReporter")
        self.output_dir = output_dir or Path("monitor_reports")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_status_report(self, agent_statuses: Dict[str, AgentInfo], 
                             include_history: bool = False) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        try:
            total_agents = len(agent_statuses)
            online_agents = len([a for a in agent_statuses.values() if a.status == AgentStatus.ONLINE])
            busy_agents = len([a for a in agent_statuses.values() if a.status == AgentStatus.BUSY])
            offline_agents = len([a for a in agent_statuses.values() if a.status == AgentStatus.OFFLINE])
            error_agents = len([a for a in agent_statuses.values() if a.status == AgentStatus.ERROR])
            
            # Calculate performance metrics
            performance_scores = [a.performance_score for a in agent_statuses.values()]
            avg_performance = sum(performance_scores) / len(performance_scores) if performance_scores else 0.0
            
            # Calculate uptime metrics
            uptimes = [a.uptime for a in agent_statuses.values() if a.uptime > 0]
            avg_uptime = sum(uptimes) / len(uptimes) if uptimes else 0.0
            
            report = {
                'timestamp': time.time(),
                'report_type': 'status_summary',
                'summary': {
                    'total_agents': total_agents,
                    'online_agents': online_agents,
                    'busy_agents': busy_agents,
                    'offline_agents': offline_agents,
                    'error_agents': error_agents,
                    'availability_rate': (online_agents + busy_agents) / total_agents if total_agents > 0 else 0.0
                },
                'performance': {
                    'average_performance_score': round(avg_performance, 3),
                    'performance_distribution': self._calculate_performance_distribution(performance_scores),
                    'top_performers': self._get_top_performers(agent_statuses, 5)
                },
                'uptime': {
                    'average_uptime_hours': round(avg_uptime / 3600, 2),
                    'uptime_distribution': self._calculate_uptime_distribution(uptimes)
                },
                'capabilities': self._analyze_capabilities(agent_statuses)
            }
            
            if include_history:
                report['trends'] = self._generate_trend_analysis(agent_statuses)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Status report generation error: {e}")
            return {
                'timestamp': time.time(),
                'error': str(e),
                'status': 'failed'
            }
    
    def generate_performance_report(self, agent_statuses: Dict[str, AgentInfo]) -> Dict[str, Any]:
        """Generate detailed performance report"""
        try:
            performance_data = {}
            
            for agent_id, agent_info in agent_statuses.items():
                performance_data[agent_id] = {
                    'name': agent_info.name,
                    'status': agent_info.status.value,
                    'performance_score': agent_info.performance_score,
                    'uptime_hours': round(agent_info.uptime / 3600, 2),
                    'current_task': agent_info.current_task,
                    'capabilities': [c.value for c in agent_info.capabilities],
                    'resource_usage': agent_info.resource_usage,
                    'health_metrics': agent_info.health_metrics
                }
            
            # Performance rankings
            ranked_agents = sorted(agent_statuses.items(), 
                                 key=lambda x: x[1].performance_score, reverse=True)
            
            report = {
                'timestamp': time.time(),
                'report_type': 'performance_analysis',
                'performance_data': performance_data,
                'rankings': {
                    'top_performers': [{'agent_id': k, 'score': v.performance_score} 
                                     for k, v in ranked_agents[:5]],
                    'bottom_performers': [{'agent_id': k, 'score': v.performance_score} 
                                        for k, v in ranked_agents[-5:]]
                },
                'statistics': {
                    'total_agents': len(agent_statuses),
                    'average_score': sum(a.performance_score for a in agent_statuses.values()) / len(agent_statuses),
                    'score_range': {
                        'min': min(a.performance_score for a in agent_statuses.values()),
                        'max': max(a.performance_score for a in agent_statuses.values())
                    }
                }
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Performance report generation error: {e}")
            return {
                'timestamp': time.time(),
                'error': str(e),
                'status': 'failed'
            }
    
    def export_report_to_json(self, report: Dict[str, Any], filename: str = None) -> Path:
        """Export report to JSON file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"monitor_report_{timestamp}.json"
            
            file_path = self.output_dir / filename
            
            with open(file_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"Report exported to {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Report export error: {e}")
            raise
    
    def generate_trend_report(self, status_history: List[Dict[str, Any]], 
                            hours: int = 24) -> Dict[str, Any]:
        """Generate trend analysis report"""
        try:
            if not status_history:
                return {'status': 'no_data', 'message': 'No history data available'}
            
            # Filter recent history
            cutoff_time = time.time() - (hours * 3600)
            recent_history = [h for h in status_history if h.get('timestamp', 0) > cutoff_time]
            
            if not recent_history:
                return {'status': 'no_recent_data', 'message': f'No data in last {hours} hours'}
            
            # Analyze trends
            timestamps = [h.get('timestamp', 0) for h in recent_history]
            agent_counts = [h.get('agent_count', 0) for h in recent_history]
            online_counts = [h.get('online_count', 0) for h in recent_history]
            
            # Calculate trends
            trend_data = {
                'period_hours': hours,
                'data_points': len(recent_history),
                'agent_count_trend': self._calculate_trend(agent_counts),
                'online_count_trend': self._calculate_trend(online_counts),
                'availability_trend': self._calculate_availability_trend(recent_history),
                'hourly_breakdown': self._generate_hourly_breakdown(recent_history)
            }
            
            return {
                'timestamp': time.time(),
                'report_type': 'trend_analysis',
                'trend_data': trend_data
            }
            
        except Exception as e:
            self.logger.error(f"Trend report generation error: {e}")
            return {
                'timestamp': time.time(),
                'error': str(e),
                'status': 'failed'
            }
    
    def _calculate_performance_distribution(self, scores: List[float]) -> Dict[str, int]:
        """Calculate performance score distribution"""
        distribution = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        for score in scores:
            if score >= 0.8: distribution['excellent'] += 1
            elif score >= 0.6: distribution['good'] += 1
            elif score >= 0.4: distribution['fair'] += 1
            else: distribution['poor'] += 1
        return distribution
    
    def _calculate_uptime_distribution(self, uptimes: List[float]) -> Dict[str, int]:
        """Calculate uptime distribution"""
        distribution = {'<1h': 0, '1-6h': 0, '6-24h': 0, '>24h': 0}
        for uptime in uptimes:
            hours = uptime / 3600
            if hours < 1: distribution['<1h'] += 1
            elif hours < 6: distribution['1-6h'] += 1
            elif hours < 24: distribution['6-24h'] += 1
            else: distribution['>24h'] += 1
        return distribution
    
    def _get_top_performers(self, agent_statuses: Dict[str, AgentInfo], count: int) -> List[Dict[str, Any]]:
        """Get top performing agents"""
        sorted_agents = sorted(agent_statuses.items(), key=lambda x: x[1].performance_score, reverse=True)
        return [{'agent_id': agent_id, 'name': agent_info.name, 'performance_score': agent_info.performance_score,
                'status': agent_info.status.value} for agent_id, agent_info in sorted_agents[:count]]
    
    def _analyze_capabilities(self, agent_statuses: Dict[str, AgentInfo]) -> Dict[str, Any]:
        """Analyze agent capabilities distribution"""
        capability_counts = {}
        total_agents = len(agent_statuses)
        for agent_info in agent_statuses.values():
            for capability in agent_info.capabilities:
                capability_counts[capability.value] = capability_counts.get(capability.value, 0) + 1
        return {'total_agents': total_agents, 'capability_distribution': capability_counts,
                'average_capabilities_per_agent': sum(len(a.capabilities) for a in agent_statuses.values()) / total_agents if total_agents > 0 else 0}
    
    def _calculate_trend(self, values: List[float]) -> Dict[str, float]:
        """Calculate trend direction and magnitude"""
        if len(values) < 2:
            return {'direction': 'stable', 'magnitude': 0.0}
        
        # Simple linear trend calculation
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        avg_first = sum(first_half) / len(first_half) if first_half else 0
        avg_second = sum(second_half) / len(second_half) if second_half else 0
        
        change = avg_second - avg_first
        magnitude = abs(change)
        
        if change > 0:
            direction = 'increasing'
        elif change < 0:
            direction = 'decreasing'
        else:
            direction = 'stable'
        
        return {
            'direction': direction,
            'magnitude': round(magnitude, 3),
            'change_percent': round((change / avg_first * 100) if avg_first > 0 else 0, 2)
        }
    
    def _calculate_availability_trend(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate availability trend over time"""
        availability_rates = []
        
        for entry in history:
            agent_count = entry.get('agent_count', 0)
            online_count = entry.get('online_count', 0)
            
            if agent_count > 0:
                availability_rate = online_count / agent_count
                availability_rates.append(availability_rate)
        
        if availability_rates:
            return {
                'average_availability': round(sum(availability_rates) / len(availability_rates), 3),
                'trend': self._calculate_trend(availability_rates)
            }
        
        return {'average_availability': 0.0, 'trend': {'direction': 'stable', 'magnitude': 0.0}}
    
    def _generate_hourly_breakdown(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate hourly breakdown of monitoring data"""
        hourly_data = {}
        
        for entry in history:
            timestamp = entry.get('timestamp', 0)
            if timestamp > 0:
                hour = datetime.fromtimestamp(timestamp).strftime("%H:00")
                if hour not in hourly_data:
                    hourly_data[hour] = {'count': 0, 'online': 0}
                
                hourly_data[hour]['count'] += 1
                hourly_data[hour]['online'] += entry.get('online_count', 0)
        
        return hourly_data
