/**
 * Dashboard Overview View Module - V2 Compliant
 * Handles overview and contract status view rendering
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

/**
 * Render overview view
 * @param {Object} data - Dashboard data
 * @returns {string} HTML content
 */
function renderOverviewView(data) {
    const systemMetrics = data.system_metrics || {};
    const contractSummary = data.contract_summary || {};

    return `
        <div class="row">
            <!-- System Health -->
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(systemMetrics.system_health?.status || 'normal')}">
                        ${systemMetrics.system_health?.value?.toFixed(1) || '0'}%
                    </div>
                    <div class="metric-label">System Health</div>
                </div>
            </div>

            <!-- Active Agents -->
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(systemMetrics.active_agents?.status || 'normal')}">
                        ${systemMetrics.active_agents?.value || '0'}
                    </div>
                    <div class="metric-label">Active Agents</div>
                </div>
            </div>

            <!-- Contract Completion -->
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${getStatusClass(systemMetrics.contract_completion?.status || 'normal')}">
                        ${systemMetrics.contract_completion?.value?.toFixed(1) || '0'}%
                    </div>
                    <div class="metric-label">Contract Completion</div>
                </div>
            </div>

            <!-- Active Alerts -->
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-${data.active_alerts_count > 5 ? 'critical' : data.active_alerts_count > 2 ? 'warning' : 'healthy'}">
                        ${data.active_alerts_count || '0'}
                    </div>
                    <div class="metric-label">Active Alerts</div>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Contract Summary Chart -->
            <div class="col-md-6">
                <div class="chart-container">
                    <h5><i class="fas fa-chart-pie me-2"></i>Contract Status Distribution</h5>
                    <canvas id="contractChart" width="400" height="300"></canvas>
                </div>
            </div>

            <!-- Workload Distribution Chart -->
            <div class="col-md-6">
                <div class="chart-container">
                    <h5><i class="fas fa-chart-bar me-2"></i>Workload Distribution</h5>
                    <canvas id="workloadChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>

        <!-- Recent Alerts -->
        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    <h5><i class="fas fa-exclamation-triangle me-2"></i>Recent Alerts</h5>
                    <div id="alertsContainer">
                        ${renderAlerts(data.alerts || [])}
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render contract status view
 * @param {Object} data - Dashboard data
 * @returns {string} HTML content
 */
function renderContractStatusView(data) {
    const contractSummary = data.contract_summary || {};
    const contractsByAgent = data.contracts_by_agent || {};

    return `
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value text-primary">${contractSummary.total_contracts || '0'}</div>
                    <div class="metric-label">Total Contracts</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-warning">${contractSummary.pending_contracts || '0'}</div>
                    <div class="metric-label">Pending</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-info">${contractSummary.in_progress_contracts || '0'}</div>
                    <div class="metric-label">In Progress</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value status-healthy">${contractSummary.completed_contracts || '0'}</div>
                    <div class="metric-label">Completed</div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    <h5><i class="fas fa-chart-pie me-2"></i>Contract Status Overview</h5>
                    <canvas id="contractStatusChart" width="400" height="300"></canvas>
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
                                <th>Success Rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.entries(contractsByAgent).map(([agentId, data]) => `
                                <tr>
                                    <td><strong>${agentId}</strong></td>
                                    <td>${data.current_contracts}</td>
                                    <td>${data.total_contracts}</td>
                                    <td>${data.success_rate.toFixed(1)}%</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}