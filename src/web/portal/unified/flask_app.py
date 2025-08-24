#!/usr/bin/env python3
"""
Flask Portal App - V2 Core Web Integration

Flask-based web application for the unified portal.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, Optional
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room

from .portal_core import UnifiedPortal
from .data_models import PortalConfig, AgentPortalInfo, PortalSection


class FlaskPortalApp:
    """
    Flask-based portal web application
    
    Single responsibility: Flask web interface for portal.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """

    def __init__(self, portal: UnifiedPortal, config: Optional[PortalConfig] = None):
        """Initialize Flask portal app"""
        self.portal = portal
        self.config = config or portal.config
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.secret_key = 'your-secret-key-here'  # Should be configurable
        
        # Initialize SocketIO for real-time features
        if self.config.enable_websockets:
            self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        else:
            self.socketio = None
        
        self.logger = logging.getLogger(f"{__name__}.FlaskPortalApp")
        self._setup_routes()
        self.logger.info("Flask portal app initialized")

    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main portal page"""
            return render_template('portal/index.html', 
                                title=self.config.title,
                                version=self.config.version)

        @self.app.route('/api/status')
        def api_status():
            """Get portal status"""
            return jsonify(self.portal.get_portal_status())

        @self.app.route('/api/agents')
        def api_agents():
            """Get all agents"""
            agents = [agent.to_dict() for agent in self.portal.agents.values()]
            return jsonify({'agents': agents})

        @self.app.route('/api/agents/<agent_id>')
        def api_agent_detail(agent_id):
            """Get specific agent details"""
            agent = self.portal.get_agent_info(agent_id)
            if agent:
                return jsonify(agent.to_dict())
            return jsonify({'error': 'Agent not found'}), 404

        @self.app.route('/api/navigation')
        def api_navigation():
            """Get navigation state"""
            return jsonify(self.portal.get_navigation_state())

        @self.app.route('/api/navigation/<section>')
        def api_navigate_to(section):
            """Navigate to specific section"""
            try:
                portal_section = PortalSection(section)
                self.portal.navigate_to_section(portal_section)
                return jsonify({'success': True, 'section': section})
            except ValueError:
                return jsonify({'error': 'Invalid section'}), 400

        @self.app.route('/api/sessions', methods=['POST'])
        def api_create_session():
            """Create new session"""
            try:
                data = request.get_json()
                user_id = data.get('user_id')
                metadata = data.get('metadata', {})
                
                if not user_id:
                    return jsonify({'error': 'user_id required'}), 400
                
                session_id = self.portal.create_session(user_id, metadata)
                return jsonify({'session_id': session_id, 'success': True})
                
            except Exception as e:
                self.logger.error(f"Session creation failed: {e}")
                return jsonify({'error': 'Session creation failed'}), 500

        @self.app.route('/api/sessions/<session_id>', methods=['GET'])
        def api_session_status(session_id):
            """Get session status"""
            is_valid = self.portal.validate_session(session_id)
            return jsonify({'valid': is_valid, 'session_id': session_id})

        @self.app.route('/api/sessions/<session_id>', methods=['DELETE'])
        def api_terminate_session(session_id):
            """Terminate session"""
            success = self.portal.terminate_session(session_id)
            return jsonify({'success': success, 'session_id': session_id})

        @self.app.route('/api/statistics')
        def api_statistics():
            """Get portal statistics"""
            return jsonify(self.portal.get_agent_statistics())

        # Error handlers
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Not found'}), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({'error': 'Internal server error'}), 500

    def _setup_socketio_events(self):
        """Setup SocketIO event handlers"""
        if not self.socketio:
            return
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            connection_id = request.sid
            self.portal.add_connection(connection_id)
            self.logger.info(f"Client connected: {connection_id}")
            emit('connected', {'status': 'connected', 'connection_id': connection_id})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            connection_id = request.sid
            self.portal.remove_connection(connection_id)
            self.logger.info(f"Client disconnected: {connection_id}")

        @self.socketio.on('join_room')
        def handle_join_room(data):
            """Handle room joining"""
            room = data.get('room')
            if room:
                join_room(room)
                emit('room_joined', {'room': room}, room=room)

        @self.socketio.on('leave_room')
        def handle_leave_room(data):
            """Handle room leaving"""
            room = data.get('room')
            if room:
                leave_room(room)
                emit('room_left', {'room': room}, room=room)

        @self.socketio.on('portal_update')
        def handle_portal_update(data):
            """Handle portal update requests"""
            update_type = data.get('type')
            if update_type == 'status':
                emit('portal_status', self.portal.get_portal_status())
            elif update_type == 'agents':
                agents = [agent.to_dict() for agent in self.portal.agents.values()]
                emit('agents_update', {'agents': agents})

    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = None):
        """Run the Flask portal app"""
        debug_mode = debug if debug is not None else self.config.debug_mode
        
        if self.config.enable_websockets:
            self._setup_socketio_events()
            self.socketio.run(self.app, host=host, port=port, debug=debug_mode)
        else:
            self.app.run(host=host, port=port, debug=debug_mode)

    def get_app(self) -> Flask:
        """Get the Flask app instance"""
        return self.app

    def get_socketio(self) -> Optional[SocketIO]:
        """Get the SocketIO instance if available"""
        return self.socketio

