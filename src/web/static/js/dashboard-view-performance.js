/**
 * Dashboard Performance Views Module - V2 Compliant
 * Handles agent performance and workload view rendering
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
 * Render system health view
 * @param {Object} data - Dashboard data
 * @returns {string} HTML content
 */
function renderSystemHealthView(data) {
    const systemMetrics = data.system_metrics || {};

    return `
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(systemMetrics.system_health?.status || 'normal')}">
                        ${systemMetrics.system_health?.value?.toFixed(1) || '0'}%
                    </div>
                    <div class="metric-label">Overall System Health</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(systemMetrics.agent_utilization?.status || 'normal')}">
                        ${systemMetrics.agent_utilization?.value?.toFixed(1) || '0'}%
                    </div>
                    <div class="metric-label">Agent Utilization</div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    <h5><i class="fas fa-chart-line me-2"></i>System Health Trend</h5>
                    <canvas id="healthTrendChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render performance metrics view
 * @param {Object} data - Dashboard data
 * @returns {string} HTML content
 */
function renderPerformanceMetricsView(data) {
    const metrics = data.metrics || {};

    return `
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(metrics.system_health?.status || 'normal')}">
                        ${metrics.system_health?.value?.toFixed(1) || '0'}%
                    </div>
                    <div class="metric-label">System Health</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(metrics.contract_completion?.status || 'normal')}">
                        ${metrics.contract_completion?.value?.toFixed(1) || '0'}%
                    </div>
                    <div class="metric-label">Contract Completion</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(metrics.active_agents?.status || 'normal')}">
                        ${metrics.active_agents?.value || '0'}
                    </div>
                    <div class="metric-label">Active Agents</div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    <h5><i class="fas fa-chart-bar me-2"></i>Agent Performance Comparison</h5>
                    <canvas id="agentPerformanceChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render workload distribution view
 * @param {Object} data - Dashboard data
 * @returns {string} HTML content
 */
function renderWorkloadDistributionView(data) {
    const workloadDistribution = data.workload_distribution || {};
    const agentWorkloads = data.agent_workloads || {};

    return `
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value text-primary">${workloadDistribution.total_agents || '0'}</div>
                    <div class="metric-label">Total Agents</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-healthy">${workloadDistribution.optimal_workload_agents || '0'}</div>
                    <div class="metric-label">Optimal Workload</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-warning">${workloadDistribution.overloaded_agents || '0'}</div>
                    <div class="metric-label">Overloaded</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-info">${workloadDistribution.underutilized_agents || '0'}</div>
                    <div class="metric-label">Underutilized</div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    <h5><i class="fas fa-chart-pie me-2"></i>Workload Distribution</h5>
                    <canvas id="workloadDistributionChart" width="400" height="300"></canvas>
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
                                <th>Current Contracts</th>
                                <th>Total Contracts</th>
                                <th>Last Activity</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.entries(agentWorkloads).map(([agentId, data]) => `
                                <tr>
                                    <td><strong>${agentId}</strong></td>
                                    <td>${data.current_contracts}</td>
                                    <td>${data.total_contracts}</td>
                                    <td>${formatTimestamp(data.last_activity)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}
