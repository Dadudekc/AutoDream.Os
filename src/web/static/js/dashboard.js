        // Dashboard state
        let currentView = 'overview';
        let socket = null;
        let charts = {};
        let updateTimer = null;

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeSocket();
            setupNavigation();
            updateCurrentTime();
            loadDashboardData(currentView);

            // Update time every second
            setInterval(updateCurrentTime, 1000);
        });

        // Initialize WebSocket connection
        function initializeSocket() {
            socket = io();

            socket.on('connect', function() {
                console.log('Connected to dashboard server');
                document.getElementById('loadingState').style.display = 'none';
            });

            socket.on('dashboard_update', function(data) {
                updateDashboard(data);
                showRefreshIndicator();
            });

            socket.on('error', function(data) {
                console.error('Dashboard error:', data.message);
                showAlert('error', data.message);
            });

            socket.on('disconnect', function() {
                console.log('Disconnected from dashboard server');
                showAlert('warning', 'Connection lost. Attempting to reconnect...');
            });
        }

        // Setup navigation
        function setupNavigation() {
            document.getElementById('dashboardNav').addEventListener('click', function(e) {
                if (e.target.classList.contains('nav-link')) {
                    e.preventDefault();

                    // Update active state
                    document.querySelectorAll('#dashboardNav .nav-link').forEach(link => {
                        link.classList.remove('active');
                    });
                    e.target.classList.add('active');

                    // Load new view
                    const view = e.target.dataset.view;
                    currentView = view;
                    loadDashboardData(view);
                }
            });
        }

        // Load dashboard data
        function loadDashboardData(view) {
            showLoading();

            fetch(`/api/dashboard/${view}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        showAlert('error', data.error);
                        return;
                    }
                    updateDashboard(data);
                })
                .catch(error => {
                    console.error('Failed to load dashboard data:', error);
                    showAlert('error', 'Failed to load dashboard data');
                })
                .finally(() => {
                    hideLoading();
                });
        }

        // Update dashboard with new data
        function updateDashboard(data) {
            const contentDiv = document.getElementById('dashboardContent');

            if (data.view === 'overview') {
                contentDiv.innerHTML = renderOverviewView(data);
            } else if (data.view === 'agent_performance') {
                contentDiv.innerHTML = renderAgentPerformanceView(data);
            } else if (data.view === 'contract_status') {
                contentDiv.innerHTML = renderContractStatusView(data);
            } else if (data.view === 'system_health') {
                contentDiv.innerHTML = renderSystemHealthView(data);
            } else if (data.view === 'performance_metrics') {
                contentDiv.innerHTML = renderPerformanceMetricsView(data);
            } else if (data.view === 'workload_distribution') {
                contentDiv.innerHTML = renderWorkloadDistributionView(data);
            }

            // Initialize charts after rendering
            requestAnimationFrame(() => initializeCharts(data));
        }

        // Render overview view
        function renderOverviewView(data) {
            const systemMetrics = data.system_metrics || {};
            const contractSummary = data.contract_summary || {};
            const workloadDistribution = data.workload_distribution || {};

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

        // Render agent performance view
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

        // Render contract status view
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

        // Render system health view
        function renderSystemHealthView(data) {
            const systemMetrics = data.system_metrics || {};
            const performanceHistory = data.performance_history || {};

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

        // Render performance metrics view
        function renderPerformanceMetricsView(data) {
            const metrics = data.metrics || {};
            const agentMetrics = data.agent_metrics || {};

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

        // Render workload distribution view
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

        // Render alerts
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
                            <button class="btn btn-sm btn-outline-primary me-1" onclick="acknowledgeAlert('${alert.alert_id}')">
                                Acknowledge
                            </button>
                            <button class="btn btn-sm btn-outline-success" onclick="resolveAlert('${alert.alert_id}')">
                                Resolve
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Initialize charts
        function initializeCharts() {
            // Contract status chart
            if (document.getElementById('contractChart')) {
                const ctx = document.getElementById('contractChart').getContext('2d');
                charts.contractChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Completed', 'In Progress', 'Pending'],
                        datasets: [{
                            data: [65, 20, 15],
                            backgroundColor: ['#28a745', '#17a2b8', '#ffc107']
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            }

            // Workload distribution chart
            if (document.getElementById('workloadChart')) {
                const ctx = document.getElementById('workloadChart').getContext('2d');
                charts.workloadChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['0', '1-2', '3-4', '5+'],
                        datasets: [{
                            label: 'Agents',
                            data: [5, 8, 12, 3],
                            backgroundColor: '#007bff'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        }

        // Utility functions
        function getStatusClass(status) {
            switch (status) {
                case 'critical': return 'critical';
                case 'warning': return 'warning';
                case 'normal': return 'healthy';
                default: return 'healthy';
            }
        }

        function getStatusBadgeColor(status) {
            switch (status) {
                case 'active': return 'success';
                case 'busy': return 'warning';
                case 'idle': return 'secondary';
                case 'offline': return 'danger';
                default: return 'secondary';
            }
        }

        function getScoreClass(score) {
            if (score >= 80) return 'high';
            if (score >= 60) return 'medium';
            return 'low';
        }

        function formatTimestamp(timestamp) {
            if (!timestamp) return 'Unknown';
            const date = new Date(timestamp);
            return date.toLocaleString();
        }

        function showLoading() {
            document.getElementById('loadingState').style.display = 'block';
        }

        function hideLoading() {
            document.getElementById('loadingState').style.display = 'none';
        }

        function showAlert(type, message) {
            // Simple alert display - could be enhanced with toast notifications
            console.log(`${type.toUpperCase()}: ${message}`);
        }

        function showRefreshIndicator() {
            const indicator = document.getElementById('refreshIndicator');
            indicator.classList.add('show');
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 3000);
        }

        function updateCurrentTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleTimeString();
        }

        function requestUpdate() {
            if (socket) {
                socket.emit('request_update');
            }
        }

        function acknowledgeAlert(alertId) {
            fetch(`/api/alerts/${alertId}/acknowledge`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    showAlert('success', data.message);
                    loadDashboardData(currentView);
                }
            })
            .catch(error => {
                console.error('Failed to acknowledge alert:', error);
                showAlert('error', 'Failed to acknowledge alert');
            });
        }

        function resolveAlert(alertId) {
            fetch(`/api/alerts/${alertId}/resolve`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    showAlert('success', data.message);
                    loadDashboardData(currentView);
                }
            })
            .catch(error => {
                console.error('Failed to resolve alert:', error);
                showAlert('error', 'Failed to resolve alert');
            });
        }
