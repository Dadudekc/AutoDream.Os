/**
 * Dashboard Wrapper - Backward Compatibility Layer
 * Maintains existing dashboard.js API while using modular architecture
 * V2 Compliance: Backward compatibility with modular implementation
 */

// Import the new modular dashboard
import { DashboardMain } from './dashboard-main.js';

// Global dashboard instance
let dashboardInstance = null;

// Backward compatibility functions - maintain existing API
function initializeSocket() {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.core.initializeSocket();
}

function setupNavigation() {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.navigation.setup();
}

function loadDashboardData(view) {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.loadDashboardData(view);
}

function updateDashboard(data) {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.updateDashboard(data);
}

function showLoading() {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.utils.showLoading();
}

function hideLoading() {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.utils.hideLoading();
}

function showAlert(type, message) {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.utils.showAlert(type, message);
}

function updateCurrentTime() {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    return dashboardInstance.utils.updateCurrentTime();
}

// Initialize dashboard when DOM is ready (backward compatibility)
document.addEventListener('DOMContentLoaded', function() {
    if (!dashboardInstance) {
        dashboardInstance = new DashboardMain();
    }
    dashboardInstance.initialize();
    
    // Update time every second (backward compatibility)
    setInterval(updateCurrentTime, 1000);
});

// Export backward compatibility functions
export {
    initializeSocket,
    setupNavigation,
    loadDashboardData,
    updateDashboard,
    showLoading,
    hideLoading,
    showAlert,
    updateCurrentTime
};
