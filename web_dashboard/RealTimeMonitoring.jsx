import './RealTimeMonitoring.css';

import React, { useEffect, useState } from 'react';

const RealTimeMonitoring = () => {
  const [logs, setLogs] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [agentStatus, setAgentStatus] = useState([]);
  const [devlogSummary, setDevlogSummary] = useState(null);
  const [systemHealth, setSystemHealth] = useState({});
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001');

    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case 'system_metrics':
          setMetrics(data.data);
          setSystemHealth({
            cpu: data.data.cpu_usage,
            memory: data.data.memory_usage,
            disk: data.data.disk_usage,
            uptime: data.data.system_uptime
          });
          break;

        case 'log':
          setLogs(prev => [...prev.slice(-99), data.data]);
          break;

        case 'agent_status':
          setAgentStatus(data.data);
          break;

        case 'devlog_summary':
          setDevlogSummary(data.data);
          break;

        case 'pong':
          // Handle ping/pong for connection keepalive
          break;

        default:
          console.log('Unknown message type:', data.type);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnectionStatus('disconnected');
    };

    // Send periodic ping to keep connection alive
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping');
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      ws.close();
    };
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'connected': return '#4CAF50';
      case 'error': return '#F44336';
      default: return '#FF9800';
    }
  };

  return (
    <div className="real-time-monitoring">
      <div className="monitoring-header">
        <h2>Real-Time Monitoring</h2>
        <div className="connection-status">
          <div
            className="status-indicator"
            style={{ backgroundColor: getStatusColor(connectionStatus) }}
          ></div>
          <span>{connectionStatus.charAt(0).toUpperCase() + connectionStatus.slice(1)}</span>
        </div>
      </div>

      <div className="monitoring-grid">
        {/* System Health */}
        <div className="monitoring-panel">
          <h3>System Health</h3>
          <div className="health-metrics">
            <div className="health-metric">
              <div className="metric-label">CPU Usage</div>
              <div className="metric-value">{systemHealth.cpu || 0}%</div>
              <div className="metric-bar">
                <div
                  className="metric-fill cpu"
                  style={{ width: `${Math.min(systemHealth.cpu || 0, 100)}%` }}
                ></div>
              </div>
            </div>
            <div className="health-metric">
              <div className="metric-label">Memory Usage</div>
              <div className="metric-value">{systemHealth.memory || 0}%</div>
              <div className="metric-bar">
                <div
                  className="metric-fill memory"
                  style={{ width: `${Math.min(systemHealth.memory || 0, 100)}%` }}
                ></div>
              </div>
            </div>
            <div className="health-metric">
              <div className="metric-label">Disk Usage</div>
              <div className="metric-value">{systemHealth.disk || 0}%</div>
              <div className="metric-bar">
                <div
                  className="metric-fill disk"
                  style={{ width: `${Math.min(systemHealth.disk || 0, 100)}%` }}
                ></div>
              </div>
            </div>
            <div className="health-metric">
              <div className="metric-label">Uptime</div>
              <div className="metric-value">{systemHealth.uptime || 'Unknown'}</div>
            </div>
          </div>
        </div>

        {/* Agent Status */}
        <div className="monitoring-panel">
          <h3>Agent Status</h3>
          <div className="agent-status-grid">
            {agentStatus.slice(0, 8).map((agent) => (
              <div key={agent.id} className="agent-status-item">
                <div className="agent-status-header">
                  <span className="agent-id">{agent.id}</span>
                  <span className={`status-dot ${agent.status.toLowerCase()}`}></span>
                </div>
                <div className="agent-efficiency">Efficiency: {agent.efficiency}</div>
                <div className="agent-task">{agent.current_task}</div>
                <div className="agent-activity">
                  {new Date(agent.last_activity).toLocaleTimeString()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Devlog Summary */}
        {devlogSummary && (
          <div className="monitoring-panel">
            <h3>Devlog Activity</h3>
            <div className="devlog-summary">
              <div className="devlog-stat">
                <div className="stat-label">Total</div>
                <div className="stat-value">{devlogSummary.total_devlogs}</div>
              </div>
              <div className="devlog-stat">
                <div className="stat-label">Today</div>
                <div className="stat-value">{devlogSummary.today_devlogs}</div>
              </div>
              <div className="devlog-stat">
                <div className="stat-label">Success Rate</div>
                <div className="stat-value">{devlogSummary.completion_rate}%</div>
              </div>
              <div className="devlog-stat">
                <div className="stat-label">Top Agent</div>
                <div className="stat-value">{devlogSummary.top_agent}</div>
              </div>
            </div>

            <div className="recent-activity">
              <h4>Recent Activity</h4>
              <div className="activity-list">
                {devlogSummary.recent_activity.map((activity, index) => (
                  <div key={index} className="activity-item">
                    <div className="activity-agent">{activity.agent}</div>
                    <div className="activity-action">{activity.action}</div>
                    <div className="activity-status">{activity.status}</div>
                    <div className="activity-time">
                      {new Date(activity.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Live Logs */}
        <div className="monitoring-panel full-width">
          <h3>Live Logs</h3>
          <div className="logs-container">
            <div className="logs-scroll">
              {logs.slice(-20).map((log, index) => (
                <div key={index} className={`log-entry ${log.level.toLowerCase()}`}>
                  <span className="log-timestamp">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="log-level">{log.level}</span>
                  <span className="log-source">[{log.source}]</span>
                  <span className="log-message">{log.message}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RealTimeMonitoring;
