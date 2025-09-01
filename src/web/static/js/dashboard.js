/**
 * Dashboard Main Module - V2 Compliant
 * Core dashboard functionality with modular imports
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

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
    
    // Initialize refresh schedule
    scheduleRefresh();
});

// Initialize WebSocket connection
function initializeSocket() {
    socket = io();

    socket.on('connect', function() {
        console.log('Connected to dashboard server');
        hideLoading();
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
    const nav = document.getElementById('dashboardNav');
    if (nav) {
        nav.addEventListener('click', function(e) {
            if (e.target.classList.contains('nav-link')) {
                e.preventDefault();

                // Update active state
                document.querySelectorAll('#dashboardNav .nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                e.target.classList.add('active');

                // Get view from data attribute
                const newView = e.target.getAttribute('data-view');
                if (newView && newView !== currentView) {
                    currentView = newView;
                    loadDashboardData(currentView);
                }
            }
        });
    }
}

// Load dashboard data
function loadDashboardData(view) {
    showLoading();
    
    fetch(`/api/dashboard/${view}`)
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
            hideLoading();
        })
        .catch(error => {
            console.error('Failed to load dashboard data:', error);
            showAlert('error', 'Failed to load dashboard data');
            hideLoading();
        });
}

// Update dashboard content
function updateDashboard(data) {
    const contentDiv = document.getElementById('dashboardContent');
    if (!contentDiv) return;

    // Render appropriate view based on current view
    switch (currentView) {
        case 'overview':
            contentDiv.innerHTML = renderOverviewView(data);
            break;
        case 'agents':
            contentDiv.innerHTML = renderAgentPerformanceView(data);
            break;
        case 'contracts':
            contentDiv.innerHTML = renderContractStatusView(data);
            break;
        case 'health':
            contentDiv.innerHTML = renderSystemHealthView(data);
            break;
        case 'performance':
            contentDiv.innerHTML = renderPerformanceMetricsView(data);
            break;
        case 'workload':
            contentDiv.innerHTML = renderWorkloadDistributionView(data);
            break;
        default:
            contentDiv.innerHTML = renderOverviewView(data);
    }

    // Initialize charts after rendering
    requestAnimationFrame(() => initializeCharts(data));
}

// Data refresh management
function scheduleRefresh() {
    if (updateTimer) {
        clearTimeout(updateTimer);
    }
    
    updateTimer = setTimeout(() => {
        loadDashboardData(currentView);
        scheduleRefresh();
    }, 30000); // Refresh every 30 seconds
}

// Manual refresh
function refreshDashboard() {
    loadDashboardData(currentView);
    showAlert('info', 'Dashboard refreshed');
}

// Global functions for onclick handlers
window.acknowledgeAlert = acknowledgeAlert;
window.resolveAlert = resolveAlert;
window.requestUpdate = requestUpdate;
window.refreshDashboard = refreshDashboard;