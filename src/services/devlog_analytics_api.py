"""
Devlog Analytics API
===================

REST API endpoints for querying and analyzing devlog data from the vector database.
Provides analytics, trends, and export capabilities for the agent devlog system.
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json
import csv
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# Import vector database integration
from vector_database.vector_database_integration import VectorDatabaseIntegration

logger = logging.getLogger(__name__)

class DevlogAnalyticsAPI:
    """REST API for devlog analytics and querying."""

    def __init__(self, host: str = "localhost", port: int = 8002):
        """Initialize the devlog analytics API."""
        self.app = Flask(__name__)
        CORS(self.app)

        self.host = host
        self.port = port

        # Initialize vector database with default path
        db_path = Path("data") / "vector_database.db"
        db_path.parent.mkdir(exist_ok=True)
        self.vector_db = VectorDatabaseIntegration(str(db_path))

        # Setup routes
        self._setup_routes()

        logger.info(f"DevlogAnalyticsAPI initialized on {host}:{port}")

    def _setup_routes(self):
        """Setup API routes."""

        @self.app.route('/api/devlogs')
        def get_devlogs():
            """Get devlogs with optional filtering."""
            try:
                # Parse query parameters
                agent_id = request.args.get('agent_id')
                status = request.args.get('status')
                limit = int(request.args.get('limit', 50))
                offset = int(request.args.get('offset', 0))
                date_from = request.args.get('date_from')
                date_to = request.args.get('date_to')

                # Build metadata filter
                metadata_filter = {}

                if agent_id:
                    metadata_filter['agent_id'] = agent_id

                if status:
                    metadata_filter['status'] = status

                if date_from or date_to:
                    date_filter = {}
                    if date_from:
                        date_filter['$gte'] = date_from
                    if date_to:
                        date_filter['$lte'] = date_to
                    metadata_filter['timestamp'] = date_filter

                # Query vector database
                devlogs = self.vector_db.query(
                    query="devlog entry",
                    namespace="agent_devlogs",
                    metadata_filter=metadata_filter if metadata_filter else None,
                    limit=limit,
                    offset=offset
                )

                return jsonify({
                    'success': True,
                    'data': devlogs,
                    'filters': {
                        'agent_id': agent_id,
                        'status': status,
                        'limit': limit,
                        'offset': offset,
                        'date_from': date_from,
                        'date_to': date_to
                    }
                })

            except Exception as e:
                logger.error(f"Error getting devlogs: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/devlogs/analytics')
        def get_devlog_analytics():
            """Get analytics data for devlogs."""
            try:
                # Get analytics data
                analytics = self._generate_analytics()

                return jsonify({
                    'success': True,
                    'data': analytics
                })

            except Exception as e:
                logger.error(f"Error getting analytics: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/devlogs/export/<format>')
        def export_devlogs(format: str):
            """Export devlogs in specified format."""
            try:
                format = format.lower()

                # Get devlogs data
                devlogs_data = self._get_export_data()

                if format == 'json':
                    return self._export_json(devlogs_data)
                elif format == 'csv':
                    return self._export_csv(devlogs_data)
                elif format == 'excel':
                    return self._export_excel(devlogs_data)
                else:
                    return jsonify({
                        'success': False,
                        'error': f'Unsupported format: {format}'
                    }), 400

            except Exception as e:
                logger.error(f"Error exporting devlogs: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/devlogs/agents')
        def get_agents():
            """Get list of all agents with their devlog counts."""
            try:
                agents_data = self._get_agents_data()

                return jsonify({
                    'success': True,
                    'data': agents_data
                })

            except Exception as e:
                logger.error(f"Error getting agents data: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/devlogs/trends')
        def get_trends():
            """Get trend data for devlogs over time."""
            try:
                days = int(request.args.get('days', 30))
                trends_data = self._get_trends_data(days)

                return jsonify({
                    'success': True,
                    'data': trends_data
                })

            except Exception as e:
                logger.error(f"Error getting trends data: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

    def _generate_analytics(self) -> Dict[str, Any]:
        """Generate comprehensive analytics data."""
        try:
            # Get all devlogs for analytics
            all_devlogs = self.vector_db.query(
                query="devlog",
                namespace="agent_devlogs",
                limit=1000  # Reasonable limit for analytics
            )

            # Calculate basic statistics
            total_devlogs = len(all_devlogs)
            agents = set()
            status_counts = {}
            daily_counts = {}

            for devlog in all_devlogs:
                metadata = devlog.get('metadata', {})

                # Count agents
                agent_id = metadata.get('agent_id')
                if agent_id:
                    agents.add(agent_id)

                # Count statuses
                status = metadata.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1

                # Count daily activity
                timestamp = metadata.get('timestamp')
                if timestamp:
                    date = timestamp.split('T')[0]
                    daily_counts[date] = daily_counts.get(date, 0) + 1

            # Calculate activity trends
            sorted_dates = sorted(daily_counts.keys())
            activity_trend = []
            for date in sorted_dates[-7:]:  # Last 7 days
                activity_trend.append({
                    'date': date,
                    'count': daily_counts[date]
                })

            return {
                'summary': {
                    'total_devlogs': total_devlogs,
                    'unique_agents': len(agents),
                    'active_agents': list(agents),
                    'status_distribution': status_counts
                },
                'trends': {
                    'daily_activity': activity_trend,
                    'average_per_day': total_devlogs / max(1, len(daily_counts))
                },
                'top_agents': self._get_top_agents(all_devlogs, 5)
            }

        except Exception as e:
            logger.error(f"Error generating analytics: {e}")
            return {
                'summary': {'total_devlogs': 0, 'unique_agents': 0, 'active_agents': []},
                'trends': {'daily_activity': [], 'average_per_day': 0},
                'top_agents': []
            }

    def _get_export_data(self) -> List[Dict[str, Any]]:
        """Get devlogs data formatted for export."""
        try:
            devlogs = self.vector_db.query(
                query="devlog entry",
                namespace="agent_devlogs",
                limit=1000
            )

            export_data = []
            for devlog in devlogs:
                metadata = devlog.get('metadata', {})
                export_data.append({
                    'id': devlog.get('id', ''),
                    'agent_id': metadata.get('agent_id', ''),
                    'action': metadata.get('action', ''),
                    'status': metadata.get('status', ''),
                    'details': metadata.get('details', ''),
                    'timestamp': metadata.get('timestamp', ''),
                    'content': devlog.get('content', '')[:200] + '...' if len(devlog.get('content', '')) > 200 else devlog.get('content', '')
                })

            return export_data

        except Exception as e:
            logger.error(f"Error getting export data: {e}")
            return []

    def _get_agents_data(self) -> List[Dict[str, Any]]:
        """Get agents data with devlog counts."""
        try:
            agents_data = []

            # Get unique agents
            agents = set()
            devlogs = self.vector_db.query(
                query="devlog",
                namespace="agent_devlogs",
                limit=1000
            )

            for devlog in devlogs:
                metadata = devlog.get('metadata', {})
                agent_id = metadata.get('agent_id')
                if agent_id:
                    agents.add(agent_id)

            # Count devlogs per agent
            for agent_id in agents:
                agent_devlogs = self.vector_db.query(
                    query="devlog",
                    namespace="agent_devlogs",
                    metadata_filter={'agent_id': agent_id},
                    limit=1000
                )

                agents_data.append({
                    'agent_id': agent_id,
                    'devlog_count': len(agent_devlogs),
                    'role': self._get_agent_role(agent_id)
                })

            # Sort by devlog count
            agents_data.sort(key=lambda x: x['devlog_count'], reverse=True)
            return agents_data

        except Exception as e:
            logger.error(f"Error getting agents data: {e}")
            return []

    def _get_trends_data(self, days: int) -> Dict[str, Any]:
        """Get trends data for the specified number of days."""
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Query devlogs in date range
            devlogs = self.vector_db.query(
                query="devlog",
                namespace="agent_devlogs",
                metadata_filter={
                    'timestamp': {
                        '$gte': start_date.isoformat(),
                        '$lte': end_date.isoformat()
                    }
                },
                limit=2000
            )

            # Group by date
            daily_data = {}
            for devlog in devlogs:
                metadata = devlog.get('metadata', {})
                timestamp = metadata.get('timestamp', '')
                if timestamp:
                    date = timestamp.split('T')[0]
                    if date not in daily_data:
                        daily_data[date] = {
                            'date': date,
                            'total': 0,
                            'completed': 0,
                            'in_progress': 0,
                            'failed': 0,
                            'agents': set()
                        }

                    daily_data[date]['total'] += 1
                    status = metadata.get('status', 'unknown')
                    if status in daily_data[date]:
                        daily_data[date][status] += 1

                    agent_id = metadata.get('agent_id', '')
                    if agent_id:
                        daily_data[date]['agents'].add(agent_id)

            # Convert sets to counts
            trends_data = []
            for date_data in sorted(daily_data.values()):
                date_data['unique_agents'] = len(date_data['agents'])
                del date_data['agents']
                trends_data.append(date_data)

            return {
                'period_days': days,
                'total_devlogs': len(devlogs),
                'daily_breakdown': trends_data
            }

        except Exception as e:
            logger.error(f"Error getting trends data: {e}")
            return {'period_days': days, 'total_devlogs': 0, 'daily_breakdown': []}

    def _get_top_agents(self, devlogs: List[Dict], limit: int = 5) -> List[Dict[str, Any]]:
        """Get top agents by devlog activity."""
        try:
            agent_counts = {}
            for devlog in devlogs:
                metadata = devlog.get('metadata', {})
                agent_id = metadata.get('agent_id')
                if agent_id:
                    agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1

            top_agents = []
            for agent_id, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True)[:limit]:
                top_agents.append({
                    'agent_id': agent_id,
                    'count': count,
                    'role': self._get_agent_role(agent_id)
                })

            return top_agents

        except Exception as e:
            logger.error(f"Error getting top agents: {e}")
            return []

    def _get_agent_role(self, agent_id: str) -> str:
        """Get the role for an agent."""
        roles = {
            'Agent-1': 'Integration & Core Systems Specialist',
            'Agent-2': 'Architecture & Design Specialist',
            'Agent-3': 'Infrastructure & DevOps Specialist',
            'Agent-4': 'Quality Assurance Specialist (CAPTAIN)',
            'Agent-5': 'Business Intelligence Specialist',
            'Agent-6': 'Coordination & Communication Specialist',
            'Agent-7': 'Web Development Specialist',
            'Agent-8': 'Operations & Support Specialist'
        }
        return roles.get(agent_id, 'Specialist')

    def _export_json(self, data: List[Dict[str, Any]]) -> Response:
        """Export data as JSON."""
        response = Response(
            json.dumps(data, indent=2),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=devlogs.json'}
        )
        return response

    def _export_csv(self, data: List[Dict[str, Any]]) -> Response:
        """Export data as CSV."""
        output = io.StringIO()
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        response = Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=devlogs.csv'}
        )
        return response

    def _export_excel(self, data: List[Dict[str, Any]]) -> Response:
        """Export data as Excel (placeholder - would need pandas/openpyxl)."""
        # For now, return JSON with Excel filename
        response = Response(
            json.dumps({
                'message': 'Excel export requires pandas and openpyxl. Install: pip install pandas openpyxl',
                'data': data
            }),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=devlogs.xlsx'}
        )
        return response

    def run(self):
        """Run the Flask development server."""
        logger.info(f"Starting Devlog Analytics API on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=True)


if __name__ == '__main__':
    api = DevlogAnalyticsAPI()
    api.run()
