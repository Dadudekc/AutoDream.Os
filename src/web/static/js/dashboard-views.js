/**
 * Dashboard Agent Performance Views Module - V2 Compliant
 * Handles agent performance view rendering
 * 
 * @author Agent-7 - Web Development Specialist  
 * @version 2.0.0
 * @license MIT
 */

/**
 * Render agent performance view
 * @param {Object} data - Dashboard data
 * @returns {string} HTML content
 */
function renderAgentPerformanceView(data) {
    const agents = data.agents || [];
    const summary = data.performance_summary || {};

    return `
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value text-primary">${summary.total_agents || '0'}</div>
                    <div class="metric-label">Total Agents</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-healthy">${summary.high_performance || '0'}</div>
                    <div class="metric-label">High Performance</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-warning">${summary.medium_performance || '0'}</div>
                    <div class="metric-label">Medium Performance</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-critical">${summary.low_performance || '0'}</div>
                    <div class="metric-label">Low Performance</div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="agent-table">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Agent</th>
                                <th>Status</th>
                                <th>Performance Score</th>
                                <th>Success Rate</th>
                                <th>Current Contracts</th>
                                <th>Last Activity</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${agents.map(agent => `
                                <tr>
                                    <td>
                                        <strong>${escapeHTML(agent.name)}</strong><br>
                                        <small class="text-muted">${escapeHTML(agent.agent_id)}</small>
                                    </td>
                                    <td>
                                        <span class="badge bg-${getStatusBadgeColor(agent.status)}">
                                            ${agent.status}
                                        </span>
                                    </td>
                                    <td>
                                        <span class="performance-score score-${getScoreClass(agent.performance_score)}">
                                            ${agent.performance_score.toFixed(1)}%
                                        </span>
                                    </td>
                                    <td>${agent.success_rate.toFixed(1)}%</td>
                                    <td>${agent.current_contracts}</td>
                                    <td>${formatTimestamp(agent.last_activity)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render alerts
 * @param {Array} alerts - Array of alert objects
 * @returns {string} HTML content
 */
function renderAlerts(alerts) {
    if (alerts.length === 0) {
        return '<p class="text-muted text-center">No active alerts</p>';
    }

    return alerts.slice(0, 5).map(alert => `
        <div class="alert-item ${alert.level}">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <strong>${escapeHTML(alert.message)}</strong>
                    <br><small class="text-muted">${formatTimestamp(alert.timestamp)}</small>
                </div>
                <div>
                    <button class="btn btn-sm btn-outline-primary me-2" onclick="acknowledgeAlert('${alert.id}')">
                        Acknowledge
                    </button>
                    <button class="btn btn-sm btn-outline-success" onclick="resolveAlert('${alert.id}')">
                        Resolve
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}