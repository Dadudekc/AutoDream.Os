/**
 * Dashboard Core Module - V2 Compliant
 * Handles core initialization and WebSocket functionality
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

// Dashboard core state
let currentView = 'overview';
let socket = null;
let charts = {};
let updateTimer = null;

/**
 * Initialize dashboard core functionality
 */
function initializeDashboard() {
    initializeSocket();
    setupNavigation();
    updateCurrentTime();
    loadDashboardData(currentView);

    // Update time every second
    setInterval(updateCurrentTime, 1000);
}

/**
 * Initialize WebSocket connection
 */
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

/**
 * Load dashboard data for specified view
 * @param {string} view - The view to load data for
 */
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

/**
 * Update dashboard with new data
 * @param {Object} data - Dashboard data to update with
 */
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

    // Initialize charts after content update
    initializeCharts();
}

/**
 * Show loading indicator
 */
function showLoading() {
    const loadingEl = document.getElementById('loadingIndicator');
    if (loadingEl) {
        loadingEl.style.display = 'block';
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loadingEl = document.getElementById('loadingIndicator');
    if (loadingEl) {
        loadingEl.style.display = 'none';
    }
}

/**
 * Show alert message
 * @param {string} type - Alert type (success, error, warning, info)
 * @param {string} message - Alert message
 */
function showAlert(type, message) {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;

    const alertEl = document.createElement('div');
    alertEl.className = `alert alert-${type} alert-dismissible fade show`;
    alertEl.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    alertContainer.appendChild(alertEl);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertEl.parentNode) {
            alertEl.remove();
        }
    }, 5000);
}

/**
 * Show refresh indicator
 */
function showRefreshIndicator() {
    const indicator = document.getElementById('refreshIndicator');
    if (indicator) {
        indicator.style.display = 'block';
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 2000);
    }
}

/**
 * Update current time display
 */
function updateCurrentTime() {
    const timeEl = document.getElementById('currentTime');
    if (timeEl) {
        timeEl.textContent = new Date().toLocaleTimeString();
    }
}

// Export core functionality
export {
    initializeDashboard,
    initializeSocket,
    loadDashboardData,
    updateDashboard,
    showLoading,
    hideLoading,
    showAlert,
    showRefreshIndicator,
    updateCurrentTime,
    currentView,
    socket,
    charts
};
