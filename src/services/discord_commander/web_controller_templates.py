#!/usr/bin/env python3
"""
Discord Commander Web Controller - Templates
============================================

HTML template creation and management for Discord Commander web interface.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- HTML template generation
- CSS styling
- JavaScript functionality
- Responsive design

Extracted from main web controller module for V2 compliance.
"""

from pathlib import Path


def create_default_templates():
    """Create default HTML templates."""
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)

    # Create main dashboard template
    dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Commander - Agent Control Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }

        .agent-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .agent-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            border-left: 4px solid #667eea;
        }

        .agent-card.online {
            border-left-color: #28a745;
        }

        .agent-card.offline {
            border-left-color: #dc3545;
        }

        .agent-card.idle {
            border-left-color: #ffc107;
        }

        .agent-name {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .agent-status {
            font-size: 0.9rem;
            color: #666;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        .form-group textarea {
            resize: vertical;
            min-height: 100px;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s ease;
            margin-right: 10px;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn-success {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }

        .btn-warning {
            background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        }

        .btn-danger {
            background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        }

        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .status-online {
            background-color: #28a745;
        }

        .status-offline {
            background-color: #dc3545;
        }

        .status-idle {
            background-color: #ffc107;
        }

        .message-log {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 20px;
        }

        .message-item {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }

        .message-time {
            font-size: 0.8rem;
            color: #666;
            margin-bottom: 5px;
        }

        .message-content {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .message-details {
            font-size: 0.9rem;
            color: #666;
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .alert-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }

        .alert-error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }

        .alert-info {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }

        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
            }

            .agent-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Discord Commander</h1>
            <p>Agent Control Dashboard - V2_SWARM System</p>
        </div>

        <div class="dashboard">
            <!-- Agent Status Panel -->
            <div class="card">
                <h2>📊 Agent Status</h2>
                <div class="agent-grid" id="agentGrid">
                    <!-- Agent cards will be populated by JavaScript -->
                </div>
                <button class="btn" onclick="refreshAgentStatus()">🔄 Refresh Status</button>
            </div>

            <!-- Message Control Panel -->
            <div class="card">
                <h2>💬 Message Control</h2>

                <div class="form-group">
                    <label for="agentSelect">Target Agent:</label>
                    <select id="agentSelect">
                        <option value="Agent-1">Agent-1</option>
                        <option value="Agent-2">Agent-2</option>
                        <option value="Agent-3">Agent-3</option>
                        <option value="Agent-4">Agent-4 (Captain)</option>
                        <option value="Agent-5">Agent-5</option>
                        <option value="Agent-6">Agent-6</option>
                        <option value="Agent-7">Agent-7</option>
                        <option value="Agent-8">Agent-8</option>
                        <option value="ALL">All Agents (Broadcast)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="prioritySelect">Priority:</label>
                    <select id="prioritySelect">
                        <option value="NORMAL">Normal</option>
                        <option value="HIGH">High</option>
                        <option value="LOW">Low</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="messageInput">Message:</label>
                    <textarea id="messageInput" placeholder="Enter your message here..."></textarea>
                </div>

                <button class="btn btn-success" onclick="sendMessage()">📤 Send Message</button>
                <button class="btn btn-warning" onclick="broadcastMessage()">📢 Broadcast</button>
            </div>
        </div>

        <!-- System Status Panel -->
        <div class="card">
            <h2>⚙️ System Status</h2>
            <div id="systemStatus">
                <p>Loading system status...</p>
            </div>
            <button class="btn" onclick="refreshSystemStatus()">🔄 Refresh System</button>
        </div>

        <!-- Message Log -->
        <div class="card">
            <h2>📋 Message Log</h2>
            <div class="message-log" id="messageLog">
                <div class="message-item">
                    <div class="message-time">System initialized</div>
                    <div class="message-content">Discord Commander Dashboard Ready</div>
                    <div class="message-details">Web interface loaded successfully</div>
                </div>
            </div>
            <button class="btn" onclick="clearMessageLog()">🗑️ Clear Log</button>
        </div>
    </div>

    <script>
        // Initialize Socket.IO connection
        const socket = io();

        // Connection status
        socket.on('connect', function() {
            addMessageLog('Connected to Discord Commander', 'System', 'success');
        });

        socket.on('disconnect', function() {
            addMessageLog('Disconnected from Discord Commander', 'System', 'error');
        });

        // Agent status updates
        socket.on('agent_status', function(data) {
            if (data.error) {
                addMessageLog('Error getting agent status: ' + data.error, 'System', 'error');
                return;
            }
            updateAgentStatus(data.agents);
        });

        // Message results
        socket.on('message_result', function(data) {
            if (data.error) {
                addMessageLog('Message failed: ' + data.error, 'System', 'error');
            } else {
                addMessageLog('Message sent successfully', 'System', 'success');
            }
        });

        socket.on('broadcast_result', function(data) {
            if (data.error) {
                addMessageLog('Broadcast failed: ' + data.error, 'System', 'error');
            } else {
                addMessageLog('Broadcast sent successfully', 'System', 'success');
            }
        });

        // System status updates
        socket.on('system_status', function(data) {
            if (data.error) {
                document.getElementById('systemStatus').innerHTML = '<p>Error: ' + data.error + '</p>';
            } else {
                updateSystemStatus(data.status);
            }
        });

        // Functions
        function refreshAgentStatus() {
            socket.emit('get_agent_status');
        }

        function sendMessage() {
            const agentId = document.getElementById('agentSelect').value;
            const message = document.getElementById('messageInput').value;
            const priority = document.getElementById('prioritySelect').value;

            if (!message.trim()) {
                alert('Please enter a message');
                return;
            }

            if (agentId === 'ALL') {
                broadcastMessage();
                return;
            }

            socket.emit('send_message', {
                agent_id: agentId,
                message: message,
                priority: priority
            });

            addMessageLog(`Sending message to ${agentId}`, 'User', 'info');
            document.getElementById('messageInput').value = '';
        }

        function broadcastMessage() {
            const message = document.getElementById('messageInput').value;
            const priority = document.getElementById('prioritySelect').value;

            if (!message.trim()) {
                alert('Please enter a message');
                return;
            }

            socket.emit('broadcast_message', {
                message: message,
                priority: priority
            });

            addMessageLog('Broadcasting message to all agents', 'User', 'info');
            document.getElementById('messageInput').value = '';
        }

        function refreshSystemStatus() {
            socket.emit('get_system_status');
        }

        function updateAgentStatus(agents) {
            const agentGrid = document.getElementById('agentGrid');
            agentGrid.innerHTML = '';

            for (const [agentId, data] of Object.entries(agents)) {
                const agentCard = document.createElement('div');
                agentCard.className = `agent-card ${data.status.toLowerCase()}`;

                const statusClass = data.status === 'ONLINE' ? 'status-online' :
                                  data.status === 'OFFLINE' ? 'status-offline' : 'status-idle';

                agentCard.innerHTML = `
                    <div class="agent-name">${agentId}</div>
                    <div class="agent-status">
                        <span class="status-indicator ${statusClass}"></span>
                        ${data.status}
                    </div>
                `;

                agentGrid.appendChild(agentCard);
            }
        }

        function updateSystemStatus(status) {
            const statusDiv = document.getElementById('systemStatus');
            statusDiv.innerHTML = `
                <p><strong>Bot Status:</strong> ${status.bot_online ? 'Online' : 'Offline'}</p>
                <p><strong>Active Agents:</strong> ${status.active_agents || 0}</p>
                <p><strong>Total Messages:</strong> ${status.total_messages || 0}</p>
                <p><strong>Last Update:</strong> ${new Date().toLocaleTimeString()}</p>
            `;
        }

        function addMessageLog(message, source, type) {
            const messageLog = document.getElementById('messageLog');
            const messageItem = document.createElement('div');
            messageItem.className = 'message-item';

            const timestamp = new Date().toLocaleTimeString();
            messageItem.innerHTML = `
                <div class="message-time">${timestamp}</div>
                <div class="message-content">${message}</div>
                <div class="message-details">Source: ${source}</div>
            `;

            messageLog.insertBefore(messageItem, messageLog.firstChild);

            // Keep only last 50 messages
            while (messageLog.children.length > 50) {
                messageLog.removeChild(messageLog.lastChild);
            }
        }

        function clearMessageLog() {
            document.getElementById('messageLog').innerHTML = '';
            addMessageLog('Message log cleared', 'User', 'info');
        }

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            refreshAgentStatus();
            refreshSystemStatus();
        });
    </script>
</body>
</html>"""

    # Write the template file
    template_file = templates_dir / "discord_commander.html"
    template_file.write_text(dashboard_html, encoding="utf-8")

    print(f"✅ Created Discord Commander template: {template_file}")


if __name__ == "__main__":
    create_default_templates()
