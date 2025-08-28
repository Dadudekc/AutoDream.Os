        // Global variables
        let socket;
        let healthMetricsChart;
        let statusDistributionChart;
        let lastUpdateTime = new Date();
        let updateInterval;

        // Initialize the dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeSocket();
            initializeCharts();
            loadInitialData();
            startAutoRefresh();
        });

        // Initialize WebSocket connection
        function initializeSocket() {
            socket = io();

            socket.on('connect', function() {
                updateConnectionStatus('Connected', 'success');
                socket.emit('subscribe_to_health_updates');
            });

            socket.on('disconnect', function() {
                updateConnectionStatus('Disconnected', 'danger');
            });

            socket.on('health_update', function(data) {
                updateDashboardData(data);
            });

            socket.on('periodic_update', function(data) {
                updateDashboardData(data);
            });

            socket.on('error', function(data) {
                console.error('Socket error:', data);
                showNotification('Error: ' + data.message, 'danger');
            });
        }

        // Initialize charts
        function initializeCharts() {
            // Health Metrics Chart
            const healthCtx = document.getElementById('healthMetricsChart').getContext('2d');
            healthMetricsChart = new Chart(healthCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Average Health Score',
                        data: [],
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    },
                    plugins: {
                        legend: {
                            display: true
                        }
                    }
                }
            });

            // Status Distribution Chart
            const statusCtx = document.getElementById('statusDistributionChart').getContext('2d');
            statusDistributionChart = new Chart(statusCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Excellent', 'Good', 'Warning', 'Critical', 'Offline'],
                    datasets: [{
                        data: [0, 0, 0, 0, 0],
                        backgroundColor: [
                            '#198754',
                            '#0d6efd',
                            '#ffc107',
                            '#dc3545',
                            '#6c757d'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }

        // Load initial data
        function loadInitialData() {
            Promise.all([
                fetch('/api/health/summary'),
                fetch('/api/health/agents'),
                fetch('/api/health/alerts'),
                fetch('/api/health/status')
            ]).then(responses => {
                return Promise.all(responses.map(r => r.json()));
            }).then(([summary, agents, alerts, status]) => {
                updateDashboardData({
                    health_summary: summary,
                    agents: agents,
                    alerts: alerts,
                    status: status
                });
            }).catch(error => {
                console.error('Error loading initial data:', error);
                showNotification('Error loading data', 'danger');
            });
        }

        // Update dashboard data
        function updateDashboardData(data) {
            if (data.health_summary) {
                updateSummaryCards(data.health_summary);
            }

            if (data.agents) {
                updateAgentHealth(data.agents);
            }

            if (data.alerts) {
                updateAlerts(data.alerts);
            }

            if (data.status) {
                updateStatusInfo(data.status);
            }

            lastUpdateTime = new Date();
            updateLastUpdateTime();
        }

        // Update summary cards
        function updateSummaryCards(summary) {
            document.getElementById('total-agents').textContent = summary.total_agents || 0;
            document.getElementById('active-alerts').textContent = summary.active_alerts || 0;
            document.getElementById('avg-health-score').textContent = summary.average_health_score || 0;
            document.getElementById('monitoring-status').textContent = summary.monitoring_active ? 'Active' : 'Inactive';

            // Update status distribution chart
            if (summary.status_distribution) {
                const statusData = [
                    summary.status_distribution.excellent || 0,
                    summary.status_distribution.good || 0,
                    summary.status_distribution.warning || 0,
                    summary.status_distribution.critical || 0,
                    summary.status_distribution.offline || 0
                ];

                statusDistributionChart.data.datasets[0].data = statusData;
                statusDistributionChart.update();
            }
        }

        // Update agent health display
        function updateAgentHealth(agents) {
            const container = document.getElementById('agent-health-container');

            if (!agents || Object.keys(agents).length === 0) {
                container.innerHTML = '<p class="text-muted text-center">No agents found</p>';
                return;
            }

            let html = '<div class="agent-list">';

            Object.values(agents).forEach(agent => {
                const statusClass = `status-${agent.overall_status}`;
                const statusBadgeClass = getStatusBadgeClass(agent.overall_status);

                html += `
                    <div class="agent-item ${statusClass}">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">${agent.agent_id}</h6>
                                <small class="text-muted">
                                    Last update: ${new Date(agent.timestamp).toLocaleTimeString()}
                                </small>
                            </div>
                            <div class="text-end">
                                <span class="badge ${statusBadgeClass} status-badge">
                                    ${agent.overall_status.toUpperCase()}
                                </span>
                                <div class="health-score text-${getHealthScoreColor(agent.health_score)}">
                                    ${Math.round(agent.health_score)}
                                </div>
                            </div>
                        </div>
                        ${agent.recommendations && agent.recommendations.length > 0 ? `
                            <div class="mt-2">
                                <small class="text-muted">
                                    <i class="bi bi-lightbulb me-1"></i>
                                    ${agent.recommendations.join(', ')}
                                </small>
                            </div>
                        ` : ''}
                    </div>
                `;
            });

            html += '</div>';
            container.innerHTML = html;
        }

        // Update alerts display
        function updateAlerts(alerts) {
            const container = document.getElementById('alerts-container');
            const alertCount = document.getElementById('alert-count');

            if (!alerts || alerts.length === 0) {
                container.innerHTML = '<p class="text-muted text-center">No active alerts</p>';
                alertCount.textContent = '0';
                return;
            }

            alertCount.textContent = alerts.length;

            let html = '';
            alerts.forEach(alert => {
                const alertClass = `alert-${alert.severity}`;
                const severityIcon = getSeverityIcon(alert.severity);

                html += `
                    <div class="alert ${alertClass} alert-card">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <h6 class="alert-heading">
                                    ${severityIcon} ${alert.agent_id}
                                </h6>
                                <p class="mb-1">${alert.message}</p>
                                <small class="text-muted">
                                    ${new Date(alert.timestamp).toLocaleString()}
                                </small>
                            </div>
                            <div class="ms-2">
                                ${!alert.acknowledged ? `
                                    <button class="btn btn-sm btn-outline-primary" onclick="acknowledgeAlert('${alert.alert_id}')" title="Acknowledge Alert" aria-label="Acknowledge Alert">
                                        <i class="bi bi-check"></i>
                                    </button>
                                ` : ''}
                                ${!alert.resolved ? `
                                    <button class="btn btn-sm btn-outline-success" onclick="resolveAlert('${alert.alert_id}')" title="Resolve Alert" aria-label="Resolve Alert">
                                        <i class="bi bi-check-circle"></i>
                                    </button>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `;
            });

            container.innerHTML = html;
        }

        // Update status information
        function updateStatusInfo(status) {
            // Update any status-specific information
            if (status.monitoring_active !== undefined) {
                const monitoringElement = document.getElementById('monitoring-status');
                monitoringElement.textContent = status.monitoring_active ? 'Active' : 'Inactive';
                monitoringElement.className = `metric-value text-${status.monitoring_active ? 'success' : 'danger'}`;
            }
        }

        // Utility functions
        function getStatusBadgeClass(status) {
            const statusClasses = {
                'excellent': 'bg-success',
                'good': 'bg-primary',
                'warning': 'bg-warning',
                'critical': 'bg-danger',
                'offline': 'bg-secondary'
            };
            return statusClasses[status] || 'bg-secondary';
        }

        function getHealthScoreColor(score) {
            if (score >= 90) return 'success';
            if (score >= 75) return 'primary';
            if (score >= 50) return 'warning';
            return 'danger';
        }

        function getSeverityIcon(severity) {
            const icons = {
                'critical': '<i class="bi bi-exclamation-triangle-fill text-danger"></i>',
                'warning': '<i class="bi bi-exclamation-triangle text-warning"></i>',
                'info': '<i class="bi bi-info-circle text-info"></i>'
            };
            return icons[severity] || '<i class="bi bi-info-circle text-info"></i>';
        }

        function updateConnectionStatus(status, type) {
            const statusElement = document.getElementById('connection-status');
            const detailElement = document.getElementById('connection-detail');

            statusElement.textContent = status;
            detailElement.textContent = status;

            // Update connection status indicator
            const indicator = document.querySelector('.connection-status .alert');
            indicator.className = `alert alert-${type} alert-dismissible fade show`;
        }

        function updateLastUpdateTime() {
            const element = document.getElementById('last-update');
            element.textContent = `Last update: ${lastUpdateTime.toLocaleTimeString()}`;
        }

        // Action functions
        function acknowledgeAlert(alertId) {
            fetch(`/api/health/alerts/${alertId}/acknowledge`, {
                method: 'POST'
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Alert acknowledged', 'success');
                    refreshAllData();
                } else {
                    showNotification('Error acknowledging alert', 'danger');
                }
            }).catch(error => {
                console.error('Error acknowledging alert:', error);
                showNotification('Error acknowledging alert', 'danger');
            });
        }

        function resolveAlert(alertId) {
            fetch(`/api/health/alerts/${alertId}/resolve`, {
                method: 'POST'
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Alert resolved', 'success');
                    refreshAllData();
                } else {
                    showNotification('Error resolving alert', 'danger');
                }
            }).catch(error => {
                console.error('Error resolving alert:', error);
                showNotification('Error resolving alert', 'danger');
            });
        }

        function acknowledgeAllAlerts() {
            if (confirm('Are you sure you want to acknowledge all alerts?')) {
                // This would need to be implemented on the backend
                showNotification('Feature not yet implemented', 'info');
            }
        }

        function exportHealthReport() {
            showNotification('Export feature not yet implemented', 'info');
        }

        function refreshAgentHealth() {
            fetch('/api/health/agents')
                .then(response => response.json())
                .then(agents => updateAgentHealth(agents))
                .catch(error => {
                    console.error('Error refreshing agent health:', error);
                    showNotification('Error refreshing data', 'danger');
                });
        }

        function refreshAllData() {
            loadInitialData();
        }

        function startAutoRefresh() {
            updateInterval = setInterval(() => {
                if (socket.connected) {
                    socket.emit('request_health_update');
                }
            }, 30000); // Refresh every 30 seconds
        }

        function showNotification(message, type) {
            // Simple notification system
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            alertDiv.style.top = '80px';
            alertDiv.style.right = '20px';
            alertDiv.style.zIndex = '1050';
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" title="Close" aria-label="Close"></button>
            `;

            document.body.appendChild(alertDiv);

            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 5000);
        }

        // Cleanup on page unload
        window.addEventListener('beforeunload', function() {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
            if (socket) {
                socket.disconnect();
            }
        });
