/**
 * Dashboard Charts Module - V2 Compliant
 * Handles all chart initialization and management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

/**
 * Initialize all dashboard charts
 * @param {Object} data - Chart data
 */
function initializeCharts(data) {
    initializeContractChart(data);
    initializeWorkloadChart(data);
    initializeAgentPerformanceChart(data);
    initializeHealthTrendChart(data);
    initializeContractStatusChart(data);
    initializeWorkloadDistributionChart(data);
}

/**
 * Initialize contract status chart
 * @param {Object} data - Chart data
 */
function initializeContractChart(data) {
    if (document.getElementById('contractChart')) {
        const ctx = document.getElementById('contractChart').getContext('2d');
        const contractSummary = data.contract_summary || {};

        charts.contractChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'In Progress', 'Pending'],
                datasets: [{
                    data: [
                        contractSummary.completed_contracts || 0,
                        contractSummary.in_progress_contracts || 0,
                        contractSummary.pending_contracts || 0
                    ],
                    backgroundColor: ['#28a745', '#17a2b8', '#ffc107']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

/**
 * Initialize workload distribution chart
 * @param {Object} data - Chart data
 */
function initializeWorkloadChart(data) {
    if (document.getElementById('workloadChart')) {
        const ctx = document.getElementById('workloadChart').getContext('2d');
        const workloadData = data.workload_distribution || {};

        charts.workloadChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['0', '1-2', '3-4', '5+'],
                datasets: [{
                    label: 'Agents',
                    data: [
                        workloadData.zero_contracts || 0,
                        workloadData.low_contracts || 0,
                        workloadData.medium_contracts || 0,
                        workloadData.high_contracts || 0
                    ],
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

/**
 * Initialize agent performance chart
 * @param {Object} data - Chart data
 */
function initializeAgentPerformanceChart(data) {
    if (document.getElementById('agentPerformanceChart')) {
        const ctx = document.getElementById('agentPerformanceChart').getContext('2d');
        const agents = data.agents || [];

        charts.agentPerformanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: agents.map(agent => agent.agent_id),
                datasets: [{
                    label: 'Performance Score',
                    data: agents.map(agent => agent.performance_score),
                    backgroundColor: '#28a745'
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
                }
            }
        });
    }
}

/**
 * Initialize health trend chart
 * @param {Object} data - Chart data
 */
function initializeHealthTrendChart(data) {
    if (document.getElementById('healthTrendChart')) {
        const ctx = document.getElementById('healthTrendChart').getContext('2d');
        const healthHistory = data.performance_history || {};

        charts.healthTrendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: healthHistory.timestamps || [],
                datasets: [{
                    label: 'System Health',
                    data: healthHistory.health_values || [],
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true
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
                }
            }
        });
    }
}

/**
 * Initialize contract status chart
 * @param {Object} data - Chart data
 */
function initializeContractStatusChart(data) {
    if (document.getElementById('contractStatusChart')) {
        const ctx = document.getElementById('contractStatusChart').getContext('2d');
        const contractSummary = data.contract_summary || {};

        charts.contractStatusChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Completed', 'In Progress', 'Pending'],
                datasets: [{
                    data: [
                        contractSummary.completed_contracts || 0,
                        contractSummary.in_progress_contracts || 0,
                        contractSummary.pending_contracts || 0
                    ],
                    backgroundColor: ['#28a745', '#17a2b8', '#ffc107']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

/**
 * Initialize workload distribution chart
 * @param {Object} data - Chart data
 */
function initializeWorkloadDistributionChart(data) {
    if (document.getElementById('workloadDistributionChart')) {
        const ctx = document.getElementById('workloadDistributionChart').getContext('2d');
        const workloadData = data.workload_distribution || {};

        charts.workloadDistributionChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Optimal', 'Overloaded', 'Underutilized'],
                datasets: [{
                    data: [
                        workloadData.optimal_workload_agents || 0,
                        workloadData.overloaded_agents || 0,
                        workloadData.underutilized_agents || 0
                    ],
                    backgroundColor: ['#28a745', '#dc3545', '#17a2b8']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

/**
 * Update chart data
 * @param {Object} newData - Updated chart data
 */
function updateCharts(newData) {
    Object.keys(charts).forEach(chartKey => {
        const chart = charts[chartKey];
        if (chart && newData) {
            // Update chart data based on chart type
            updateChartData(chart, newData, chartKey);
        }
    });
}

/**
 * Update individual chart data
 * @param {Chart} chart - Chart instance
 * @param {Object} data - New data
 * @param {string} chartKey - Chart identifier
 */
function updateChartData(chart, data, chartKey) {
    try {
        switch (chartKey) {
            case 'contractChart':
            case 'contractStatusChart':
                const contractSummary = data.contract_summary || {};
                chart.data.datasets[0].data = [
                    contractSummary.completed_contracts || 0,
                    contractSummary.in_progress_contracts || 0,
                    contractSummary.pending_contracts || 0
                ];
                break;
            case 'workloadChart':
            case 'workloadDistributionChart':
                const workloadData = data.workload_distribution || {};
                chart.data.datasets[0].data = [
                    workloadData.optimal_workload_agents || 0,
                    workloadData.overloaded_agents || 0,
                    workloadData.underutilized_agents || 0
                ];
                break;
            case 'agentPerformanceChart':
                const agents = data.agents || [];
                chart.data.labels = agents.map(agent => agent.agent_id);
                chart.data.datasets[0].data = agents.map(agent => agent.performance_score);
                break;
            case 'healthTrendChart':
                const healthHistory = data.performance_history || {};
                chart.data.labels = healthHistory.timestamps || [];
                chart.data.datasets[0].data = healthHistory.health_values || [];
                break;
        }
        chart.update();
    } catch (error) {
        console.error(`Error updating chart ${chartKey}:`, error);
    }
}
